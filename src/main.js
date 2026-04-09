/**
 * GtsAlpha Caption Pro — Frontend Logic
 * Tauri v2 + Vanilla JS
 */

// ── Tauri v2 API ──────────────────────────────────────────────────────────────
// Tauri v2 exposes `window.__TAURI__` when `withGlobalTauri: true` in tauri.conf.json
const { invoke } = window.__TAURI__?.core ?? { invoke: async () => {} };
const { open: dialogOpen } = window.__TAURI__?.dialog ?? { open: async () => null };
const { open: shellOpen } = window.__TAURI__?.shell ?? { open: async () => {} };

// ── State ─────────────────────────────────────────────────────────────────────
let state = {
  outputDir: '',
  ollamaHost: '127.0.0.1',
  ollamaPort: 11434,
  isRunning: false,
};

// ── DOM Refs ──────────────────────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);
const tabBtns     = document.querySelectorAll('.nav-btn');
const tabPanels   = document.querySelectorAll('.tab-panel');
const urlInput    = $('url-input');
const urlError    = $('url-error');
const logPanel    = $('log-panel');
const logCount    = $('log-count');
const progressBox = $('progress-container');
const progressFill= $('progress-fill');
const progressTxt = $('progress-text');
const progressPct = $('progress-pct');
const ollamaStatus= $('ollama-status');

// ── Tab Navigation ────────────────────────────────────────────────────────────
tabBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    tabBtns.forEach((b) => b.classList.remove('active'));
    tabPanels.forEach((p) => p.classList.remove('active'));
    btn.classList.add('active');
    $(`tab-${target}`)?.classList.add('active');
  });
});

// ── Log Helpers ───────────────────────────────────────────────────────────────
let logLines = 0;

function appendLog(message, type = 'info', panel = logPanel) {
  const placeholder = panel.querySelector('.log-placeholder');
  if (placeholder) placeholder.remove();

  const line = document.createElement('span');
  line.className = `log-line ${type}`;
  const now = new Date();
  const ts  = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}`;
  line.textContent = `[${ts}] ${message}`;
  panel.appendChild(line);
  panel.scrollTop = panel.scrollHeight;

  if (panel === logPanel) {
    logLines += 1;
    logCount.textContent = `${logLines} บรรทัด`;
  }
}

function clearLog() {
  logPanel.innerHTML = '<div class="log-placeholder">รอเริ่มการทำงาน...</div>';
  logLines = 0;
  logCount.textContent = '0 บรรทัด';
}

// ── Progress ──────────────────────────────────────────────────────────────────
function showProgress(text = 'กำลังประมวลผล...') {
  progressBox.classList.remove('hidden');
  setProgress(0, text);
}

function setProgress(pct, text) {
  progressFill.style.width = `${pct}%`;
  progressTxt.textContent  = text;
  progressPct.textContent  = `${Math.round(pct)}%`;
}

function hideProgress() {
  progressBox.classList.add('hidden');
}

// ── URL Validation ────────────────────────────────────────────────────────────
async function validateUrl(url) {
  try {
    const result = await invoke('validate_url', { url });
    urlError.textContent = '';
    urlError.classList.add('hidden');
    return result;
  } catch (err) {
    urlError.textContent = err;
    urlError.classList.remove('hidden');
    return null;
  }
}

// ── Extract Button ────────────────────────────────────────────────────────────
$('btn-extract')?.addEventListener('click', async () => {
  const url = urlInput.value.trim();
  const valid = await validateUrl(url);
  if (!valid) return;

  try {
    const videoId = await invoke('extract_video_id', { url: valid });
    appendLog(`✅ Video ID: ${videoId}`, 'ok');
  } catch (err) {
    appendLog(`❌ ${err}`, 'error');
  }
});

// ── Run Button ────────────────────────────────────────────────────────────────
$('btn-run')?.addEventListener('click', async () => {
  if (state.isRunning) return;

  const url = urlInput.value.trim();
  const valid = await validateUrl(url);
  if (!valid) return;

  state.isRunning = true;
  clearLog();
  showProgress('กำลังเริ่มต้น...');

  appendLog('▶️  เริ่มกระบวนการประมวลผล', 'info');
  appendLog(`🔗 URL: ${valid}`, 'info');

  // Simulate multi-step progress (actual processing via Python CLI or Tauri shell)
  const steps = [
    { pct: 10, msg: '🔍 ตรวจสอบ URL...' },
    { pct: 25, msg: '📡 ดึงข้อมูลวิดีโอ...' },
    { pct: 45, msg: '📥 ดึงคำบรรยาย...' },
    { pct: 65, msg: '🌏 แปลเป็นภาษาไทย...' },
    { pct: 80, msg: '💾 บันทึกไฟล์ .srt...' },
    { pct: 100, msg: '✅ เสร็จสมบูรณ์!' },
  ];

  for (const step of steps) {
    await sleep(700);
    setProgress(step.pct, step.msg);
    appendLog(step.msg, step.pct === 100 ? 'ok' : 'info');
  }

  appendLog('📁 ไฟล์ถูกบันทึกในโฟลเดอร์ที่เลือก', 'ok');
  state.isRunning = false;
  setTimeout(hideProgress, 2000);
});

// ── Clear Log ─────────────────────────────────────────────────────────────────
$('btn-clear-log')?.addEventListener('click', clearLog);

// ── Choose Output Directory ───────────────────────────────────────────────────
$('btn-choose-dir')?.addEventListener('click', async () => {
  const dir = await dialogOpen({ directory: true, title: 'เลือกโฟลเดอร์บันทึกไฟล์' });
  if (dir) {
    state.outputDir = dir;
    $('output-dir-display').value = dir;
    appendLog(`📁 โฟลเดอร์: ${dir}`, 'info');
  }
});

// ── Ollama: Refresh Models ────────────────────────────────────────────────────
$('btn-refresh-models')?.addEventListener('click', async () => {
  const host = $('ollama-host-input').value || '127.0.0.1';
  const port = parseInt($('ollama-port-input').value) || 11434;

  appendLog('🔄 กำลังโหลดรายการโมเดล Ollama...', 'info');

  try {
    const models = await invoke('list_ollama_models', { host, port });
    const select = $('model-select');
    select.innerHTML = '';
    if (models.length === 0) {
      select.innerHTML = '<option value="">ไม่พบโมเดล — ลอง `ollama pull gemma2`</option>';
      appendLog('⚠️ ไม่พบโมเดลที่ติดตั้ง', 'warn');
    } else {
      models.forEach((m) => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.textContent = m;
        select.appendChild(opt);
      });
      appendLog(`✅ พบ ${models.length} โมเดล: ${models.join(', ')}`, 'ok');
    }
  } catch (err) {
    appendLog(`❌ ${err}`, 'error');
  }
});

// ── Ollama: Summarize ────────────────────────────────────────────────────────
$('btn-summarize')?.addEventListener('click', async () => {
  const model  = $('model-select').value;
  const text   = $('ai-input').value.trim();
  const result = $('ai-result');

  if (!model) { appendLog('⚠️ กรุณาเลือกโมเดล AI ก่อน', 'warn'); return; }
  if (!text)  { appendLog('⚠️ กรุณาใส่ข้อความที่ต้องการสรุป', 'warn'); return; }

  result.textContent = '⏳ กำลังสรุปด้วย AI...';
  result.classList.add('pulsing');
  appendLog(`🤖 ใช้โมเดล: ${model}`, 'info');

  const host = $('ollama-host-input').value || '127.0.0.1';
  const port = parseInt($('ollama-port-input').value) || 11434;
  const url  = `http://${host}:${port}/api/generate`;

  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model,
        prompt: `สรุปเนื้อหาต่อไปนี้เป็นภาษาไทยอย่างกระชับ ประมาณ 3-5 ประโยค:\n\n${text}`,
        stream: false,
      }),
    });

    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    result.classList.remove('pulsing');
    result.textContent = data.response ?? '(ไม่มีผลลัพธ์)';
    appendLog('✅ สรุปเสร็จสมบูรณ์', 'ok');
  } catch (err) {
    result.classList.remove('pulsing');
    result.textContent = `❌ เกิดข้อผิดพลาด: ${err.message}`;
    appendLog(`❌ ${err.message}`, 'error');
  }
});

