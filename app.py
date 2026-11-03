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

# Custom Ambient CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 50% 20%, #111827 0%, #07090e 100%);
        color: #e2e8f0;
    }
    .stChatMessage {
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .stButton>button {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(129, 140, 248, 0.2) 100%);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 10px 18px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.3) 0%, rgba(129, 140, 248, 0.35) 100%);
        border-color: #38bdf8;
        color: #ffffff;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Interactive Fluid Starlight Canvas & Audio Generator (Embedded HTML5 Canvas)
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
  }
  #container {
    position: relative;
    width: 100%;
    height: 440px;
    border-radius: 20px;
    overflow: hidden;
    background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.15);
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
    cursor: crosshair;
  }
  #hud {
    position: absolute;
    top: 16px;
    left: 20px;
    pointer-events: none;
    color: #94a3b8;
    font-size: 13px;
    letter-spacing: 0.5px;
  }
  #breath-hint {
    position: absolute;
    bottom: 16px;
    width: 100%;
    text-align: center;
    color: #38bdf8;
    font-size: 14px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 500;
    pointer-events: none;
    opacity: 0.85;
  }
</style>
</head>
<body>
<div id="container">
  <div id="hud">✨ Touch or drag mouse to ripple light & release warmth</div>
  <canvas id="c"></canvas>
  <div id="breath-hint" id="breathTxt">Gently breathe with the pulse</div>
</div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const hint = document.getElementById('breath-hint');

let width, height;
function resize() {
  width = canvas.width = canvas.parentElement.clientWidth;
  height = canvas.height = canvas.parentElement.clientHeight;
}
window.addEventListener('resize', resize);
resize();

// Ambient Web Audio synth for soothing chime on touch
let audioCtx = null;
function playChime(freq) {
  try {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.6);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 1.6);
  } catch(e) {}
}

const pentatonic = [220, 261.63, 293.66, 329.63, 392.00, 440, 523.25];

class Particle {
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
    this.vx *= 0.96;
    this.vy *= 0.96;
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
    ctx.shadowBlur = 12;
    ctx.fill();
    ctx.restore();
  }
}

let particles = [];
const colors = ['#38bdf8', '#818cf8', '#34d399', '#f472b6', '#fbbf24'];

function spawnBurst(x, y, count=12) {
  const note = pentatonic[Math.floor(Math.random() * pentatonic.length)];
  playChime(note);
  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 3 + 1;
    const vx = Math.cos(angle) * speed;
    const vy = Math.sin(angle) * speed;
    const color = colors[Math.floor(Math.random() * colors.length)];
    const size = Math.random() * 3.5 + 1.5;
    particles.push(new Particle(x, y, vx, vy, color, size, Math.floor(Math.random() * 40 + 35)));
  }
}

let isPointerDown = false;
canvas.addEventListener('pointerdown', (e) => {
  isPointerDown = true;
  spawnBurst(e.offsetX, e.offsetY, 20);
});
canvas.addEventListener('pointerup', () => isPointerDown = false);
canvas.addEventListener('pointermove', (e) => {
  if (isPointerDown || Math.random() < 0.25) {
    spawnBurst(e.offsetX, e.offsetY, isPointerDown ? 6 : 2);
  }
});

