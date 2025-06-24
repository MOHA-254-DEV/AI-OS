// dashboard/frontend/components/GoalCard.jsx
import React from 'react';

export default function GoalCard({ goal }) {
  return (
    <div>
      <h2 className="text-xl font-semibold text-indigo-600">{goal.agent_name}</h2>
      <p className="text-gray-700">🎯 Goal: {goal.description}</p>
      <p className="text-gray-500 text-sm">📅 Deadline: {goal.deadline}</p>
      <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-indigo-500 h-2 rounded-full"
          style={{ width: `${goal.progress}%` }}
        />
      </div>
      <p className="text-right text-xs text-gray-600 mt-1">{goal.progress}% complete</p>
    </div>
  );
}
