@@ -0,0 +1,18 @@
import gradio as gr
from env import SmartEnergyEnv
def run():
    env = SmartEnergyEnv(); obs = env.reset(); done = False; res = []
    while not done:
        b = int(obs['battery'].replace('%',''))
        if obs['solar_ready'] == 'sunny': a = 0; d = "☀️ Solar"
        elif obs['grid_price'] == 'low' and b <= 85: a = 3; d = "🔌 Charge"
        elif b >= 10: a = 1; d = "🔋 Battery"
        else: a = 2; d = "⚡ Grid"
        o, r, done = env.step(a); res.append([f"{env.current_hour}:00", obs['grid_price'], d, r])
    return res, f"Score: {env.total_reward}"
with gr.Blocks() as demo:
    gr.Markdown("# 🌿 EcoPulse AI")
    btn = gr.Button("Run Simulation")
    out = [gr.Dataframe(headers=["Hour", "Price", "Action", "Reward"]), gr.Textbox()]
    btn.click(run, outputs=out)
demo.launch()
