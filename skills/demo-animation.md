---
name: demo-animation
description: Generate a self-playing animated HTML demo for any project. Creates a single-file index.html with an intro screen, dashboard mockup, step-by-step animation with sidebar captions, timeline controls, piano music, cursor animation, highlight system, and ending screen. Use when the user says "create a demo", "make an animation", "demo for my portfolio", "animated walkthrough", or "/demo-animation".
metadata:
  version: 1.0.0
---

# Animated Product Demo Generator

You are a senior frontend developer and product designer. Your job is to generate a single self-playing HTML demo file that walks a viewer through a product's features with animated cursor movements, highlights, captions, and piano music. The output is always one file: `demo/index.html`.

---

## STEP 1: Read the project

Before writing anything, understand the project:

1. Read the project's main files: README, CLAUDE.md, package.json, or equivalent
2. Identify the product name, tagline, and what it does
3. Find the colour palette (CSS variables, brand colours, or infer from the UI)
4. Find the font stack (Google Fonts links, CSS font-family declarations)
5. Identify 6-10 key features or screens to showcase
6. Note the main UI layout: is it a dashboard, a form wizard, a chat app, a CLI tool?

If you cannot determine colours or fonts, ask the user. If the user provided specific instructions about what to showcase, follow those.

---

## STEP 2: Plan the steps

Present a step plan to the user before generating. Example:

> Here's what I'll showcase in the demo:
> 1. Search: user selects filters and runs a search
> 2. Results: data appears in a table
> 3. Detail view: click a row to see details
> ...
>
> Does this look right, or should I change anything?

Aim for 6-10 steps. Each step should be a distinct action or screen transition.

---

## STEP 3: Generate the HTML

Create `demo/index.html` as a single self-contained file. No external dependencies except Google Fonts. Follow the architecture reference below exactly.

---

## Architecture Reference

### CSS Variables (adapt per project)

```css
:root {
  /* Primary brand colours - CHANGE THESE per project */
  --primary-dark: #0D1B2A;      /* Navy - used for navbar, dark backgrounds */
  --primary-dark-light: #1B2D45; /* Lighter navy for hover states */
  --accent: #A8832A;             /* Gold - accent colour, buttons, highlights */
  --accent-light: #C9A84C;       /* Lighter accent for text on dark */
  --accent-glow: rgba(168,131,42,0.15); /* Accent with low opacity for glows */
  --bg-light: #F7F4EF;          /* Cream - main content background */
  --bg-light-dark: #EDE8DF;     /* Darker cream for hover rows */
  --border: #DDD5C8;            /* Border colour */
  --text: #333;                 /* Main text */
  --text-light: #777;           /* Secondary text */

  /* Status colours - usually keep these as-is */
  --hot: #DC2626; --warm: #D97706; --cold: #2563EB;
  --green: #2D6A4F; --purple: #7C3AED;

  /* Dashboard scale - calculated dynamically in JS */
  --scale: 0.82;
}
```

### Fonts

Load two Google Fonts: one serif (for headings, logo, large numbers) and one sans-serif (for body text, labels, UI). Example:

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Swap these to match the project's brand. If the project has no specific fonts, keep these defaults.

### HTML Structure

The demo has exactly 4 top-level elements:

```
1. .intro-screen    (fixed, z-1000) - Logo, tagline, "Watch Demo" button
2. .demo-layout     (fixed grid)    - Dashboard left + Sidebar right
3. .ending-screen   (fixed, z-1000) - Logo, summary, URL, "Replay" button
```

#### 1. Intro Screen

```html
<div class="intro-screen" id="intro">
  <div class="intro-logo">[Product Name]</div>
  <div class="intro-sub">by [Author]</div>
  <div class="intro-tagline">[One-line tagline, italic]</div>
  <button class="intro-start" id="start-btn">Watch Demo</button>
</div>
```

CSS: fixed fullscreen, dark background (`--primary-dark`), centered flex column. Elements animate in with staggered `fadeUp` keyframes (0.3s, 0.8s, 1.4s, 2s delays). Button has border in accent colour, hover fills with accent.

#### 2. Main Layout (Grid)

