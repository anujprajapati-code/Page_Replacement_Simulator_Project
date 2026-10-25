# Assignment Answers — Page Replacement Simulator

Name: Anuj Prajapati
Roll No.: BTE25DTA000008

## Part B — Manual tracing
Reference string: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2`  
Number of frames: `3`

The frame rows below show frame contents **after** each page reference. `F` means page fault and `H` means page hit. A dash means the frame is empty/not yet filled.

### FIFO
| Step | Ref | Frame 1 | Frame 2 | Frame 3 | F/H | Replaced |
|---|---|---|---|---|---|---|
| 1 | 7 | 7 | — | — | F | — |
| 2 | 0 | 7 | 0 | — | F | — |
| 3 | 1 | 7 | 0 | 1 | F | — |
| 4 | 2 | 2 | 0 | 1 | F | 7 |
| 5 | 0 | 2 | 0 | 1 | H | — |
| 6 | 3 | 2 | 3 | 1 | F | 0 |
| 7 | 0 | 2 | 3 | 0 | F | 1 |
| 8 | 4 | 4 | 3 | 0 | F | 2 |
| 9 | 2 | 4 | 2 | 0 | F | 3 |
| 10 | 3 | 4 | 2 | 3 | F | 0 |
| 11 | 0 | 0 | 2 | 3 | F | 4 |
| 12 | 3 | 0 | 2 | 3 | H | — |
| 13 | 2 | 0 | 2 | 3 | H | — |

**Faults:** 10 · **Hits:** 3 · **Hit ratio:** 23.08% · **Fault ratio:** 76.92%

### LRU
| Step | Ref | Frame 1 | Frame 2 | Frame 3 | F/H | Replaced |
|---|---|---|---|---|---|---|
| 1 | 7 | 7 | — | — | F | — |
| 2 | 0 | 7 | 0 | — | F | — |
| 3 | 1 | 7 | 0 | 1 | F | — |
| 4 | 2 | 2 | 0 | 1 | F | 7 |
| 5 | 0 | 2 | 0 | 1 | H | — |
| 6 | 3 | 2 | 0 | 3 | F | 1 |
| 7 | 0 | 2 | 0 | 3 | H | — |
| 8 | 4 | 4 | 0 | 3 | F | 2 |
| 9 | 2 | 4 | 0 | 2 | F | 3 |
| 10 | 3 | 4 | 3 | 2 | F | 0 |
| 11 | 0 | 0 | 3 | 2 | F | 4 |
| 12 | 3 | 0 | 3 | 2 | H | — |
| 13 | 2 | 0 | 3 | 2 | H | — |

**Faults:** 9 · **Hits:** 4 · **Hit ratio:** 30.77% · **Fault ratio:** 69.23%

### Optimal
| Step | Ref | Frame 1 | Frame 2 | Frame 3 | F/H | Replaced |
|---|---|---|---|---|---|---|
| 1 | 7 | 7 | — | — | F | — |
| 2 | 0 | 7 | 0 | — | F | — |
| 3 | 1 | 7 | 0 | 1 | F | — |
| 4 | 2 | 2 | 0 | 1 | F | 7 |
| 5 | 0 | 2 | 0 | 1 | H | — |
| 6 | 3 | 2 | 0 | 3 | F | 1 |
| 7 | 0 | 2 | 0 | 3 | H | — |
| 8 | 4 | 2 | 4 | 3 | F | 0 |
| 9 | 2 | 2 | 4 | 3 | H | — |
| 10 | 3 | 2 | 4 | 3 | H | — |
| 11 | 0 | 2 | 0 | 3 | F | 4 |
| 12 | 3 | 2 | 0 | 3 | H | — |
| 13 | 2 | 2 | 0 | 3 | H | — |

**Faults:** 7 · **Hits:** 6 · **Hit ratio:** 46.15% · **Fault ratio:** 53.85%

## Part B — Summary

| Algorithm | Page faults | Page hits | Hit ratio |
|---|---:|---:|---:|
| FIFO | 10 | 3 | 23.08% |
| LRU | 9 | 4 | 30.77% |
| Optimal | 7 | 6 | 46.15% |

## Part C — Experiment 1: Belady's anomaly
Reference string: `1 2 3 4 1 2 5 1 2 3 4 5`

| Algorithm | Faults (3 frames) | Faults (4 frames) |
|---|---:|---:|
| FIFO | 9 | 10 |
| LRU | 10 | 8 |
| Optimal | 7 | 6 |

### Questions
1. **Does any algorithm produce more faults with more frames? Which one?**  
   Yes. FIFO has 9 faults with 3 frames and 10 faults with 4 frames for this reference string. This is Belady's anomaly: adding frames can increase FIFO page faults.

2. **Why do LRU and Optimal never show this behaviour?**  
   LRU and Optimal are stack algorithms: the set of pages resident with a smaller number of frames is contained in the set resident with a larger number of frames at corresponding points. Therefore, adding frames cannot increase their page-fault count. FIFO does not have this stack property.

## Part C — Experiment 2: Custom reference strings

These are example strings with 18 references each. Run them in the simulator to verify.

| Case | Reference string | Frames | FIFO faults | LRU faults |
|---|---|---:|---:|---:|
| LRU better | `5 4 1 5 1 2 5 1 5 5 4 1 2 1 5 2 3 4` | 3 | 11 | 9 |
| FIFO better/equal | `5 1 5 3 5 2 1 5 5 2 3 1 5 1 5 1 5 2` | 4 | 4 | 4 |

### Short questions
1. **Why can Optimal not be implemented in a real operating system?**  
   Optimal needs to know future page references to select the page that will be used farthest in the future. A real OS cannot know the exact future reference string, so Optimal is mainly used as a theoretical benchmark.

2. **What extra hardware or bookkeeping does LRU need compared with FIFO?**  
   LRU must track the recency of page use, for example with timestamps/counters or a stack/list updated on every reference. This adds bookkeeping and can require hardware support. FIFO generally only needs queue order or a replacement pointer.

3. **If the number of frames equals the number of distinct pages in the string, how many faults will every algorithm produce? Why?**  
   Each algorithm faults once for each distinct page on its first reference, then all later references hit because all distinct pages fit in memory. Thus, faults equal the number of distinct pages, assuming the frames start empty.

## Ratio formulas
- Hit ratio = page hits / total page references
- Fault ratio = page faults / total page references
- Hit ratio + fault ratio = 1 (or 100%)
