from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
NB_PATH = ROOT / "pandas_阶段目标完整版.ipynb"
_CELL_COUNTER = 0


def next_cell_id():
    global _CELL_COUNTER
    _CELL_COUNTER += 1
    return f"cell-{_CELL_COUNTER:03d}"


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
    md(
        """# Pandas：从公司财务表到可分析数据

本章用阶段目标组织 pandas 的主要知识。我们不按函数列表讲，而是每一阶段先说明要得到什么结果，再引出需要的操作。

本章使用两张教学表：

- `finance_teaching_clean.xlsx`：公司年度财务数据。
- `company_profile_teaching_clean.xlsx`：公司基本信息。

第一阶段先暂时放下 `证券代码`，集中学习表格基础操作。第二阶段开始正式处理证券代码，并把两张表合并。"""
    ),
    md(
        """## 本章知识点安排

**阶段 1：从一张财务表得到 2020 年公司表现排名**

读取 Excel；查看 `head()`、`tail()`、`shape`、`columns`、`dtypes`、`info()`、`describe()`；理解 `Series` 和 `DataFrame`；选列；`loc` / `iloc`；条件筛选和复合条件；`query()`；列运算；`pd.cut()`；按条件赋值；排序；简单统计。

**阶段 2：处理证券代码，并合并公司信息**

编号列的字符串处理；`converters`；`str.zfill()`；`str.strip()`；`str.contains()`；`pd.to_datetime()`；`.dt.year`、`.dt.month`、`.dt.quarter`；`value_counts()`；`rename()`；`merge()`；`left_on` / `right_on`；合并后检查。

**阶段 3：处理真实数据中的常见小问题**

构造工作副本；检查缺失值；检查重复行；`drop_duplicates()`；清理特殊文本；`pd.to_numeric()`；`dropna()`；`fillna()`；`replace()`；`map()`。

**阶段 4：按行业和年份做汇总分析**

`groupby()`；多指标 `agg()`；自定义聚合函数；按多列分组；分组后排序；每组取前几名；分组循环；`concat()`。

**阶段 5：重建更适合分析的数据表**

`pivot_table()`；长表和宽表；构造公司层面摘要表；`set_index()`；`reset_index()`；构造 `Series` / `DataFrame`；`to_excel()`；`to_csv()`；`read_csv()`。

**阶段 6：时间序列入门**

`date_range()`；日期索引；按日期切片；`shift()`；`diff()`；`pct_change()`；`cumprod()`；`resample()`。"""
    ),
    md(
        """## 阶段 1：从一张财务表得到 2020 年公司表现排名

目标：读入年度财务表，选出 2020 年公司，计算几个财务指标，并做出一张公司排名表。"""
    ),
    code(
        """import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", "{:.4f}".format)

finance_raw = pd.read_excel("data/finance_teaching_clean.xlsx")
finance_raw.head()"""
    ),
    md(
        """先查看数据规模、字段和类型。真实工作中，不要急着计算，先确认表长什么样。"""
    ),
    code(
        """print("行列数：", finance_raw.shape)
print("列名：", finance_raw.columns.tolist())
print("数据类型：")
print(finance_raw.dtypes)

finance_raw.info()"""
    ),
    code(
        """finance_raw.tail()"""
    ),
    code(
        """finance_raw.describe()"""
    ),
    md(
        """`证券代码` 是编号，不是这一阶段要计算的财务指标。先把它临时放到一边。这里使用 `.copy()` 明确生成工作副本。"""
    ),
    code(
        """finance = finance_raw.drop(columns=["证券代码"]).copy()
finance.head()"""
    ),
    md(
        """一列数据是 `Series`，多列数据是 `DataFrame`。这是 pandas 最基本的两个对象。"""
    ),
    code(
        """one_col = finance["营业收入_亿元"]
some_cols = finance[["证券简称", "年份", "营业收入_亿元"]]

print(type(one_col))
print(type(some_cols))"""
    ),
    md(
        """选择列时，单个列名返回 `Series`；列名列表返回 `DataFrame`。"""
    ),
    code(
        """finance[["证券简称", "年份", "营业收入_亿元", "净利润_亿元"]].head()"""
    ),
    md(
        """`.iloc` 按位置选择，适合快速查看“第几行、第几列”。"""
    ),
    code(
        """finance.iloc[:5, :4]"""
    ),
    md(
        """`.loc` 按标签选择，常和条件一起使用。"""
    ),
    code(
        """finance.loc[
    finance["年份"] == 2020,
    ["证券简称", "营业收入_亿元", "净利润_亿元", "资产负债率"],
].head()"""
    ),
    md(
        """复合条件要用 `&`、`|`、`~`，每个条件外面加括号。"""
    ),
    code(
        """good_2020 = finance.loc[
    (finance["年份"] == 2020)
    & (finance["净利润_亿元"] > 0)
    & (finance["营业收入_亿元"].notna())
    & (finance["资产负债率"] < 0.7),
    ["证券简称", "营业收入_亿元", "净利润_亿元", "资产负债率"],
]

good_2020.head()"""
    ),
    md(
        """筛选之后最好看一眼结果。`head()` 看前几行，`tail()` 看后几行，能帮助我们发现结果是否大致符合预期。"""
    ),
    code(
        """print("筛选结果行数：", len(good_2020))
display(good_2020.head())
display(good_2020.tail())"""
    ),
    md(
        """`query()` 可以把筛选条件写成字符串。它不是必须用，但在条件较短时很方便。"""
    ),
    code(
        """finance.query("年份 == 2020 and 净利润_亿元 > 0").head()"""
    ),
    md(
        """用已有列生成新列，是 pandas 中最常见的操作之一。"""
    ),
    code(
        """finance["净利率"] = finance["净利润_亿元"] / finance["营业收入_亿元"]
finance["资产收益率"] = finance["净利润_亿元"] / finance["总资产_亿元"]
finance["是否盈利"] = finance["净利润_亿元"] > 0
finance["资产规模"] = pd.cut(
    finance["总资产_亿元"],
    bins=[0, 100, 1000, np.inf],
    labels=["小", "中", "大"],
)

finance[["证券简称", "年份", "净利率", "资产收益率", "是否盈利", "资产规模"]].head()"""
    ),
    md(
        """也可以按条件给新列赋值。"""
    ),
    code(
        """finance["负债水平"] = "正常"
finance.loc[finance["资产负债率"] >= 0.7, "负债水平"] = "较高"

finance[["证券简称", "年份", "资产负债率", "负债水平"]].head()"""
    ),
    md(
        """按一个或多个指标排序，得到阶段性结果：2020 年公司表现排名。"""
    ),
    code(
        """finance_2020_rank = (
    finance[finance["年份"] == 2020]
    .sort_values(["营业收入_亿元", "净利率"], ascending=[False, False])
)

finance_2020_rank[[
    "证券简称", "营业收入_亿元", "净利润_亿元", "净利率", "资产收益率", "资产负债率", "负债水平"
]].head(10)"""
    ),
    md(
        """排序后也要看一眼尾部。前几行告诉我们谁排在前面，后几行能帮助我们理解这个排名的另一端。"""
    ),
    code(
        """finance_2020_rank[[
    "证券简称", "营业收入_亿元", "净利润_亿元", "净利率", "资产负债率"
]].tail(5)"""
    ),
    md(
        """简单统计可以快速了解样本。"""
    ),
    code(
        """finance_2020 = finance[finance["年份"] == 2020]

print("公司数量：", finance_2020["证券简称"].nunique())
print("营业收入平均值：", finance_2020["营业收入_亿元"].mean())
print("营业收入最大值：", finance_2020["营业收入_亿元"].max())

finance_2020[["营业收入_亿元", "净利润_亿元", "资产负债率", "净利率"]].describe()"""
    ),
    md(
        """如果只是为了展示，也可以重命名结果表中的列。"""
    ),
    code(
        """rank_display = finance_2020_rank.rename(
    columns={
        "营业收入_亿元": "营业收入",
        "净利润_亿元": "净利润",
    }
)

rank_display[["证券简称", "营业收入", "净利润", "净利率"]].head()"""
    ),
    md(
        """阶段 1 小结：我们得到了 `finance_2020_rank`。这一阶段带出了读取、查看、选行选列、`loc`、`iloc`、条件筛选、`query`、列运算、按条件赋值、排序和简单统计。"""
    ),
    md(
        """## 阶段 2：处理证券代码，并合并公司信息

目标：把财务表和公司信息表合并，让财务指标带上行业、省份、城市、上市日期等背景信息。"""
    ),
    md(
        """证券代码是编号，不能当作普通数字。读取时把它转成字符串，并补齐到 6 位。"""
    ),
    code(
        """def read_code(x):
    return str(x).strip().zfill(6)

finance_code = pd.read_excel(
    "data/finance_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)

company = pd.read_excel(
    "data/company_profile_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)

finance_code.head()"""
    ),
    md(
        """公司信息表中有文本列和日期列，可以先做几个轻量处理。"""
    ),
    code(
        """company = company.copy()
company["证券简称"] = company["证券简称"].str.strip()
company["行业名称"] = company["行业名称"].str.strip()
company["上市日期"] = pd.to_datetime(company["上市日期"])
company["上市年份"] = company["上市日期"].dt.year
company["是否ST"] = company["证券简称"].str.contains("ST", na=False)

company.head()"""
    ),
    code(
        """company["行业名称"].value_counts()"""
    ),
    md(
        """字符串方法常用于筛选文本。比如找出行业名称中包含“制造”的公司，或找出简称中包含 `ST` 的公司。"""
    ),
    code(
        """manufacturing = company.loc[
    company["行业名称"].str.contains("制造", na=False),
    ["证券代码", "证券简称", "行业名称", "省份"],
]

print("制造业相关公司数量：", len(manufacturing))
display(manufacturing.head())
display(manufacturing.tail())"""
    ),
    code(
        """st_companies = company.loc[
    company["证券简称"].str.contains("ST", na=False),
    ["证券代码", "证券简称", "行业名称", "上市年份"],
]

st_companies"""
    ),
    md(
        """日期方法常用于按时间筛选。比如根据上市日期提取年份、月份、季度，再筛选较早上市的公司。"""
    ),
    code(
        """company["上市月份"] = company["上市日期"].dt.month
company["上市季度"] = company["上市日期"].dt.quarter

old_listed = company.loc[
    company["上市年份"] < 2000,
    ["证券代码", "证券简称", "行业名称", "上市日期", "上市年份", "上市月份", "上市季度"],
].sort_values("上市日期")

display(old_listed.head())
display(old_listed.tail())"""
    ),
    md(
        """重新在带证券代码的财务表中生成阶段 1 的指标。"""
    ),
    code(
        """finance_code["净利率"] = finance_code["净利润_亿元"] / finance_code["营业收入_亿元"]
finance_code["资产收益率"] = finance_code["净利润_亿元"] / finance_code["总资产_亿元"]
finance_code["是否盈利"] = finance_code["净利润_亿元"] > 0
finance_code["负债水平"] = np.where(finance_code["资产负债率"] >= 0.7, "较高", "正常")

finance_2020_rank_code = (
    finance_code[finance_code["年份"] == 2020]
    .sort_values("营业收入_亿元", ascending=False)
)

finance_2020_rank_code.head()"""
    ),
    md(
        """合并前先把右表压缩成需要的列。"""
    ),
    code(
        """company_small = company[
    ["证券代码", "行业名称", "省份", "城市", "上市市场", "上市日期", "上市年份", "是否ST"]
]

company_small.head()"""
    ),
    md(
        """用 `merge()` 按证券代码合并。合并后检查行数和关键列缺失，确认没有明显匹配失败。"""
    ),
    code(
        """rank_with_info = finance_2020_rank_code.merge(company_small, on="证券代码", how="left")

print("合并前行数：", len(finance_2020_rank_code))
print("合并后行数：", len(rank_with_info))
print("行业缺失数量：", rank_with_info["行业名称"].isna().sum())

rank_with_info[[
    "证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利率", "上市年份"
]].head(10)"""
    ),
    code(
        """rank_with_info[[
    "证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利率", "上市年份"
]].tail(5)"""
    ),
    md(
        """如果两个表的连接键列名不同，可以用 `left_on` 和 `right_on`。下面只是演示。"""
    ),
    code(
        """company_key_demo = company_small.rename(columns={"证券代码": "公司代码"})

demo_merge = finance_2020_rank_code.merge(
    company_key_demo,
    left_on="证券代码",
    right_on="公司代码",
    how="left",
)

demo_merge[["证券代码", "公司代码", "行业名称"]].head()"""
    ),
    md(
        """阶段 2 小结：我们得到了 `rank_with_info`。这一阶段带出了证券代码处理、字符串方法、日期方法、`value_counts()`、`merge()` 和合并检查。"""
    ),
    md(
        """## 阶段 3：处理真实数据中的常见小问题

目标：理解现实数据为什么不能直接计算，并掌握最常见的检查和处理方法。

为了集中演示，这里从干净财务表复制出一份带问题的小表。"""
    ),
    code(
        """dirty = finance_code.head(12).copy()
dirty[["总资产_亿元", "净利润_亿元"]] = dirty[["总资产_亿元", "净利润_亿元"]].astype("object")

dirty.loc[1, "营业收入_亿元"] = np.nan
dirty.loc[2, "净利润_亿元"] = "--"
dirty.loc[3, "总资产_亿元"] = "15,285.79"
dirty.loc[4, "负债水平"] = ""
dirty = pd.concat([dirty, dirty.iloc[[0]]], ignore_index=True)

dirty"""
    ),
    md(
        """先检查缺失值和重复行。"""
    ),
    code(
        """print("缺失值：")
print(dirty.isna().sum())

print("重复行数量：", dirty.duplicated().sum())"""
    ),
    md(
        """删除重复行。"""
    ),
    code(
        """dirty = dirty.drop_duplicates()
dirty = dirty.copy()
print("删除重复后行数：", len(dirty))"""
    ),
    md(
        """把特殊文本和带逗号的数字清理成真正的数值。"""
    ),
    code(
        """dirty["总资产_亿元"] = (
    dirty["总资产_亿元"]
    .astype(str)
    .str.replace(",", "", regex=False)
)
dirty["总资产_亿元"] = pd.to_numeric(dirty["总资产_亿元"], errors="coerce")

dirty["净利润_亿元"] = dirty["净利润_亿元"].mask(dirty["净利润_亿元"] == "--", np.nan)
dirty["净利润_亿元"] = pd.to_numeric(dirty["净利润_亿元"], errors="coerce")

dirty[["总资产_亿元", "营业收入_亿元", "净利润_亿元"]].head()"""
    ),
    md(
        """缺失值可以删除，也可以填补。怎么处理取决于分析目的。这里演示两种常见做法。"""
    ),
    code(
        """drop_missing = dirty.dropna(subset=["营业收入_亿元", "净利润_亿元"])

fill_missing = dirty.copy()
fill_missing["营业收入_亿元"] = fill_missing["营业收入_亿元"].fillna(
    fill_missing["营业收入_亿元"].median()
)
fill_missing["净利润_亿元"] = fill_missing["净利润_亿元"].fillna(0)
fill_missing["负债水平"] = fill_missing["负债水平"].replace({"": "未知"})

fill_missing.isna().sum()"""
    ),
    md(
        """`map()` 适合把一组取值映射成另一组取值。"""
    ),
    code(
        """debt_map = {"正常": "低风险", "较高": "需关注", "未知": "待确认"}
fill_missing["负债风险"] = fill_missing["负债水平"].map(debt_map)

fill_missing[["证券简称", "负债水平", "负债风险"]].head()"""
    ),
    md(
        """`replace()` 适合替换特殊值。现实数据里常见 `999`、`-1`、`--` 等特殊编码。"""
    ),
    code(
        """special = pd.Series([1, 2, 999, -1, 5], name="原始值")
special.replace({999: np.nan, -1: 0})"""
    ),
    md(
        """阶段 3 小结：这一阶段带出了 `isna()`、`dropna()`、`fillna()`、`duplicated()`、`drop_duplicates()`、`replace()`、`pd.to_numeric()`、`map()` 和清洗副本的做法。"""
    ),
    md(
        """## 阶段 4：按行业和年份做汇总分析

目标：从公司层面的明细表，上升到行业和年份层面的比较。"""
    ),
    code(
        """analysis_df = finance_code.merge(company_small, on="证券代码", how="left")
analysis_df.head()"""
    ),
    md(
        """先做一个普通的行业汇总。"""
    ),
    code(
        """industry_2020 = (
    analysis_df[analysis_df["年份"] == 2020]
    .groupby("行业名称")
    .agg(
        公司数=("证券简称", "nunique"),
        平均营业收入_亿元=("营业收入_亿元", "mean"),
        营业收入合计_亿元=("营业收入_亿元", "sum"),
        平均净利率=("净利率", "mean"),
        平均资产负债率=("资产负债率", "mean"),
    )
    .sort_values("营业收入合计_亿元", ascending=False)
)

industry_2020"""
    ),
    md(
        """也可以同时按行业和年份分组。"""
    ),
    code(
        """industry_year = (
    analysis_df
    .groupby(["行业名称", "年份"])
    .agg(
        公司数=("证券简称", "nunique"),
        平均营业收入_亿元=("营业收入_亿元", "mean"),
        平均净利率=("净利率", "mean"),
    )
    .reset_index()
)

industry_year.head(12)"""
    ),
    md(
        """`agg()` 可以使用自定义函数。"""
    ),
    code(
        """def value_range(x):
    return x.max() - x.min()

analysis_df.groupby("行业名称").agg(
    收入均值=("营业收入_亿元", "mean"),
    收入差距=("营业收入_亿元", value_range),
).head()"""
    ),
    md(
        """每组取前几名：先排序，再分组，再 `head()`。"""
    ),
    code(
        """top2_by_industry = (
    analysis_df[analysis_df["年份"] == 2020]
    .sort_values(["行业名称", "营业收入_亿元"], ascending=[True, False])
    .groupby("行业名称")
    .head(2)
)

top2_by_industry[["行业名称", "证券简称", "营业收入_亿元"]].head(14)"""
    ),
    md(
        """分组循环适合处理每组内部较复杂的逻辑。循环得到的结果可以用 `concat()` 合并回来。"""
    ),
    code(
        """top_list = []

for industry, group in analysis_df[analysis_df["年份"] == 2020].groupby("行业名称"):
    top_company = group.sort_values("营业收入_亿元", ascending=False).head(1)
    top_list.append(top_company)

industry_top_company = pd.concat(top_list)[
    ["行业名称", "证券代码", "证券简称", "营业收入_亿元", "净利率"]
].sort_values("营业收入_亿元", ascending=False)

industry_top_company"""
    ),
    md(
        """阶段 4 小结：这一阶段带出了 `groupby()`、多指标 `agg()`、自定义聚合、每组取前几名、分组循环和 `concat()`。"""
    ),
    md(
        """## 阶段 5：重建更适合分析的数据表

目标：把明细表改造成更适合回答问题的表。原始数据是什么形状，不代表分析时就应该保持什么形状。"""
    ),
    md(
        """先把公司年度营业收入整理成宽表，每家公司一行，每一年一列。"""
    ),
    code(
        """revenue_wide = analysis_df.pivot_table(
    index=["证券代码", "证券简称", "行业名称"],
    columns="年份",
    values="营业收入_亿元",
)

revenue_wide.head()"""
    ),
    code(
        """revenue_wide["收入增长率_2018_2020"] = revenue_wide[2020] / revenue_wide[2018] - 1

company_summary = (
    revenue_wide
    .reset_index()
    .sort_values("收入增长率_2018_2020", ascending=False)
)

company_summary.head(10)"""
    ),
    md(
        """`set_index()` 和 `reset_index()` 常用于在“普通列”和“索引”之间切换。"""
    ),
    code(
        """indexed = company_summary.set_index("证券代码")
indexed.head()"""
    ),
    code(
        """indexed.reset_index().head()"""
    ),
    md(
        """也可以自己构造小的 `Series` 和 `DataFrame`，理解 pandas 对象如何组成表格。"""
    ),
    code(
        """s = pd.Series([10, 20, 30], index=["A", "B", "C"], name="得分")
demo_df = pd.DataFrame({
    "公司": ["甲", "乙", "丙"],
    "收入": [100, 120, 80],
})

print(s)
demo_df"""
    ),
    md(
        """保存结果。Excel 适合给人看，CSV 更通用。一般保存普通表格时使用 `index=False`。"""
    ),
    code(
        """finance_2020_rank_code.to_excel("data/finance_2020_rank_full.xlsx", index=False)
industry_2020.to_excel("data/industry_2020_full_summary.xlsx")
company_summary.to_excel("data/company_full_summary.xlsx", index=False)
company_summary.to_csv("data/company_full_summary.csv", index=False)

print("已保存阶段成果")"""
    ),
    code(
        """pd.read_csv("data/company_full_summary.csv").head()"""
    ),
    md(
        """阶段 5 小结：这一阶段带出了 `pivot_table()`、`set_index()`、`reset_index()`、构造 `Series` / `DataFrame`，以及保存 Excel 和 CSV。"""
    ),
    md(
        """## 阶段 6：时间序列入门

目标：理解带日期的数据如何切片、滞后、差分、计算增长率和重采样。这里构造一份日度价格数据。"""
    ),
    code(
        """dates = pd.date_range("2020-01-01", "2020-03-31", freq="B")
rng = np.random.default_rng(42)

returns = pd.DataFrame(
    {
        "平安银行": rng.normal(0.0005, 0.015, len(dates)),
        "万科A": rng.normal(0.0003, 0.018, len(dates)),
    },
    index=dates,
)

prices = 100 * (1 + returns).cumprod()
prices.head()"""
    ),
    md(
        """日期作为索引后，可以直接按日期字符串切片。"""
    ),
    code(
        """prices.loc["2020-02"].head()"""
    ),
    code(
        """prices.loc["2020-02-10":"2020-02-20"]"""
    ),
    md(
        """`shift()` 做滞后，`diff()` 做差分，`pct_change()` 计算百分比变化。"""
    ),
    code(
        """ts = prices["平安银行"].to_frame("price")
ts["lag_price"] = ts["price"].shift(1)
ts["diff"] = ts["price"].diff()
ts["return"] = ts["price"].pct_change()

ts.head()"""
    ),
    md(
        """如果已经有收益率，也可以用 `cumprod()` 还原价格路径。"""
    ),
    code(
        """rebuilt_price = 100 * (1 + ts["return"].fillna(0)).cumprod()
rebuilt_price.head()"""
    ),
    md(
        """`resample()` 可以把高频数据汇总到较低频率。例如把日度价格变成月末价格，把日收益变成月收益。"""
    ),
    code(
        """month_end_price = prices.resample("ME").last()
month_return = month_end_price.pct_change()

month_end_price"""
    ),
    code(
        """month_return"""
    ),
    md(
        """阶段 6 小结：这一阶段带出了 `date_range()`、日期索引、按日期切片、`shift()`、`diff()`、`pct_change()`、`cumprod()` 和 `resample()`。"""
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
