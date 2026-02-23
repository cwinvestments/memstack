---
name: kdp-format
description: "KDP book formatter. Converts markdown manuscripts to KDP-ready .docx files with proper trim, fonts, headers. Triggers on format kdp, format book, kdp."
---


# 📚 KDP Format — Converting manuscript to KDP-ready .docx...
*Convert a markdown manuscript into a professionally formatted Word document for Amazon KDP.*

## Activation

When this skill activates, output:

`📚 KDP Format — Converting manuscript to KDP-ready .docx...`

Then execute the protocol below.

## Context Guard

| Context | Status |
|---------|--------|
| **User asks to format a manuscript for KDP** | ACTIVE — full conversion |
| **User says "format for kdp" with a file path** | ACTIVE — full conversion |
| **User mentions book formatting or manuscript** | ACTIVE — ask for file path |
| **User is writing content, not formatting** | DORMANT — do not activate |
| **Discussing KDP concepts generally** | DORMANT — do not activate |

## Output Specifications

| Property | Value |
|----------|-------|
| **Trim size** | 6" × 9" (standard trade paperback) |
| **Body font** | Georgia 11pt |
| **Heading font** | Arial (24pt chapters, 14pt sub, 13pt sections) |
| **Code font** | Courier New 10pt, gray background |
| **Margins** | Top 0.75", Bottom 0.75", Inside 0.75" (gutter), Outside 0.5" |
| **Line spacing** | 1.3× body, 1.0× code/quotes |
| **Paragraph indent** | 0.3" first-line (except first after heading) |

## Markdown Conventions

The input markdown file should follow these conventions:

```
---
title: "Book Title"
subtitle: "Optional Subtitle"
author: "Author Name"
publisher: "Publisher or Self-published"
year: 2025
isbn: "978-..."
---

# Part One: Part Title        → Part header (own page, centered)
## Chapter 1: Chapter Title   → Chapter (new page, drop spacing)
### Section Heading            → Section heading (bold, left)
Regular paragraph text.        → Body text (Georgia 11pt, indented)
> Blockquote text              → Teal left border, indented
```code here```               → Gray background, Courier New
---                            → Scene break (* * * centered)
**bold** *italic* `code`       → Inline formatting
[text](url)                    → Hyperlink
```

## Protocol

### Step 1: Get the manuscript path

If the user hasn't provided a markdown file path, ask:

> What is the path to your markdown manuscript file?

### Step 2: Verify dependencies

Check that the `docx` npm package is available:

```bash
cd C:/Projects/memstack/skills/kdp-format && npm ls docx 2>/dev/null || npm install docx
```

### Step 3: Run the formatter

```bash
node C:/Projects/memstack/skills/kdp-format/format-kdp.js "<manuscript-path>" "<output-path>"
```

- If `<output-path>` is not specified, it defaults to the manuscript filename with `.docx` extension
- Example: `manuscript.md` → `manuscript.docx`

### Step 4: Report results

After successful generation, report:

```
📚 KDP Format — Complete!

Generated: <output-path>
Trim size: 6" × 9"
Sections: Title page, Copyright, Table of Contents, Body
Chapters: <count>
Parts: <count>

Next steps:
1. Open in Word to verify formatting
2. Check page count for KDP margin requirements
3. Upload to KDP dashboard
```

## Reference

Full KDP specifications are in `skills/kdp-format/kdp-format-SKILL.md` including:
- Front matter and back matter ordering
- Copyright page template
- Ebook vs paperback differences
- KDP upload checklist
- Pricing and category guidance
