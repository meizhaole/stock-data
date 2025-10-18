# 1. 导入2508赛题可视化所需核心库（匹配赛题数据处理流程）
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 2. 读取2508赛题已生成的核心数据（关联系数矩阵，路径需与之前一致）
# 该矩阵为2508赛题任务1的核心输出，需确保与“板块联动模型”计算结果一致
corr_matrix_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块关联系数矩阵.csv"  # 若未单独保存，可重新计算：price_matrix.corr()
price_matrix_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块收盘价矩阵_预处理后.csv"
price_matrix = pd.read_csv(price_matrix_path, index_col="时间戳")
corr_matrix = price_matrix.corr()  # 若已保存关联系数矩阵，直接用pd.read_csv读取

# 3. 配置热力图样式（符合2508赛题“成果展示”的直观性要求）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 适配中文，避免2508赛题文档要求的成果展示乱码
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常问题
fig, ax = plt.subplots(figsize=(10, 8))  # 设置图表尺寸，确保股票名称不拥挤

# 4. 绘制热力图（核心可视化逻辑，贴合2508赛题关联系数分布需求）
# 颜色映射：RdYlBu_r（红色=弱联动，蓝色=强联动），符合金融数据可视化常规认知
im = ax.imshow(corr_matrix.values, cmap="RdYlBu_r", vmin=-1, vmax=1)  # vmin/vmax固定系数范围，确保颜色梯度统一

# 5. 添加颜色条（解释颜色与关联系数的对应关系，满足2508赛题“分析可读性”要求）
cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Pearson关联系数（值越接近1，联动性越强）", fontsize=12, labelpad=10)

# 6. 配置坐标轴（标注军工股票名称，对应2508赛题“军工板块股票”分析对象）
stocks = corr_matrix.columns.tolist()  # 2508赛题筛选后的军工股票名称
ax.set_xticks(np.arange(len(stocks)))
ax.set_yticks(np.arange(len(stocks)))
ax.set_xticklabels(stocks, rotation=45, ha="right", fontsize=10)  # 旋转x轴标签，避免重叠
ax.set_yticklabels(stocks, fontsize=10)

# 7. 添加关联系数数值标签（直接展示具体数值，支撑2508赛题“降序排名”的结论验证）
for i in range(len(stocks)):
    for j in range(len(stocks)):
        # 数值保留2位小数，颜色根据系数大小调整（深色背景用白色字，浅色背景用黑色字）
        text_color = "white" if abs(corr_matrix.iloc[i, j]) > 0.6 else "black"
        ax.text(j, i, round(corr_matrix.iloc[i, j], 2),
                ha="center", va="center", color=text_color, fontsize=9, fontweight="bold")

# 8. 设置图表标题（明确对应2508赛题任务1，符合赛题文档“板块联动模型”要求）
ax.set_title("2508赛题-沪深300军工板块股票关联系数热力图", fontsize=14, pad=20, fontweight="bold")

# 9. 调整布局与保存（确保图表完整，可直接放入2508赛题提交材料）
plt.tight_layout()  # 自动调整布局，避免标签被截断
heatmap_save_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块关联系数热力图.png"
plt.savefig(heatmap_save_path, dpi=300, bbox_inches="tight")  # 300dpi确保高清，符合提交要求
plt.close()

print(f"✅ 2508赛题联动性可视化（热力图）完成！")
print(f"热力图保存路径：{heatmap_save_path}")
print(f"关键结论提示：热力图中深蓝色单元格对应2508赛题要求的'高联动股票对'，可直接用于论文结果分析。")