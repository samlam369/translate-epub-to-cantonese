# EPUB Colloquial Cantonese Translation & Localization Guidebook

This document serves as the standard operating procedure (SOP) for the translation workflow. Linguistic rules are managed within the custom slash commands.

---

## 1. Workflow & Token Optimization Strategy

### Phase 1: Chapter 1 Alignment (Human-in-the-Loop)
- **Action:** Translate only Chapter 1 first.
- **Commands:** Use `/translate-1st` followed by `/translate-2nd`.
- **Review:** Request human sign-off on the tone.

### Phase 2: Batch Translation
- **Action:** Proceed with all remaining chapters in batches of 10 files.
- **Todo Management:** Each batch of 10 files (1st + 2nd pass) is tracked as a single todo list item.
- **Parallel Strategy:** Launch 5 subagents at a time.
  - **Round 1:** All 5 subagents complete 1st pass for their assigned files.
  - **Round 2:** All 5 subagents complete 2nd pass for their assigned files.
- **Execution:**
  1. **1st Pass:** `/translate-1st <file_path>` (parallel across 5 subagents)
  2. **2nd Pass:** `/translate-2nd <file_path>` (parallel across 5 subagents)
  3. **Reporting:** Sub-agents report completion status to the main agent.

---

## 2. Technical Pipeline & Automation

### Step A: Extraction
```bash
unzip -q original_book.epub -d extracted
```

### Step B: Rebuilding
```bash
python3 repack_epub.py extracted output_book.epub
```

### Step C: Validation
Use `epubcheck` to ensure integrity:
```bash
# Individual file check
java -jar epubcheck-5.3.0/epubcheck.jar -mode xhtml -v 3.0 <file_path>

# Full package check
java -jar epubcheck-5.3.0/epubcheck.jar output_book.epub
```

---

## 3. Sub-Agent Coordination Rules
- **Direct Modification:** Sub-agents must overwrite files directly on disk.
- **Context Preservation:** The main agent coordinates the pipeline but does not read book content.
- **Todo Management:** Track each chapter's 1st and 2nd pass as separate tasks to ensure no duplicate work and clear progress tracking.
