import random

class SmartEnergyEnv:
    def __init__(self):
        self.prices = ["low"]*8 + ["high"]*10 + ["low"]*6
        self.solar_power = ["cloudy"]*7 + ["sunny"]*11 + ["cloudy"]*6
        self.reset()

    def reset(self):
        self.current_hour = 0
        self.battery = 50  # અહીં નામ 'battery' રાખવું જરૂરી છે
        self.total_reward = 0
        return self._get_observation()

    def _get_observation(self):
        # સિસ્ટમને આ 3 કી (Keys) ખાસ જોઈએ છે
        return {
            "grid_price": self.prices[self.current_hour],
            "solar_ready": self.solar_power[self.current_hour],
            "battery": self.battery 
        }

    def step(self, action):
        price = self.prices[self.current_hour]
        sun = self.solar_power[self.current_hour]
        reward = 0
        
        if action == 0: # Solar
            reward += 25 if sun == "sunny" else -15
        elif action == 1: # Discharge Battery
            self.battery -= 10
            reward += 20 if price == "high" else 5
        elif action == 2: # Grid
            reward -= 25 if price == "high" else 5
        elif action == 3: # Charge Battery
            self.battery += 15
            reward += 15 if price == "low" else -15
            
        # બેટરીની મર્યાદા નક્કી કરવી (0 થી 100 ની વચ્ચે)
        self.battery = max(0, min(100, self.battery))
        
        self.current_hour = (self.current_hour + 1) % 24
        done = (self.current_hour == 0)
        
        return self._get_observation(), reward, done