let timeVal = 0;
function animate() {
  timeVal += 0.015;
  
  // Fading trail
  ctx.fillStyle = 'rgba(2, 6, 23, 0.15)';
  ctx.fillRect(0, 0, width, height);
  
  // Center gentle pulsating orb (Breathing anchor)
  const breathCycle = Math.sin(timeVal * 1.2);
  const orbRadius = 55 + breathCycle * 18;
  const gradient = ctx.createRadialGradient(width/2, height/2, 5, width/2, height/2, orbRadius * 1.5);
  
  if (breathCycle > 0.1) {
    hint.innerText = "Inhale slowly...";
    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.4)');
    gradient.addColorStop(1, 'rgba(2, 6, 23, 0)');
  } else if (breathCycle < -0.1) {
    hint.innerText = "Release... let shoulders drop";
    gradient.addColorStop(0, 'rgba(52, 211, 153, 0.35)');
    gradient.addColorStop(1, 'rgba(2, 6, 23, 0)');
  } else {
    hint.innerText = "Gently pause";
    gradient.addColorStop(0, 'rgba(129, 140, 248, 0.35)');
    gradient.addColorStop(1, 'rgba(2, 6, 23, 0)');
  }
  
  ctx.save();
  ctx.fillStyle = gradient;
  ctx.beginPath();
  ctx.arc(width/2, height/2, orbRadius * 1.8, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // Update particles
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

# Crisis Companion Knowledge / Grounding Responses
COMPANION_RESPONSES = {
    "blank": [
        "Your mind going completely blank is your nervous system's way of hitting the pause button when it is overwhelmed. You do not need to force thoughts right now. Just rest your hands on the table or your lap and feel your feet on the floor.",
        "When the void feels heavy, don't try to think your way out of it. Look around the room right now and name three things you can see that are blue or green. Tell me what they are.",
    ],
    "bursting": [
        "That intense pressure—feeling like your veins or chest might burst—is adrenaline rushing through your bloodstream. Your heart is strong and your blood vessels are built to handle this surge. It is uncomfortable, but it is not dangerous. Let your shoulders drop down one inch right now.",
        "Your body is in false alarm overdrive. Take one slow breath in through your nose, then a second tiny sip of air at the very top, and let it all out through your mouth like a long sigh. Let's do that together.",
    ],
    "ground": [
        "Let us do a simple sensory reset together. Name:
- 3 things you can see right now
- 2 physical textures you can feel with your fingertips
- 1 sound you can hear in the background.",
        "Touch something cool or solid nearby—a glass of water, the edge of your desk, or your keys. Focus entirely on how smooth or cold it feels against your skin.",
    ],
    "default": [
        "I am right here with you. There is no rush, no expectations, and you don't have to explain anything. Just take things one second at a time.",
        "You are safe in this physical space. What you are feeling is an adrenaline wave, and every wave has a peak and then subsides. You are going to be okay.",
        "You don't have to carry all the weight right now. Let yourself just breathe and exist for a few minutes. I am listening whenever you want to type.",
    ]
}

def get_companion_reply(user_text):
    t = user_text.lower()
    if any(k in t for k in ["blank", "void", "numb", "empty", "nothing"]):
        return random.choice(COMPANION_RESPONSES["blank"])
    elif any(k in t for k in ["burst", "vein", "heart", "pressure", "blood", "chest", "shaking", "panic"]):
        return random.choice(COMPANION_RESPONSES["bursting"])
    elif any(k in t for k in ["ground", "help", "scared", "fear", "lost"]):
        return random.choice(COMPANION_RESPONSES["ground"])
    else:
        return random.choice(COMPANION_RESPONSES["default"])

# Header
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("## 🌌 Haven")
    st.caption("A sensory sanctuary for severe anxiety, mental exhaustion, and sensory grounding.")
with col_head2:
    if st.button("🚨 Reset / Center Me", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Layout: Left column is the interactive sensory anchor, Right column is the comforting companion
col_visual, col_chat = st.columns([1.1, 1], gap="large")

with col_visual:
    st.markdown("### 🪐 Somatic Anchor")
    st.caption("Touch, drag, or ripple your cursor across the canvas. Gentle chimes harmonize with touch.")
    components.html(interactive_canvas_html, height=450)
    
    st.markdown("#### Quick Grounding Actions")
    g_col1, g_col2, g_col3 = st.columns(3)
    if g_col1.button("🌊 Blood Pressure Release"):
        st.info("💡 **Physiological Sigh**: Take a deep breath through your nose. At the very top, take one more sharp sip of air. Then blow it all out smoothly through your mouth. Repeat 3 times to immediately lower heart rate.")
    if g_col2.button("🧊 Ice / Temperature Reset"):
        st.info("💡 **Mammalian Dive Reflex**: Splash cold water on your temples and wrists, or hold an ice cube in your palm. It sends an immediate survival signal to force your heart rate down.")
    if g_col3.button("🛋️ Body Weight Grounding"):
        st.info("💡 **Gravity Check**: Press your heels hard into the floor. Feel the chair supporting your lower back. Your body is held and anchored by gravity right now.")

with col_chat:
    st.markdown("### 🕊️ Compassionate Companion")
    st.caption("Talk freely. No judgment, no advice lecturing, no pressure.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hey. If your thoughts are spinning, or if everything feels completely blank and heavy right now, you are safe here. What is your body feeling right now?"}
        ]

    chat_container = st.container(height=380)
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
                    time.sleep(0.01)
                message_placeholder.markdown(full_reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
