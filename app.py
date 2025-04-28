<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AI Book Summarizer</title>
  <style>
    /* full-screen Matrix canvas behind everything */
    body, html {
      margin: 0; padding: 0;
      overflow: hidden;
      height: 100%; width: 100%;
      background: black;
      font-family: 'JetBrains Mono', monospace;
      color: #eee;
    }
    #matrix {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      z-index: 1;
    }
    /* UI container sits above the canvas */
    .ui-container {
      position: relative;
      z-index: 2;
      height: 100%;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      text-align: center;
      pointer-events: none; /* allow clicks to pass to children only */
    }
    h1, p, .upload, button {
      pointer-events: auto; /* re-enable interaction */
    }
    h1 {
      font-size: 2rem; margin: 0 0 0.5rem;
    }
    p {
      color: #aaa; margin: 0 0 2rem;
    }
    .upload {
      border: 2px dashed #666;
      padding: 2rem; width: 20rem;
      border-radius: 0.5rem; cursor: pointer;
      transition: background 0.3s;
      background: rgba(0,0,0,0.2);
      margin-bottom: 1.5rem;
    }
    .upload:hover {
      background: rgba(255,255,255,0.05);
    }
    button {
      padding: 0.75rem 1.5rem;
      background: none; border: 1px solid #eee;
      border-radius: 0.5rem; cursor: pointer;
      transition: background 0.3s, color 0.3s;
    }
    button:hover {
      background: #eee; color: #111;
    }
    #loader {
      display: none;
      margin-top: 1rem;
      border: 6px solid #444;
      border-top: 6px solid #eee;
      border-radius: 50%;
      width: 2.5rem; height: 2.5rem;
      animation: spin 1s linear infinite;
    }
    @keyframes spin {
      0%   { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    .modal {
      position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(30,30,30,0.95);
      padding: 1.5rem; border-radius: 0.5rem;
      max-width: 30rem; width: 90%;
      color: #eee; display: none;
      z-index: 3; text-align: left;
    }
    .modal.show { display: block; }
    .modal-header {
      display: flex; justify-content: space-between;
      align-items: center; margin-bottom: 1rem;
    }
    .close-btn {
      background: none; border: none;
      color: #eee; font-size: 1.25rem; cursor: pointer;
    }
    footer {
      position: fixed; bottom: 1rem; width: 100%;
      text-align: center; color: #555; font-size: 0.75rem;
      z-index: 2;
      pointer-events: none;
    }
  </style>
</head>
<body>

  <!-- 1) Matrix canvas -->
  <canvas id="matrix"></canvas>

  <!-- 2) UI layer -->
  <div class="ui-container">
    <h1>AI Book Summarizer</h1>
    <p>Summarize any book in minutes.</p>

    <label class="upload" id="file-label">
      <input type="file" id="file-input" style="display: none" accept=".pdf,.epub"/>
      Click to upload a book (PDF/EPUB)
    </label>

    <button onclick="summarize()">Summarize</button>
    <div id="loader"></div>
  </div>

  <!-- 3) Summary modal -->
  <div class="modal" id="summary-modal">
    <div class="modal-header">
      <h3>Summary</h3>
      <button class="close-btn" onclick="closeModal()">×</button>
    </div>
    <div id="summary-text"></div>
  </div>

  <footer>© 2025 | Built by You</footer>

  <script>
  // —— Matrix-style waterfall setup —— 
  const canvas = document.getElementById('matrix');
  const ctx    = canvas.getContext('2d');
  let W = canvas.width  = innerWidth;
  let H = canvas.height = innerHeight;

  const words = [
    'Knowledge','Power','Wisdom','Truth','Insight','Mastery','Strength','Clarity',
    'Intelligence','Perception','Awareness','Vision','Genius','Revelation',
    'Sovereignty','Understanding','Illumination','Authority','Strategy','Dominion',
    'Consciousness','Discovery','Discipline','Awakening','Willpower','Purpose',
    'Influence','Cognition','Innovation','Legacy','Enlightenment','Intuition',
    'Command','Ascendancy','Fortitude','Honor','Reality','Foresight','Memory',
    'Adaptation','Ingenuity','Reason','Potential','Sovereignty','Sagacity',
    'Aptitude','Precision','Curiosity','Alchemy','Logos','Ethos','Praxis','Nexus',
    'Synthesis','Momentum','Transcendence'
  ];
  const fontSize = 24;
  const columns  = Math.floor(W / fontSize);
  const drops    = Array(columns).fill(0).map(_ => Math.random() * H);

  function drawMatrix() {
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0,0,W,H);
    ctx.fillStyle = '#FFF';
    ctx.font = fontSize + 'px monospace';
    for (let i = 0; i < columns; i++) {
      const text = words[Math.floor(Math.random() * words.length)];
      const x = i * fontSize;
      const y = drops[i] * fontSize;
      ctx.fillText(text, x, y);
      if (y > H && Math.random() > 0.975) drops[i] = 0;
      drops[i]++;
    }
    requestAnimationFrame(drawMatrix);
  }
  drawMatrix();

  window.addEventListener('resize', () => {
    W = canvas.width  = innerWidth;
    H = canvas.height = innerHeight;
  });

  // —— File upload & summarizer UI —— 
  let selectedFile = null;
  const fileInput  = document.getElementById('file-input');
  const fileLabel  = document.getElementById('file-label');

  fileInput.addEventListener('change', e => {
    selectedFile = e.target.files[0];
    if (selectedFile) fileLabel.innerText = selectedFile.name;
  });

  function summarize() {
    if (!selectedFile) {
      alert('Please upload a file first.'); 
      return;
    }
    const loader = document.getElementById('loader');
    loader.style.display = 'block';

    const fdata = new FormData();
    fdata.append('file', selectedFile);

    fetch('https://book-summarizer-backend.onrender.com/upload', {
      method: 'POST', body: fdata
    })
    .then(res => res.json())
    .then(data => {
      loader.style.display = 'none';
      document.getElementById('summary-text').innerText =
        data.summary || data.excerpt || 'No summary available.';
      document.getElementById('summary-modal').classList.add('show');
    })
    .catch(err => {
      loader.style.display = 'none';
      console.error(err);
      alert('Error summarizing file.');
    });
  }

  function closeModal() {
    document.getElementById('summary-modal').classList.remove('show');
  }
  </script>
</body>
</html>
