import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class HeatmapEngine:
    def __init__(self):
        self.task_matrix = {}

    def feed_data(self, data: dict):
        self.task_matrix = data.get("time_heat", {})

    def render_heatmap(self, filename="heatmap.png"):
        heat_data = [v for k, v in sorted(self.task_matrix.items())]
        heat_array = np.array(heat_data).reshape(-1, 1)

        plt.figure(figsize=(10, 6))
        sns.heatmap(heat_array, cmap="YlGnBu", annot=True)
        plt.title("Task Frequency Over Time (per Minute Bucket)")
        plt.ylabel("Minute Buckets")
        plt.xlabel("Agent Activity Intensity")
        plt.tight_layout()
        plt.savefig(filename)
