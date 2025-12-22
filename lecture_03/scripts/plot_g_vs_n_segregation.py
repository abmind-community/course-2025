import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def parse_results(root_dir="results"):
    data = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(root_dir):
        if "moran.csv" in files:
            # Expected format: .../h_{always_happy}/n_{nh_size}/t_{threshold}/s_{seed}
            path_parts = root.split(os.sep)

            h_val, n_val, t_val, s_val = None, None, None, None

            for part in path_parts:
                if part.startswith("h_"):
                    try:
                        h_val = float(part.split("_")[1])
                    except ValueError:
                        pass
                elif part.startswith("n_"):
                    try:
                        n_val = int(part.split("_")[1])
                    except ValueError:
                        pass
                elif part.startswith("t_"):
                    try:
                        t_val = float(part.split("_")[1])
                    except ValueError:
                        pass
                elif part.startswith("s_"):
                    try:
                        s_val = int(part.split("_")[1])
                    except ValueError:
                        pass

            if None not in [h_val, n_val, t_val]:
                try:
                    file_path = os.path.join(root, "moran.csv")
                    with open(file_path, "r") as f:
                        content = f.read().strip()
                        if content:
                            moran_i = float(content)
                            data.append(
                                {
                                    "Always Happy": h_val,
                                    "Neighborhood Size": n_val,
                                    "Threshold": t_val,
                                    "Seed": s_val,
                                    "Moran's I": moran_i,
                                }
                            )
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return pd.DataFrame(data)


def plot_g_vs_n(df, output_path="output/plots/h_vs_n_moran_gt_0.6.png"):
    # Filter for Moran's I > 0.6
    filtered_df = df[df["Moran's I"] > 0.6].copy()

    if filtered_df.empty:
        print("No data points found with Moran's I > 0.6")
        return

    plt.figure(figsize=(10, 8))
    sns.set_style("whitegrid")

    # Scatter plot
    # X: Always Happy
    # Y: Neighborhood Size
    # Hue: Threshold
    sns.scatterplot(
        data=filtered_df,
        x="Always Happy",
        y="Neighborhood Size",
        hue="Threshold",
        palette="viridis",
        alpha=0.7,
        s=100,
    )

    plt.title("Phase Diagram: Configurations with Moran's I > 0.6")
    plt.xlabel("Always Happy Ratio")
    plt.ylabel("Neighborhood Size")
    plt.legend(title="Threshold", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150)
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    print("Parsing results...")
    df = parse_results()
    print(f"Total data points: {len(df)}")

    plot_g_vs_n(df)
