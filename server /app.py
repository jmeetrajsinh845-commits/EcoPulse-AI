import os
import uvicorn
from fastapi import FastAPI, Request
from env import SmartEnergyEnv

app = FastAPI()
env = SmartEnergyEnv()

@app.post("/reset")
async def reset(request: Request):
    obs = env.reset()
    if isinstance(obs, tuple): obs = obs[0]
    return {"observation": obs.tolist() if hasattr(obs, 'tolist') else obs}

@app.post("/step")
async def step(request: Request):
    data = await request.json()
    action = data.get("action", 0)
    obs, reward, done, _ = env.step(int(action))
    return {
        "observation": obs.tolist() if hasattr(obs, 'tolist') else obs,
        "reward": float(reward),
        "done": bool(done)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
