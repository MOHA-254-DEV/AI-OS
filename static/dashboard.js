// Navigation (already present)
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        const id = this.getAttribute('href').substring(1);
        document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    });
});

// Live STATUS
async function updateOverview() {
    try {
        const [statusRes, healthRes, apiRes] = await Promise.all([
            fetch('/api/v1/status'),
            fetch('/health'),
            fetch('/api/v1/status')
        ]);
        const api = await statusRes.json();
        const health = await healthRes.json();
        document.getElementById('status-value').textContent = api.status || "Unknown";
        document.getElementById('health-value').textContent = health.status || "Unknown";
        const features = api.features || [];
        document.getElementById('features-list').innerHTML = features.map(f => `<li>${f}</li>`).join('');
    } catch (e) {
        document.getElementById('status-value').textContent = "Error";
        document.getElementById('health-value').textContent = "Error";
        document.getElementById('features-list').innerHTML = "<li>Error loading features</li>";
    }
}
updateOverview();
setInterval(updateOverview, 4000);

// AGENTS
async function loadAgents() {
    const res = await fetch('/api/v1/agents');
    const data = await res.json();
    const list = document.getElementById('agents-list');
    list.innerHTML = data.agents.length ? data.agents.map(a => `
        <li>
            ${a.name} (Status: ${a.status})
            <button onclick="deleteAgent(${a.id})">Delete</button>
        </li>
    `).join('') : '<li>No agents yet</li>';
}
window.deleteAgent = async function(id) {
    await fetch(`/api/v1/agents?id=${id}`, { method: 'DELETE' });
    loadAgents();
};
document.getElementById('add-agent-form').onsubmit = async function(e) {
    e.preventDefault();
    const name = document.getElementById('agent-name').value;
    await fetch('/api/v1/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    document.getElementById('agent-name').value = '';
    loadAgents();
};
loadAgents();
setInterval(loadAgents, 5000);

// TASKS
async function loadTasks() {
    const res = await fetch('/api/v1/tasks');
    const data = await res.json();
    const list = document.getElementById('tasks-list');
    list.innerHTML = data.tasks.length ? data.tasks.map(t => `
        <li>
            ${t.description} (Status: ${t.status})
            <button onclick="deleteTask(${t.id})">Delete</button>
        </li>
    `).join('') : '<li>No tasks yet</li>';
}
window.deleteTask = async function(id) {
    await fetch(`/api/v1/tasks?id=${id}`, { method: 'DELETE' });
    loadTasks();
};
document.getElementById('add-task-form').onsubmit = async function(e) {
    e.preventDefault();
    const description = document.getElementById('task-desc').value;
    await fetch('/api/v1/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description })
    });
    document.getElementById('task-desc').value = '';
    loadTasks();
};
loadTasks();
setInterval(loadTasks, 5000);
