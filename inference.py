import os
from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn

app = FastAPI()
env = SmartEnergyEnv()

# આ બે લાઈન હોવી જ જોઈએ (ચેકલિસ્ટ મુજબ)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    print("START: Environment Resetting") # લોગિંગ જરૂરી છે
    result = env.reset()
    obs = result[0] if isinstance(result, tuple) else result
    if hasattr(obs, 'tolist'): obs = obs.tolist()
    return {"observation": obs}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
    except:
        action = 0
    
    print(f"STEP: Action taken: {action}") # લોગિંગ જરૂરી છે
    result = env.step(int(action))
    obs, reward, done = result[0], result[1], result[2]
    
    if hasattr(obs, 'tolist'): obs = obs.tolist()
    if done: print("END: Episode Finished") # લોગિંગ જરૂરી છે

    return {"observation": obs, "reward": float(reward), "done": bool(done)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
    
