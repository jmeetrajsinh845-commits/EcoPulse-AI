import random
class SmartEnergyEnv:
    def __init__(self):
        self.prices = ["low"]*8 + ["high"]*10 + ["low"]*6
        self.solar_power = ["cloudy"]*7 + ["sunny"]*11 + ["cloudy"]*6
        self.reset()
    def reset(self):
        self.current_hour = 0; self.battery_level = 50; self.total_reward = 0
        return self._get_observation()
    def _get_observation(self):
        return {"time": "day", "grid_price": self.prices[self.current_hour], "solar_ready": self.solar_power[self.current_hour], "battery": f"{self.battery_level}%"}
    def step(self, action):
        price = self.prices[self.current_hour]; sun = self.solar_power[self.current_hour]; reward = 0
        if action == 0: reward += 25 if sun == "sunny" else -15
        elif action == 1: self.battery_level -= 10; reward += 20 if price == "high" else 5
        elif action == 2: reward -= 25 if price == "high" else 5
        elif action == 3: self.battery_level += 15; reward += 15 if price == "low" else -15
        self.current_hour = (self.current_hour + 1) % 24
        return self._get_observation(), reward, self.current_hour == 0
