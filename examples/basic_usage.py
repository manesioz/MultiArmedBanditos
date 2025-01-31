from mab_platform.core.platform import ExperimentPlatform
from mab_platform.core.strategies import ThompsonSampling
from datetime import datetime
import numpy as np

def run_simulation():
    # Initialize platform with Thompson Sampling strategy
    platform = ExperimentPlatform(strategy=ThompsonSampling())
    
    # Create an experiment
    exp_id = platform.create_experiment(
        name="Button Color Test",
        variants=["blue", "green", "red"],
        start_date=datetime.now()
    )
    
    # Simulate user interactions
    # True probabilities (in real life, these would be unknown)
    true_probabilities = {
        "blue": 0.1,   # 10% click rate
        "green": 0.2,  # 20% click rate
        "red": 0.15    # 15% click rate
    }
    
    print("Starting simulation...")
    print("True probabilities:", true_probabilities)
    print()
    
    # Run 1000 simulated user interactions
    for i in range(1000):
        # Get variant to test
        variant = platform.get_variant(exp_id)
        
        # Simulate user behavior (click/no-click)
        reward = np.random.binomial(1, true_probabilities[variant])
        
        # Record the result
        platform.record_reward(exp_id, variant, reward)
        
        # Print progress every 100 iterations
        if (i + 1) % 100 == 0:
            results = platform.get_experiment_results(exp_id)
            print(f"After {i + 1} trials:")
            for variant, stats in results.items():
                print(f"{variant}: {stats['mean_reward']:.3f} "
                      f"({stats['total_trials']} trials)")
            print()

    # Final results
    print("Final Results:")
    results = platform.get_experiment_results(exp_id)
    for variant, stats in results.items():
        print(f"{variant}:")
        print(f"  Mean Reward: {stats['mean_reward']:.3f}")
        print(f"  Total Trials: {stats['total_trials']}")
        print(f"  Total Rewards: {stats['total_rewards']}")
        print()

if __name__ == "__main__":
    run_simulation()