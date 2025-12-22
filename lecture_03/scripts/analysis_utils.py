import glob
import os

import numpy as np
import pandas as pd
from scipy.signal import convolve2d


def load_data(log_file):
    """
    Load Agent log data, handling potentially split MPI files (e.g., agent_log_1.csv).
    """
    if not os.path.exists(log_file):
        # Try finding split files
        base_name = log_file.replace(".csv", "_*.csv")
        files = glob.glob(base_name)
        if not files:
            return None
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    else:
        df = pd.read_csv(log_file)
        # Check for split files even if main file exists
        base_name = log_file.replace(".csv", "_*.csv")
        files = glob.glob(base_name)
        if files:
            split_df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
            if len(split_df) > len(df):
                df = split_df
    return df


def calculate_morans_i(grid_matrix):
    """
    Calculate Global Moran's I for a grid matrix (numpy array) using fast convolution.
    NaN values are treated as empty cells.

    This vectorized implementation is significantly faster than nested loops.
    """
    # Create a mask for valid (non-NaN) cells
    mask = ~np.isnan(grid_matrix)

    # Extract values
    values = grid_matrix.copy()
    values[~mask] = 0  # Zero out NaNs to not affect sums

    # Count valid cells
    N = np.sum(mask)
    if N < 2:
        return np.nan

    # Calculate mean of valid cells
    mean_val = np.sum(values) / N

    # Calculate deviations
    z = np.zeros_like(grid_matrix)
    z[mask] = grid_matrix[mask] - mean_val

    # Denominator: sum of squared deviations
    denom = np.sum(z[mask] ** 2)
    if denom == 0:
        return np.nan

    # Define kernel for Moore neighborhood (8 neighbors)
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    # Calculate W: Sum of weights (valid neighbor pairs)
    # Convolve mask with kernel to get count of valid neighbors for each cell
    valid_neighbor_counts = convolve2d(
        mask.astype(int), kernel, mode="same", boundary="fill", fillvalue=0
    )
    # Sum these counts only for valid central cells
    W = np.sum(valid_neighbor_counts[mask])

    if W == 0:
        return np.nan

    # Calculate Numerator: sum_i sum_j w_ij * z_i * z_j
    # convolution of z with kernel gives sum_j w_ij * z_j for each i
    neighbor_z_sum = convolve2d(z, kernel, mode="same", boundary="fill", fillvalue=0)

    # Multiply by z_i and sum over valid i
    num = np.sum(z[mask] * neighbor_z_sum[mask])

    return (N / W) * (num / denom)


def parse_results(root_dir="results"):
    """
    Parse result directories to extract parameters and metrics.
    """
    data = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(root_dir):
        if "moran.csv" in files:
            # Expected format: .../h_{always_happy}/n_{nh_size}/t_{threshold}/s_{seed}
            # Or old format: .../g_{size}/...
            path_parts = root.split(os.sep)

            h_val, g_val, n_val, t_val, s_val = None, None, None, None, None

            for part in path_parts:
                if part.startswith("h_"):
                    try:
                        h_val = float(part.split("_")[1])
                    except ValueError:
                        pass
                elif part.startswith("g_"):
                    try:
                        g_val = int(part.split("_")[1])
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

            if None not in [n_val, t_val]:  # Minimal requirement
                try:
                    file_path = os.path.join(root, "moran.csv")
                    with open(file_path, "r") as f:
                        content = f.read().strip()
                        if content:
                            moran_i = float(content)
                            entry = {
                                "Neighborhood Size": n_val,
                                "Threshold": t_val,
                                "Seed": s_val,
                                "Moran's I": moran_i,
                            }
                            if h_val is not None:
                                entry["Always Happy"] = h_val
                            if g_val is not None:
                                entry["Grid Size"] = g_val
                            data.append(entry)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return pd.DataFrame(data)
