class PluginRegistry:
    def __init__(self):
        self.plugins = [
            {"name": "MarketAnalysis", "entry": "plugins/market_analyzer.py", "runtime": "python", "tags": ["finance", "trading"]},
            {"name": "WebScraper", "entry": "plugins/web_scraper.py", "runtime": "python", "tags": ["data", "scraping"]},
            {"name": "GPTWriter", "entry": "plugins/text_writer.py", "runtime": "python", "tags": ["writing", "assistant"]},
        ]

    def find_plugins_for_goal(self, goal_desc):
        matched = []
        for plugin in self.plugins:
            for tag in plugin["tags"]:
                if tag.lower() in goal_desc.lower():
                    matched.append(plugin)
        return matched
