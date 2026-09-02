const state = { agent: null, sessionId: null, agents: [] };
const picker = document.querySelector('#agent-picker');
const messages = document.querySelector('#messages');
const welcome = document.querySelector('#welcome');
const title = document.querySelector('#conversation-title');
const welcomeTitle = document.querySelector('#welcome-title');
const textarea = document.querySelector('#message');
const composer = document.querySelector('#composer');
const send = document.querySelector('.send');
const toolCount = document.querySelector('#tool-count');
const toolsPopover = document.querySelector('#tools-popover');
const toolList = document.querySelector('#tool-list');

function initials(label) { return label === 'OpenAI' ? 'O' : label[0]; }
function renderAgents() {
  picker.innerHTML = state.agents.map(agent => `<button class="agent-card ${state.agent === agent.id ? 'selected' : ''}" style="--accent:${agent.accent}" data-agent="${agent.id}" type="button"><div class="agent-card-head"><span class="agent-badge">${initials(agent.label)}</span><span class="agent-name">${agent.label}</span></div><div class="agent-model">${agent.model}</div></button>`).join('');
  picker.querySelectorAll('[data-agent]').forEach(button => button.addEventListener('click', () => selectAgent(button.dataset.agent)));
}
function selectAgent(id) {
  state.agent = id; state.sessionId = null;
  const agent = state.agents.find(item => item.id === id);
  title.textContent = `${agent.label} workspace`;
  welcomeTitle.textContent = `Talk to ${agent.label}`;
  textarea.disabled = false; send.disabled = false; textarea.placeholder = `Message ${agent.label}...`;
  toolCount.textContent = `${agent.tools.length} tools ready`;
  toolCount.disabled = false;
  toolList.innerHTML = agent.tools.map(tool => `<span class="tool-chip">${tool.replaceAll('_', ' ')}</span>`).join('');
  closeTools();
  messages.innerHTML = ''; welcome.style.display = '';
  renderAgents(); textarea.focus();
}
function closeTools() {
  toolsPopover.hidden = true;
  toolCount.setAttribute('aria-expanded', 'false');
}
toolCount.addEventListener('click', event => {
  event.stopPropagation();
  const isOpen = !toolsPopover.hidden;
  closeTools();
  if (!isOpen) {
    toolsPopover.hidden = false;
    toolCount.setAttribute('aria-expanded', 'true');
  }
});
document.addEventListener('click', closeTools);
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeTools(); });
function addMessage(role, text) {
  welcome.style.display = 'none';
  const item = document.createElement('div'); item.className = `message ${role}`;
  item.innerHTML = `<span class="message-label">${role === 'user' ? 'YOU' : 'AGENT'}</span><div class="bubble"></div>`;
  item.querySelector('.bubble').textContent = text; messages.appendChild(item); messages.parentElement.scrollTop = messages.parentElement.scrollHeight;
}
async function sendMessage(message) {
  if (!state.agent || !message.trim()) return;
  addMessage('user', message.trim()); textarea.value = ''; textarea.disabled = true; send.disabled = true;
  const typing = document.createElement('div'); typing.className = 'typing'; typing.textContent = 'Thinking...'; messages.appendChild(typing);
  try {
    const response = await fetch('/api/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({agent: state.agent, message, session_id: state.sessionId}) });
    const data = await response.json(); if (!response.ok) throw new Error(data.detail || 'The agent could not respond.');
    state.sessionId = data.session_id; typing.remove(); addMessage('assistant', data.response || 'I completed that request.');
  } catch (error) { typing.remove(); addMessage('assistant', `I could not reach the agent: ${error.message}`); }
  textarea.disabled = false; send.disabled = false; textarea.focus();
}
composer.addEventListener('submit', event => { event.preventDefault(); sendMessage(textarea.value); });
textarea.addEventListener('keydown', event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); composer.requestSubmit(); } });
document.querySelector('#new-chat').addEventListener('click', () => { state.sessionId = null; messages.innerHTML = ''; welcome.style.display = ''; if (state.agent) textarea.focus(); });
document.querySelectorAll('[data-prompt]').forEach(button => button.addEventListener('click', () => { if (state.agent) sendMessage(button.dataset.prompt); }));
fetch('/api/agents').then(response => response.json()).then(data => { state.agents = data.agents; renderAgents(); });