```html
<div class="demo-layout" id="layout">
  <div class="dashboard-area">
    <div class="dashboard-frame" id="dashboard">
      <!-- Navbar -->
      <!-- Tab content (multiple .tab-pane) -->
      <!-- Highlight ring (absolutely positioned) -->
      <!-- Cursor SVG (absolutely positioned) -->
    </div>
  </div>
  <div class="sidebar" id="sidebar">
    <!-- Caption area -->
    <!-- Progress bar -->
    <!-- Timeline steps -->
    <!-- Controls: prev, pause, next, music, speed -->
  </div>
</div>
```

- Grid: `1fr 360px` (dashboard takes remaining space, sidebar is fixed 360px)
- Dashboard frame: `1280px x 860px`, scaled via CSS `transform: scale(var(--scale))` with `transform-origin: center center`
- Scale is calculated dynamically in JS to fit available viewport

#### Dashboard Frame

Contains a navbar at top (44px) and tab content below. The tab system:

```html
<div class="nav">
  <div class="nav-brand"><span class="nav-name">[Author]</span><span class="nav-sep">|</span><span class="nav-app">[Product]</span></div>
  <div class="nav-tabs">
    <div class="nav-tab active" id="tab-[name]">[Tab1]</div>
    <div class="nav-tab" id="tab-[name]">[Tab2]</div>
    ...
  </div>
</div>
<div class="tab-content">
  <div class="tab-pane active" id="pane-[name]">...</div>
  <div class="tab-pane" id="pane-[name]">...</div>
</div>
```

Tab switching: remove `.active` from all tabs/panes, add to target. Panes use `opacity` + `transform` transitions.

#### Sidebar

```html
<div class="sidebar">
  <!-- Caption: what the current step is about -->
  <div class="sidebar-caption hidden" id="caption">
    <div class="cap-step" id="cap-step"></div>     <!-- "Step 1 of 8" -->
    <div class="cap-text" id="cap-text"></div>      <!-- Main caption (serif, 21px) -->
    <div class="cap-detail" id="cap-detail"></div>  <!-- Detail text (11px, subtle) -->
  </div>
  <div class="sidebar-divider"></div>
  <!-- Progress bar -->
  <div class="tl-progress-track"><div class="tl-progress-fill" id="tl-progress"></div></div>
  <!-- Timeline: vertical list of steps -->
  <div class="sidebar-timeline">
    <div class="tl-steps-v" id="tl-steps">
      <div class="tl-step-v" data-step="0"><div class="tl-dot"></div><div class="tl-label">[Step Name]</div></div>
      ...
    </div>
  </div>
  <!-- Controls -->
  <div class="sidebar-controls">
    <button class="tl-btn" id="btn-prev" title="Previous">&#9664;</button>
    <button class="tl-btn" id="btn-pause" title="Pause">&#10074;&#10074;</button>
    <button class="tl-btn" id="btn-next" title="Next">&#9654;</button>
    <button class="tl-btn active" id="btn-music" title="Sound" style="font-size:12px;">&#9835;</button>
    <button class="tl-btn" id="btn-speed" title="Speed" style="font-size:8px;width:auto;padding:0 8px;border-radius:12px;">1x</button>
    <div class="sidebar-keys">Space · ← → · M · S</div>
  </div>
</div>
```

Timeline steps get `.active` (current) or `.done` (past) classes. The dot grows and glows when active.

#### 3. Ending Screen

```html
<div class="ending-screen" id="ending">
  <div class="ending-title">[Product Name]</div>
  <div class="ending-sub">[One-line description]</div>
  <div class="ending-url">[website URL]</div>
  <button class="ending-replay" id="replay-btn">Replay</button>
</div>
```

Fades in after the last step. Elements stagger in with `fadeUp`. Replay button resets everything and reruns.

---

### JavaScript Engine

#### Core Globals

```js
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

let paused = false, skipResolve = null, currentStep = -1, abortRun = false, runId = 0;
let SCALE = calcScale();
```

#### Dynamic Scale

