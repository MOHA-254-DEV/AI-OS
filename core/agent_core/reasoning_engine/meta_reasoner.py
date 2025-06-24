from typing import List, Dict, Any
from collections import Counter
import math


class MetaReasoner:
    """
    Analyzes a reasoning trace for diversity, structural integrity, and depth of thought.
    Useful for optimizing agent reflection and multi-step decision quality.
    """

    def __init__(self, reasoning_trace: List[Dict[str, Any]]):
        if not isinstance(reasoning_trace, list):
            raise ValueError("Reasoning trace must be a list of dictionaries.")
        for entry in reasoning_trace:
            if not isinstance(entry, dict):
                raise ValueError("Each entry must be a dictionary.")

        self.trace = reasoning_trace
        self.concepts = self._extract_concepts()

    def _extract_concepts(self) -> List[str]:
        return [
            str(entry.get("thought", "")).strip().lower()
            for entry in self.trace
            if isinstance(entry.get("thought", ""), str) and entry.get("thought", "").strip()
        ]

    def _calculate_structure_score(self) -> float:
        """Uniqueness ratio of reasoning steps."""
        total = len(self.concepts)
        if total == 0:
            return 0.0
        unique = len(set(self.concepts))
        return unique / total

    def _calculate_depth_score(self) -> float:
        """Measures informational depth by average character size of 'data' content."""
        total_chars = sum(len(str(entry.get("data", ""))) for entry in self.trace)
        return round(total_chars / max(len(self.trace), 1) / 100.0, 2)

    def _calculate_entropy(self) -> float:
        """Shannon entropy over concept frequency – higher is more diverse."""
        counts = Counter(self.concepts)
        total = sum(counts.values())
        entropy = -sum((freq / total) * math.log2(freq / total) for freq in counts.values() if freq > 0)
        return round(entropy, 2)

    def _average_thought_length(self) -> float:
        """Average word count per 'thought'."""
        if not self.concepts:
            return 0.0
        total_words = sum(len(thought.split()) for thought in self.concepts)
        return round(total_words / len(self.concepts), 2)

    def _detect_redundant_patterns(self, threshold=3) -> List[str]:
        """Detects thoughts that repeat more than threshold times."""
        counts = Counter(self.concepts)
        return [k for k, v in counts.items() if v >= threshold]

    def _most_common_thoughts(self, top_n=3) -> List[str]:
        counts = Counter(self.concepts)
        return [f"{k} ({v})" for k, v in counts.most_common(top_n)]

    def analyze(self) -> Dict[str, Any]:
        if not self.trace:
            return {
                "structure_score": 0.0,
                "depth_score": 0.0,
                "entropy_score": 0.0,
                "avg_thought_length": 0.0,
                "summary": "No reasoning steps to analyze.",
                "redundant": [],
                "top_thoughts": []
            }

        structure_score = round(self._calculate_structure_score(), 2)
        depth_score = self._calculate_depth_score()
        entropy_score = self._calculate_entropy()
        avg_length = self._average_thought_length()
        redundant = self._detect_redundant_patterns()
        common = self._most_common_thoughts()

        return {
            "structure_score": structure_score,
            "depth_score": depth_score,
            "entropy_score": entropy_score,
            "avg_thought_length": avg_length,
            "redundant_patterns": redundant,
            "top_thoughts": common,
            "summary": f"{len(self.trace)} reasoning steps analyzed across {len(set(self.concepts))} unique thoughts."
        }
