from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from threading import Lock
from typing import List, Tuple


class SemanticSearchEngine:
    """
    A simple semantic search engine using TF-IDF and cosine similarity.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.indexed_memories = {}  # {memory_id: text}
        self.tfidf_matrix = None
        self.lock = Lock()

    def index_memory(self, memory_id: str, text: str) -> None:
        """
        Adds or updates a memory in the semantic index.

        Args:
            memory_id (str): Unique memory ID.
            text (str): Memory content.
        """
        with self.lock:
            self.indexed_memories[memory_id] = text
            self._rebuild_index()

    def remove_from_index(self, memory_id: str) -> bool:
        """
        Removes a memory from the index.

        Args:
            memory_id (str): Memory ID to remove.

        Returns:
            bool: True if removed, False if not found.
        """
        with self.lock:
            if memory_id in self.indexed_memories:
                del self.indexed_memories[memory_id]
                self._rebuild_index()
                return True
            return False

    def search(self, query: str, top_k: int = 5, return_scores: bool = False) -> List:
        """
        Performs a semantic search on the indexed memories.

        Args:
            query (str): The search query.
            top_k (int): Number of top results to return.
            return_scores (bool): Whether to return similarity scores.

        Returns:
            List[str] or List[Tuple[str, float]]: Top matching memory IDs or (ID, score) tuples.
        """
        with self.lock:
            if not self.indexed_memories:
                return []

            documents = list(self.indexed_memories.values())
            memory_ids = list(self.indexed_memories.keys())

            all_texts = documents + [query]
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)

            query_vec = tfidf_matrix[-1]
            doc_matrix = tfidf_matrix[:-1]

            similarities = cosine_similarity(query_vec, doc_matrix).flatten()
            ranked_indices = similarities.argsort()[::-1][:top_k]

            if return_scores:
                return [(memory_ids[i], float(similarities[i])) for i in ranked_indices]
            return [memory_ids[i] for i in ranked_indices]

    def _rebuild_index(self):
        """
        Rebuilds the TF-IDF matrix after any insert/delete operation.
        """
        texts = list(self.indexed_memories.values())
        if texts:
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        else:
            self.tfidf_matrix = None

    def list_all_indexed_ids(self) -> List[str]:
        """
        Returns all memory IDs currently in the index.

        Returns:
            List[str]: List of memory IDs.
        """
        with self.lock:
            return list(self.indexed_memories.keys())

    def clear_index(self) -> None:
        """
        Clears the entire index.
        """
        with self.lock:
            self.indexed_memories.clear()
            self.tfidf_matrix = None