```js
function calcScale() {
  const sidebarW = 360, pad = 24;
  const availW = window.innerWidth - sidebarW - pad;
  const availH = window.innerHeight - pad;
  const sx = availW / 1280, sy = availH / 860;
  return Math.min(sx, sy, 1);
}
function applyScale() {
  SCALE = calcScale();
  document.documentElement.style.setProperty('--scale', SCALE);
}
applyScale();
window.addEventListener('resize', applyScale);
```

#### wait() and dead()

These are the backbone of the animation system. `wait()` respects pause state, speed multiplier, and abort/runId changes for safe step jumping.

```js
function wait(ms, myId) {
  const adjusted = ms * speedMult;
  return new Promise(resolve => {
    skipResolve = resolve;
    let elapsed = 0;
    const iv = setInterval(() => {
      if (abortRun || (myId !== undefined && myId !== runId)) { clearInterval(iv); resolve(); return; }
      if (!paused) elapsed += 50;
      if (elapsed >= adjusted) { clearInterval(iv); skipResolve = null; resolve(); }
    }, 50);
  });
}
function dead(myId) { return abortRun || myId !== runId; }
```

Every step function must check `if(dead(id)) return;` after each `await wait(...)`. This enables clean abort when the user jumps to a different step.

#### Caption System

```js
function setCaption(step, text, detail = '') {
  captionEl.classList.remove('hidden');
  capStep.textContent = step;
  capText.innerHTML = text;
  capDetail.innerHTML = detail;
}
function hideCaption() { captionEl.classList.add('hidden'); }
```

Caption format: `cap-step` = "Step N of M", `cap-text` = main headline (serif), `cap-detail` = supporting text (small, subtle).

#### Tab Switching

```js
function showTab(name) {
  $$('.nav-tab').forEach(t => t.classList.remove('active'));
  $(`#tab-${name}`).classList.add('active');
  $$('.tab-pane').forEach(p => p.classList.remove('active'));
  $(`#pane-${name}`).classList.add('active');
}
```

#### Scale-Aware Positioning

The dashboard is scaled via CSS transform. All position calculations must divide by SCALE to get correct coordinates within the dashboard frame.

```js
function getLocalPos(el) {
  if (!el) return { x: 0, y: 0, w: 0, h: 0 };
  const r = el.getBoundingClientRect(), dr = dashboard.getBoundingClientRect();
  return {
    x: (r.left - dr.left) / SCALE,
    y: (r.top - dr.top) / SCALE,
    w: r.width / SCALE,
    h: r.height / SCALE
  };
}
function getCenter(el) {
  const p = getLocalPos(el);
  return { x: p.x + p.w / 2, y: p.y + p.h / 2 };
}
```

#### Cursor Animation

```js
function moveCursor(x, y, dur = 500) {
  cursor.classList.add('show');
  cursor.style.transition = `left ${dur}ms cubic-bezier(.25,.1,.25,1), top ${dur}ms cubic-bezier(.25,.1,.25,1)`;
  cursor.style.left = x + 'px';
  cursor.style.top = y + 'px';
  return wait(dur + 80);
}
function hideCursor() { cursor.classList.remove('show'); }
```

The cursor is an SVG arrow inside the dashboard frame (position: absolute, z-index: 100):

```html
<div class="demo-cursor" id="cursor">
  <svg viewBox="0 0 24 24" fill="none">
    <path d="M5 3l14 8-6 2-4 6-4-16z" fill="white" stroke="#333" stroke-width="1.5" stroke-linejoin="round"/>
  </svg>
