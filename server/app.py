from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn

app = FastAPI()
env = SmartEnergyEnv()

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    result = env.reset()
    if isinstance(result, tuple):
        obs = result[0]
    else:
        obs = result
    if hasattr(obs, 'tolist'):
        obs = obs.tolist()
    return {"observation": obs}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
    except:
        action = 0
    result = env.step(int(action))
    obs, reward, done = result[0], result[1], result[2]
    if hasattr(obs, 'tolist'):
        obs = obs.tolist()
    return {
        "observation": obs,
        "reward": float(reward),
        "done": bool(done)
    }

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
    
