---
name: kdp-format
description: "Use when the user says 'kdp', 'format for kdp', 'format book', or 'manuscript' and needs print-ready output."
---


# 📚 KDP Format — Converting manuscript to KDP-ready .docx...
*Convert a markdown manuscript into a professionally formatted Word document for Amazon KDP.*

> **⚠️ WARNING — Unit Systems in python-docx**
>
> - Property setters (e.g., `section.left_margin = Inches(0.75)`) handle unit conversion automatically
> - Raw XML attributes use **TWIPS** (1 inch = 1440 twips), NOT EMU (1 inch = 914400 EMU)
> - **NEVER** use `str(Inches(x))` in raw XML — it produces EMU values, which are 635× too large
> - If you must use raw XML: `twips = int(inches * 1440)`
> - This is the #1 source of "margins are insanely huge" bugs

> **📝 Note:** `format-kdp.js` exists as a companion file in this skill directory. It is a **deprecated JavaScript implementation** (uses the `docx` npm package). The canonical approach is Python with `python-docx`. Do not use or extend `format-kdp.js` for new work — it is retained only as an alternative reference.

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

---

## Implementation Patterns

*Patterns below are derived from real-world python-docx implementations. They supplement the spec sections above with tested code and gotchas.*

### Table of Contents Implementation

python-docx has **no field code API** — TOC entries with page references or hyperlinks require raw XML construction.

#### Paperback (dot-leader page references)

1. **Add bookmarks** to all chapter `Heading 1` paragraphs using `w:bookmarkStart` / `w:bookmarkEnd` XML:

```python
from docx.oxml.ns import qn
import random

def add_bookmark(paragraph, bookmark_name):
    """Add a bookmark to a paragraph for PAGEREF targeting."""
    bookmark_id = str(random.randint(100000, 999999))
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), bookmark_id)
    start.set(qn('w:name'), bookmark_name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), bookmark_id)
    paragraph._p.append(start)
    paragraph._p.append(end)
```

2. **Bookmark naming convention:** `_ch1`, `_ch2`, `_appendix_a`, etc.

3. **Create right-aligned tab stop** with dot leader at text area width:

```python
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_dot_leader_tab(paragraph, text_width_inches):
    """Add a right-aligned tab stop with dot leader."""
    pPr = paragraph._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right')
    tab.set(qn('w:leader'), 'dot')
    tab.set(qn('w:pos'), str(int(text_width_inches * 1440)))  # TWIPS!
    tabs.append(tab)
    pPr.append(tabs)
```

4. **After each TOC entry**, add tab + `PAGEREF` field code using `w:fldChar` (begin/separate/end) + `w:instrText`:

```xml
<!-- Complete PAGEREF field XML pattern -->
<w:r>
  <w:rPr><w:noProof/></w:rPr>
  <w:fldChar w:fldCharType="begin"/>
</w:r>
<w:r>
  <w:rPr><w:noProof/></w:rPr>
  <w:instrText xml:space="preserve"> PAGEREF _ch1 \h </w:instrText>
</w:r>
<w:r>
  <w:rPr><w:noProof/></w:rPr>
  <w:fldChar w:fldCharType="separate"/>
</w:r>
<w:r>
  <w:rPr><w:noProof/></w:rPr>
  <w:t>?</w:t>  <!-- Placeholder until Word resolves -->
</w:r>
<w:r>
  <w:rPr><w:noProof/></w:rPr>
  <w:fldChar w:fldCharType="end"/>
</w:r>
```

5. **PAGEREF resolves** when the user opens in Word and updates fields: **Ctrl+A → F9**
6. python-docx **cannot calculate page numbers** — only Word's layout engine can

#### Ebook (internal hyperlinks)

1. Same bookmarks on `Heading 1` paragraphs (reuse `add_bookmark` above)
2. TOC entries use `w:hyperlink` with `w:anchor` attribute pointing to bookmark names:

```xml
<!-- Complete w:hyperlink pattern for ebook TOC -->
<w:hyperlink w:anchor="_ch1">
  <w:r>
    <w:rPr>
      <w:rStyle w:val="Hyperlink"/>
    </w:rPr>
    <w:t>Chapter 1: Chapter Title</w:t>
  </w:r>
</w:hyperlink>
```

3. **No page numbers, no dot leaders** — ebook readers handle navigation natively

### Mirror Margins (Paperback Only)

Required for proper gutter alternation on verso/recto pages. Only apply to paperback output, **never** ebook.

```python
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sectPr = section._sectPr
sectPr.append(parse_xml(f'<w:mirrorMargins {nsdecls("w")}/>'))
```

This tells Word to swap inside/outside margins on even pages, so the gutter (binding edge) is always on the correct side.

### KDP eBook TOC Validation Requirements

KDP/Kindle requires THREE structural markers to detect a valid TOC — a visually correct TOC that's missing any of these will fail validation:

1. A bookmark named exactly `toc` on the TOC heading paragraph
2. A `{ TOC }` field code (w:fldChar + w:instrText pattern)
3. TOC paragraph styles applied: "TOC Heading" for the title, "TOC 1" / "TOC 2" for entries

