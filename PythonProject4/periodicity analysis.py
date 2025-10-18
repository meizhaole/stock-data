# 1. 导入2508赛题周期性分析核心库（匹配赛题数据处理需求）
import pandas as pd
import matplotlib.pyplot as plt

# 2. 读取2508赛题预处理后的军工板块收盘价矩阵（路径需与预处理结果一致）
matrix_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块收盘价矩阵_预处理后.csv"
price_matrix = pd.read_csv(matrix_path, index_col="时间戳")

# 3. 时间格式转换（确保符合2508赛题“时间序列分析”要求）
try:
    price_matrix.index = pd.to_datetime(price_matrix.index)
    print("✅ 2508赛题数据时间格式转换成功！时间范围：", price_matrix.index[0], "~", price_matrix.index[-1])
except ValueError:
    raise ValueError("❌ 2508赛题收盘价矩阵'时间戳'格式异常，无法完成周期性分析")

# 4. 【关键修复】月度重采样标识替换为ME（解决FutureWarning，功能与原M一致）
# 按《2508股票数据分析模型.docx》任务2要求，分析板块股价周期性，此处为月度平均股价计算
monthly_avg_price = price_matrix.resample("ME").mean()  # ME=Month End，代表月末重采样，适配pandas新版本
# 若需分析季度周期性（可选拓展，贴合赛题“多尺度分析”需求），可改为：quarterly_avg_price = price_matrix.resample("QE").mean()

# 5. 输出2508赛题周期性分析核心结果
print("\n=== 2508赛题-军工板块月度平均股价（前6个月） ===")
print(monthly_avg_price.head(6).round(2))  # 保留2位小数，符合金融数据展示习惯

# 6. 周期性趋势可视化（支撑赛题“数据分析功能”评分项，占比60%）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12, 6))

# 绘制各军工股月度趋势线（体现板块联动性与周期性）
for stock in monthly_avg_price.columns:
    plt.plot(monthly_avg_price.index, monthly_avg_price[stock], marker="o", linewidth=2, label=stock)

# 图表格式适配赛题成果展示需求
plt.xlabel("时间（月）", fontsize=12)
plt.ylabel("月度平均收盘价（元）", fontsize=12)
plt.title("2508赛题-沪深300军工板块股价月度周期性趋势", fontsize=14)
plt.legend(loc="best")
plt.grid(alpha=0.3)
plt.tight_layout()

# 保存可视化结果（需随2508赛题提交，作为周期性分析的核心支撑材料）
trend_save_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块股价周期性趋势图.png"
plt.savefig(trend_save_path, dpi=300)
plt.close()

print(f"\n🎉 2508赛题周期性分析完成！")
print(f"1. 月度平均股价数据维度：{monthly_avg_price.shape}（时间节点×股票数量）")
print(f"2. 周期性趋势图保存路径：{trend_save_path}")