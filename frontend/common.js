// ── 通用工具 ──────────────────────────────────────────────────────
const API = window.location.origin + '/api';

function getToken() { return localStorage.getItem('token'); }
function getRole()  { return localStorage.getItem('role'); }
function getUsername() { return localStorage.getItem('username'); }

function authHeaders() {
  return { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + getToken() };
}

async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: authHeaders(),
    ...options
  });
  if (res.status === 401) { logout(); return null; }
  return res;
}

function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}

// 守卫：未登录跳回登录页，角色不对也跳
function requireRole(role) {
  if (!getToken()) { window.location.href = 'login.html'; return false; }
  if (role && getRole() !== role) { window.location.href = getRole() + '.html'; return false; }
  return true;
}

// 简单 toast 提示
function toast(msg, type = 'success') {
  const el = document.createElement('div');
  el.className = 'toast toast-' + type;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.classList.add('show'), 10);
  setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 300); }, 2500);
}

// 通用弹窗
function showModal(html, onConfirm) {
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `<div class="modal-box">${html}
    <div class="modal-actions">
      <button class="btn-secondary" id="modal-cancel">取消</button>
      <button class="btn-primary" id="modal-confirm">确认</button>
    </div></div>`;
  document.body.appendChild(overlay);
  setTimeout(() => overlay.classList.add('show'), 10);
  overlay.querySelector('#modal-cancel').onclick = () => closeModal(overlay);
  overlay.querySelector('#modal-confirm').onclick = () => { onConfirm(overlay); };
}

function closeModal(overlay) {
  overlay.classList.remove('show');
  setTimeout(() => overlay.remove(), 200);
}
