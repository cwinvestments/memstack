# SKILL: KDP Book Formatting (kdp-format)

## Purpose
Convert markdown manuscript files into a KDP-ready Word document (.docx) for Amazon Kindle Direct Publishing. Handles both paperback and ebook formatting.

## When to Use
- Converting completed manuscript chapters from .md to .docx
- Formatting a book for KDP paperback or ebook submission
- Generating print-ready interior files

---

## KDP PAPERBACK SPECIFICATIONS

### Trim Size
- **Standard non-fiction:** 6" x 9" (most common, recommended)
- **Alternative:** 5.5" x 8.5" (compact non-fiction)
- Use 6x9 unless author specifies otherwise

### Margins (for 6" x 9")
- **Inside (gutter):** 0.75" (accounts for binding)
- **Outside:** 0.5"
- **Top:** 0.75"
- **Bottom:** 0.75"
- For books over 400 pages, increase gutter to 0.875"

### Fonts
- **Body text:** Garamond, 11pt (preferred) or Georgia 11pt or Palatino 11pt
- **Chapter titles:** Same font family, 24pt bold, centered
- **Chapter subtitles:** Same font, 14pt italic, centered
- **Section headings:** Same font, 13pt bold, left-aligned
- **Epigraphs/quotes:** Same font, 10pt italic, indented 0.5" both sides
- **Line spacing:** 1.3 (body text), 1.0 (quotes/epigraphs)

### Page Layout
- **Chapter starts:** Always on recto (right/odd) page — insert blank page if needed
- **First paragraph of chapter:** No indent, optional drop cap (3 lines)
- **All other paragraphs:** 0.3" first-line indent, no space between paragraphs
- **Scene breaks:** Three asterisks centered (* * *) or ornamental dingbat, with 1 blank line above and below
- **Page numbers:** Centered bottom, 9pt, start numbering from Chapter 1 (front matter uses roman numerals)

### Headers/Footers
- **Odd (recto) pages:** Chapter title, right-aligned, 9pt italic
- **Even (verso) pages:** Book title or author name, left-aligned, 9pt italic
- **Chapter opening pages:** No header, page number only
- **Front matter:** No headers

---

## FRONT MATTER (order)
1. **Half title page** — Book title only, centered, no subtitle
2. **Also by page** (optional) — "Also by [Author]" with list of other books
3. **Title page** — Full title, subtitle, author name, centered
4. **Copyright page** — Copyright notice, ISBN, publisher, rights statement, edition info
5. **Dedication** — Short, centered, own page
6. **Epigraph** (optional) — Opening quote for the whole book
7. **Table of Contents** — Chapter numbers and titles with page numbers
8. **Author's Note / Preface** (optional)

### Copyright Page Template
```
Copyright © [Year] [Author Name]
All rights reserved.

No part of this publication may be reproduced, distributed, or transmitted
in any form or by any means without the prior written permission of the
publisher, except in the case of brief quotations in reviews and certain
other noncommercial uses permitted by copyright law.

Published by [Publisher Name or "Self-published"]
[City, State]

ISBN: [Paperback ISBN]
ISBN: [Ebook ISBN]

First Edition: [Month Year]

Cover design by [Designer]

www.[authorwebsite].com
```

---

## BACK MATTER (order)
1. **Acknowledgments** (optional)
2. **Appendices** — Labeled Appendix A, B, C etc.
3. **Notes / Endnotes** — Chapter-by-chapter if used
4. **Bibliography / Sources**
5. **Index** (optional, complex non-fiction)
6. **About the Author** — Short bio, photo optional, links to website/social
7. **Also by the Author** — Other books with brief descriptions
8. **Call to Action** — Review request, newsletter signup, website link

### About the Author Template
```
[Author Name] is [credentials]. [One sentence about relevant work].
[One sentence about what drives them].

[Website]
[Social media]
```

### Review Request Template
```
Did you enjoy this book?

Reviews help independent authors reach new readers.
If this book gave you something to think about, please
consider leaving a review on Amazon. It takes 30 seconds
and makes a real difference.

Thank you for your support.
```

---

## CHAPTER FORMATTING

### Chapter Opening Page
```
[Blank space — approximately 1/3 down the page]

CHAPTER [NUMBER]
[Chapter Title]
[Subtitle if applicable]

[Epigraph in italics, 10pt, indented]
— [Attribution]

[Section separator]

[Body text begins — no indent on first paragraph]
```

### Section Breaks Within Chapters
- Use `---` in markdown → convert to centered ornamental break or `* * *`
- 1 blank line above and below

### Blockquotes / Epigraphs
- Indented 0.5" from both margins
- Italic
- Attribution on its own line, right-aligned, preceded by em dash
- 10pt font (1pt smaller than body)

---

## PYTHON DOCX IMPLEMENTATION

### Required Package
```
pip install python-docx
```

### Key Code Patterns

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

doc = Document()

# Page setup (6x9)
section = doc.sections[0]
section.page_width = Inches(6)
section.page_height = Inches(9)
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.75)   # gutter/inside
section.right_margin = Inches(0.5)   # outside