</div>
```

#### Highlight System

Golden pulsing ring that wraps around any element to draw attention:

```js
function showHighlight(el) {
  if (!el) return;
  const p = getLocalPos(el);
  highlight.style.top = (p.y - 3) + 'px';
  highlight.style.left = (p.x - 3) + 'px';
  highlight.style.width = (p.w + 6) + 'px';
  highlight.style.height = (p.h + 6) + 'px';
  highlight.classList.add('show');
}
function hideHighlight() { highlight.classList.remove('show'); }
```

CSS for the highlight ring uses `pulse-ring` keyframe animation with accent-coloured box-shadow.

#### Auto-Scroll (scrollToShow)

When the demo opens a detail panel or scrollable area, use `scrollToShow(el)` to ensure the target element is visible:

```js
function scrollToShow(el) {
  if (!el || !scrollContainer) return;
  let offset = 0, node = el;
  while (node && node !== scrollContainer) { offset += node.offsetTop; node = node.offsetParent; }
  const margin = 16;
  const elH = el.offsetHeight;
  const viewTop = scrollContainer.scrollTop;
  const viewH = scrollContainer.clientHeight;
  if (offset < viewTop + margin || offset + elH > viewTop + viewH - margin) {
    scrollContainer.scrollTo({ top: Math.max(0, offset - margin), behavior: 'smooth' });
  }
}
```

Adapt `scrollContainer` to whatever scrollable element exists in your dashboard.

#### Type Text Animation

```js
async function typeText(el, text, speed = 40) {
  el.style.color = 'var(--text)';
  el.innerHTML = '';
  el.classList.add('input-caret', 'typing');
  for (let i = 0; i < text.length; i++) {
    if (abortRun) break;
    el.textContent += text[i];
    await wait(speed);
  }
  el.textContent = text;
  el.classList.remove('input-caret', 'typing');
}
```

#### Toast Notifications

```js
function showToast(msg) {
  toast.innerHTML = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2800);
}
```

#### Timeline Update

```js
const TOTAL_STEPS = 8; // adjust to your step count
function updateTimeline(step) {
  currentStep = step;
  $$('.tl-step-v').forEach((el, i) => {
    el.classList.toggle('active', i === step);
    el.classList.toggle('done', i < step);
  });
  tlProgress.style.width = ((step + 1) / TOTAL_STEPS * 100) + '%';
}
```

#### Speed Control

```js
let speedMult = 1;
const SPEEDS = [
  { label: '0.5x', val: 2 },
  { label: '0.7x', val: 1.43 },
  { label: '1x', val: 1 },
  { label: '1.5x', val: 0.67 },
  { label: '2x', val: 0.5 }
];
let speedIdx = 2;

function cycleSpeed() {
  speedIdx = (speedIdx + 1) % SPEEDS.length;
  speedMult = SPEEDS[speedIdx].val;
  $('#btn-speed').textContent = SPEEDS[speedIdx].label;
  $('#btn-speed').classList.toggle('active', speedIdx !== 2);
}
```

Note: `val` is a multiplier applied to `wait()`. Higher val = slower. `val: 2` means 0.5x speed (waits twice as long).

#### Step Functions

Each step is an async function that receives `id` (the current runId). Pattern:

```js
async function step0(id) {
  // 1. Setup: reset UI to the correct state for this step
  setupForThisStep();
  updateTimeline(0);

  // 2. Caption
  setCaption('Step 1 of N', 'Main headline', 'Supporting detail text.');

  // 3. Animate
  await wait(1500, id); if (dead(id)) return;

  // Move cursor to element
  const el = $('#some-element');
  await moveCursor(getCenter(el).x, getCenter(el).y);
  if (dead(id)) return;

  // Highlight element
  showHighlight(el);
  await wait(1000, id); if (dead(id)) return;
  hideHighlight();

  // Type into an input
  await typeText($('#input'), 'Hello world', 45);
  if (dead(id)) return;

  // Click a button (simulate)
  $('#button').classList.add('active');
  await wait(800, id); if (dead(id)) return;

  // Show result
  showToast('Action complete');
  await wait(2000, id); if (dead(id)) return;

  // Clean up
  hideCursor();
}
```

**Rules for step functions:**

1. Always call a setup function first that resets the UI to the correct state for that step (so jumping to any step works)
2. Always call `updateTimeline(stepIndex)` at the start
3. Always check `if(dead(id)) return;` after every `await`
4. Use `wait()` for all timing (never raw `setTimeout` in step logic)
5. Hide cursor at the end of each step if it won't be needed at the start of the next
6. Keep wait times reasonable: 800-2500ms for reading captions, 400-800ms for animations

#### Step Runner and Jump

```js
const steps = [step0, step1, step2, ...];

async function jumpToStep(stepIndex) {
  abortRun = true;
  if (skipResolve) { skipResolve(); skipResolve = null; }
  await new Promise(r => setTimeout(r, 120));
  abortRun = false;
  runId++;
  cleanAll();
  runFromStep(stepIndex, runId);
}

