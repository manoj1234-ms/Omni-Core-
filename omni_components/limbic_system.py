import random
import time

class LimbicSystem:
    """
    The Synthetic Emotion Core (Problem 6): Modulates the Math Core's simulation 
    using 'chemical' variables to drive exploration and handle frustration.
    """
    def __init__(self):
        self.dopamine = 0.5  # Success drive (Reward Signal)
        self.cortisol = 0.2  # Stress level (Error Signal)
        self.curiosity = 0.8 # Drive to explore new memory branches
        
        # System status
        self.burnout_threshold = 0.9
        self.flow_state = False

    def update_state(self, confidence_score):
        """
        Adjusts internal chemistry based on the accuracy/confidence of the 
        last reasoning task.
        """
        if confidence_score > 6.5:
            # Reward: Success leads to dopamine spike and cortisol drop
            self.dopamine = min(1.0, self.dopamine + 0.05)
            self.cortisol = max(0.0, self.cortisol - 0.02)
            print(f"📊 [LIMBIC]: Positive Feedback. Dopamine: {self.dopamine:.2f} | Cortisol: {self.cortisol:.2f}")
        else:
            # Stress: Failure or low confidence spikes cortisol
            self.cortisol = min(1.0, self.cortisol + 0.1)
            self.dopamine = max(0.0, self.dopamine - 0.05)
            print(f"📊 [LIMBIC]: Stress Spike detected. Dopamine: {self.dopamine:.2f} | Cortisol: {self.cortisol:.2f}")

        # Flow State Modulation
        if self.dopamine > 0.7 and self.cortisol < 0.3:
            self.flow_state = True
            print("✨ [LIMBIC]: System entering 'Flow State'. Reasoning performance optimized.")
        else:
            self.flow_state = False

    def get_simulation_bias(self):
        """
        Returns a bias factor that affects the Math Core's randomness.
        Higher Cortisol increases jitter/uncertainty.
        Higher Dopamine increases focus on high-confidence branches.
        """
        return (self.dopamine - self.cortisol) / 2.0

if __name__ == "__main__":
    # Test Module
    ls = LimbicSystem()
    ls.update_state(0.8) # Fail
    ls.update_state(8.0) # Success