# Styles
style = doc.styles['Normal']
font = style.font
font.name = 'Garamond'
font.size = Pt(11)
style.paragraph_format.line_spacing = 1.3
style.paragraph_format.first_line_indent = Inches(0.3)
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.space_before = Pt(0)

# Chapter title style
chapter_style = doc.styles.add_style('ChapterTitle', 1)  # WD_STYLE_TYPE.PARAGRAPH
chapter_style.font.name = 'Garamond'
chapter_style.font.size = Pt(24)
chapter_style.font.bold = True
chapter_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
chapter_style.paragraph_format.space_before = Inches(2.5)  # push down page
chapter_style.paragraph_format.space_after = Pt(6)
chapter_style.paragraph_format.first_line_indent = Inches(0)

# Force new page for chapters
paragraph = doc.add_paragraph('Chapter 1', style='ChapterTitle')
# Add section break (odd page) before each chapter:
new_section = doc.add_section()
new_section.start_type = 3  # WD_SECTION_START.ODD_PAGE

# Epigraph
epigraph = doc.add_paragraph()
epigraph.paragraph_format.left_indent = Inches(0.5)
epigraph.paragraph_format.right_indent = Inches(0.5)
epigraph.paragraph_format.first_line_indent = Inches(0)
run = epigraph.add_run('"Quote text here"')
run.italic = True
run.font.size = Pt(10)

# First paragraph (no indent)
first_para = doc.add_paragraph('Opening text...')
first_para.paragraph_format.first_line_indent = Inches(0)

# Scene break
scene_break = doc.add_paragraph('* * *')
scene_break.alignment = WD_ALIGN_PARAGRAPH.CENTER
scene_break.paragraph_format.space_before = Pt(12)
scene_break.paragraph_format.space_after = Pt(12)
scene_break.paragraph_format.first_line_indent = Inches(0)
```

### Markdown to DOCX Conversion Logic
```
# in markdown → Chapter Title (24pt bold centered)
## in markdown → Section Heading (13pt bold left)
> blockquote → Epigraph style (10pt italic indented)
--- → Scene break (* * * centered)
**bold** → bold run
*italic* → italic run
Normal paragraph → Body text with 0.3" indent
First paragraph after heading/break → No indent
```

---

## EBOOK (KINDLE) SPECIFICATIONS

### File Format
- Submit .docx or .epub (KDP converts to .mobi/.azw)
- .docx is easiest if using python-docx

### Key Differences from Paperback
- No fixed page size (reflowable)
- No headers/footers
- No page numbers
- Table of Contents uses hyperlinks (NCX/HTML TOC)
- Images must be embedded, not linked
- No drop caps (unreliable on Kindle)
- Use relative font sizes, not absolute

### Ebook-Specific Formatting
- Chapter titles: Heading 1 style (Kindle uses for auto-TOC)
- Section headings: Heading 2 style
- No first-line indent on first paragraph after heading
- 0.3" indent on all other paragraphs
- Scene breaks: centered ornament or `* * *`
- Front matter: keep minimal (readers want to get to content)

---

## KDP UPLOAD CHECKLIST

### Before Upload
- [ ] Spell check entire manuscript
- [ ] Verify all chapter titles match Table of Contents
- [ ] Check page numbers are correct
- [ ] Verify no widows/orphans (single lines at top/bottom of page)
- [ ] Confirm margins meet KDP minimums for page count
- [ ] Test print at 6x9 to check layout
- [ ] Front matter complete (title, copyright, dedication, TOC)
- [ ] Back matter complete (about author, review request, also by)
- [ ] ISBN obtained (KDP provides free one, or use your own)

### KDP Dashboard Settings
- **Category:** Choose 2 BISAC categories
- **Keywords:** 7 keywords/phrases (use all 7)
- **Description:** 4,000 char max, supports basic HTML (<b>, <i>, <br>, <h2>)
- **Pricing:** $2.99-$9.99 for 70% royalty, outside range = 35% royalty
- **Paperback pricing:** Must cover printing cost + your royalty
- **Territories:** Worldwide rights (unless restricted)

---

## CC PROMPT TEMPLATE FOR FORMATTING

```
Read C:\Projects\memstack\MEMSTACK.md and follow the MemStack skill framework.
Read C:\Projects\memstack\skills\kdp-format\SKILL.md for book formatting specs.

Working directory: C:\Projects\[BookName]

Convert all manuscript/*.md files into a single KDP-ready .docx file.

1. Parse all .md files in order (00-front-matter.md, 01-*.md, 02-*.md, etc.)
2. Apply 6x9 trim, Garamond 11pt, proper margins per the skill spec
3. Each chapter starts on odd (recto) page
4. Convert markdown formatting to proper Word styles
5. Add Table of Contents after dedication
6. Add page numbers (centered bottom, starting from Chapter 1)
7. Save to [BookName]-manuscript.docx

Do NOT use any external templates. Build the document from scratch using python-docx.
```
