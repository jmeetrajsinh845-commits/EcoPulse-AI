@app.api_route("/reset", methods=["GET", "POST"])
async def reset():
    try:
        result = env.reset()
        obs = result[0] if isinstance(result, tuple) else result
        if hasattr(obs, 'tolist'): obs = obs.tolist()
        
        # --- આ લાઈન ઉમેરી (ફરજિયાત છે) ---
        print(f"[START] task=SmartEnergy, observation={obs}", flush=True)
        
        return {"observation": obs}
    except Exception as e:
        return {"observation": [], "error": str(e)}

@app.post("/step")
async def step(request: Request):
    try:
        data = await request.json()
        action = data.get("action", 0)
        result = env.step(int(action))
        obs, reward, done = result[0], result[1], result[2]
        
        if hasattr(obs, 'tolist'): obs = obs.tolist()
        
        # --- આ લાઈન ઉમેરી (ફરજિયાત છે) ---
        print(f"[STEP] action={action} reward={reward} done={done}", flush=True)
        
        if done:
            print(f"[END] task=SmartEnergy score={reward}", flush=True)
            
        return {"observation": obs, "reward": float(reward), "done": bool(done)}
    except Exception as e:
        return {"observation": [], "reward": 0.0, "done": True, "error": str(e)}
