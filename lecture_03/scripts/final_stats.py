import glob
import os
import sys

import numpy as np
import pandas as pd


def load_data(log_file):
    """
    加载 Agent 日志数据，处理可能存在的 MPI 分割文件 (例如 agent_log_1.csv)。
    """
    if not os.path.exists(log_file):
        # 尝试查找分割文件
        base_name = log_file.replace(".csv", "_*.csv")
        files = glob.glob(base_name)
        if not files:
            return None
        df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    else:
        df = pd.read_csv(log_file)
        # 即使主文件存在，也检查分割文件
        base_name = log_file.replace(".csv", "_*.csv")
        files = glob.glob(base_name)
        if files:
            split_df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
            if len(split_df) > len(df):
                df = split_df
    return df


def calculate_morans_i(grid_matrix):
    """
    计算网格矩阵（numpy 数组）的全局莫兰指数 (Global Moran's I)。
    NaN 值被视为空单元格。
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


def calc_single(input_file, output_file):
    """
    为单个日志文件计算最后时刻的莫兰指数。
    """
    df = load_data(input_file)
    if df is None:
        print(f"错误: 未找到数据文件 {input_file}")
        sys.exit(1)

    # 获取最后一个 tick
    last_tick = df["tick"].max()
    subset = df[df["tick"] == last_tick]

    # 构建网格
    width = int(df["x"].max()) + 1
    height = int(df["y"].max()) + 1

    grid = np.full((height, width), np.nan)

    # 去除重复项以防万一
    subset = subset.drop_duplicates(subset=["x", "y"])

    for _, row in subset.iterrows():
        x, y = int(row["x"]), int(row["y"])
        val = 1 if row["type"] == 1 else -1
        if 0 <= x < width and 0 <= y < height:
            grid[y, x] = val

    moran_i = calculate_morans_i(grid)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        f.write(str(moran_i))


def aggregate(output_file, input_files):
    """
    聚合多个包含单个浮点数的文件，计算平均值。
    """
    values = []
    for f in input_files:
        try:
            with open(f, "r") as file:
                content = file.read().strip()
                if content:
                    values.append(float(content))
        except Exception as e:
            print(f"警告: 无法读取 {f}: {e}")

    if not values:
        print("错误: 未找到有效的聚合值。")
        sys.exit(1)

    avg_value = np.mean(values)

    with open(output_file, "w") as f:
        f.write(str(avg_value))


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python final_stats.py calc <input_log_csv> <output_file>")
        print(
            "  python final_stats.py aggregate <output_file> <input_file_1> <input_file_2> ..."
        )
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "calc":
        if len(sys.argv) != 4:
            print("用法: python final_stats.py calc <input_log_csv> <output_file>")
            sys.exit(1)
        calc_single(sys.argv[2], sys.argv[3])

    elif mode == "aggregate":
        if len(sys.argv) < 4:
            print(
                "用法: python final_stats.py aggregate <output_file> <input_file_1> ..."
            )
            sys.exit(1)
        aggregate(sys.argv[2], sys.argv[3:])

    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
