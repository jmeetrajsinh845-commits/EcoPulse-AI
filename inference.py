from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn

app = FastAPI()
env = SmartEnergyEnv()

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.post("/reset")
async def reset():
    obs = env.reset()
    # ખાતરી કરો કે બેટરી નંબર ફોર્મેટમાં જાય (દા.ત. 50% ના બદલે 50)
    if isinstance(obs.get('battery'), str):
        obs['battery'] = int(obs['battery'].replace('%', ''))
    return obs

@app.post("/step")
async def step(request: Request):
    data = await request.json()
    action = data.get("action")
    obs, reward, done = env.step(action)
    if isinstance(obs.get('battery'), str):
        obs['battery'] = int(obs['battery'].replace('%', ''))
    return {"observation": obs, "reward": reward, "done": done}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