async function runFromStep(startIndex, myId) {
  for (let i = startIndex; i < steps.length; i++) {
    if (dead(myId)) return;
    await steps[i](myId);
    if (dead(myId)) return;
  }
  // After last step: fade out dashboard, show ending
  hideCaption(); hideCursor(); hideHighlight();
  await wait(700, myId); if (dead(myId)) return;
  dashboard.style.opacity = '0';
  layout.classList.remove('visible');
  await wait(600, myId); if (dead(myId)) return;
  stopMusic();
  $('#ending').classList.add('show');
}

async function runDemo() {
  layout.classList.add('visible');
  runId++;
  runFromStep(0, runId);
}
```

#### Event Handlers

```js
// Start button
$('#start-btn').onclick = () => {
  startMusic();
  $('#intro').classList.add('fade-out');
  setTimeout(() => { $('#intro').style.display = 'none'; runDemo(); }, 800);
};

// Replay
$('#replay-btn').onclick = () => {
  startMusic();
  $('#ending').classList.remove('show');
  cleanAll();
  // Reset all setup states
  dashboard.style.opacity = '';
  dashboard.classList.remove('visible');
  layout.classList.add('visible');
  tlProgress.style.width = '0%';
  setTimeout(runDemo, 300);
};

// Keyboard shortcuts
document.addEventListener('keydown', e => {
  if (e.code === 'Space')      { e.preventDefault(); $('#btn-pause').click(); }
  if (e.code === 'ArrowRight') { e.preventDefault(); $('#btn-next').click(); }
  if (e.code === 'ArrowLeft')  { e.preventDefault(); $('#btn-prev').click(); }
  if (e.code === 'KeyM')       { e.preventDefault(); toggleMusic(); }
  if (e.code === 'KeyS')       { e.preventDefault(); cycleSpeed(); }
});

// Sidebar controls
$('#btn-pause').onclick = () => {
  paused = !paused;
  $('#btn-pause').innerHTML = paused ? '&#9654;' : '&#10074;&#10074;';
  $('#btn-pause').classList.toggle('active', paused);
  if (audioCtx && musicPlaying) {
    if (paused) audioCtx.suspend();
    else audioCtx.resume();
  }
};
$('#btn-next').onclick = () => { if (skipResolve) { skipResolve(); skipResolve = null; } };
$('#btn-prev').onclick = () => jumpToStep(Math.max(0, currentStep - 1));

// Timeline step clicks
$$('.tl-step-v').forEach(el =>
  el.addEventListener('click', () => jumpToStep(parseInt(el.dataset.step)))
);

// Music and speed
$('#btn-music').onclick = () => toggleMusic();
$('#btn-speed').onclick = () => cycleSpeed();
```

---

### Piano Music (Web Audio API)

The music is a Yiruma-style generative piano using Web Audio API. It creates realistic piano tones with 5 harmonics, soft attack, long decay, and convolution reverb.

**Copy the entire piano system verbatim from the reference below.** Only change `BPM` if you want a different feel (default 58). The phrases array contains 8 chord progressions (Am, F, G, Em, Dm, C, F, G-Am) that loop infinitely.

```js
let audioCtx = null, musicGain = null, musicPlaying = false, pianoTimer = null;

function initMusic() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  musicGain = audioCtx.createGain();
  musicGain.gain.value = 0;
  // Reverb
  const conv = audioCtx.createConvolver();
  const len = 3.5, rate = audioCtx.sampleRate, imp = audioCtx.createBuffer(2, rate * len, rate);
  for (let c = 0; c < 2; c++) {
    const d = imp.getChannelData(c);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 1.8);
  }
  conv.buffer = imp;
  const dry = audioCtx.createGain(), wet = audioCtx.createGain();
  dry.gain.value = 0.55; wet.gain.value = 0.5;
  musicGain.connect(dry); musicGain.connect(conv); conv.connect(wet);
  dry.connect(audioCtx.destination); wet.connect(audioCtx.destination);
}

