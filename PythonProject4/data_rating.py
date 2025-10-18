import pandas as pd

import matplotlib.pyplot as plt

# 1. 读取已预处理的军工板块收盘价矩阵（替换为你的矩阵文件路径）
matrix_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块收盘价矩阵_预处理后.csv"
price_matrix = pd.read_csv(matrix_path, index_col="时间戳")  # 时间戳设为索引

# 2. 计算Pearson关联系数矩阵（2508赛题文档要求的“板块关联系数”）
corr_matrix = price_matrix.corr()
print("=== 2508赛题-军工板块股票关联系数矩阵 ===")
print(corr_matrix.round(4))  # 保留4位小数，符合分析精度

# 3. 提取股票对并按关联系数降序排名（赛题要求“给出降序排名”）
corr_results = []
stocks = corr_matrix.columns.tolist()
for i in range(len(stocks)):
    print(f"外层循环，当前i值: {i}")
    for j in range(i + 1, len(stocks)):
        print(f"内层循环，当前j值: {j}")
        corr_value = corr_matrix.iloc[i, j]
        corr_results.append({
            "股票对": f"{stocks[i]}-{stocks[j]}",
            "关联系数": round(corr_value, 4),
            "联动强度": "强联动" if corr_value >= 0.8 else "中等联动" if corr_value >= 0.5 else "弱联动"
        })
# 生成排名表
corr_ranking = pd.DataFrame(corr_results).sort_values("关联系数", ascending=False)
# 保存排名结果（2508赛题提交需提供数据文件）
ranking_save_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块关联系数排名.csv"
corr_ranking.to_csv(ranking_save_path, index=False, encoding="utf-8-sig")

print("\n=== 2508赛题-军工板块关联系数TOP10排名 ===")
print(corr_ranking.head(10))
print(f"\n排名结果已保存至：{ranking_save_path}")