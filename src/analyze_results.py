import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def analyze():
    with open("results/metrics.json", "r") as f:
        data = json.load(f)
        
    # Convert to DataFrame for plotting
    records = []
    for method, steps in data.items():
        for step_data in steps:
            step = step_data['step']
            for task_key, acc in step_data['accuracies'].items():
                task_name = task_key.split('_')[2] # Task_0_natural science -> natural science
                records.append({
                    "Method": method,
                    "Step": step,
                    "Task": task_name,
                    "Accuracy": acc
                })
                
    df = pd.DataFrame(records)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Step", y="Accuracy", hue="Method", style="Task", markers=True)
    plt.title("Continual Learning Performance: Nested vs Flat Memory")
    plt.ylim(0.5, 1.0)
    plt.ylabel("Accuracy")
    plt.xlabel("Task Step")
    plt.grid(True)
    
    os.makedirs("results/plots", exist_ok=True)
    plt.savefig("results/plots/learning_curves.png")
    print("Saved plot to results/plots/learning_curves.png")
    
    # Compute stats
    print("\n--- Statistics ---")
    for method in df['Method'].unique():
        print(f"\nMethod: {method}")
        method_df = df[df['Method'] == method]
        # Avg Acc at final step
        final_step = method_df['Step'].max()
        final_acc = method_df[method_df['Step'] == final_step]['Accuracy'].mean()
        print(f"Final Average Accuracy: {final_acc:.3f}")
        
        # Forgetting (Task 0)
        t0_initial = method_df[(method_df['Step'] == 0) & (method_df['Task'] == 'natural science')]['Accuracy'].values[0]
        t0_final = method_df[(method_df['Step'] == final_step) & (method_df['Task'] == 'natural science')]['Accuracy'].values[0]
        print(f"Task 0 Forgetting: {t0_initial:.3f} -> {t0_final:.3f} (Delta: {t0_final - t0_initial:.3f})")

if __name__ == "__main__":
    analyze()
