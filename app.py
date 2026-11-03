import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(
    page_title="Haven | Anchor in the Storm",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Ambient CSS & Fixes for Chat Input Visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 50% 15%, #0f172a 0%, #030712 100%);
        color: #f1f5f9;
    }
    
    /* CRITICAL FIX: Chat Input Text Color & Visibility */
    [data-testid="stChatInput"] {
        background-color: #1e293b !important;
        border: 1.5px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background-color: transparent !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        caret-color: #38bdf8 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
        font-weight: 400 !important;
    }
    [data-testid="stChatInput"] button {
        color: #38bdf8 !important;
        background-color: rgba(56, 189, 248, 0.15) !important;
        border-radius: 10px !important;
    }

    /* Message Bubbles */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.3) !important;
        color: #f8fafc !important;
    }
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(56, 189, 248, 0.15) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
    }
    
    /* Elegant Glowing Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 14px;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(129, 140, 248, 0.3) 100%);
        border-color: #38bdf8;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Rich Interactive Audio-Visual Canvas Component
interactive_canvas_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    overflow: hidden;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none;
    -webkit-user-select: none;
  }
  #container {
    position: relative;
    width: 100%;
    height: 480px;
    border-radius: 24px;
    overflow: hidden;
    background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
    box-shadow: 0 16px 40px rgba(0,0,0,0.6), inset 0 0 40px rgba(56, 189, 248, 0.12);
    border: 1.5px solid rgba(56, 189, 248, 0.22);
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
    cursor: grab;
  }
  canvas:active {
    cursor: grabbing;
  }
  #top-bar {
    position: absolute;
    top: 14px;
    left: 18px;
    right: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: none;
  }
  .hud-badge {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 20px;
    padding: 6px 14px;
    color: #94a3b8;
    font-size: 12px;
    font-weight: 500;
    backdrop-filter: blur(8px);
    letter-spacing: 0.4px;
  }
  .hud-btn {
    pointer-events: auto;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.4);
    border-radius: 20px;
    padding: 6px 14px;
    color: #38bdf8;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
  }
  .hud-btn:hover {
    background: rgba(56, 189, 248, 0.25);
    color: #ffffff;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
  }
  #center-guide {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    pointer-events: none;
  }
  #breath-instruction {
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-shadow: 0 0 20px rgba(56, 189, 248, 0.8), 0 2px 8px rgba(0,0,0,0.9);
    transition: all 0.5s ease;
  }
  #breath-sub {
    color: #38bdf8;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 1px;
    margin-top: 6px;
    opacity: 0.9;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
  }
  #bottom-bar {
    position: absolute;
    bottom: 14px;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    gap: 8px;
    pointer-events: none;
  }
  .mode-pill {
    pointer-events: auto;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 5px 12px;
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .mode-pill.active {
    background: rgba(56, 189, 248, 0.2);
    border-color: #38bdf8;
    color: #38bdf8;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
  }
</style>
</head>
<body>
<div id="container">
  <div id="top-bar">
    <div class="hud-badge">✨ Drag to ripple light • Tap to play calming chime</div>
    <button class="hud-btn" id="ambientToggle" onclick="toggleAmbientSound()">🔊 Ocean Hum: OFF</button>
  </div>
  
  <canvas id="c"></canvas>
  
  <div id="center-guide">
    <div id="breath-instruction">Inhale Gently</div>
    <div id="breath-sub">expand your belly • let thoughts flow away</div>
  </div>

  <div id="bottom-bar">
    <button class="mode-pill active" id="btnSigh" onclick="setBreathMode('sigh')">Physiological Sigh (Rapid Calming)</button>
    <button class="mode-pill" id="btnBox" onclick="setBreathMode('box')">4-4-4 Box Breathing</button>
    <button class="mode-pill" id="btnSleep" onclick="setBreathMode('sleep')">4-7-8 Deep Sleep Drift</button>
  </div>
</div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const mainTxt = document.getElementById('breath-instruction');
const subTxt = document.getElementById('breath-sub');
const ambBtn = document.getElementById('ambientToggle');

let width, height;
function resize() {
  width = canvas.width = canvas.parentElement.clientWidth;
  height = canvas.height = canvas.parentElement.clientHeight;
}
window.addEventListener('resize', resize);
resize();

// --- MULTI-OCTAVE HARMONIC AUDIO SYNTHESIZER ---
let audioCtx = null;
let ambientGain = null;
let isAmbientPlaying = false;

function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

// Gentle Crystal Chime upon touch
const scale = [
  {freq: 196.00, name: "G3"},
  {freq: 220.00, name: "A3"},
  {freq: 261.63, name: "C4"},
  {freq: 293.66, name: "D4"},
  {freq: 329.63, name: "E4"},
  {freq: 392.00, name: "G4"},
  {freq: 440.00, name: "A4"},
  {freq: 523.25, name: "C5"},
  {freq: 659.25, name: "E5"}
];

function playZenNote(freq, panPos = 0) {
  try {
    initAudio();
    const now = audioCtx.currentTime;
    
    // Fundamental tone
    const osc1 = audioCtx.createOscillator();
    const osc2 = audioCtx.createOscillator(); // Shimmer harmonic
    const gainNode = audioCtx.createGain();
    const panner = audioCtx.createStereoPanner ? audioCtx.createStereoPanner() : null;

    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(freq, now);

    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(freq * 2.01, now); // subtle crystalline overtone

    // Soft organic envelope
    gainNode.gain.setValueAtTime(0.0001, now);
    gainNode.gain.exponentialRampToValueAtTime(0.06, now + 0.08); // gentle soft attack
    gainNode.gain.exponentialRampToValueAtTime(0.0001, now + 2.4); // lingering warm decay

    osc1.connect(gainNode);
    osc2.connect(gainNode);

    if (panner) {
      panner.pan.setValueAtTime(Math.max(-0.8, Math.min(0.8, panPos)), now);
      gainNode.connect(panner);
      panner.connect(audioCtx.destination);
    } else {
      gainNode.connect(audioCtx.destination);
    }

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 2.5);
    osc2.stop(now + 2.5);
  } catch(e) {}
}

// Low-Frequency Binaural Brown Noise Generator (Warm Ocean Hum)
function toggleAmbientSound() {
  initAudio();
  if (isAmbientPlaying) {
    if (ambientGain) {
      ambientGain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + 1.2);
    }
    isAmbientPlaying = false;
    ambBtn.innerText = "🔊 Ocean Hum: OFF";
    ambBtn.style.color = "#38bdf8";
  } else {
    // Generate soothing low-frequency pink/brown noise
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      output[i] = (lastOut + (0.02 * white)) / 1.02; // Brown noise algorithm
      lastOut = output[i];
      output[i] *= 3.5;
    }

    const whiteNoise = audioCtx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    // Filter to warm deep frequencies only (< 320 Hz)
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(280, audioCtx.currentTime);

    ambientGain = audioCtx.createGain();
    ambientGain.gain.setValueAtTime(0.0001, audioCtx.currentTime);
    ambientGain.gain.exponentialRampToValueAtTime(0.045, audioCtx.currentTime + 2.0);

    whiteNoise.connect(filter);
    filter.connect(ambientGain);
    ambientGain.connect(audioCtx.destination);

    whiteNoise.start();
    isAmbientPlaying = true;
    ambBtn.innerText = "🌊 Ocean Hum: ON";
    ambBtn.style.color = "#34d399";
  }
}

// --- PARTICLE DYNAMICS & LIQUID TRAIL SYSTEM ---
class LiquidStarlight {
  constructor(x, y, vx, vy, color, size, life) {
    this.x = x;
    this.y = y;
    this.vx = vx;
    this.vy = vy;
    this.color = color;
    this.size = size;
    this.alpha = 1;
    this.life = life;
    this.maxLife = life;
  }
  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.vx *= 0.95;
    this.vy *= 0.95;
    this.life--;
    this.alpha = Math.max(0, this.life / this.maxLife);
  }
  draw(ctx) {
    ctx.save();
    ctx.globalAlpha = this.alpha;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.shadowColor = this.color;
    ctx.shadowBlur = 18;
    ctx.fill();
    ctx.restore();
  }
}

class RippleWave {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    this.radius = 8;
    this.maxRadius = 140;
    this.color = color;
    this.alpha = 0.8;
  }
  update() {
    this.radius += 2.8;
    this.alpha = Math.max(0, 1 - (this.radius / this.maxRadius));
  }
  draw(ctx) {
    ctx.save();
    ctx.globalAlpha = this.alpha * 0.45;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.strokeStyle = this.color;
    ctx.lineWidth = 2.5;
    ctx.shadowColor = this.color;
    ctx.shadowBlur = 15;
    ctx.stroke();
    ctx.restore();
  }
}

let particles = [];
let ripples = [];
const colorPalette = ['#38bdf8', '#818cf8', '#34d399', '#f472b6', '#fbbf24', '#a78bfa'];

function spawnSensation(x, y, count=14) {
  const pan = (x / width) * 2 - 1;
  const pickedNote = scale[Math.floor(Math.random() * scale.length)];
  playZenNote(pickedNote.freq, pan);

  const pickedColor = colorPalette[Math.floor(Math.random() * colorPalette.length)];
  ripples.push(new RippleWave(x, y, pickedColor));

  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 4.5 + 1.2;
    const vx = Math.cos(angle) * speed;
    const vy = Math.sin(angle) * speed;
    const size = Math.random() * 4.2 + 1.8;
    particles.push(new LiquidStarlight(x, y, vx, vy, pickedColor, size, Math.floor(Math.random() * 45 + 35)));
  }
}

let isDragging = false;
canvas.addEventListener('pointerdown', (e) => {
  isDragging = true;
  spawnSensation(e.offsetX, e.offsetY, 22);
});
window.addEventListener('pointerup', () => isDragging = false);
canvas.addEventListener('pointermove', (e) => {
  if (isDragging || Math.random() < 0.28) {
    spawnSensation(e.offsetX, e.offsetY, isDragging ? 7 : 2);
  }
});

// --- BREATHING REGULATION ALGORITHMS ---
let breathMode = 'sigh';
function setBreathMode(mode) {
  breathMode = mode;
  document.querySelectorAll('.mode-pill').forEach(el => el.classList.remove('active'));
  if (mode === 'sigh') document.getElementById('btnSigh').classList.add('active');
  if (mode === 'box') document.getElementById('btnBox').classList.add('active');
  if (mode === 'sleep') document.getElementById('btnSleep').classList.add('active');
}

let timer = 0;
function animate() {
  timer += 0.02;

  // Fluid background trail
  ctx.fillStyle = 'rgba(2, 6, 23, 0.18)';
  ctx.fillRect(0, 0, width, height);

  // Determine Breath Phase based on Mode
  let orbProgress = 0; // 0 to 1
  let glowColor = '#38bdf8';

  if (breathMode === 'sigh') {
    // Physiological Sigh Cycle: 8.5s total
    // 0 - 3.5s: First deep inhale
    // 3.5 - 4.5s: Sharp top-up sip
    // 4.5 - 8.5s: Long sigh exhale
    const cycle = (timer % 8.5);
    if (cycle < 3.2) {
      orbProgress = cycle / 3.2;
      mainTxt.innerText = "Inhale Deeply (Nose)";
      subTxt.innerText = "Filling lower lungs... expanding ribs";
      glowColor = '#38bdf8';
    } else if (cycle < 4.4) {
      orbProgress = 1.0 + (cycle - 3.2) * 0.15;
      mainTxt.innerText = "Take Second Sip of Air!";
      subTxt.innerText = "Pop open collapsed alveoli at the top";
      glowColor = '#fbbf24';
    } else {
      const exProgress = (cycle - 4.4) / 4.1;
      orbProgress = 1.15 - exProgress * 1.15;
      mainTxt.innerText = "Release Slowly (Mouth Sigh)";
      subTxt.innerText = "Feel shoulders drop... vascular pressure easing";
      glowColor = '#34d399';
    }
  } else if (breathMode === 'box') {
    // 4-4-4-4 Box Breathing (16s total)
    const cycle = (timer % 16.0);
    if (cycle < 4.0) {
      orbProgress = cycle / 4.0;
      mainTxt.innerText = "Inhale (4s)";
      subTxt.innerText = "Smooth, calm steady stream";
      glowColor = '#38bdf8';
    } else if (cycle < 8.0) {
      orbProgress = 1.0;
      mainTxt.innerText = "Hold Gently (4s)";
      subTxt.innerText = "Resting in peaceful stillness";
      glowColor = '#818cf8';
    } else if (cycle < 12.0) {
      orbProgress = 1.0 - (cycle - 8.0) / 4.0;
      mainTxt.innerText = "Exhale Smoothly (4s)";
      subTxt.innerText = "Releasing all muscular tension";
      glowColor = '#34d399';
    } else {
      orbProgress = 0.0;
      mainTxt.innerText = "Hold Empty (4s)";
      subTxt.innerText = "Quiet baseline stillness";
      glowColor = '#64748b';
    }
  } else if (breathMode === 'sleep') {
    // 4-7-8 Sleep Drift (19s total)
    const cycle = (timer % 19.0);
    if (cycle < 4.0) {
      orbProgress = cycle / 4.0;
      mainTxt.innerText = "Inhale Gently (4s)";
      subTxt.innerText = "Soothing calm drawing inward";
      glowColor = '#a78bfa';
    } else if (cycle < 11.0) {
      orbProgress = 1.0;
      mainTxt.innerText = "Hold & Retain (7s)";
      subTxt.innerText = "Saturating oxygen through body";
      glowColor = '#f472b6';
    } else {
      orbProgress = 1.0 - (cycle - 11.0) / 8.0;
      mainTxt.innerText = "Slow Whoosh Exhale (8s)";
      subTxt.innerText = "Drifting into heavy relaxation";
      glowColor = '#34d399';
    }
  }

  // Draw Pulsating Central Living Orb
  const cx = width / 2;
  const cy = height / 2;
  const baseRadius = 55 + orbProgress * 35;

  // Outer ambient chromatic aura
  const auraGrad = ctx.createRadialGradient(cx, cy, 10, cx, cy, baseRadius * 2.4);
  auraGrad.addColorStop(0, glowColor + '66');
  auraGrad.addColorStop(0.5, glowColor + '22');
  auraGrad.addColorStop(1, 'rgba(2, 6, 23, 0)');

  ctx.save();
  ctx.fillStyle = auraGrad;
  ctx.beginPath();
  ctx.arc(cx, cy, baseRadius * 2.4, 0, Math.PI * 2);
  ctx.fill();

  // Core Solid Inner Orb
  const innerGrad = ctx.createRadialGradient(cx, cy, 2, cx, cy, baseRadius);
  innerGrad.addColorStop(0, '#ffffff');
  innerGrad.addColorStop(0.4, glowColor);
  innerGrad.addColorStop(1, glowColor + '88');

  ctx.fillStyle = innerGrad;
  ctx.shadowColor = glowColor;
  ctx.shadowBlur = 35;
  ctx.beginPath();
  ctx.arc(cx, cy, baseRadius, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // Render expanding liquid ripples
  for (let i = ripples.length - 1; i >= 0; i--) {
    ripples[i].update();
    ripples[i].draw(ctx);
    if (ripples[i].alpha <= 0.01) {
      ripples.splice(i, 1);
    }
  }

  // Render & update starlight particles
  for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].update();
    particles[i].draw(ctx);
    if (particles[i].life <= 0) {
      particles.splice(i, 1);
    }
  }

  requestAnimationFrame(animate);
}
animate();
</script>
</body>
</html>
"""

# Enhanced Empathetic Grounding Engine with Specific Vascular & Dissociation Protocols
COMPANION_RESPONSES = {
    "blank": [
        "Your mind going completely blank is your nervous system's circuit-breaker. When sensory input becomes too intense, the brain shuts the blinds to protect you. You are not broken. Do not strain to think right now.\n\nLook around you right now without naming anything complex. Find 3 things in your room that are blue or green. Type them to me when you see them.",
        "That empty void is not forever—it is just emotional numbness shielding your brain from exhaustion. Press your heels down into the floor as hard as you comfortably can. Feel the firm ground pushing back up against you. Tell me: what are your feet resting on right now?"
    ],
    "bursting": [
        "That terrifying sensation of your veins bursting or blood pounding violently in your neck and temples is **acute sympathetic vasoconstriction** (adrenaline surge). Your blood vessels are incredibly flexible and built like durable elastic bands—they cannot burst from this. Your heart is strong and doing its best to shield you.\n\nRight now, drop your shoulders down away from your ears. Unclench your jaw. Take a slow breath through your nose, take a tiny second sip of air at the top, and let out a long sigh through your mouth.",
        "Your blood pressure feeling like it is spiking is pure adrenaline misfiring a false alarm. Try the **Mammalian Dive Reflex**: reach for a cold glass of water, run cold tap water over your wrists, or touch a cool wall with both palms. The rapid temperature drop triggers your vagus nerve to physically slow your pulse down."
    ],
    "chest": [
        "When your chest feels tight or like a heavy stone is pressing on it, the intercostal muscles between your ribs are clenching tightly due to shallow breathing. Place one hand flat over your stomach and one hand on your chest. Focus only on making the bottom hand move when you breathe in.",
        "You are taking in plenty of air even if your chest feels constricted. Let your hands open flat on your thighs with palms facing up. Letting your fingers relax signals to your brain that you are not in physical danger."
    ],
    "ground": [
        "Let us do a gentle **5-4-3-2-1 anchor** together right now:\n- **5 things** you can see (colors, shadows, shapes)\n- **4 physical things** you can touch (your shirt, desk, cool phone screen)\n- **3 sounds** you can hear (fan hum, distant cars, your breath)\n- **2 things** you can smell or feel in the air\n- **1 deep, slow sigh**.\n\nWhat is the first physical object you can touch right beside you?",
        "Touch something solid and cold near you right now—a metal key, the edge of a table, or a glass. Focus 100% of your attention on the exact temperature and texture of that surface. How does it feel under your fingertips?"
    ],
    "default": [
        "I am right here with you. There are no tests, no expectations, and you don't need to perform or pretend to be okay. Take all the time you need.",
        "What you are feeling right now is an adrenaline wave. All waves rise, reach their peak, and then break and recede. You are completely safe in this moment.",
        "Take a slow breath. Watch the glowing center orb on the left expand and release. Let your mind take a break while your body settles back down."
    ]
}

def get_companion_reply(user_text):
    t = user_text.lower()
    if any(k in t for k in ["blank", "void", "numb", "empty", "nothing", "spaced"]):
        return random.choice(COMPANION_RESPONSES["blank"])
    elif any(k in t for k in ["burst", "vein", "blood", "pressure", "vessel", "throbbing"]):
        return random.choice(COMPANION_RESPONSES["bursting"])
    elif any(k in t for k in ["chest", "heart", "tight", "suffocat", "breath"]):
        return random.choice(COMPANION_RESPONSES["chest"])
    elif any(k in t for k in ["ground", "help", "scared", "fear", "lost", "panic"]):
        return random.choice(COMPANION_RESPONSES["ground"])
    else:
        return random.choice(COMPANION_RESPONSES["default"])

# Header Bar
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("## 🌌 Haven")
    st.caption("A sanctuary for severe anxiety, sensory overload, and physical grounding.")
with col_head2:
    if st.button("🔄 Reset / Clear Space", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Layout Columns
col_visual, col_chat = st.columns([1.15, 1], gap="large")

with col_visual:
    st.markdown("### 🪐 Somatic Anchor & Breath Pacer")
    st.caption("Touch or drag to ripple liquid starlight & crystal chimes. Follow the breathing cycles below.")
    components.html(interactive_canvas_html, height=500)
    
    st.markdown("#### Instant Nervous System Resets")
    g_col1, g_col2, g_col3 = st.columns(3)
    if g_col1.button("🌊 Vascular De-escalation", use_container_width=True):
        st.info("💡 **Physiological Sigh Protocol**: Inhale deeply through your nose. At the very top, inhale a second sharp sip of air to pop open collapsed alveoli. Exhale slowly through your mouth like a long sigh. Repeat 3 times to immediately trigger the parasympathetic brake.")
    if g_col2.button("🧊 Dive Reflex (Pulse Drop)", use_container_width=True):
        st.info("💡 **Mammalian Temperature Reset**: Splash cold water on your eyelids and temples, or hold an ice cube in your palm. This triggers immediate carotid baroreceptors to slow down an elevated pulse.")
    if g_col3.button("🛋️ Gravity Anchor", use_container_width=True):
        st.info("💡 **Proprioceptive Grounding**: Press your heels into the floor. Feel the back of your legs and spine supported by your chair. Remind your body: *Gravity is holding me securely right now. I do not have to hold everything up.*")

with col_chat:
    st.markdown("### 🕊️ Compassionate Companion")
    st.caption("Speak freely. No judgment, no lectures, no pressure.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey. If your mind is spinning, or if everything feels completely blank and like a heavy void, you are safe here. What is your body feeling right now?"}
        ]

    chat_container = st.container(height=420)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if user_input := st.chat_input("Tell me what you feel, or type anything..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)

            reply = get_companion_reply(user_input)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_reply = ""
                for char in reply:
                    full_reply += char
                    message_placeholder.markdown(full_reply + "▌")
                    time.sleep(0.008)
                message_placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
