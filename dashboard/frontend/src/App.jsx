import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [agents, setAgents] = useState([]);
  const [status, setStatus] = useState("");

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setAgents(data.agents);
    };
  }, []);

  const controlAgent = async (id, action) => {
    await fetch(`http://localhost:8000/agents/${id}/action`, {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    });
    setStatus(`${action} command sent to ${id}`);
  };

  const voiceCommand = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recog = new SpeechRecognition();
    recog.onresult = (e) => {
      const command = e.results[0][0].transcript.toLowerCase();
      const words = command.split(" ");
      if (words.includes("pause")) controlAgent(words[1], "pause");
      if (words.includes("resume")) controlAgent(words[1], "resume");
      if (words.includes("scale")) controlAgent(words[1], "scale");
    };
    recog.start();
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">AI Agent Dashboard</h1>
      <button onClick={voiceCommand} className="px-4 py-2 bg-blue-600 text-white rounded mb-4">
        🎙️ Voice Command
      </button>
      <div className="grid grid-cols-1 gap-4">
        {agents.map(agent => (
          <div key={agent.id} className="bg-white p-4 shadow rounded-lg">
            <h2 className="text-lg font-semibold">{agent.id}</h2>
            <p>CPU: {agent.cpu}%</p>
            <p>Memory: {agent.memory}MB</p>
            <p>Queue: {agent.queue}</p>
            <div className="mt-2 space-x-2">
              <button onClick={() => controlAgent(agent.id, "pause")} className="btn">⏸ Pause</button>
              <button onClick={() => controlAgent(agent.id, "resume")} className="btn">▶ Resume</button>
              <button onClick={() => controlAgent(agent.id, "scale")} className="btn">📈 Scale</button>
            </div>
          </div>
        ))}
      </div>
      <p className="mt-4 text-green-600">{status}</p>
    </div>
  );
}

export default App;
// dashboard/frontend/App.jsx
import React, { useEffect, useState } from 'react';
import GoalCard from './components/GoalCard';
import StrategySelector from './components/StrategySelector';

export default function App() {
  const [goals, setGoals] = useState([]);
  const [strategies, setStrategies] = useState({});

  useEffect(() => {
    fetch("/api/goals")
      .then(res => res.json())
      .then(data => setGoals(data));

    fetch("/api/strategies")
      .then(res => res.json())
      .then(data => setStrategies(data));
  }, []);

  const handleStrategyUpdate = (agentId, newStrategy) => {
    fetch(`/api/strategies/${agentId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ strategy: newStrategy }),
    }).then(() => {
      setStrategies({ ...strategies, [agentId]: newStrategy });
    });
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">🎯 AI Goal Planner</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {goals.map(goal => (
          <div key={goal.agent_id} className="bg-white shadow p-4 rounded-xl">
            <GoalCard goal={goal} />
            <StrategySelector
              agentId={goal.agent_id}
              current={strategies[goal.agent_id] || "neutral"}
              onUpdate={handleStrategyUpdate}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
