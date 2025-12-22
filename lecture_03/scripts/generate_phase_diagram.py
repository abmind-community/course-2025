import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def parse_results(root_dir="results"):
    data = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(root_dir):
        if "moran.csv" in files:
            # Extract parameters from path
            # Expected format: .../g_{size}/n_{nh_size}/t_{threshold}/s_{seed}
            path_parts = root.split(os.sep)

            g_val, n_val, t_val, s_val = None, None, None, None

            for part in path_parts:
                if part.startswith("g_"):
                    g_val = int(part.split("_")[1])
                elif part.startswith("n_"):
                    n_val = int(part.split("_")[1])
                elif part.startswith("t_"):
                    t_val = float(part.split("_")[1])
                elif part.startswith("s_"):
                    s_val = int(part.split("_")[1])

            if None not in [g_val, n_val, t_val]:
                try:
                    file_path = os.path.join(root, "moran.csv")
                    with open(file_path, "r") as f:
                        content = f.read().strip()
                        if content:
                            moran_i = float(content)
                            data.append(
                                {
                                    "Grid Size": g_val,
                                    "Neighborhood Size": n_val,
                                    "Threshold": t_val,
                                    "Seed": s_val,
                                    "Moran's I": moran_i,
                                }
                            )
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return pd.DataFrame(data)


def plot_phase_diagram(df, output_dir="output/plots"):
    os.makedirs(output_dir, exist_ok=True)

    # Get unique grid sizes
    grid_sizes = df["Grid Size"].unique()

    for g in sorted(grid_sizes):
        subset = df[df["Grid Size"] == g]

        # Average over seeds
        averaged = (
            subset.groupby(["Neighborhood Size", "Threshold"])["Moran's I"]
            .mean()
            .reset_index()
        )

        # Pivot for heatmap
        pivot_table = averaged.pivot(
            index="Neighborhood Size", columns="Threshold", values="Moran's I"
        )

        # Sort index (Neighborhood Size) descending for Y-axis (Standard convention: small at bottom? or large at top?)
        # Usually Phase Diagrams have Y going up. So Neighborhood size increasing upwards.
        pivot_table = pivot_table.sort_index(ascending=False)

        plt.figure(figsize=(12, 8))
        sns.set_context("notebook")

        # Create Heatmap
        # annot=True might be too crowded if there are many thresholds. Let's check size.
        annot = True if pivot_table.shape[1] < 15 else False

        sns.heatmap(
            pivot_table,
            annot=annot,
            fmt=".2f",
            cmap="viridis",
            vmin=0,
            vmax=1,
            cbar_kws={"label": "Moran's I (Segregation)"},
        )

        plt.title(f"Schelling Model Phase Diagram (Grid Size: {g}x{g})")
        plt.xlabel("Similarity Threshold")
        plt.ylabel("Neighborhood Size")

        # Fix X-axis labels to be pretty
        # If there are too many, we might need to reduce tick frequency, but seaborn usually handles this okay.

        output_path = os.path.join(output_dir, f"phase_diagram_g_{g}.png")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        print(f"Saved plot to {output_path}")


if __name__ == "__main__":
    print("Parsing results...")
    df = parse_results()

    if df.empty:
        print("No data found in results/ directory.")
    else:
        print(f"Found {len(df)} data points.")
        print(df.head())
        plot_phase_diagram(df)
