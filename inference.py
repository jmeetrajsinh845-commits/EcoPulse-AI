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
    obs = env.reset()
    # જજની સિસ્ટમ માટે observation કી (key) માં ડેટા મોકલવો જરૂરી છે
    return {"observation": obs}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
    except:
        action = 0
    
    obs, reward, done = env.step(int(action))
    return {
        "observation": obs, 
        "reward": float(reward), 
        "done": bool(done)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
