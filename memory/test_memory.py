# memory/test_memory.py

from memory.memory_manager import MemoryManager

def test_memory():
    mm = MemoryManager()
    agent = "design_bot"

    # Record short-term
    mm.record_task(agent, "Create Logo", "Success")
    mm.record_task(agent, "Design Brochure", "Success")
    mm.record_task(agent, "Sketch Product Concept", "Failed: Incomplete Brief")

    print("Recent Short-Term Memory:")
    for mem in mm.retrieve_recent(agent):
        print(mem)

    # Commit to long-term
    mm.commit_to_long_term(agent)

    print("\nSearching Long-Term Memory for 'logo':")
    found = mm.find_by_keyword(agent, "logo")
    for f in found:
        print(f)

if __name__ == "__main__":
    test_memory()
