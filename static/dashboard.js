// --- Navigation ---
document.querySelectorAll('.list-group-item-action').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    document.querySelectorAll('.list-group-item-action').forEach(l => l.classList.remove('active'));
    this.classList.add('active');
    const section = this.getAttribute('data-section');
    document.querySelectorAll('.content-section').forEach(sec => sec.classList.add('d-none'));
    document.getElementById(section + '-section').classList.remove('d-none');
  });
});

// --- Dashboard Data ---
async function updateDashboard() {
  try {
    const [statusRes, healthRes, apiRes] = await Promise.all([
      fetch('/api/v1/status'),
      fetch('/health'),
      fetch('/api/v1/status')
    ]);
    const status = await statusRes.json();
    const health = await healthRes.json();
    const api = await apiRes.json();
    document.getElementById('status-value').textContent = status.status || "Unknown";
    document.getElementById('status-detail').textContent = "API Version: " + (api.api_version || "Unknown");
    document.getElementById('health-value').textContent = health.status || "Unknown";
    document.getElementById('health-timestamp').textContent = health.timestamp || "";
    const features = api.features || [];
    document.getElementById('features-list').innerHTML = features.length ? features.map(f => `<li>✅ ${f}</li>`).join('') : "<li>No features</li>";
  } catch {
    document.getElementById('status-value').textContent = "Error";
    document.getElementById('health-value').textContent = "Error";
    document.getElementById('features-list').innerHTML = "<li>Error loading features</li>";
  }
}
updateDashboard();
setInterval(updateDashboard, 6000);

// --- AGENTS CRUD ---
const agentsList = document.getElementById('agents-list');
const agentsLoading = document.getElementById('agents-loading');
const agentsFeedback = document.getElementById('agents-feedback');

async function loadAgents() {
  agentsLoading.classList.remove('d-none');
  try {
    const res = await fetch('/api/v1/agents');
    const data = await res.json();
    agentsList.innerHTML = '';
    if (!data.agents.length) {
      agentsList.innerHTML = `<div class="col-12"><div class="alert alert-secondary">No agents yet. Add your first agent!</div></div>`;
    } else {
      data.agents.forEach(agent => {
        const card = document.createElement('div');
        card.className = 'col-12 col-md-6 col-lg-4';
        card.innerHTML = `
          <div class="card glass h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title mb-2">${agent.name}</h5>
              <div class="mb-2">Status: <span class="badge bg-${agent.status === 'idle' ? 'secondary' : 'success'}">${agent.status}</span></div>
              <div class="mt-auto d-flex justify-content-end">
                <button class="btn btn-sm btn-outline-danger" onclick="deleteAgent(${agent.id})">Delete</button>
              </div>
            </div>
          </div>
        `;
        agentsList.appendChild(card);
      });
    }
  } catch {
    agentsList.innerHTML = `<div class="col-12"><div class="alert alert-danger">Failed to load agents.</div></div>`;
  }
  agentsLoading.classList.add('d-none');
}
window.deleteAgent = async function(id) {
  if (!confirm('Delete this agent?')) return;
  const res = await fetch(`/api/v1/agents?id=${id}`, { method: 'DELETE' });
  if (res.ok) {
    showFeedback(agentsFeedback, 'Agent deleted.', 'success');
    loadAgents();
  } else {
    showFeedback(agentsFeedback, 'Failed to delete.', 'danger');
  }
};
document.getElementById('add-agent-form').onsubmit = async function(e) {
  e.preventDefault();
  const name = document.getElementById('agent-name').value.trim();
  if (!name) return;
  const btn = this.querySelector('button[type=submit]');
  btn.disabled = true;
  const res = await fetch('/api/v1/agents', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  btn.disabled = false;
  if (res.ok) {
    showFeedback(agentsFeedback, 'Agent added successfully!', 'success');
    document.getElementById('agent-name').value = '';
    bootstrap.Modal.getInstance(document.getElementById('addAgentModal')).hide();
    loadAgents();
  } else {
    showFeedback(agentsFeedback, 'Error adding agent.', 'danger');
  }
};
loadAgents();
setInterval(loadAgents, 8000);

// --- TASKS CRUD ---
const tasksList = document.getElementById('tasks-list');
const tasksLoading = document.getElementById('tasks-loading');
const tasksFeedback = document.getElementById('tasks-feedback');

async function loadTasks() {
  tasksLoading.classList.remove('d-none');
  try {
    const res = await fetch('/api/v1/tasks');
    const data = await res.json();
    tasksList.innerHTML = '';
    if (!data.tasks.length) {
      tasksList.innerHTML = `<div class="col-12"><div class="alert alert-secondary">No tasks yet. Add your first task!</div></div>`;
    } else {
      data.tasks.forEach(task => {
        const card = document.createElement('div');
        card.className = 'col-12 col-md-6 col-lg-4';
        card.innerHTML = `
          <div class="card glass h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title mb-2">${task.description}</h5>
              <div class="mb-2">Status: <span class="badge bg-${task.status === 'pending' ? 'warning' : 'success'}">${task.status}</span></div>
              <div class="mt-auto d-flex justify-content-end">
                <button class="btn btn-sm btn-outline-danger" onclick="deleteTask(${task.id})">Delete</button>
              </div>
            </div>
          </div>
        `;
        tasksList.appendChild(card);
      });
    }
  } catch {
    tasksList.innerHTML = `<div class="col-12"><div class="alert alert-danger">Failed to load tasks.</div></div>`;
  }
  tasksLoading.classList.add('d-none');
}
window.deleteTask = async function(id) {
  if (!confirm('Delete this task?')) return;
  const res = await fetch(`/api/v1/tasks?id=${id}`, { method: 'DELETE' });
  if (res.ok) {
    showFeedback(tasksFeedback, 'Task deleted.', 'success');
    loadTasks();
  } else {
    showFeedback(tasksFeedback, 'Failed to delete.', 'danger');
  }
};
document.getElementById('add-task-form').onsubmit = async function(e) {
  e.preventDefault();
  const description = document.getElementById('task-desc').value.trim();
  if (!description) return;
  const btn = this.querySelector('button[type=submit]');
  btn.disabled = true;
  const res = await fetch('/api/v1/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description })
  });
  btn.disabled = false;
  if (res.ok) {
    showFeedback(tasksFeedback, 'Task added successfully!', 'success');
    document.getElementById('task-desc').value = '';
    bootstrap.Modal.getInstance(document.getElementById('addTaskModal')).hide();
    loadTasks();
  } else {
    showFeedback(tasksFeedback, 'Error adding task.', 'danger');
  }
};
loadTasks();
setInterval(loadTasks, 8000);

// --- Feedback Helper ---
function showFeedback(div, msg, type="info") {
  div.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
    ${msg}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  </div>`;
  setTimeout(() => { div.innerHTML = ""; }, 4000);
}
