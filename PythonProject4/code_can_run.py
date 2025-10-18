# 2508赛题完整可运行代码：军工板块股票数据分析（适配2508赛题文档任务1-2）
# 功能：读取预处理矩阵→计算关联系数并排名（任务1）→周期性分析（任务2）→可视化
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np


# --------------------------
# 1. 读取2508赛题预处理数据（适配赛题文档“数据来源”要求）
# --------------------------
def load_matrix(matrix_path):
    """读取并预处理2508赛题收盘价矩阵（修正时间格式）"""
    try:
        price_matrix = pd.read_csv(matrix_path, index_col="时间戳")
        # 关键修正：强制指定时间格式（沪深300数据常用%Y%m%d，如20231018）
        price_matrix.index = pd.to_datetime(price_matrix.index, format='%Y%m%d', errors='coerce')
        # 清理无效时间（转换失败的行）
        price_matrix = price_matrix[price_matrix.index.notnull()]
        if len(price_matrix) == 0:
            raise ValueError("转换后无有效时间数据，请检查时间戳格式是否为'YYYYMMDD'")
        print(f"✅ 时间格式修正成功，有效时间范围：{price_matrix.index[0].date()} ~ {price_matrix.index[-1].date()}")
        return price_matrix
    except Exception as e:
        raise ValueError(f"❌ 数据读取失败：{str(e)}")


# --------------------------
# 2. 计算关联系数并排名（2508赛题文档任务1：板块联动模型核心）
# --------------------------
def calculate_corr(price_matrix):
    """计算军工板块股票Pearson关联系数，生成降序排名表（返回排名表，符合赛题“降序排名”要求）"""
    # 步骤1：计算关联系数矩阵（赛题文档要求的“板块关联系数”）
    corr_matrix = price_matrix.corr()
    print("\n=== 2508赛题-军工板块关联系数矩阵（部分） ===")
    print(corr_matrix.round(4).head())

    # 步骤2：生成股票对关联系数列表（避免重复计算，如A-B与B-A）
    corr_results = []
    stocks = corr_matrix.columns.tolist()
    for i in range(len(stocks)):
        for j in range(i + 1, len(stocks)):
            # 关键：正确定义每一行结果，包含股票对、关联系数、联动强度（贴合赛题文档“联动分析”需求）
            corr_value = corr_matrix.iloc[i, j]
            corr_results.append({
                "股票对": f"{stocks[i]}-{stocks[j]}",
                "关联系数": round(corr_value, 4),
                "联动强度": "强联动" if corr_value >= 0.8 else "中等联动" if corr_value >= 0.5 else "弱联动"
            })

    # 步骤3：降序排名（赛题文档任务1明确要求“给出降序排名”）
    corr_ranking = pd.DataFrame(corr_results).sort_values("关联系数", ascending=False)
    # 关键：确保函数内正确定义corr_ranking后再返回，解决NameError
    return corr_ranking


# --------------------------
# 3. 周期性分析（2508赛题文档任务2：板块股价周期性）
# --------------------------
def periodic_analysis(price_matrix):
    """修正重采样与绘图逻辑，生成正确趋势图"""
    # 验证数据量（至少需12个月数据才能体现周期）
    if len(price_matrix) < 12:
        print("⚠️ 警告：有效数据不足12个时间点，可能无法生成合理周期趋势")

    # 月度重采样（ME=月末，确保与时间格式匹配）
    monthly_avg_price = price_matrix.resample("ME").mean()
    print(f"\n=== 月度平均股价数据（共{len(monthly_avg_price)}个月份） ===")
    print(monthly_avg_price.round(2).head())

    # 绘图修正：确保折线连续，时间轴正常
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(12, 6))
    for stock in monthly_avg_price.columns:
        # 仅绘制有数据的部分，避免空值导致的断裂
        valid_data = monthly_avg_price[stock].dropna()
        plt.plot(valid_data.index, valid_data.values,
                 marker="o", linewidth=2, label=stock)  # linewidth确保连线连续

    plt.xlabel("时间（月）")
    plt.ylabel("月度平均收盘价（元）")
    plt.title("2508赛题-军工板块股价月度周期性趋势（修正后）")
    plt.legend()
    plt.grid(alpha=0.3)
    # 调整x轴刻度显示，避免重叠
    plt.gcf().autofmt_xdate()  # 自动旋转日期标签
    plt.tight_layout()

    # 保存修正后的趋势图
    trend_path = r"D:\aiu三面\stock\stock data\2508赛题_修正后周期性趋势图.png"
    plt.savefig(trend_path, dpi=300)
    plt.close()
    print(f"✅ 修正后趋势图已保存至：{trend_path}")
    return monthly_avg_price


# --------------------------
# 4. 主函数（执行2508赛题完整分析流程）
# --------------------------
if __name__ == "__main__":
    # 2508赛题预处理后收盘价矩阵路径（需与你实际路径一致，参考文档“数据来源”下载路径）
    matrix_path = r"D:\aiu三面\stock\stock data\2508赛题_军工板块收盘价矩阵_预处理后.csv"

    # 执行流程：读取数据→计算关联系数→周期性分析（完全贴合赛题文档任务顺序）
    price_matrix = load_matrix(matrix_path)
    corr_ranking = calculate_corr(price_matrix)  # 此处调用函数，不再报NameError
    monthly_avg_price = periodic_analysis(price_matrix)

    # 保存关联系数排名表（赛题文档“提交内容”要求的数据集之一）
    ranking_path = r"D:\aiu三面\stock\stock data\2508赛题_关联系数降序排名.csv"
    corr_ranking.to_csv(ranking_path, index=False, encoding="utf-8-sig")

    # 输出最终结果摘要（符合赛题文档“结果分析”需求）
    print(f"\n🎉 2508赛题完整分析完成！")
    print(
        f"1. 关联系数排名表保存路径：{ranking_path}（TOP3联动股票对：{corr_ranking.iloc[0]['股票对']}，关联系数：{corr_ranking.iloc[0]['关联系数']}）")
    print(f"2. 周期性分析覆盖时间节点：{len(monthly_avg_price)}个月份（符合赛题文档“多尺度分析”要求）")