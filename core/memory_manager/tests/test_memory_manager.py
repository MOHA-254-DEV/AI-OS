# File: tests/test_memory_manager.py

from core.memory_manager.memory_engine import MemoryEngine
import os

def test_memory_store_and_recall():
    engine = MemoryEngine()
    engine.remember("test_key", "This is a short-term memory test.")
    assert engine.recall("test_key") == "This is a short-term memory test."

def test_memory_persistence():
    engine = MemoryEngine()
    engine.remember("persistent_key", "Stored permanently", persistent=True)
    new_engine = MemoryEngine()
    assert new_engine.recall("persistent_key") == "Stored permanently"

def test_context_search():
    engine = MemoryEngine()
    engine.remember("k1", "Search this context about AI.", persistent=True)
    engine.remember("k2", "Another AI topic context.")
    results = engine.context_search("AI")
    assert any("AI" in res for res in results)

def test_forget_behavior():
    engine = MemoryEngine()
    engine.remember("temp_key", "To be forgotten")
    engine.forget("temp_key")
    assert engine.recall("temp_key") == ""

def test_list_memory_keys():
    engine = MemoryEngine()
    engine.remember("key1", "Data in STM")
    engine.remember("key2", "Data in LTM", persistent=True)
    keys = engine.list_memory()
    assert "key1" in keys["short_term"]
    assert "key2" in keys["long_term"]

def teardown_module(module):
    """
    Clean up long_term_mem.json after tests to prevent contamination.
    """
    path = "long_term_mem.json"
    if os.path.exists(path):
        os.remove(path)
