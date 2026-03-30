from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn

app = FastAPI()
env = SmartEnergyEnv()

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

# Reset endpoint: GET અને POST બંનેને સપોર્ટ કરશે
@app.api_route("/reset", methods=["GET", "POST"])
async def reset(request: Request = None):
    obs = env.reset()
    if isinstance(obs.get('battery'), str):
        obs['battery'] = int(obs['battery'].replace('%', ''))
    return obs

# Step endpoint
@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
    except:
        data = {}
    
    action = data.get("action", 0) # જો action ન મળે તો default 0 લેશે
    obs, reward, done = env.step(action)
    
    if isinstance(obs.get('battery'), str):
        obs['battery'] = int(obs['battery'].replace('%', ''))
    return {"observation": obs, "reward": reward, "done": done}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
