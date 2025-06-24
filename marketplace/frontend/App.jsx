// marketplace/frontend/App.jsx
import React, { useEffect, useState } from "react";
import PluginCard from "./components/PluginCard";

export default function App() {
  const [plugins, setPlugins] = useState([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetch("/api/plugins")
      .then((res) => res.json())
      .then((data) => setPlugins(data));
  }, []);

  const filtered = plugins.filter((p) =>
    p.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">🔌 Plugin Marketplace</h1>

      <input
        className="mb-4 p-2 w-full border rounded-lg"
        type="text"
        placeholder="Search plugins..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((plugin) => (
          <PluginCard key={plugin.id} plugin={plugin} />
        ))}
      </div>
    </div>
  );
}
