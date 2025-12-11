# tools
def split_text(state):
    """Splits text into chunks."""
    text = state.get("input", "")
    state["chunks"] = [text[i:i+20] for i in range(0, len(text), 20)]
    state["logs"].append(f"Split into {len(state['chunks'])} chunks.")

def summarize_chunks(state):
    """Mock summarization."""
    state["summaries"] = [f"sum({c})" for c in state["chunks"]]
    state["logs"].append("Summarized chunks.")

def merge_summaries(state):
    """Merges summaries into one string."""
    state["final"] = " | ".join(state["summaries"])
    state["logs"].append("Merged summaries.")

def refine_result(state):
    """Refines the result. Loops if too long."""
    current = state["final"]
    if len(current) > 10:
        state["final"] = current[:-5]
        state["logs"].append(f"Refining... length is now {len(state['final'])}")
    else:
        state["logs"].append("Refinement complete.")
# tool registry
TOOL_MAP = {
    "split": split_text,
    "summarize": summarize_chunks,
    "merge": merge_summaries,
    "refine": refine_result
}
