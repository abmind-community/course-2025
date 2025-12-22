import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(log_file):
    """
    加载日志数据，支持 MPI 分割日志。
    """
    if not os.path.exists(log_file):
        base_name = log_file.replace(".csv", "_*.csv")
        files = glob.glob(base_name)
        if not files:
            return None
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    else:
        df = pd.read_csv(log_file)
        base_name = log_file.replace(".csv", "_*.csv")
        files = glob.glob(base_name)
        if files:
            split_df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
            if len(split_df) > len(df):
                df = split_df
    return df


def calculate_morans_i(grid_matrix):
    """
    计算网格矩阵的全局莫兰指数。
    """
    rows, cols = grid_matrix.shape
    valid_mask = ~np.isnan(grid_matrix)
    values = grid_matrix[valid_mask]
    if len(values) < 2:
        return np.nan
    N = len(values)
    mean_val = np.mean(values)
    denom = np.sum((values - mean_val) ** 2)
    if denom == 0:
        return np.nan
    num = 0.0
    W = 0.0
    neighbors_offsets = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    for r in range(rows):
        for c in range(cols):
            if np.isnan(grid_matrix[r, c]):
                continue
            val_i = grid_matrix[r, c]
            for dr, dc in neighbors_offsets:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if not np.isnan(grid_matrix[nr, nc]):
                        val_j = grid_matrix[nr, nc]
                        num += (val_i - mean_val) * (val_j - mean_val)
                        W += 1.0
    if W == 0:
        return np.nan
    return (N / W) * (num / denom)


def plot_snapshots(log_file, output_dir):
    """
    绘制并保存每个时间步（tick）的网格快照。
    """
    df = load_data(log_file)
    if df is None:
        print(f"错误: 未找到 {log_file}")
        return

    if "x" not in df.columns or "y" not in df.columns:
        print("错误: 缺少 'x' 或 'y' 列。")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    width = int(df["x"].max()) + 1
    height = int(df["y"].max()) + 1

    ticks = sorted(df["tick"].unique())
    print(f"正在为 {len(ticks)} 个 tick 生成快照...")

    for tick in ticks:
        subset = df[df["tick"] == tick]
        plt.figure(figsize=(8, 8))
        sns.scatterplot(
            data=subset,
            x="x",
            y="y",
            hue="type",
            palette=["blue", "red"],
            style="happy",
            markers={0: "X", 1: "o"},
            s=60,
            legend="full",
        )
        plt.title(f"Schelling Segregation Model - Tick {tick}")
        plt.xlim(-1, width)
        plt.ylim(-1, height)
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        outfile = os.path.join(output_dir, f"tick_{int(tick):03d}.png")
        plt.savefig(outfile, bbox_inches="tight", dpi=100)
        plt.close()
    print(f"快照已保存至 {output_dir}")


def plot_series(log_file, output_file):
    """
    绘制并保存全局莫兰指数随时间变化的曲线图。
    """
    df = load_data(log_file)
    if df is None:
        print(f"错误: 未找到 {log_file}")
        return

    ticks = sorted(df["tick"].unique())
    moran_values = []
    width = int(df["x"].max()) + 1
    height = int(df["y"].max()) + 1

    print(f"正在计算 {len(ticks)} 个 tick 的莫兰指数序列...")

    for tick in ticks:
        tick_df = df[df["tick"] == tick]
        grid = np.full((height, width), np.nan)
        tick_df = tick_df.drop_duplicates(subset=["x", "y"])
        for _, row in tick_df.iterrows():
            x, y = int(row["x"]), int(row["y"])
            val = 1 if row["type"] == 1 else -1
            if 0 <= x < width and 0 <= y < height:
                grid[y, x] = val
        moran_values.append(calculate_morans_i(grid))

    plt.figure(figsize=(10, 6))
    plt.plot(ticks, moran_values, marker="o", linestyle="-", color="purple")
    plt.title("Moran's I over Time (Segregation Index)")
    plt.xlabel("Tick")
    plt.ylabel("Global Moran's I")
    plt.grid(True)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)
    print(f"序列图已保存至 {output_file}")


def main():
    if len(sys.argv) < 4:
        print("用法:")
        print("  python plot_process.py snapshots <log_file> <output_dir>")
        print("  python plot_process.py series <log_file> <output_file>")
        sys.exit(1)

    mode = sys.argv[1]
    log_file = sys.argv[2]
    output = sys.argv[3]

    if mode == "snapshots":
        plot_snapshots(log_file, output)
    elif mode == "series":
        plot_series(log_file, output)
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
