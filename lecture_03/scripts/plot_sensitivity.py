import collections
import re
import sys

import matplotlib.pyplot as plt


def plot_single(output_image, input_files):
    """
    绘制单个邻域配置的敏感性分析图（阈值 vs 莫兰指数）。
    """
    data = []
    pattern = re.compile(r"t_(\d+\.?\d*)")

    for fpath in input_files:
        match = pattern.search(fpath)
        if match:
            threshold = float(match.group(1))
            try:
                with open(fpath, "r") as f:
                    val = float(f.read().strip())
                    data.append((threshold, val))
            except Exception as e:
                print(f"警告: 无法读取 {fpath}: {e}")

    data.sort(key=lambda x: x[0])
    if not data:
        print("未找到有效的数据点。")
        return

    thresholds, values = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, values, marker="o", linestyle="-", color="teal")
    plt.title("Sensitivity Analysis: Segregation vs Threshold")
    plt.xlabel("Threshold (Similarity Preference)")
    plt.ylabel("Final Global Moran's I")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(output_image)
    print(f"敏感性图已保存至 {output_image}")


def plot_combined(output_image, input_files):
    """
    绘制合并的敏感性分析图，在同一张图上比较不同邻域大小的结果。
    """
    data = collections.defaultdict(list)
    pattern = re.compile(r"n_(\d+)/t_(\d+\.?\d*)")

    for fpath in input_files:
        match = pattern.search(fpath)
        if match:
            n = int(match.group(1))
            t = float(match.group(2))
            try:
                with open(fpath, "r") as f:
                    val = float(f.read().strip())
                    data[n].append((t, val))
            except Exception as e:
                print(f"警告: 无法读取 {fpath}: {e}")

    if not data:
        print("未找到有效的数据点。")
        return

    plt.figure(figsize=(12, 8))
    for n in sorted(data.keys()):
        points = data[n]
        points.sort(key=lambda x: x[0])
        thresholds, values = zip(*points)
        plt.plot(thresholds, values, marker="o", linestyle="-", label=f"N={n}")

    plt.title("Combined Sensitivity Analysis: Segregation vs Threshold")
    plt.xlabel("Threshold (Similarity Preference)")
    plt.ylabel("Final Global Moran's I")
    plt.legend(title="Neighborhood Size")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.savefig(output_image)
    print(f"合并图已保存至 {output_image}")


def main():
    if len(sys.argv) < 3:
        print("用法:")
        print("  python plot_sensitivity.py single <output_image> <input_file_1> ...")
        print("  python plot_sensitivity.py combined <output_image> <input_file_1> ...")
        sys.exit(1)

    mode = sys.argv[1]
    output_image = sys.argv[2]
    input_files = sys.argv[3:]

    if mode == "single":
        plot_single(output_image, input_files)
    elif mode == "combined":
        plot_combined(output_image, input_files)
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
