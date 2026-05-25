# EPUB Colloquial Cantonese Translation & Localization Guidebook

This document serves as the standard operating procedure (SOP) for the translation workflow. Linguistic rules are managed within specialized subagents.

---

## 1. Orchestration Rules (CRITICAL FOR MAIN AGENT)

- **🚫 NO READING BOOK CONTENT:** Do NOT use `read_file` or any tool to look inside `.html` or `.xhtml` files. Your context window must remain clean from the book content for your concentration in coordination.
- **✅ USE THE TASK TOOL:** You MUST use the `task` tool for translation delegation.
  - **Subagent Type:** Set `subagent_type` to `translate-1st` or `translate-2nd`.
  - **Direct Path in Prompt:** Include the full file path directly in the `prompt` field (e.g., `prompt: "Translate file /root/book/extracted/OEBPS/..."`).
  - **No Args Array:** Do NOT use the `args` array for file injection as it is currently unreliable in this environment.
  - **Built-in Instructions:** The subagent has built-in linguistic rules; your prompt should focus on specifying the file and the general action (translate or polish).
- **Direct Modification:** Sub-agents must overwrite files directly on disk.
- **Todo Management:** Track each chapter's 1st and 2nd pass as separate tasks to ensure no duplicate work and clear progress tracking.

---

## 2. Execution Protocol

### Phase 1: Chapter 1 Alignment (Human-in-the-Loop)
- **Action:** Translate only Chapter 1 first.
- **Locate:** Find the first chapter file in the `extracted/` folder.
- **1st Pass:** Call the `task` tool with `subagent_type: "translate-1st"` and specify the file path in the prompt.
- **2nd Pass:** After the 1st pass returns its final report, call the `task` tool with `subagent_type: "translate-2nd"` and specify the same file path in the prompt.
- **Review:** Stop and request human sign-off on the translated tone before proceeding.

### Phase 2: Batch Translation
- **Action:** Proceed with all remaining chapters in batches of 10 files.
- **Todo Management:** Each batch of 10 files (1st + 2nd pass) is tracked as a single todo list item.
- **Parallel Strategy:** Process 5 files at a time concurrently.
  - **Round 1:** Call `task` tool with `subagent_type: "translate-1st"` in parallel for 5 files. Wait for all to complete.
  - **Round 2:** Call `task` tool with `subagent_type: "translate-2nd"` in parallel for the same 5 files.
- **Reporting:** Ensure you receive the summary report from each subtask indicating success before moving to the next file.

---

## 3. Technical Pipeline & Automation

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
