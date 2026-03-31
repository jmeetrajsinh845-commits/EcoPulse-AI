class SmartEnergyEnv:
    def __init__(self):
        self.reset()
    def reset(self):
        self.current_hour = 0
        self.total_reward = 0
        self.battery = 50
        return self._get_obs()
    def _get_obs(self):
        prices = ['low', 'medium', 'high']
        weather = ['sunny', 'cloudy']
        # અહીં બેટરીને સીધી સંખ્યા (int) તરીકે જ મોકલીએ
        return {
            'grid_price': prices[self.current_hour % 3],
            'solar_ready': weather[0] if self.current_hour < 15 else weather[1],
            'battery': self.battery 
        }
    def step(self, action):
        reward = 0
        if action == 0: reward = 10 
        elif action == 1: 
            if self.battery >= 10: self.battery -= 10; reward = 5
            else: reward = -5
        elif action == 2: reward = -2 
        elif action == 3: 
            if self.battery <= 90: self.battery += 10; reward = 2
            else: reward = -1
        self.current_hour += 1
        done = self.current_hour >= 24
        self.total_reward += reward
        return self._get_obs(), reward, done
