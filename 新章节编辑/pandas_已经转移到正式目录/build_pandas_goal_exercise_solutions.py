from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
NB_PATH = ROOT / "pandas_goal_exercise_solutions.ipynb"
_CELL_COUNTER = 0


def next_cell_id():
    global _CELL_COUNTER
    _CELL_COUNTER += 1
    return f"solution-cell-{_CELL_COUNTER:03d}"


def md(source):
    return {
        "cell_type": "markdown",
        "id": next_cell_id(),
        "metadata": {},
        "source": source.splitlines(True),
    }


def code(source):
    return {
        "cell_type": "code",
        "id": next_cell_id(),
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(True),
    }


cells = [
    md("""# Pandas 阶段目标练习答案"""),
    md(
        """## **练习 1.1**：查看财务表结构

读取 `finance_teaching_clean.xlsx`，赋值给变量 `finance_ex1`。显示前 5 行和后 5 行，打印行列数、列名列表和各列数据类型。"""
    ),
    code(
        """import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", "{:.4f}".format)

finance_ex1 = pd.read_excel("data/finance_teaching_clean.xlsx")

display(finance_ex1.head())
display(finance_ex1.tail())
print("行列数：", finance_ex1.shape)
print("列名：", finance_ex1.columns.tolist())
print("数据类型：")
print(finance_ex1.dtypes)"""
    ),
    md(
        """## **练习 1.2**：查看关键财务指标的分布

在 `finance_ex1` 中选择 `营业收入_亿元`、`净利润_亿元`、`总资产_亿元`、`资产负债率` 四列，赋值给变量 `key_finance_ex1`。显示这四列的描述统计，并打印 2020 年样本行数。"""
    ),
    code(
        """key_finance_ex1 = finance_ex1[["营业收入_亿元", "净利润_亿元", "总资产_亿元", "资产负债率"]]

display(key_finance_ex1.describe())
print("2020 年样本行数：", len(finance_ex1[finance_ex1["年份"] == 2020]))"""
    ),
    md(
        """## **练习 2.1**：找出低负债且盈利的公司

暂时删除 `证券代码` 列，结果赋值给变量 `finance_no_code_ex2`。筛选 2020 年同时满足以下条件的公司：`净利润_亿元 > 0`、`资产负债率 < 0.6`。结果赋值给变量 `low_debt_profit_2020`，只保留 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`资产负债率` 四列，并按 `资产负债率` 从低到高排序。打印结果行数，并显示前 5 行。"""
    ),
    code(
        """finance_no_code_ex2 = finance_ex1.drop(columns=["证券代码"]).copy()

low_debt_profit_2020 = (
    finance_no_code_ex2.loc[
        (finance_no_code_ex2["年份"] == 2020)
        & (finance_no_code_ex2["净利润_亿元"] > 0)
        & (finance_no_code_ex2["资产负债率"] < 0.6),
        ["证券简称", "营业收入_亿元", "净利润_亿元", "资产负债率"],
    ]
    .sort_values("资产负债率")
)

print("结果行数：", len(low_debt_profit_2020))
low_debt_profit_2020.head()"""
    ),
    md(
        """## **练习 2.2**：选出收入和资产都较高的公司

在 2020 年公司中，筛选 `营业收入_亿元` 高于当年中位数、并且 `总资产_亿元` 高于当年中位数的公司，赋值给变量 `large_revenue_asset_2020`。显示 `证券简称`、`营业收入_亿元`、`总资产_亿元`、`资产负债率`，并查看前 5 行和后 5 行。"""
    ),
    code(
        """finance_2020_ex2 = finance_no_code_ex2[finance_no_code_ex2["年份"] == 2020]
revenue_median_ex2 = finance_2020_ex2["营业收入_亿元"].median()
asset_median_ex2 = finance_2020_ex2["总资产_亿元"].median()

large_revenue_asset_2020 = finance_2020_ex2.loc[
    (finance_2020_ex2["营业收入_亿元"] > revenue_median_ex2)
    & (finance_2020_ex2["总资产_亿元"] > asset_median_ex2),
    ["证券简称", "营业收入_亿元", "总资产_亿元", "资产负债率"],
].sort_values("营业收入_亿元", ascending=False)

display(large_revenue_asset_2020.head())
display(large_revenue_asset_2020.tail())"""
    ),
    md(
        """## **练习 3.1**：找出收入高但净利率较低的公司

在 `finance_no_code_ex2` 中新增 `净利率 = 净利润_亿元 / 营业收入_亿元`。筛选 2020 年 `营业收入_亿元` 高于当年中位数、同时 `净利率` 低于当年中位数的公司，赋值给变量 `high_revenue_low_margin`。这个结果代表“规模不小、利润率相对偏低”的公司。再为 2020 年公司按营业收入生成 `收入排名`。显示 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`净利率`、`收入排名`，并查看前 5 行和后 5 行。"""
    ),
    code(
        """finance_no_code_ex2["净利率"] = (
    finance_no_code_ex2["净利润_亿元"] / finance_no_code_ex2["营业收入_亿元"]
)

finance_2020_ex3 = finance_no_code_ex2[finance_no_code_ex2["年份"] == 2020].copy()
finance_2020_ex3["收入排名"] = (
    finance_2020_ex3["营业收入_亿元"]
    .rank(ascending=False, method="min")
    .astype(int)
)
revenue_median_ex3 = finance_2020_ex3["营业收入_亿元"].median()
margin_median_ex3 = finance_2020_ex3["净利率"].median()

high_revenue_low_margin = finance_2020_ex3.loc[
    (finance_2020_ex3["营业收入_亿元"] > revenue_median_ex3)
    & (finance_2020_ex3["净利率"] < margin_median_ex3),
    ["证券简称", "营业收入_亿元", "净利润_亿元", "净利率", "收入排名"],
].sort_values("营业收入_亿元", ascending=False)

display(high_revenue_low_margin.head())
display(high_revenue_low_margin.tail())"""
    ),
    md(
        """## **练习 3.2**：给公司打上资产规模标签

用 `pd.cut()` 根据 `总资产_亿元` 生成 `资产规模`：`0-100` 为“小”，`100-1000` 为“中”，`1000` 以上为“大”。统计 2020 年不同 `资产规模` 的公司数量，赋值给变量 `size_counts_2020`。要求输出计数结果。"""
    ),
    code(
        """finance_no_code_ex2["资产规模"] = pd.cut(
    finance_no_code_ex2["总资产_亿元"],
    bins=[0, 100, 1000, np.inf],
    labels=["小", "中", "大"],
)

size_counts_2020 = finance_no_code_ex2.loc[
    finance_no_code_ex2["年份"] == 2020,
    "资产规模",
].value_counts()
size_counts_2020"""
    ),
    md(
        """## **练习 3.3**：按条件生成负债水平

在 `finance_no_code_ex2` 中新增 `负债水平`，先全部赋值为“正常”，再用 `.loc` 把 `资产负债率 >= 0.7` 的行改为“较高”。显示 `证券简称`、`年份`、`资产负债率`、`负债水平` 四列的前 8 行，并统计不同 `负债水平` 的数量。"""
    ),
    code(
        """finance_no_code_ex2["负债水平"] = "正常"
finance_no_code_ex2.loc[finance_no_code_ex2["资产负债率"] >= 0.7, "负债水平"] = "较高"

display(finance_no_code_ex2[["证券简称", "年份", "资产负债率", "负债水平"]].head(8))
finance_no_code_ex2["负债水平"].value_counts()"""
    ),
    md(
        """## **练习 4.1**：清洗一张带问题的小表

重新读取带代码的财务表，读取时把 `证券代码` 处理成 6 位字符串。取前 12 行，复制为 `dirty_ex1`。为练习清洗操作，加入以下情况：把第 2 行 `营业收入_亿元` 改成缺失值；把第 3 行 `净利润_亿元` 改成 `"--"`；把第 4 行 `总资产_亿元` 改成带逗号的字符串；再重复添加第 1 行。完成缺失值检查、重复行检查、去重、数值转换。最终结果赋值给变量 `dirty_ex1_clean`，要求 `总资产_亿元` 和 `净利润_亿元` 都是数值列。"""
    ),
    code(
        """def read_code(x):
    return str(x).strip().zfill(6)

finance_code = pd.read_excel(
    "data/finance_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)
finance_code["净利率"] = finance_code["净利润_亿元"] / finance_code["营业收入_亿元"]

dirty_ex1 = finance_code.head(12).copy()
dirty_ex1[["总资产_亿元", "净利润_亿元"]] = dirty_ex1[["总资产_亿元", "净利润_亿元"]].astype("object")

dirty_ex1.loc[1, "营业收入_亿元"] = np.nan
dirty_ex1.loc[2, "净利润_亿元"] = "--"
dirty_ex1.loc[3, "总资产_亿元"] = "15,285.79"
dirty_ex1 = pd.concat([dirty_ex1, dirty_ex1.iloc[[0]]], ignore_index=True)

print("缺失值：")
display(dirty_ex1.isna().sum())
print("重复行数量：", dirty_ex1.duplicated().sum())

dirty_ex1_clean = dirty_ex1.drop_duplicates().copy()
dirty_ex1_clean["总资产_亿元"] = (
    dirty_ex1_clean["总资产_亿元"]
    .astype(str)
    .str.replace(",", "", regex=False)
)
dirty_ex1_clean["总资产_亿元"] = pd.to_numeric(dirty_ex1_clean["总资产_亿元"], errors="coerce")
dirty_ex1_clean["净利润_亿元"] = dirty_ex1_clean["净利润_亿元"].mask(
    dirty_ex1_clean["净利润_亿元"] == "--",
    np.nan,
)
dirty_ex1_clean["净利润_亿元"] = pd.to_numeric(dirty_ex1_clean["净利润_亿元"], errors="coerce")

display(dirty_ex1_clean[["总资产_亿元", "净利润_亿元"]].dtypes)
dirty_ex1_clean.head()"""
    ),
    md(
        """## **练习 4.2**：替换特殊值并填补缺失

在 `dirty_ex1_clean` 中，把 `净利润_亿元` 的缺失值填为 0，把 `营业收入_亿元` 的缺失值填为该列中位数。新增 `是否盈利` 列：`净利润_亿元 > 0` 为 `True`，否则为 `False`。输出每列缺失值数量，并显示 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`是否盈利`。"""
    ),
    code(
        """dirty_ex1_clean["净利润_亿元"] = dirty_ex1_clean["净利润_亿元"].fillna(0)
dirty_ex1_clean["营业收入_亿元"] = dirty_ex1_clean["营业收入_亿元"].fillna(
    dirty_ex1_clean["营业收入_亿元"].median()
)
dirty_ex1_clean["是否盈利"] = dirty_ex1_clean["净利润_亿元"] > 0

display(dirty_ex1_clean.isna().sum())
dirty_ex1_clean[["证券简称", "营业收入_亿元", "净利润_亿元", "是否盈利"]].head()"""
    ),
    md(
        """## **练习 4.3**：用映射生成风险标签

根据 `资产负债率` 新增 `负债水平`：大于等于 0.7 为“较高”，否则为“正常”。再用 `map()` 把“较高”映射为“需关注”，把“正常”映射为“低风险”，生成 `负债风险`。统计不同 `负债风险` 的数量。"""
    ),
    code(
        """dirty_ex1_clean["负债水平"] = np.where(dirty_ex1_clean["资产负债率"] >= 0.7, "较高", "正常")
debt_risk_map = {"较高": "需关注", "正常": "低风险"}
dirty_ex1_clean["负债风险"] = dirty_ex1_clean["负债水平"].map(debt_risk_map)

dirty_ex1_clean["负债风险"].value_counts()"""
    ),
    md(
        """## **练习 5.1**：处理证券代码并合并行业信息

重新读取 `finance_teaching_clean.xlsx` 和 `company_profile_teaching_clean.xlsx`。读取时把 `证券代码` 处理成 6 位字符串。筛选 2020 年财务数据，与公司信息表按 `证券代码` 合并，赋值给变量 `finance_company_2020`。检查合并前后行数是否一致，并检查 `行业名称` 是否有缺失。"""
    ),
    code(
        """company_code = pd.read_excel(
    "data/company_profile_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)

company_code["上市日期"] = pd.to_datetime(company_code["上市日期"])
company_code["上市年份"] = company_code["上市日期"].dt.year

finance_2020_code = finance_code[finance_code["年份"] == 2020].copy()
finance_company_2020 = finance_2020_code.merge(company_code, on=["证券代码", "证券简称"], how="left")

print("合并前行数：", len(finance_2020_code))
print("合并后行数：", len(finance_company_2020))
print("行业缺失数量：", finance_company_2020["行业名称"].isna().sum())
finance_company_2020.head()"""
    ),
    md(
        """## **练习 5.2**：找出制造业中收入最高的公司

在 `finance_company_2020` 中筛选 `行业名称` 包含“制造”的公司，赋值给变量 `manufacturing_2020`。按 `营业收入_亿元` 从高到低排序，显示前 8 行。结果应包含 `证券代码`、`证券简称`、`行业名称`、`省份`、`营业收入_亿元`、`净利润_亿元`。"""
    ),
    code(
        """manufacturing_2020 = (
    finance_company_2020.loc[
        finance_company_2020["行业名称"].str.contains("制造", na=False),
        ["证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利润_亿元"],
    ]
    .sort_values("营业收入_亿元", ascending=False)
)

manufacturing_2020.head(8)"""
    ),
    md(
        """## **练习 5.3**：比较早上市公司和较晚上市公司

把公司表中的 `上市日期` 转为日期格式，并生成 `上市年份`。在 `finance_company_2020` 中新增 `上市阶段`：`上市年份 < 2000` 标记为“较早上市”，否则标记为“较晚上市”。分别计算两组公司的平均 `营业收入_亿元` 和平均 `净利率`。"""
    ),
    code(
        """finance_company_2020["上市阶段"] = np.where(
    finance_company_2020["上市年份"] < 2000,
    "较早上市",
    "较晚上市",
)

finance_company_2020.groupby("上市阶段").agg(
    平均营业收入_亿元=("营业收入_亿元", "mean"),
    平均净利率=("净利率", "mean"),
)"""
    ),
    md(
        """## **练习 6.1**：行业年度摘要表

把财务表和公司信息表合并为 `analysis_ex6`。按 `行业名称` 和 `年份` 分组，计算 `公司数`、`营业收入合计_亿元`、`平均净利率`、`平均资产负债率`，赋值给变量 `industry_year_summary`。显示前 12 行。"""
    ),
    code(
        """analysis_ex6 = finance_code.merge(
    company_code[["证券代码", "行业名称", "省份"]],
    on="证券代码",
    how="left",
)

industry_year_summary = (
    analysis_ex6
    .groupby(["行业名称", "年份"])
    .agg(
        公司数=("证券简称", "nunique"),
        营业收入合计_亿元=("营业收入_亿元", "sum"),
        平均净利率=("净利率", "mean"),
        平均资产负债率=("资产负债率", "mean"),
    )
    .reset_index()
)

industry_year_summary.head(12)"""
    ),
    md(
        """## **练习 6.2**：每个行业找两家公司

在 2020 年数据中，按 `行业名称` 分组，找出每个行业 `营业收入_亿元` 最高的 2 家公司，赋值给变量 `top2_revenue_by_industry`。结果只保留 `行业名称`、`证券代码`、`证券简称`、`营业收入_亿元`、`净利率`，并按行业名称和营业收入排序。"""
    ),
    code(
        """top2_revenue_by_industry = (
    analysis_ex6[analysis_ex6["年份"] == 2020]
    .sort_values(["行业名称", "营业收入_亿元"], ascending=[True, False])
    .groupby("行业名称")
    .head(2)
    .loc[:, ["行业名称", "证券代码", "证券简称", "营业收入_亿元", "净利率"]]
)

top2_revenue_by_industry"""
    ),
    md(
        """## **练习 6.3**：计算行业内部收入差距

自定义函数 `value_range(x)`，返回 `x.max() - x.min()`。按 `行业名称` 分组，计算 2020 年各行业营业收入的均值和收入差距，赋值给变量 `industry_gap_2020`。按收入差距从高到低排序。"""
    ),
    code(
        """def value_range(x):
    return x.max() - x.min()

industry_gap_2020 = (
    analysis_ex6[analysis_ex6["年份"] == 2020]
    .groupby("行业名称")
    .agg(
        收入均值=("营业收入_亿元", "mean"),
        收入差距=("营业收入_亿元", value_range),
    )
    .sort_values("收入差距", ascending=False)
)

industry_gap_2020"""
    ),
    md(
        """## **练习 6.4**：判断公司是否高于行业平均

在 2020 年数据中，用 `groupby()` 和 `transform()` 计算每家公司所在行业的平均营业收入，生成 `行业平均收入_亿元`。再生成 `高于行业平均`，表示该公司营业收入是否高于所在行业平均值。显示 `行业名称`、`证券简称`、`营业收入_亿元`、`行业平均收入_亿元`、`高于行业平均`，并查看前 10 行。"""
    ),
    code(
        """industry_compare_ex6 = analysis_ex6[analysis_ex6["年份"] == 2020].copy()
industry_compare_ex6["行业平均收入_亿元"] = (
    industry_compare_ex6
    .groupby("行业名称")["营业收入_亿元"]
    .transform("mean")
)
industry_compare_ex6["高于行业平均"] = (
    industry_compare_ex6["营业收入_亿元"] > industry_compare_ex6["行业平均收入_亿元"]
)

industry_compare_ex6[[
    "行业名称", "证券简称", "营业收入_亿元", "行业平均收入_亿元", "高于行业平均"
]].head(10)"""
    ),
    md(
        """## **练习 7.1**：构造公司收入宽表

用 `pivot_table()` 把 `analysis_ex6` 整理为每家公司一行、年份为列、值为 `营业收入_亿元` 的宽表，赋值给变量 `revenue_wide_ex7`。计算 `收入增长率_2018_2020 = 2020 / 2018 - 1`，按增长率从高到低排序，显示前 10 行。"""
    ),
    code(
        """revenue_wide_ex7 = analysis_ex6.pivot_table(
    index=["证券代码", "证券简称", "行业名称"],
    columns="年份",
    values="营业收入_亿元",
)
revenue_wide_ex7["收入增长率_2018_2020"] = revenue_wide_ex7[2020] / revenue_wide_ex7[2018] - 1

revenue_wide_ex7.sort_values("收入增长率_2018_2020", ascending=False).head(10)"""
    ),
    md(
        """## **练习 7.2**：构造公司综合摘要表

基于 `analysis_ex6` 构造 `company_profile_summary`，每家公司一行，至少包含：`证券代码`、`证券简称`、`行业名称`、`省份`、`2018` 年营业收入、`2020` 年营业收入、`收入增长率_2018_2020`、`2020` 年资产负债率。按 `收入增长率_2018_2020` 从高到低排序，显示前 10 行。"""
    ),
    code(
        """revenue_summary = analysis_ex6.pivot_table(
    index=["证券代码", "证券简称", "行业名称", "省份"],
    columns="年份",
    values="营业收入_亿元",
).reset_index()
revenue_summary["收入增长率_2018_2020"] = revenue_summary[2020] / revenue_summary[2018] - 1

debt_2020 = analysis_ex6.loc[
    analysis_ex6["年份"] == 2020,
    ["证券代码", "资产负债率"],
].rename(columns={"资产负债率": "2020年资产负债率"})

company_profile_summary = revenue_summary.merge(debt_2020, on="证券代码", how="left")
company_profile_summary = company_profile_summary.sort_values("收入增长率_2018_2020", ascending=False)

company_profile_summary.head(10)"""
    ),
    md(
        """## **练习 7.3**：核对公司摘要表

检查 `company_profile_summary` 的行数是否等于公司数量。再按 `行业名称` 统计公司数量，并显示统计结果。最后显示 `company_profile_summary` 的前 5 行和后 5 行。"""
    ),
    code(
        """print("摘要表行数：", len(company_profile_summary))
print("公司数量：", analysis_ex6["证券代码"].nunique())

display(company_profile_summary["行业名称"].value_counts())
display(company_profile_summary.head())
display(company_profile_summary.tail())"""
    ),
    md(
        """## **练习 8.1**：构造价格序列并计算收益率

构造 2021 年 1 月到 2021 年 6 月的工作日日期。使用随机数生成一列日收益率 `return`，从初始价格 100 出发构造价格 `price`。把结果赋值给以日期为索引的变量 `price_df`，并新增 `lag_price`、`diff`、`pct_return` 三列。显示前 8 行。"""
    ),
    code(
        """dates_ex8 = pd.date_range("2021-01-01", "2021-06-30", freq="B")
rng = np.random.default_rng(2021)

price_df = pd.DataFrame(
    {"return": rng.normal(0.0004, 0.012, len(dates_ex8))},
    index=dates_ex8,
)
price_df["price"] = 100 * (1 + price_df["return"]).cumprod()
price_df["lag_price"] = price_df["price"].shift(1)
price_df["diff"] = price_df["price"].diff()
price_df["pct_return"] = price_df["price"].pct_change()

price_df.head(8)"""
    ),
    md(
        """## **练习 8.2**：按月份观察价格变化

从 `price_df` 中筛选 2021 年 3 月的数据，赋值给变量 `march_price`。显示前 5 行和后 5 行。然后用 `resample("ME").last()` 得到月末价格，赋值给变量 `month_end_price_ex8`。"""
    ),
    code(
        """march_price = price_df.loc["2021-03"]
display(march_price.head())
display(march_price.tail())

month_end_price_ex8 = price_df["price"].resample("ME").last()
month_end_price_ex8"""
    ),
    md(
        """## **练习 8.3**：从月末价格计算月收益

基于 `month_end_price_ex8` 计算月收益率，赋值给变量 `month_return_ex8`。找出月收益率最高的月份和最低的月份，并打印对应月份和收益率。"""
    ),
    code(
        """month_return_ex8 = month_end_price_ex8.pct_change().dropna()

best_month = month_return_ex8.idxmax()
worst_month = month_return_ex8.idxmin()

print("月收益率最高：", best_month.strftime("%Y-%m"), month_return_ex8.loc[best_month])
print("月收益率最低：", worst_month.strftime("%Y-%m"), month_return_ex8.loc[worst_month])

month_return_ex8"""
    ),
]


nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(NB_PATH)
