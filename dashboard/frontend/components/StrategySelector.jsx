// dashboard/frontend/components/StrategySelector.jsx
import React from 'react';

const STRATEGY_OPTIONS = ["aggressive", "conservative", "neutral", "exploratory"];

export default function StrategySelector({ agentId, current, onUpdate }) {
  return (
    <div className="mt-4">
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Strategy Behavior:
      </label>
      <select
        value={current}
        onChange={(e) => onUpdate(agentId, e.target.value)}
        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
      >
        {STRATEGY_OPTIONS.map(opt => (
          <option key={opt} value={opt}>
            {opt.charAt(0).toUpperCase() + opt.slice(1)}
          </option>
        ))}
      </select>
    </div>
  );
}
