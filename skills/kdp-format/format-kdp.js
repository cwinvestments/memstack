#!/usr/bin/env node

/**
 * KDP Book Formatter
 * Converts markdown manuscripts to KDP-ready .docx files (6×9 trade paperback).
 *
 * Usage: node format-kdp.js <input.md> [output.docx]
 *
 * Requires: npm install docx
 *
 * Markdown conventions:
 *   YAML frontmatter → title, subtitle, author, publisher, year, isbn
 *   # Part Title       → Part header (own page, centered)
 *   ## Chapter Title    → Chapter (new page, drop spacing)
 *   ### Section Head    → Section heading (bold, left-aligned)
 *   > quote             → Blockquote (teal left border)
 *   ```lang             → Code block (gray background, Courier New)
 *   ---                 → Scene break (* * * centered)
 *   **bold** *italic*   → Inline formatting
 *   `code`              → Inline code (Courier New)
 *   [text](url)         → External hyperlink
 */

const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Header,
  Footer,
  PageNumber,
  AlignmentType,
  SectionType,
  BorderStyle,
  ShadingType,
  InternalHyperlink,
  Bookmark,
  ExternalHyperlink,
  convertInchesToTwip,
  PageBreak,
  Tab,
  TabStopType,
  TabStopPosition,
} = require("docx");

// ─── Constants ───────────────────────────────────────────────────────────────

const FONT_BODY = "Georgia";
const FONT_HEADING = "Arial";
const FONT_CODE = "Courier New";

// Font sizes in half-points (11pt = 22, 24pt = 48, etc.)
const SIZE_BODY = 22; // 11pt
const SIZE_CHAPTER_TITLE = 48; // 24pt
const SIZE_CHAPTER_SUB = 28; // 14pt
const SIZE_SECTION = 26; // 13pt
const SIZE_CODE = 20; // 10pt
const SIZE_HEADER = 18; // 9pt
const SIZE_TITLE_PAGE = 72; // 36pt
const SIZE_TITLE_SUB = 36; // 18pt
const SIZE_AUTHOR = 28; // 14pt
const SIZE_COPYRIGHT = 20; // 10pt

// Spacing in twips (1pt = 20 twips, 1 inch = 1440 twips)
const LINE_SPACING_BODY = 312; // 1.3× (240 × 1.3)
const LINE_SPACING_CODE = 240; // 1.0× (single)
const CHAPTER_DROP = convertInchesToTwip(2.25); // push ~1/3 down page
const PART_DROP = convertInchesToTwip(3); // push ~halfway down

// Colors
const TEAL = "008080";
const GRAY_BG = "F2F2F2";
const GRAY_CODE_INLINE = "E8E8E8";
const LINK_COLOR = "0563C1";

// Page properties (6×9 trim)
const PAGE_PROPS = {
  size: {
    width: convertInchesToTwip(6),
    height: convertInchesToTwip(9),
  },
  margin: {
    top: convertInchesToTwip(0.75),
    bottom: convertInchesToTwip(0.75),
    left: convertInchesToTwip(0.75), // inside/gutter
    right: convertInchesToTwip(0.5), // outside
  },
};

// ─── Markdown Parsing ────────────────────────────────────────────────────────

/**
 * Extract YAML frontmatter from markdown content.
 * Returns { meta: {key: value}, body: "remaining markdown" }
 */
function extractFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { meta: {}, body: content };

  const meta = {};
  match[1].split("\n").forEach((line) => {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) return;
    const key = line.slice(0, colonIdx).trim();
    const val = line
      .slice(colonIdx + 1)
      .trim()
      .replace(/^["']|["']$/g, "");
    if (key) meta[key] = val;
  });

  return { meta, body: content.slice(match[0].length).trim() };
}

/**
 * Parse markdown content into an array of block objects.
 */
