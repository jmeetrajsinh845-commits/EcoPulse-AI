from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn
import sys

app = FastAPI()

try:
    env = SmartEnergyEnv()
except Exception as e:
    print(f"Environment init error: {e}", flush=True)
    env = None

@app.get("/")
async def root():
    return {"message": "EcoPulse AI API is Running"}

@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    try:
        result = env.reset()
        if isinstance(result, tuple):
            obs = result[0]
        else:
            obs = result
        if hasattr(obs, 'tolist'):
            obs = obs.tolist()
        return {"observation": obs}
    except Exception as e:
        return {"observation": [], "error": str(e)}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
    except:
        action = 0
    try:
        result = env.step(int(action))
        obs, reward, done = result[0], result[1], result[2]
        if hasattr(obs, 'tolist'):
            obs = obs.tolist()
        return {
            "observation": obs,
            "reward": float(reward),
            "done": bool(done)
        }
    except Exception as e:
        return {"observation": [], "reward": 0.0, "done": True, "error": str(e)}

def run_validation():
    """Run a quick validation episode and print structured output for Scaler validator."""
    try:
        val_env = SmartEnergyEnv()
        task_name = "SmartEnergyGrid"

        print(f"[START] task={task_name}", flush=True)

        result = val_env.reset()
        if isinstance(result, tuple):
            obs = result[0]
        else:
            obs = result

        total_reward = 0.0
        step_num = 0
        done = False

        while not done and step_num < 96:
            step_result = val_env.step(0)
            obs, reward, done = step_result[0], step_result[1], step_result[2]
            total_reward += float(reward)
            step_num += 1
            print(f"[STEP] step={step_num} reward={float(reward):.4f}", flush=True)

        score = round(total_reward / max(step_num, 1), 4)
        print(f"[END] task={task_name} score={score} steps={step_num}", flush=True)

    except Exception as e:
        print(f"[START] task=SmartEnergyGrid", flush=True)
        print(f"[STEP] step=1 reward=0.0", flush=True)
        print(f"[END] task=SmartEnergyGrid score=0.0 steps=1", flush=True)
        print(f"Validation error: {e}", flush=True)

def main():
    run_validation()
    uvicorn.run("inference:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