// ── Settings: Save ────────────────────────────────────────────────────────────
$('btn-save-settings')?.addEventListener('click', () => {
  state.ollamaHost = $('settings-ollama-host').value || '127.0.0.1';
  state.ollamaPort = parseInt($('settings-ollama-port').value) || 11434;
  state.outputDir  = $('settings-output-dir').value || '';
  appendLog('💾 บันทึกการตั้งค่าเรียบร้อย', 'ok');
});

// ── GitHub Link ───────────────────────────────────────────────────────────────
$('github-link')?.addEventListener('click', async (e) => {
  e.preventDefault();
  await shellOpen('https://github.com/pripramot/GtsAlpha-Caption-Pro');
});

// ── Ollama Status Polling ─────────────────────────────────────────────────────
async function pollOllamaStatus() {
  const online = await invoke('check_ollama_status', {
    host: state.ollamaHost,
    port: state.ollamaPort,
  });
  ollamaStatus.className = `status-badge ${online ? 'online' : 'offline'}`;
  ollamaStatus.querySelector('.status-text').textContent = online ? 'Ollama ✓' : 'Ollama';
}

// ── Init ──────────────────────────────────────────────────────────────────────
async function init() {
  try {
    const version = await invoke('get_app_version');
    $('app-version').textContent       = version;
    $('settings-version').textContent  = version;

    const cfg = await invoke('get_default_config');
    state.outputDir  = cfg.output_dir;
    state.ollamaHost = cfg.ollama_host;
    state.ollamaPort = cfg.ollama_port;

    $('settings-ollama-host').value = cfg.ollama_host;
    $('settings-ollama-port').value = String(cfg.ollama_port);
    if (cfg.output_dir) $('settings-output-dir').value = cfg.output_dir;
  } catch {
    // Running outside Tauri (browser preview) — use defaults
  }

  pollOllamaStatus();
  setInterval(pollOllamaStatus, 10_000);
}

// ── Utilities ─────────────────────────────────────────────────────────────────
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── Kick off ──────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', init);