function parseBlocks(markdown) {
  const lines = markdown.split(/\r?\n/);
  const blocks = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Skip empty lines
    if (line.trim() === "") {
      i++;
      continue;
    }

    // Fenced code block
    if (line.trim().startsWith("```")) {
      const lang = line.trim().slice(3).trim();
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      if (i < lines.length) i++; // skip closing ```
      blocks.push({ type: "code", content: codeLines.join("\n"), lang });
      continue;
    }

    // Part header: # Title
    if (/^# /.test(line)) {
      blocks.push({ type: "part", title: line.slice(2).trim() });
      i++;
      continue;
    }

    // Chapter header: ## Title
    if (/^## /.test(line)) {
      blocks.push({ type: "chapter", title: line.slice(3).trim() });
      i++;
      continue;
    }

    // Section heading: ### Title
    if (/^### /.test(line)) {
      blocks.push({ type: "heading", title: line.slice(4).trim() });
      i++;
      continue;
    }

    // Subheading: #### Title
    if (/^#### /.test(line)) {
      blocks.push({ type: "subheading", title: line.slice(5).trim() });
      i++;
      continue;
    }

    // Scene break
    if (/^(---|___|\*\*\*|\* \* \*)$/.test(line.trim())) {
      blocks.push({ type: "break" });
      i++;
      continue;
    }

    // Blockquote (collect consecutive > lines)
    if (line.trim().startsWith(">")) {
      const quoteLines = [];
      while (i < lines.length && lines[i].trim().startsWith(">")) {
        quoteLines.push(lines[i].trim().replace(/^>\s?/, ""));
        i++;
      }
      blocks.push({ type: "blockquote", content: quoteLines.join("\n") });
      continue;
    }

    // Unordered list
    if (/^[\-\*\+] /.test(line)) {
      const items = [];
      while (i < lines.length && /^[\-\*\+] /.test(lines[i])) {
        items.push(lines[i].replace(/^[\-\*\+] /, "").trim());
        i++;
      }
      blocks.push({ type: "list", items, ordered: false });
      continue;
    }

    // Ordered list
    if (/^\d+\. /.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\. /, "").trim());
        i++;
      }
      blocks.push({ type: "list", items, ordered: true });
      continue;
    }

    // Regular paragraph
    blocks.push({ type: "paragraph", content: line.trim() });
    i++;
  }

  return blocks;
}

/**
 * Parse inline markdown into an array of TextRun objects.
 */
