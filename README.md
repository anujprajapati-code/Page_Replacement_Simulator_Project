# Page Replacement Algorithm Simulator

A Python/Jupyter Notebook project for the Operating Systems Lab assignment. It simulates **FIFO**, **LRU**, and **Optimal** page replacement and compares their page faults, hits, hit ratio, and fault ratio.

## Features
- Accepts comma-separated or space-separated integer page references.
- Validates input and frame count.
- Shows step-by-step frame contents, Hit/Fault, and replaced page.
- Calculates page faults, page hits, hit ratio, and fault ratio.
- Compares FIFO, LRU, and Optimal on identical input.
- Includes manual tracing, Belady's anomaly experiment, and custom-string analysis.

## Files
- `Page_Replacement_Simulator.ipynb` — notebook with explanations, implementation, sample outputs, and assignment answers.
- `page_replacement.py` — standalone Python source code.
- `Project_Report.docx` — brief report.
- `Assignment_Answers.md` — manual tracing and Part C answers.
- `screenshots/` — sample execution screenshots.

## Run the project
### Jupyter Notebook
1. Install Python 3 and Jupyter Notebook (or use Google Colab).
2. Open `Page_Replacement_Simulator.ipynb`.
3. Run the cells from top to bottom.
4. In the interactive cell, enter a page string such as `1 2 3 1 4 2 5` and frame count `3`.

### Run as a Python script
```bash
python page_replacement.py
```
Example input:
```text
Enter page reference string (comma or space separated): 1 2 3 1 4 2 5
Enter number of frames: 3
```

## Algorithm overview
- **FIFO:** evicts the page that has been in memory the longest.
- **LRU:** evicts the page whose most recent use is farthest in the past.
- **Optimal:** evicts the page whose next use is farthest in the future (or that will never be used again). It is a benchmark because future references are not known in advance in a real operating system.

## Sample result
For reference string `1 2 3 1 4 2 5` with 3 frames:
- FIFO: 5 faults, 2 hits
- LRU: 6 faults, 1 hit
- Optimal: 5 faults, 2 hits

Ratios are calculated as `hits / total references` and `faults / total references`.

## Tie-breaking rule
For Optimal, if multiple pages are never referenced again, the page appearing first in the frame list is replaced, as specified in the assignment.

## Author
Name: Anuj Prajapati 
Roll No.: BTE25DTA000008

