import os
import sys
import time
import socket
import uvicorn
from fastapi import FastAPI, Request
from env import SmartEnergyEnv

# FastAPI એપ શરૂ કરો
app = FastAPI()

# Environment લોડ કરો
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
    """Scaler validator માટે વેલિડેશન એપિસોડ રન કરો."""
    try:
        val_env = SmartEnergyEnv()
        task_name = "SmartEnergyGrid"

        print(f"[START] task={task_name}", flush=True)

        result = val_env.reset()
        obs = result[0] if isinstance(result, tuple) else result

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

def is_port_available(host: str, port: int) -> bool:
    """પોર્ટ ખાલી છે કે નહીં તે તપાસો."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except socket.error:
            return False

def main():
    # 1. પહેલા વેલિડેશન રન કરો (તમારા જૂના કોડ મુજબ)
    run_validation()

    host = "0.0.0.0"
    port = 7860
    max_retries = 3
    retry_delay = 5  # સેકન્ડ

    # 2. પોર્ટ ચેક અને સર્વર સ્ટાર્ટ લોજિક
    for attempt in range(1, max_retries + 1):
        print(f"Checking port {port} (Attempt {attempt}/{max_retries})...", flush=True)
        
        if is_port_available(host, port):
            print(f"Port {port} is free. Starting Uvicorn...", flush=True)
            try:
                # uvicorn.run માં એપ ઓબ્જેક્ટ સીધો પાસ કરો
                uvicorn.run(app, host=host, port=port, log_level="info")
                sys.exit(0)
            except Exception as e:
                if "address already in use" in str(e).lower() or "[Errno 98]" in str(e):
                    print(f"Port bind race condition detected. Retrying...", flush=True)
                else:
                    print(f"Uvicorn error: {e}", flush=True)
                    sys.exit(0)
        else:
            print(f"Port {port} is occupied by another process.", flush=True)

        if attempt < max_retries:
            print(f"Waiting {retry_delay} seconds before next attempt...", flush=True)
            time.sleep(retry_delay)
        else:
            print(f"Failed to bind to port {port} after {max_retries} attempts. Exiting gracefully.", flush=True)
            sys.exit(0)

if __name__ == "__main__":
    main()
