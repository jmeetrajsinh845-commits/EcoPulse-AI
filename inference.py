import sys
import os
import socket
import uvicorn
from fastapi import FastAPI, Request
from env import SmartEnergyEnv

app = FastAPI()

# Environment Initialization
try:
    env = SmartEnergyEnv()
except Exception as e:
    sys.stdout.write(f"Environment init error: {e}\n")
    sys.stdout.flush()
    env = None

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    try:
        result = env.reset()
        obs = result[0] if isinstance(result, tuple) else result
        if hasattr(obs, 'tolist'): 
            obs = obs.tolist()
        
        # --- PROFESSIONAL LOGGING (STDOUT) ---
        output = f"[START] task=SmartEnergy, observation={obs}\n"
        sys.stdout.write(output)
        sys.stdout.flush()
        
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
        
        if hasattr(obs, 'tolist'): 
            obs = obs.tolist()
        
        # --- PROFESSIONAL LOGGING (STDOUT) ---
        step_output = f"[STEP] action={action} reward={reward} done={done}\n"
        sys.stdout.write(step_output)
        
        if done:
            end_output = f"[END] task=SmartEnergy score={reward}\n"
            sys.stdout.write(end_output)
            
        sys.stdout.flush()
            
        return {"observation": obs, "reward": float(reward), "done": bool(done)}
    except Exception as e:
        return {"observation": [], "reward": 0.0, "done": True, "error": str(e)}

def main():
    # Port Check to avoid 'Address already in use' errors
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('0.0.0.0', 7860))
    sock.close()
    
    if result == 0:
        sys.stdout.write("Port 7860 already in use. Server is likely running.\n")
        sys.stdout.flush()
    else:
        uvicorn.run("inference:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