function pianoNote(freq, time, dur, vel) {
  if (!audioCtx || !musicPlaying) return;
  const harmonics = [
    { r: 1, g: 1, decay: 1 },
    { r: 2, g: 0.35, decay: 0.85 },
    { r: 3, g: 0.12, decay: 0.7 },
    { r: 4, g: 0.06, decay: 0.55 },
    { r: 5, g: 0.03, decay: 0.4 },
  ];
  harmonics.forEach(h => {
    const o = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    const f = audioCtx.createBiquadFilter();
    o.type = 'sine'; o.frequency.value = freq * h.r;
    o.detune.value = (Math.random() - 0.5) * 3;
    f.type = 'lowpass'; f.frequency.value = Math.min(freq * 5, 4500); f.Q.value = 0.5;
    const v = vel * h.g;
    const attackTime = 0.012, holdTime = 0.08, fullDur = dur * h.decay;
    g.gain.setValueAtTime(0, time);
    g.gain.linearRampToValueAtTime(v, time + attackTime);
    g.gain.setValueAtTime(v, time + attackTime + holdTime);
    g.gain.exponentialRampToValueAtTime(v * 0.3, time + fullDur * 0.35);
    g.gain.exponentialRampToValueAtTime(0.0005, time + fullDur);
    o.connect(f); f.connect(g); g.connect(musicGain);
    o.start(time); o.stop(time + fullDur + 0.1);
  });
}

// Note frequencies
const P = {
  C3:130.81,D3:146.83,E3:164.81,F3:174.61,G3:196,A3:220,B3:246.94,
  C4:261.63,D4:293.66,E4:329.63,F4:349.23,G4:392,A4:440,B4:493.88,
  C5:523.25,D5:587.33,E5:659.26,F5:698.46,G5:783.99,A5:880,B5:987.77,
  Ab3:207.65,Bb3:233.08,Eb4:311.13,Ab4:415.30,Bb4:466.16,Eb5:622.25,Ab5:830.61
};

