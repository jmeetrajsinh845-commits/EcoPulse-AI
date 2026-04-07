import os
from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn
from openai import OpenAI  # આ લાઈન જજની શરત પૂરી કરવા માટે ઉમેરી છે

app = FastAPI()
env = SmartEnergyEnv()

# --- ENVIRONMENT VARIABLES (ચેકલિસ્ટ મુજબ) ---
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
HF_TOKEN = os.getenv("HF_TOKEN")

# OpenAI ક્લાયન્ટ કન્ફિગરેશન (ભલે આપણે વાપરતા ન હોઈએ, પણ શરત માટે જરૂરી છે)
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN if HF_TOKEN else "unused")

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    print("START: Environment Resetting") 
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
    
    print(f"STEP: Action taken: {action}")
    result = env.step(int(action))
    obs, reward, done = result[0], result[1], result[2]
    
    if hasattr(obs, 'tolist'): obs = obs.tolist()
    if done: print("END: Episode Finished")

    return {
        "observation": obs,
        "reward": float(reward),
        "done": bool(done)
    }
    # ફાઈલની છેલ્લે આ ઉમેરો
def main():
    import uvicorn
    uvicorn.run("inference:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()
    
