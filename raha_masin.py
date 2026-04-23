```python
import asyncio
import os
import aiohttp
from datetime import datetime

# CONFIG
TOKEN = os.getenv("TELEGRAM_TOKEN", "8740053883:AAHBfNjeYIRn4YNWHxWR8_n8ztc7K86uBzc")
CHAT_ID = "8740053883"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGETS_FILE = os.path.join(PROJECT_DIR, "targets.txt")

async def send_tele(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with aiohttp.ClientSession() as session:
        await session.post(url, json={"chat_id": CHAT_ID, "text": f"💎 [V4-ARCHITECT] \n{msg}"})

async def run_cmd(cmd, target):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    res = stdout.decode().strip()
    if any(x in res.lower() for x in ["high", "critical", "vulnerable"]):
        await send_tele(f"LEID: {target}\n{res[:400]}")
    return res

async def main():
    await send_tele("Skanner käivitatud.")
    while True:
        if os.path.exists(TARGETS_FILE):
            with open(TARGETS_FILE, 'r') as f:
                targets = [l.strip() for l in f if l.strip()]
            for t in targets:
                # Recon & Vulnerability scan
                out = os.path.join(PROJECT_DIR, "results", datetime.now().strftime("%Y-%m-%d"), t)
                os.makedirs(out, exist_ok=True)
                
                # Piping: Subfinder -> Httpx -> Nuclei
                cmd = f"subfinder -d {t} -silent | httpx -silent | nuclei -severity high,critical -silent > {out}/nuclei.txt"
                await run_cmd(cmd, t)
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

```
