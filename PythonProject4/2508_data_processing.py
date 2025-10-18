# 1. 导入2508赛题数据处理核心库（按赛题需求仅用pandas/os）
import pandas as pd
import os

# 2. 配置2508赛题数据路径（严格匹配你的多CSV文件存放路径）
data_folder = r"D:\aiu三面\stock\stock data"  # 你的2508赛题CSV文件所在文件夹
print(f"🔍 正在扫描2508赛题数据文件夹：{data_folder}")

# 3. 适配2508赛题真实字段名（已确认：ts_code=股票代码，trade_date=时间戳，close=收盘价）
# 按2508赛题文档要求，将真实字段名映射为统一逻辑字段名，便于后续分析
FIELD_MAPPING = {
    "ts_code": "股票代码",  # 2508赛题要求的"股票代码"对应真实字段ts_code
    "trade_date": "时间戳",  # 2508赛题要求的"时间戳"对应真实字段trade_date
    "close": "收盘价"  # 2508赛题要求的"收盘价"对应真实字段close
}
required_real_fields = list(FIELD_MAPPING.keys())  # 需检查的真实字段列表

# 4. 自动识别2508赛题所有CSV文件（遍历文件夹内所有.csv文件）
csv_files = []
for root, dirs, files in os.walk(data_folder):
    for file in files:
        if file.lower().endswith(".csv"):  # 忽略大小写，避免漏检.CSV后缀文件
            csv_files.append(os.path.join(root, file))

# 验证CSV文件数量（确保获取2508赛题数据）
if len(csv_files) == 0:
    raise FileNotFoundError(f"❌ 2508赛题数据文件夹中未找到任何CSV文件，请确认数据路径：{data_folder}")
print(f"✅ 找到{len(csv_files)}个2508赛题CSV文件，开始合并处理")

# 5. 合并所有CSV文件（按2508赛题核心字段筛选，避免无关数据干扰）
df_all = pd.DataFrame()  # 存储合并后的2508赛题核心数据
for csv_path in csv_files:
    # 读取CSV文件（适配2508赛题数据常见编码，避免乱码）
    try:
        df_single = pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        df_single = pd.read_csv(csv_path, encoding="gbk")

    # 检查当前文件是否包含2508赛题所有核心真实字段
    missing_fields = [f for f in required_real_fields if f not in df_single.columns]
    if missing_fields:
        print(f"⚠️ 跳过非2508赛题数据文件：{os.path.basename(csv_path)}（缺失核心字段：{missing_fields}）")
        continue

    # 按2508赛题需求，仅保留核心字段并统一重命名（便于后续板块联动分析）
    df_single_filtered = df_single[required_real_fields].rename(columns=FIELD_MAPPING)
    # 合并到总数据中
    df_all = pd.concat([df_all, df_single_filtered], ignore_index=True)

# 验证合并结果（确保符合2508赛题分析要求）
if df_all.empty:
    raise ValueError("❌ 所有CSV文件均未包含2508赛题核心字段（ts_code/trade_date/close），请确认数据为沪深300成分股数据")
print(f"\n📊 2508赛题CSV数据合并完成！合并后总数据量：{len(df_all)}行 × {len(df_all.columns)}列")
print("合并后数据（前5行）：")
print(df_all.head())

# 6. 2508赛题核心任务1：筛选军工板块股票（按赛题要求分析板块联动）
# 沪深300军工股代码-名称映射（符合2508赛题"军工板块分析"需求，无需额外找数据）
military_stocks = {
    "600038.SH": "中直股份",  # 注意：若ts_code含市场后缀（如.SH/.SZ），需补充完整代码
    "600316.SH": "洪都航空",
    "600893.SH": "航发动力",
    "000738.SZ": "航发控制",
    "002179.SZ": "中航光电",
    "601718.SH": "际华集团",
    "002265.SZ": "西仪股份"
}

# 数据清洗：确保股票代码格式一致（避免因后缀缺失导致匹配失败）
df_all["股票代码"] = df_all["股票代码"].astype(str)
# 筛选2508赛题目标军工板块数据
df_military = df_all[df_all["股票代码"].isin(military_stocks.keys())]
print(f"\n🎯 军工板块数据筛选完成！筛选前总数据量：{len(df_all)}行，筛选后军工股数据量：{len(df_military)}行")

# 7. 构建2508赛题任务1所需的"时间×股票"收盘价矩阵（计算关联系数基础）
# 按时间戳排序（符合2508赛题"时间序列分析"要求）
df_military = df_military.sort_values("时间戳")
# 生成矩阵：行=时间戳（赛题要求的"交易时间段"），列=股票名称，值=收盘价
price_matrix = df_military.pivot_table(
    index="时间戳",
    columns="股票代码",
    values="收盘价"
)
# 用股票名称替换代码（提升结果可读性，符合2508赛题"分析结果展示"需求）
price_matrix.columns = [military_stocks[code] for code in price_matrix.columns]

# 8. 缺失值处理（按2508赛题数据质量要求，避免关联系数计算报错）
price_matrix = price_matrix.ffill()  # 前向填充：用前一日收盘价填补当日缺失值
price_matrix = price_matrix.dropna()  # 删除仍有缺失值的时间行，确保数据完整性
price_matrix = price_matrix.dropna()  # 删除仍有缺失值的时间行（确保数据完整性）

# 9. 保存结果（按2508赛题提交要求，需提供预处理后的数据）
save_path = os.path.join(data_folder, "2508赛题_军工板块收盘价矩阵_预处理后.csv")
price_matrix.to_csv(save_path, encoding="utf-8-sig")  # utf-8-sig支持中文文件名，适配提交需求

# 10. 输出2508赛题数据处理结果摘要（验证是否符合任务1要求）
print(f"\n🎉 2508赛题数据处理全部完成！")
print(f"1. 预处理结果保存路径：{save_path}")
print(f"2. 军工板块分析对象：{len(price_matrix.columns)}只股票（符合2508赛题'板块联动'需求）")
print(f"3. 时间序列范围：{price_matrix.index[0]} ~ {price_matrix.index[-1]}（覆盖赛题要求的交易时间段）")
print(f"4. 收盘价矩阵形状：{price_matrix.shape}（时间条数×股票数量，可直接用于关联系数计算）")
print("\n军工板块收盘价矩阵（前5行预览）：")
print(price_matrix.head())
