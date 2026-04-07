from fastapi import FastAPI, Request
from env import SmartEnergyEnv
import uvicorn

app = FastAPI()

try:
    env = SmartEnergyEnv()
except Exception as e:
    print(f"Environment init error: {e}")
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

import socket
import uvicorn

def main():
    # પોર્ટ 7860 ખાલી છે કે નહીં તે નેટવર્ક ચેક કરીએ (Risky operation wrapped)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('0.0.0.0', 7860))
    sock.close()
    
    if result == 0:
        # જો પોર્ટ 7860 પર સર્વર પહેલેથી જ ચાલુ હોય તો ક્રેશ થવાથી બચાવો
        print("Port 7860 is already in use. Server is likely already running.")
    else:
        # જો સર્વર ચાલુ ન હોય, તો જ નવું સર્વર સ્ટાર્ટ કરો
        try:
            uvicorn.run("inference:app", host="0.0.0.0", port=7860)
        except SystemExit:
            print("Uvicorn exited gracefully.")
        except Exception as e:
            print(f"Unhandled error: {e}")

if __name__ == "__main__":
    main()