function parseInline(text, opts = {}) {
  const {
    font = FONT_BODY,
    size = SIZE_BODY,
    bold = false,
    italics = false,
  } = opts;
  const runs = [];
  let remaining = text;

  while (remaining.length > 0) {
    let m;

    // Bold: **text**
    if ((m = remaining.match(/^\*\*(.+?)\*\*/))) {
      runs.push(
        new TextRun({ text: m[1], font, size, bold: true, italics })
      );
      remaining = remaining.slice(m[0].length);
      continue;
    }

    // Italic: *text*
    if ((m = remaining.match(/^\*(.+?)\*/))) {
      runs.push(
        new TextRun({ text: m[1], font, size, bold, italics: true })
      );
      remaining = remaining.slice(m[0].length);
      continue;
    }

    // Inline code: `text`
    if ((m = remaining.match(/^`(.+?)`/))) {
      runs.push(
        new TextRun({
          text: m[1],
          font: FONT_CODE,
          size: SIZE_CODE,
          bold,
          italics,
          shading: { type: ShadingType.CLEAR, fill: GRAY_CODE_INLINE },
        })
      );
      remaining = remaining.slice(m[0].length);
      continue;
    }

    // Link: [text](url)
    if ((m = remaining.match(/^\[(.+?)\]\((.+?)\)/))) {
      runs.push(
        new ExternalHyperlink({
          children: [
            new TextRun({
              text: m[1],
              font,
              size,
              style: "Hyperlink",
              color: LINK_COLOR,
            }),
          ],
          link: m[2],
        })
      );
      remaining = remaining.slice(m[0].length);
      continue;
    }

    // Plain text — consume until next special character
    if ((m = remaining.match(/^[^*`\[]+/))) {
      runs.push(new TextRun({ text: m[0], font, size, bold, italics }));
      remaining = remaining.slice(m[0].length);
      continue;
    }

    // Single special char that didn't match a pattern
    runs.push(new TextRun({ text: remaining[0], font, size, bold, italics }));
    remaining = remaining.slice(1);
  }

  if (runs.length === 0) {
    runs.push(new TextRun({ text, font, size, bold, italics }));
  }

  return runs;
}

/**
 * Create a URL-safe slug from text for bookmark IDs.
 */
function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

// ─── Document Builders ───────────────────────────────────────────────────────

/**
 * Build title page paragraphs.
 */
function buildTitlePage(meta) {
  const children = [];

  // Vertical spacing to push content down
  children.push(
    new Paragraph({
      spacing: { before: convertInchesToTwip(2.5) },
      children: [],
    })
  );

  // Book title
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
      children: [
        new TextRun({
          text: meta.title || "Untitled",
          font: FONT_HEADING,
          size: SIZE_TITLE_PAGE,
          bold: true,
        }),
      ],
    })
  );

  // Subtitle
  if (meta.subtitle) {
    children.push(
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [
          new TextRun({
            text: meta.subtitle,
            font: FONT_HEADING,
            size: SIZE_TITLE_SUB,
            italics: true,
          }),
        ],
      })
    );
  }

  // Author name
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: meta.subtitle ? 0 : 600 },
      children: [
        new TextRun({
          text: meta.author || "Anonymous",
          font: FONT_BODY,
          size: SIZE_AUTHOR,
        }),
      ],
    })
  );

  return children;
}

/**
 * Build copyright page paragraphs.
 */
function buildCopyrightPage(meta) {
  const year = meta.year || new Date().getFullYear();
  const author = meta.author || "the author";
  const publisher = meta.publisher || "Self-published";

  const lines = [
    `Copyright \u00A9 ${year} ${author}`,
    "All rights reserved.",
    "",
    "No part of this publication may be reproduced, distributed, or transmitted",
    "in any form or by any means without the prior written permission of the",
    "publisher, except in the case of brief quotations in reviews and certain",
    "other noncommercial uses permitted by copyright law.",
    "",
    `Published by ${publisher}`,
  ];

  if (meta.isbn) {
    lines.push("", `ISBN: ${meta.isbn}`);
  }

  lines.push("", `First Edition: ${year}`);

  if (meta.website) {
    lines.push("", meta.website);
  }

  return lines.map(
    (line) =>
      new Paragraph({
        spacing: { after: line === "" ? 120 : 40 },
        children:
          line === ""
            ? []
            : [
                new TextRun({
                  text: line,
                  font: FONT_BODY,
                  size: SIZE_COPYRIGHT,
                }),
              ],
      })
  );
}

/**
 * Build Table of Contents with internal hyperlinks.
 */
function buildTOC(blocks) {
  const children = [];

  // TOC Title
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: CHAPTER_DROP, after: 480 },
      children: [
        new TextRun({
          text: "Table of Contents",
          font: FONT_HEADING,
          size: SIZE_CHAPTER_TITLE,
          bold: true,
        }),
      ],
    })
  );

  // Collect parts and chapters
  blocks.forEach((block) => {
    if (block.type === "part") {
      const anchor = slugify(block.title);
      children.push(
        new Paragraph({
          spacing: { before: 240, after: 80 },
          children: [
            new InternalHyperlink({
              anchor,
              children: [
                new TextRun({
                  text: block.title,
                  font: FONT_HEADING,
                  size: SIZE_SECTION,
                  bold: true,
                }),
              ],
            }),
          ],
        })
      );
    } else if (block.type === "chapter") {
      const anchor = slugify(block.title);
      children.push(
        new Paragraph({
          spacing: { before: 80, after: 80 },
          indent: { left: convertInchesToTwip(0.3) },
          children: [
            new InternalHyperlink({
              anchor,
              children: [
                new TextRun({
                  text: block.title,
                  font: FONT_BODY,
                  size: SIZE_BODY,
                }),
              ],
            }),
          ],
        })
      );
    }
  });

  return children;
}

/**
 * Build body content paragraphs from parsed blocks.
 */
function buildBody(blocks) {
  const children = [];
  let isFirstAfterHeading = false;

  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];

    switch (block.type) {
      case "part": {
        const anchor = slugify(block.title);
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: PART_DROP, after: 240 },
            pageBreakBefore: true,
            children: [
              new Bookmark({
                id: anchor,
                children: [
                  new TextRun({
                    text: block.title,
                    font: FONT_HEADING,
                    size: SIZE_CHAPTER_TITLE,
                    bold: true,
                  }),
                ],
              }),
            ],
          })
        );
        isFirstAfterHeading = true;
        break;
      }

      case "chapter": {
        const anchor = slugify(block.title);
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: CHAPTER_DROP, after: 200 },
            pageBreakBefore: i > 0, // no page break before first chapter
            children: [
              new Bookmark({
                id: anchor,
                children: [
                  new TextRun({
                    text: block.title,
                    font: FONT_HEADING,
                    size: SIZE_CHAPTER_TITLE,
                    bold: true,
                  }),
                ],
              }),
            ],
          })
        );
        isFirstAfterHeading = true;
        break;
      }

      case "heading": {
        children.push(
          new Paragraph({
            spacing: { before: 360, after: 120 },
            children: [
              new TextRun({
                text: block.title,
                font: FONT_HEADING,
                size: SIZE_SECTION,
                bold: true,
              }),
            ],
          })
        );
        isFirstAfterHeading = true;
        break;
      }

      case "subheading": {
        children.push(
          new Paragraph({
            spacing: { before: 240, after: 80 },
            children: [
              new TextRun({
                text: block.title,
                font: FONT_HEADING,
                size: SIZE_BODY,
                bold: true,
                italics: true,
              }),
            ],
          })
        );
        isFirstAfterHeading = true;
        break;
      }

      case "paragraph": {
        children.push(
          new Paragraph({
            indent: isFirstAfterHeading
              ? undefined
              : { firstLine: convertInchesToTwip(0.3) },
            spacing: { line: LINE_SPACING_BODY },
            children: parseInline(block.content),
          })
        );
        isFirstAfterHeading = false;
        break;
      }

      case "blockquote": {
        const quoteLines = block.content.split("\n");
        quoteLines.forEach((line, idx) => {
          children.push(
            new Paragraph({
              indent: {
                left: convertInchesToTwip(0.4),
              },
              spacing: {
                line: LINE_SPACING_BODY,
                before: idx === 0 ? 160 : 0,
                after: idx === quoteLines.length - 1 ? 160 : 0,
              },
              border: {
                left: {
                  style: BorderStyle.SINGLE,
                  size: 6,
                  color: TEAL,
                  space: 10,
                },
              },
              children: parseInline(line, { italics: true }),
            })
          );
        });
        isFirstAfterHeading = false;
        break;
      }

      case "code": {
        const codeLines = block.content.split("\n");
        codeLines.forEach((line, idx) => {
          children.push(
            new Paragraph({
              spacing: {
                line: LINE_SPACING_CODE,
                before: idx === 0 ? 160 : 0,
                after: idx === codeLines.length - 1 ? 160 : 0,
              },
              indent: { left: convertInchesToTwip(0.2) },
              shading: { type: ShadingType.CLEAR, fill: GRAY_BG },
              children: [
                new TextRun({
                  text: line || " ", // preserve empty lines
                  font: FONT_CODE,
                  size: SIZE_CODE,
                }),
              ],
            })
          );
        });
        isFirstAfterHeading = false;
        break;
      }

      case "break": {
        children.push(
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 240, after: 240 },
            children: [
              new TextRun({
                text: "*  *  *",
                font: FONT_BODY,
                size: SIZE_BODY,
              }),
            ],
          })
        );
        isFirstAfterHeading = true; // no indent after break
        break;
      }

      case "list": {
        block.items.forEach((item, idx) => {
          const bullet = block.ordered ? `${idx + 1}. ` : "\u2022 ";
          children.push(
            new Paragraph({
              indent: {
                left: convertInchesToTwip(0.5),
                hanging: convertInchesToTwip(0.25),
              },
              spacing: { line: LINE_SPACING_BODY, after: 40 },
              children: [
                new TextRun({
                  text: bullet,
                  font: FONT_BODY,
                  size: SIZE_BODY,
                }),
                ...parseInline(item),
              ],
            })
          );
        });
        isFirstAfterHeading = false;
        break;
      }
    }
  }

  return children;
}

/**
 * Create the running header with book title.
 */
function makeRunningHeader(title) {
  return new Header({
    children: [
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [
          new TextRun({
            text: title,
            font: FONT_BODY,
            size: SIZE_HEADER,
            italics: true,
            color: "666666",
          }),
        ],
      }),
    ],
  });
}

/**
 * Create a page number footer.
 */
function makePageFooter() {
  return new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            children: [PageNumber.CURRENT],
            font: FONT_BODY,
            size: SIZE_HEADER,
          }),
        ],
      }),
    ],
  });
}

/**
 * Create an empty header/footer (for title/copyright pages).
 */
function makeEmptyHeader() {
  return new Header({ children: [new Paragraph({ children: [] })] });
}

function makeEmptyFooter() {
  return new Footer({ children: [new Paragraph({ children: [] })] });
}

// ─── Document Assembly ───────────────────────────────────────────────────────

function createDocument(meta, blocks) {
  const title = meta.title || "Untitled";

  const sections = [
    // Section 1: Title page (no headers/footers)
    {
      properties: { page: PAGE_PROPS },
      headers: { default: makeEmptyHeader() },
      footers: { default: makeEmptyFooter() },
      children: buildTitlePage(meta),
    },

    // Section 2: Copyright page (no headers/footers)
    {
      properties: {
        page: PAGE_PROPS,
        type: SectionType.NEXT_PAGE,
      },
      headers: { default: makeEmptyHeader() },
      footers: { default: makeEmptyFooter() },
      children: buildCopyrightPage(meta),
    },

    // Section 3: Table of Contents
    {
      properties: {
        page: PAGE_PROPS,
        type: SectionType.NEXT_PAGE,
      },
      headers: { default: makeEmptyHeader() },
      footers: { default: makePageFooter() },
      children: buildTOC(blocks),
    },

    // Section 4: Body content (running headers + page numbers)
    {
      properties: {
        page: PAGE_PROPS,
        type: SectionType.NEXT_PAGE,
      },
      headers: { default: makeRunningHeader(title) },
      footers: { default: makePageFooter() },
      children: buildBody(blocks),
    },
  ];

  return new Document({ sections });
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === "--help" || args[0] === "-h") {
    console.log(`
📚 KDP Book Formatter

Usage: node format-kdp.js <input.md> [output.docx]

Converts a markdown manuscript into a KDP-ready Word document.
  - 6×9 trim size (standard trade paperback)
  - Georgia body, Arial headings, Courier New code blocks
  - Title page, copyright page, clickable Table of Contents
  - Running headers with book title, page numbers
  - Chapters start on new pages with drop spacing
  - Code blocks with gray background
  - Blockquotes with teal left border

Markdown frontmatter (optional):
  ---
  title: "Book Title"
  subtitle: "Optional Subtitle"
  author: "Author Name"
  publisher: "Publisher Name"
  year: 2025
  isbn: "978-..."
  website: "https://example.com"
  ---
`);
    process.exit(0);
  }

  const inputPath = path.resolve(args[0]);
  const defaultOutput = inputPath.replace(/\.md$/i, ".docx");
  const outputPath = args[1] ? path.resolve(args[1]) : defaultOutput;

  // Read markdown
  if (!fs.existsSync(inputPath)) {
    console.error(`Error: File not found: ${inputPath}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(inputPath, "utf-8");
  const { meta, body } = extractFrontmatter(raw);
  const blocks = parseBlocks(body);

  // Stats
  const partCount = blocks.filter((b) => b.type === "part").length;
  const chapterCount = blocks.filter((b) => b.type === "chapter").length;
  const paragraphCount = blocks.filter((b) => b.type === "paragraph").length;

  console.log(`📚 KDP Format — Processing "${meta.title || "Untitled"}"...`);
  console.log(
    `   Parts: ${partCount} | Chapters: ${chapterCount} | Paragraphs: ${paragraphCount}`
  );

  // Build document
  const doc = createDocument(meta, blocks);

  // Write .docx
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);

  console.log(`\n✅ Generated: ${outputPath}`);
  console.log(`   Trim: 6" × 9" | Sections: Title, Copyright, TOC, Body`);
  console.log(`\n   Next steps:`);
  console.log(`   1. Open in Word to verify formatting`);
  console.log(`   2. Check page count for KDP margin requirements`);
  console.log(`   3. Upload to KDP dashboard`);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
