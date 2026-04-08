import os
import sys
import time
import requests
from openai import OpenAI

# ૧. Meta Validator દ્વારા અપાતા એન્વાયરમેન્ટ વેરિએબલ્સ
API_KEY = os.environ.get("API_KEY")
API_BASE_URL = os.environ.get("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# તમારા Hugging Face Space નું URL - આ ખાસ ચેક કરજો
ENV_URL = "https://sakshiba008-ecopulse-ai-final.hf.space"

# LLM ક્લાયન્ટ સેટઅપ
client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

def run_agent():
    # વેલિડેટરની શરત: ઓછામાં ઓછા ૩ ટાસ્ક હોવા જોઈએ
    tasks = ["task_easy", "task_medium", "task_hard"]

    for task in tasks:
        # [START] બ્લોક પ્રિન્ટ કરો
        print(f"[START] task={task} env=ecopulse model={MODEL_NAME}", flush=True)
        
        try:
            # એન્વાયરમેન્ટ રીસેટ કરો
            reset_req = requests.post(f"{ENV_URL}/reset", json={"task": task}, timeout=15)
            reset_data = reset_req.json()
            obs = reset_data.get("observation", [])

            total_reward = 0.0
            num_steps = 5 # ટેસ્ટિંગ માટે ૫ સ્ટેપ
            
            for step_num in range(1, num_steps + 1):
                # LLM પ્રોક્સી દ્વારા એક્શન મેળવો
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": "Analyze these energy metrics and provide action 0-5. Output only the digit."}],
                    max_tokens=5
                )
                
                # એક્શન ક્લીન કરો
                content = response.choices[0].message.content.strip()
                action = 0
                for char in content:
                    if char.isdigit():
                        action = int(char)
                        break
                
                # એન્વાયરમેન્ટમાં સ્ટેપ લો
                step_req = requests.post(f"{ENV_URL}/step", json={"action": action}, timeout=15)
                step_data = step_req.json()
                
                reward = float(step_data.get("reward", 0.0))
                total_reward += reward
                done = step_data.get("done", False)

                # [STEP] બ્લોક પ્રિન્ટ કરો
                print(f"[STEP] step={step_num} reward={reward:.4f} done={done} error=null", flush=True)
                
                if done:
                    break

            # --- સ્કોરની ગણતરી (0 અને 1 ની વચ્ચે રાખવી ફરજિયાત છે) ---
            # જો એવરેજ સ્કોર 0 કે તેથી ઓછો હોય તો 0.01 આપવો
