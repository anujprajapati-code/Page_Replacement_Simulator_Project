from typing import List, Dict, Any, Tuple

def _validate_input(reference: List[int], num_frames: int) -> None:
    if not reference:
        raise ValueError("The page reference string must contain at least one page.")
    if not isinstance(num_frames, int) or num_frames < 1:
        raise ValueError("Number of frames must be an integer greater than or equal to 1.")
    if any(not isinstance(page, int) for page in reference):
        raise ValueError("Every page reference must be an integer.")

def fifo(reference: List[int], num_frames: int) -> Tuple[int, int, List[Dict[str, Any]]]:
    """FIFO replaces the page that entered memory earliest."""
    _validate_input(reference, num_frames)
    frames = []
    pointer = 0
    trace = []
    faults = hits = 0
    for step, page in enumerate(reference, start=1):
        replaced = None
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Fault"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                replaced = frames[pointer]
                frames[pointer] = page
                pointer = (pointer + 1) % num_frames
        trace.append({"step": step, "page": page, "frames": frames.copy(),
                      "status": status, "replaced": replaced})
    return faults, hits, trace

def lru(reference: List[int], num_frames: int) -> Tuple[int, int, List[Dict[str, Any]]]:
    """LRU replaces the page whose most recent use was farthest in the past."""
    _validate_input(reference, num_frames)
    frames = []
    last_used = {}
    trace = []
    faults = hits = 0
    for step, page in enumerate(reference, start=1):
        replaced = None
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Fault"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                victim = min(frames, key=lambda p: last_used[p])
                replaced = victim
                frames[frames.index(victim)] = page
        last_used[page] = step
        trace.append({"step": step, "page": page, "frames": frames.copy(),
                      "status": status, "replaced": replaced})
    return faults, hits, trace

def optimal(reference: List[int], num_frames: int) -> Tuple[int, int, List[Dict[str, Any]]]:
    """Optimal replaces the page whose next use is farthest in the future."""
    _validate_input(reference, num_frames)
    frames = []
    trace = []
    faults = hits = 0
    for i, page in enumerate(reference):
        replaced = None
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Fault"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                future = reference[i + 1:]
                # Tie rule required by the assignment: replace the first frame
                # whose page is never used again; otherwise farthest next use.
                next_positions = []
                for candidate in frames:
                    try:
                        next_positions.append(future.index(candidate))
                    except ValueError:
                        next_positions.append(float("inf"))
                max_distance = max(next_positions)
                victim_index = next_positions.index(max_distance)
                replaced = frames[victim_index]
                frames[victim_index] = page
        trace.append({"step": i + 1, "page": page, "frames": frames.copy(),
                      "status": status, "replaced": replaced})
    return faults, hits, trace

def parse_reference_string(raw: str) -> List[int]:
    """Accept comma-separated or whitespace-separated non-negative integer pages."""
    tokens = raw.replace(",", " ").split()
    if not tokens:
        raise ValueError("Enter at least one page number.")
    try:
        pages = [int(token) for token in tokens]
    except ValueError as exc:
        raise ValueError("Invalid page reference: use only integer page numbers separated by commas or spaces.") from exc
    if any(page < 0 for page in pages):
        raise ValueError("Page numbers must be non-negative integers.")
    return pages

def print_trace(name: str, result: Tuple[int, int, List[Dict[str, Any]]], total: int) -> None:
    faults, hits, trace = result
    print(f"\\n{name}")
    frame_count = max(len(row["frames"]) for row in trace)
    headers = ["Step", "Page"] + [f"Frame {i+1}" for i in range(frame_count)] + ["Result", "Replaced"]
    print(" | ".join(headers))
    print("-" * (len(" | ".join(headers)) + 12))
    for row in trace:
        frame_values = [str(x) for x in row["frames"]] + ["-"] * (frame_count - len(row["frames"]))
        print(" | ".join([str(row["step"]), str(row["page"])] + frame_values +
                         [row["status"], "-" if row["replaced"] is None else str(row["replaced"])]))
    print(f"Page faults: {faults}")
    print(f"Page hits:   {hits}")
    print(f"Hit ratio:   {hits / total:.2%}")
    print(f"Fault ratio: {faults / total:.2%}")

def compare_algorithms(reference: List[int], num_frames: int, show_traces: bool = True):
    results = {
        "FIFO": fifo(reference, num_frames),
        "LRU": lru(reference, num_frames),
        "Optimal": optimal(reference, num_frames),
    }
    if show_traces:
        for name, result in results.items():
            print_trace(name, result, len(reference))
    print("\\nPERFORMANCE COMPARISON")
    print(f"{'Algorithm':<12} {'Faults':>8} {'Hits':>8} {'Hit ratio':>12} {'Fault ratio':>12}")
    print("-" * 56)
    for name, (faults, hits, _) in results.items():
        print(f"{name:<12} {faults:>8} {hits:>8} {hits/len(reference):>11.2%} {faults/len(reference):>11.2%}")
    return results

def run_interactive():
    try:
        raw = input("Enter page reference string (comma or space separated): ")
        reference = parse_reference_string(raw)
        raw_frames = input("Enter number of frames: ").strip()
        try:
            num_frames = int(raw_frames)
        except ValueError as exc:
            raise ValueError("Number of frames must be a whole number.") from exc
        if num_frames < 1:
            raise ValueError("Number of frames must be at least 1.")
        compare_algorithms(reference, num_frames)
    except ValueError as error:
        print(f"Input error: {error}")

if __name__ == "__main__":
    run_interactive()