If any of these are missing, KDP treats the TOC as "structurally invisible" even if it looks perfect in Word.

### Kindle Create Fallback (eBook)

When DOCX TOC doesn't pass KDP eBook validation, use Kindle Create as the preferred workflow:

1. Import the DOCX into Kindle Create
2. Kindle Create auto-detects chapters and builds a navigable TOC
3. Export as .kpf format
4. Upload .kpf to KDP instead of raw DOCX

This is more reliable than debugging DOCX TOC field codes for eBook specifically. Reserve direct DOCX upload for paperback only.

### Margin Settings — No Raw XML

Add to the existing TWIPS/EMU warning: Even with correct unit values, KDP may reject DOCX files where margins were set via raw XML manipulation (direct w:pgMar attributes). Always use python-docx property setters (`section.left_margin = Inches(x)`) which write XML that KDP accepts. If margins must be fine-tuned beyond what python-docx supports, do it in Word's native interface after generation, not in code.

### KDP Spine Text Margins

- Spine text requires minimum 0.0625" (1/16") padding on EACH side
- At 300 DPI, this equals 19 pixels minimum margin per side
- Usable spine text area = spine_width - 0.125"
- Spine width calculation: pages × 0.002252" (white paper)
- Example: 195-page book has 0.439" spine → usable text area is only 0.314"
- Font sizing loops should use max_height = spine_width_px - 38 (for 19px margins on each side)
- KDP will reject covers where spine text extends into the margin zone
- Always verify margins meet this requirement before outputting final cover PDF

### Dual Output Guidance

Generate paperback and ebook from the same source manuscript:

1. **Build one master document** with all content (title page, copyright, TOC, body, back matter)
2. **Post-process into two variants:**

| Feature | Paperback | Ebook |
|---------|-----------|-------|
| TOC style | Dot-leader with PAGEREF | Hyperlinks with w:anchor |
| Mirror margins | Yes (`w:mirrorMargins`) | No |
| Headers/footers | Yes (author/title, page numbers) | No |
| Page numbers | Yes (suppressed in front matter) | No |
| Trim size | Fixed (e.g., 6" × 9") | No fixed page dimensions |
| Section breaks | Next Page for chapters | Continuous or omitted |

3. **Recommended build script pattern:**
   - Accept a `--format` flag: `paperback` or `ebook`
   - Shared function builds the master document
   - Format-specific post-processing applies/removes features
   - Example: `python format_book.py manuscript.md --format paperback --output book.docx`

### Markdown Table Conversion

Non-fiction manuscripts commonly use pipe tables. Convert to Word tables with proper styling:

- Parse markdown pipe tables (header row, separator, data rows)
- Create `document.add_table()` with appropriate row/column counts
- Apply consistent cell padding and border styling
- Match body font (Georgia 11pt) for table content
- Use bold for header row
- Handle column alignment from the separator row (`:---`, `:---:`, `---:`)

### Section Break Management

Proper section breaks are critical for front matter, body, and back matter formatting:

- **`pgNumType` inheritance:** Each new section inherits page number format from the previous unless explicitly overridden. Set `w:fmt` (e.g., `"lowerRoman"` for front matter, `"decimal"` for body) and `w:start` to reset numbering.
- **Footer chain control:** `w:headerReference` and `w:footerReference` with `w:type` control linking. To make a section's footer independent, you must explicitly unlink it (set "link to previous" to false) before modifying content.
- **Front matter page number suppression:** Use Roman numerals (`i, ii, iii`) or suppress page numbers entirely in front matter sections. Reset to Arabic `1` at the start of the body.
- **Section break + header/footer interaction:** Adding a new section break creates a new section that defaults to "link to previous." You must break the link *before* changing header/footer content, or changes propagate backward to previous sections.

### Pre-Export Checklist

Before generating final output:

- [ ] **TOC sync:** Keep TOC entries in sync with actual document headings — phantom entries cause broken `PAGEREF` fields
- [ ] **Update fields:** Open in Word → Ctrl+A → F9 to update all field codes before final PDF export
- [ ] **Mirror margins:** Verify mirror margins produce correct gutter on odd/even pages (print a test page spread)
- [ ] **Ebook clean:** Check that ebook variant has NO fixed page dimensions, headers/footers, or mirror margins
- [ ] **Cover separate:** Cover is handled separately — this skill is interior formatting only
- [ ] **Bookmark integrity:** Every `PAGEREF` target bookmark must exist in the document; missing bookmarks produce `Error! Bookmark not defined.`

## Level History

- **Lv.1** — Base: Original spec-based formatting guidelines — trim size, fonts, margins, heading hierarchy, page break rules, KDP specifications reference. (Origin: MemStack v2.0–v3.1, Feb 2026)
- **Lv.2** — Implementation: Added real-world implementation patterns — TWIPS/EMU unit warning, TOC field codes (PAGEREF + hyperlink XML), mirror margins XML, dual output guidance (paperback vs ebook), markdown table conversion, section break management, pre-export checklist, KDP validation requirements, Kindle Create fallback, margin safety rules, spine text margin rules. (Origin: MemStack v3.2, Feb 2026)
