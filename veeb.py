```python
import asyncio
from flask import Flask, render_template_string, jsonify, request, abort
import psutil
import os
import subprocess

app = Flask(__name__)

# --- KONFIGURATSIOON ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGETS_FILE = os.path.join(PROJECT_DIR, "targets.txt")
ACCESS_PASSWORD = "1122334455"

# --- UI DISAIN ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="et">
<head>
    <meta charset="UTF-8">
    <title>Bounty Architect V4</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white p-8">
    <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold text-blue-400 font-mono italic">V4 ARCHITECT</h1>
            <div class="flex gap-2">
                <span class="bg-blue-900 text-blue-300 px-3 py-1 rounded text-xs">DOCKER ACTIVE</span>
                <span class="bg-green-900 text-green-300 px-3 py-1 rounded text-xs animate-pulse">SCANNER RUNNING</span>
            </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-2xl">
                <h2 class="text-xs font-bold uppercase text-slate-500 mb-2">CPU</h2>
                <p id="cpu" class="text-4xl font-mono font-black text-white">0%</p>
            </div>
            <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-2xl">
                <h2 class="text-xs font-bold uppercase text-slate-500 mb-2">RAM</h2>
                <p id="ram" class="text-4xl font-mono font-black text-white">0%</p>
            </div>
        </div>

        <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-2xl">
            <h2 class="text-xl font-bold mb-4">TARGETS.TXT</h2>
            <textarea id="targets" class="w-full h-64 bg-slate-950 text-green-400 p-4 font-mono rounded-lg border border-slate-700 focus:border-blue-500 outline-none" placeholder="domeen.ee"></textarea>
            <button onclick="saveTargets()" class="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition active:scale-95">SALVESTA</button>
            <span id="status-msg" class="ml-4 font-bold"></span>
        </div>
    </div>

    <script>
        const pass = "1122334455";
        async function updateStats() {
            try {
                const res = await fetch(`/stats?pw=${pass}`);
                const data = await res.json();
                document.getElementById('cpu').innerText = data.cpu + '%';
                document.getElementById('ram').innerText = data.ram + '%';
            } catch (e) {}
        }
        async function loadTargets() {
            const res = await fetch(`/get_targets?pw=${pass}`);
            const text = await res.text();
            document.getElementById('targets').value = text;
        }
        async function saveTargets() {
            const text = document.getElementById('targets').value;
            const res = await fetch(`/save_targets?pw=${pass}`, {
                method: 'POST',
                body: JSON.stringify({targets: text}),
                headers: {'Content-Type': 'application/json'}
            });
            if(res.ok) {
                document.getElementById('status-msg').innerText = "SALVESTATUD!";
                setTimeout(() => document.getElementById('status-msg').innerText = "", 3000);
            }
        }
        setInterval(updateStats, 2000);
        loadTargets();
    </script>
</body>
</html>
"""

def check_auth():
    if request.args.get('pw') != ACCESS_PASSWORD: abort(403)

@app.route('/')
def home():
    if request.args.get('pw') == ACCESS_PASSWORD: return render_template_string(HTML_TEMPLATE)
    return "Forbidden", 403

@app.route('/stats')
def stats():
    check_auth()
    return jsonify({"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent})

@app.route('/get_targets')
def get_targets():
    check_auth()
    if not os.path.exists(TARGETS_FILE): return ""
    with open(TARGETS_FILE, 'r') as f: return f.read()

@app.route('/save_targets', methods=['POST'])
def save_targets():
    check_auth()
    data = request.json
    with open(TARGETS_FILE, 'w') as f: f.write(data['targets'])
    return "OK"

if __name__ == '__main__':
    # Käivitame skanneri taustal
    subprocess.Popen(["python3", os.path.join(PROJECT_DIR, "raha_masin.py")])
    app.run(host='0.0.0.0', port=5000)

```
