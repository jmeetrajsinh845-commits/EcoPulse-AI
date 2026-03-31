from fastapi import FastAPI, Request
from env import SmartEnergyEnv

app = FastAPI()
env = SmartEnergyEnv()

@app.get("/")
async def root():
    return {"message": "EcoPulse AI is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset(request: Request = None):
    obs = env.reset()
    return {"observation": obs}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
    except:
        action = 0
    obs, reward, done = env.step(int(action))
    return {"observation": obs, "reward": float(reward), "done": bool(done)}