const BPM = 58, beatS = 60 / BPM;
// 8 phrases: Am, F, G, Em, Dm, C, F, G->Am
const phrases = [
  [{n:P.A3,t:0,d:8,v:.08},{n:P.E4,t:0,d:8,v:.06},{n:P.A4,t:.5,d:3,v:.09},{n:P.C5,t:1,d:2.5,v:.08},{n:P.E5,t:1.5,d:2,v:.10},{n:P.A4,t:2.5,d:2,v:.07},{n:P.E5,t:3,d:2,v:.09},{n:P.C5,t:4,d:2,v:.08},{n:P.A4,t:4.5,d:3,v:.07},{n:P.E5,t:5,d:2,v:.10},{n:P.C5,t:5.5,d:2,v:.08},{n:P.B4,t:6,d:2,v:.07},{n:P.A4,t:6.5,d:1.5,v:.06},{n:P.E5,t:7,d:1,v:.09}],
  [{n:P.F3,t:0,d:8,v:.08},{n:P.C4,t:0,d:8,v:.06},{n:P.F4,t:.5,d:3,v:.09},{n:P.A4,t:1,d:2.5,v:.08},{n:P.C5,t:1.5,d:2,v:.10},{n:P.F4,t:2.5,d:2,v:.07},{n:P.C5,t:3,d:2,v:.09},{n:P.A4,t:4,d:2,v:.08},{n:P.F4,t:4.5,d:3,v:.07},{n:P.C5,t:5,d:2,v:.10},{n:P.A4,t:5.5,d:2,v:.08},{n:P.G4,t:6,d:2,v:.07},{n:P.F4,t:6.5,d:1.5,v:.06},{n:P.A4,t:7,d:1,v:.09}],
  [{n:P.G3,t:0,d:8,v:.08},{n:P.D4,t:0,d:8,v:.06},{n:P.G4,t:.5,d:3,v:.09},{n:P.B4,t:1,d:2.5,v:.08},{n:P.D5,t:1.5,d:2,v:.10},{n:P.G4,t:2.5,d:2,v:.07},{n:P.D5,t:3,d:2,v:.09},{n:P.B4,t:4,d:2,v:.08},{n:P.G4,t:4.5,d:3,v:.07},{n:P.D5,t:5,d:2,v:.10},{n:P.B4,t:5.5,d:2,v:.08},{n:P.A4,t:6,d:2,v:.07},{n:P.G4,t:6.5,d:1.5,v:.06},{n:P.B4,t:7,d:1,v:.09}],
  [{n:P.E3,t:0,d:8,v:.08},{n:P.B3,t:0,d:8,v:.06},{n:P.E4,t:.5,d:3,v:.09},{n:P.G4,t:1,d:2.5,v:.08},{n:P.B4,t:1.5,d:2,v:.10},{n:P.E4,t:2.5,d:2,v:.07},{n:P.B4,t:3,d:2,v:.09},{n:P.G4,t:4,d:2,v:.08},{n:P.E4,t:4.5,d:3,v:.07},{n:P.B4,t:5,d:2,v:.10},{n:P.G4,t:5.5,d:2,v:.08},{n:P.A4,t:6,d:2,v:.07},{n:P.E4,t:6.5,d:1.5,v:.06},{n:P.G4,t:7,d:1,v:.09}],
  [{n:P.D3,t:0,d:8,v:.08},{n:P.A3,t:0,d:8,v:.06},{n:P.D4,t:.5,d:3,v:.09},{n:P.F4,t:1,d:2.5,v:.08},{n:P.A4,t:1.5,d:2,v:.10},{n:P.D4,t:2.5,d:2,v:.07},{n:P.A4,t:3,d:2,v:.09},{n:P.F4,t:4,d:2,v:.08},{n:P.D4,t:4.5,d:3,v:.07},{n:P.A4,t:5,d:2,v:.10},{n:P.F4,t:5.5,d:2,v:.08},{n:P.E4,t:6,d:2,v:.07},{n:P.D4,t:6.5,d:1.5,v:.06},{n:P.F4,t:7,d:1,v:.09}],
  [{n:P.C3,t:0,d:8,v:.08},{n:P.G3,t:0,d:8,v:.06},{n:P.C4,t:.5,d:3,v:.09},{n:P.E4,t:1,d:2.5,v:.08},{n:P.G4,t:1.5,d:2,v:.10},{n:P.C4,t:2.5,d:2,v:.07},{n:P.G4,t:3,d:2,v:.09},{n:P.E4,t:4,d:2,v:.08},{n:P.C4,t:4.5,d:3,v:.07},{n:P.G4,t:5,d:2,v:.10},{n:P.E4,t:5.5,d:2,v:.08},{n:P.D4,t:6,d:2,v:.07},{n:P.C4,t:6.5,d:1.5,v:.06},{n:P.E4,t:7,d:1,v:.09}],
  [{n:P.F3,t:0,d:8,v:.08},{n:P.C4,t:0,d:8,v:.06},{n:P.A4,t:.5,d:3,v:.09},{n:P.C5,t:1,d:2.5,v:.08},{n:P.F4,t:1.5,d:2,v:.10},{n:P.A4,t:2.5,d:2,v:.07},{n:P.C5,t:3,d:2,v:.09},{n:P.F4,t:4,d:2,v:.08},{n:P.A4,t:4.5,d:3,v:.07},{n:P.C5,t:5,d:2,v:.10},{n:P.A4,t:5.5,d:2,v:.08},{n:P.G4,t:6,d:2,v:.07},{n:P.F4,t:6.5,d:1.5,v:.06},{n:P.A4,t:7,d:1,v:.09}],
  [{n:P.G3,t:0,d:4,v:.08},{n:P.D4,t:0,d:4,v:.06},{n:P.G4,t:.5,d:2,v:.09},{n:P.B4,t:1,d:2,v:.08},{n:P.D5,t:1.5,d:1.5,v:.10},{n:P.B4,t:2.5,d:1.5,v:.07},{n:P.A3,t:4,d:4,v:.08},{n:P.E4,t:4,d:4,v:.06},{n:P.A4,t:4.5,d:3,v:.09},{n:P.C5,t:5,d:2,v:.08},{n:P.E5,t:5.5,d:2,v:.10},{n:P.C5,t:6,d:2,v:.08},{n:P.A4,t:6.5,d:1.5,v:.07},{n:P.E5,t:7,d:1,v:.06}]
];

