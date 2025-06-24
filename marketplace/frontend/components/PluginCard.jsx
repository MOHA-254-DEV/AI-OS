// marketplace/frontend/components/PluginCard.jsx
import React from "react";

export default function PluginCard({ plugin }) {
  const handleInstall = () => {
    fetch(`/api/plugins/install/${plugin.id}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => alert(`✅ Installed: ${plugin.name}`));
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-xl font-bold text-indigo-600">{plugin.name}</h2>
      <p className="text-gray-700">{plugin.description}</p>
      <p className="text-xs text-gray-500 mt-2">
        🧾 Version: {plugin.version} | ⭐ {plugin.rating}/5
      </p>
      <button
        onClick={handleInstall}
        className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded"
      >
        Install Plugin
      </button>
    </div>
  );
}
