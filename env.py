import gymnasium as gym
from gymnasium import spaces
import numpy as np

class SmartEnergyEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0], dtype=np.float32),
            high=np.array([24, 100, 10, 1, 1], dtype=np.float32)
        )
        self.action_space = spaces.Discrete(4)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_hour = 0
        self.battery = 50
        self.total_reward = 0
        obs = self._get_obs()
        return obs, {}

    def _get_obs(self):
        price = self.current_hour % 3
        solar = 1.0 if self.current_hour < 15 else 0.0
        return np.array([
            self.current_hour,
            self.battery,
            price,
            solar,
            0.0
        ], dtype=np.float32)

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
        self.total_reward += reward
        done = self.current_hour >= 24
        obs = self._get_obs()
        return obs, reward, done, False, {}
        