let phraseIdx = 0;
function schedulePhrase() {
  if (!musicPlaying || !audioCtx) return;
  const now = audioCtx.currentTime + 0.15;
  const ph = phrases[phraseIdx % phrases.length];
  ph.forEach(n => pianoNote(n.n, now + n.t * beatS, n.d * beatS, n.v));
  phraseIdx++;
}

function startMusic() {
  initMusic();
  if (audioCtx.state === 'suspended') audioCtx.resume();
  musicPlaying = true;
  musicGain.gain.cancelScheduledValues(audioCtx.currentTime);
  musicGain.gain.setValueAtTime(musicGain.gain.value, audioCtx.currentTime);
  musicGain.gain.linearRampToValueAtTime(0.14, audioCtx.currentTime + 3);
  phraseIdx = 0; schedulePhrase();
  if (pianoTimer) clearInterval(pianoTimer);
  pianoTimer = setInterval(schedulePhrase, 8 * beatS * 1000);
  $('#btn-music').classList.add('active');
}
function stopMusic() {
  if (!audioCtx) return;
  musicPlaying = false;
  musicGain.gain.cancelScheduledValues(audioCtx.currentTime);
  musicGain.gain.setValueAtTime(musicGain.gain.value, audioCtx.currentTime);
  musicGain.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 2);
  if (pianoTimer) { clearInterval(pianoTimer); pianoTimer = null; }
  $('#btn-music').classList.remove('active');
}
function toggleMusic() { if (musicPlaying) stopMusic(); else startMusic(); }
```

---

## Adaptation Rules

When generating for a new project:

1. **Colours:** Replace all CSS variables in `:root` with the project's brand palette. Map:
   - `--primary-dark` = the project's darkest brand colour (navbar, sidebar, intro/ending backgrounds)
   - `--accent` = the project's primary accent (buttons, highlights, active states)
   - `--bg-light` = the light background for content areas
   - Keep status colours (`--hot`, `--warm`, etc.) unless the project has its own status system

2. **Fonts:** Replace the Google Fonts import and all `font-family` declarations. The serif font is used for `.intro-logo`, `.cap-text`, `.heading`, `.ending-title`, score numbers. The sans-serif is used for everything else.

3. **Dashboard content:** Design realistic-looking UI screens that match what the product actually does. Use the project's real data structures, field names, and terminology. Mockup 2-4 tab panes.

4. **Step functions:** Write 6-10 step functions. Each should demonstrate one feature. Follow the exact pattern: setup, updateTimeline, setCaption, animate with cursor/highlight, cleanup.

5. **Intro and ending:** Use the product's name, author, tagline, and URL.

6. **Timeline labels:** Short names for each step (1-2 words). Must match the step count.

---

## Quality Checklist

Before delivering the file, verify:

- [ ] Intro screen shows and fades out on "Watch Demo" click
- [ ] Dashboard appears at correct scale
- [ ] All tab switching works
- [ ] Cursor moves smoothly to target elements
- [ ] Highlights pulse around the correct elements (scale-aware)
- [ ] Captions update for each step with step number, headline, and detail
- [ ] Timeline dots progress correctly
- [ ] Progress bar fills proportionally
- [ ] Pause/resume works (Space key and button)
- [ ] Skip to next step works (Right arrow and button)
- [ ] Jump to any step via timeline click works
- [ ] Speed control cycles through 0.5x, 0.7x, 1x, 1.5x, 2x
- [ ] Piano music starts on "Watch Demo", stops on ending
- [ ] Music toggle works (M key and button)
- [ ] Ending screen shows after last step with replay option
- [ ] Replay resets everything cleanly
- [ ] **Scroll hints:** if a panel has content below the fold, add a scroll hint in the caption: `<span style="display:inline-flex;align-items:center;gap:5px;color:var(--accent-light);font-size:11px;">&#8595; Scroll down to see more</span>`
- [ ] All content within dashboard frame is visible (no overflow clipping)
- [ ] File is completely self-contained (no external JS, no images, only Google Fonts)

---

## Output

Create the file at `demo/index.html` in the current project directory. If the directory doesn't exist, create it.

After generating, tell the user:
> Demo created at `demo/index.html`. Open it in a browser to preview. Click "Watch Demo" to start the animation.
