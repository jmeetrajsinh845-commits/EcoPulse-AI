from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn
import os
import socket

# ૧. આ લાઈન હોવી ખૂબ જરૂરી છે
app = FastAPI()

try:
    env = SmartEnergyEnv()
except Exception as e:
    print(f"Environment init error: {e}")
    env = None

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    try:
        result = env.reset()
        obs = result[0] if isinstance(result, tuple) else result
        if hasattr(obs, 'tolist'): obs = obs.tolist()
        
        # હેકાથોન માટે જરૂરી પ્રિન્ટ સ્ટેટમેન્ટ
        print(f"[START] task=SmartEnergy, observation={obs}", flush=True)
        
        return {"observation": obs}
    except Exception as e:
        return {"observation": [], "error": str(e)}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
        result = env.step(int(action))
        obs, reward, done = result[0], result[1], result[2]
        
        if hasattr(obs, 'tolist'): obs = obs.tolist()
        
        # હેકાથોન માટે જરૂરી પ્રિન્ટ સ્ટેટમેન્ટ
        print(f"[STEP] action={action} reward={reward} done={done}", flush=True)
        
        if done:
            print(f"[END] task=SmartEnergy score={reward}", flush=True)
            
        return {"observation": obs, "reward": float(reward), "done": bool(done)}
    except Exception as e:
        return {"observation": [], "reward": 0.0, "done": True, "error": str(e)}

def main():
    # પોર્ટ ચેક - એરર ફ્રી રન માટે
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('0.0.0.0', 7860))
    sock.close()
    
    if result == 0:
        print("Port 7860 already in use. Skipping uvicorn.run")
    else:
        uvicorn.run("inference:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
