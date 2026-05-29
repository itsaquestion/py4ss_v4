from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
NB_PATH = ROOT / "pandas_目标驱动极简版.ipynb"


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(True),
    }


cells = [
    md(
        """# Pandas 入门：从财务表到行业分析

我们有两张表：

- `financial_data_example.xlsx`：公司年度财务数据。
- `company_info_example.xlsx`：公司基本信息。

本节不按函数顺序讲 pandas，而是围绕三个阶段目标展开。"""
    ),
    md(
        """## 阶段 1：整理财务表，找出 2020 年表现较好的公司

第一阶段只使用财务表。目标不是“学会读取和筛选”，而是把一张略乱的财务表整理成可以排序和比较的公司名单。"""
    ),
    code(
        """import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 20)

def read_code(x):
    return str(x).strip().zfill(6)

finance_raw = pd.read_excel(
    "data/financial_data_example.xlsx",
    converters={"证券代码": read_code},
)

finance_raw.head()"""
    ),
    md("""先判断这张表的规模、字段、数据类型和明显问题。"""),
    code(
        """print("行列数：", finance_raw.shape)
print("列名：", finance_raw.columns.tolist())

finance_raw.info()"""
    ),
    code(
        """finance_raw.isna().sum()"""
    ),
    md("""财务表里有重复行，也有数字列混入文本。先做一份工作副本，逐步清洗。"""),
    code(
        """finance = finance_raw.copy()

print("重复行数量：", finance.duplicated().sum())
finance = finance.drop_duplicates()

num_cols = ["总资产", "总负债", "净资产", "营业收入", "净利润", "资产负债率"]

for col in num_cols:
    finance[col] = (
        finance[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .replace({"--": np.nan, "nan": np.nan})
    )
    finance[col] = pd.to_numeric(finance[col], errors="coerce")

finance[num_cols].isna().sum()"""
    ),
    md("""把日期转成真正的日期，并基于原有列构造几个更容易解释的指标。"""),
    code(
        """finance["统计截止日期"] = pd.to_datetime(finance["统计截止日期"], errors="coerce")
finance["年份"] = finance["统计截止日期"].dt.year

finance["总资产_亿元"] = finance["总资产"] / 1e8
finance["营业收入_亿元"] = finance["营业收入"] / 1e8
finance["净利率"] = finance["净利润"] / finance["营业收入"]
finance["资产收益率"] = finance["净利润"] / finance["总资产"]
finance["是否盈利"] = finance["净利润"] > 0

finance[["证券代码", "证券简称", "年份", "营业收入_亿元", "净利率", "资产收益率", "是否盈利"]].head()"""
    ),
    md("""现在可以得到一个阶段性结果：2020 年盈利且营业收入不缺失的公司，按营业收入排序。"""),
    code(
        """finance_2020_rank = (
    finance
    .loc[
        (finance["年份"] == 2020)
        & finance["是否盈利"]
        & finance["营业收入"].notna(),
        ["证券代码", "证券简称", "营业收入_亿元", "净利率", "资产收益率", "资产负债率"],
    ]
    .sort_values("营业收入_亿元", ascending=False)
)

finance_2020_rank.head(10)"""
    ),
    md(
        """阶段 1 小结：我们只用一张财务表，已经用到了读取、查看、复制、去重、缺失值检查、类型转换、日期转换、列运算、条件筛选、排序。"""
    ),
    md(
        """## 阶段 2：加入公司信息，让排名结果有行业和地区背景

现在的问题是：财务表只能告诉我们哪家公司收入高，但不能告诉我们它们来自哪些行业和地区。第二阶段读取公司信息表，并把它接到财务结果上。"""
    ),
    code(
        """company_raw = pd.read_excel(
    "data/company_info_example.xlsx",
    converters={"证券代码": read_code},
)

company_raw.head()"""
    ),
    md("""公司信息表也需要简单清洗：文本去空格、日期转换、填补少量缺失。"""),
    code(
        """company = company_raw.copy()

company["证券简称"] = company["证券简称"].str.strip()
company["上市日期"] = pd.to_datetime(company["上市日期"], errors="coerce")
company["成立日期"] = pd.to_datetime(company["成立日期"], errors="coerce")

company[["行业名称", "城市"]] = company[["行业名称", "城市"]].fillna("未知")

company["行业名称"].value_counts().head(10)"""
    ),
    md("""把阶段 1 的公司排名和公司信息表合并。合并后检查行数和缺失，确认没有明显匹配失败。"""),
    code(
        """rank_with_info = finance_2020_rank.merge(
    company[["证券代码", "行业名称", "省份", "城市", "上市日期"]],
    on="证券代码",
    how="left",
)

print("合并前行数：", len(finance_2020_rank))
print("合并后行数：", len(rank_with_info))
print("行业缺失数量：", rank_with_info["行业名称"].isna().sum())

rank_with_info.head(10)"""
    ),
    md("""现在可以回答更具体的问题：2020 年营业收入最高的公司主要来自哪些行业。"""),
    code(
        """rank_with_info[["证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利率"]].head(10)"""
    ),
    md(
        """阶段 2 小结：这里带出了第二张表的读取和清洗、`merge`、合并结果检查，以及带背景变量的筛选和展示。"""
    ),
    md(
        """## 阶段 3：从公司名单上升到行业比较

第三阶段不再只看单家公司，而是按行业汇总。目标是得到一张行业层面的分析表。"""
    ),
    code(
        """analysis_df = finance.merge(
    company[["证券代码", "行业名称", "省份"]],
    on="证券代码",
    how="left",
)

analysis_df.head()"""
    ),
    md("""先做 2020 年行业汇总。"""),
    code(
        """industry_2020 = (
    analysis_df[analysis_df["年份"] == 2020]
    .groupby("行业名称")
    .agg(
        公司数=("证券代码", "nunique"),
        平均营业收入_亿元=("营业收入_亿元", "mean"),
        平均净利率=("净利率", "mean"),
        平均资产负债率=("资产负债率", "mean"),
        盈利公司数=("是否盈利", "sum"),
    )
    .sort_values("平均营业收入_亿元", ascending=False)
)

industry_2020"""
    ),
    md("""再做一个稍复杂的目标：找出每个行业 2020 年营业收入最高的公司。这里用分组循环展示思路。"""),
    code(
        """top_companies = []

for industry, group in analysis_df[analysis_df["年份"] == 2020].groupby("行业名称"):
    top = group.sort_values("营业收入_亿元", ascending=False).head(1)
    top_companies.append(top)

industry_top_company = pd.concat(top_companies)[
    ["行业名称", "证券代码", "证券简称", "营业收入_亿元", "净利率"]
].sort_values("营业收入_亿元", ascending=False)

industry_top_company"""
    ),
    md(
        """也可以重建一张公司层面的摘要表：每家公司一行，比较 2018 到 2020 年的营业收入变化。"""
    ),
    code(
        """revenue_wide = analysis_df.pivot_table(
    index=["证券代码", "证券简称", "行业名称"],
    columns="年份",
    values="营业收入_亿元",
)

revenue_wide["收入增长率_2018_2020"] = (revenue_wide[2020] / revenue_wide[2018]) - 1

company_summary = (
    revenue_wide
    .reset_index()
    .sort_values("收入增长率_2018_2020", ascending=False)
)

company_summary.head(10)"""
    ),
    md("""保存最终结果。"""),
    code(
        """industry_2020.to_excel("data/industry_2020_summary.xlsx")
company_summary.to_excel("data/company_summary.xlsx", index=False)

print("已保存行业汇总表和公司摘要表")"""
    ),
    md(
        """阶段 3 小结：这里带出了 `groupby().agg()`、排序、分组循环、`concat`、`pivot_table`，以及按分析目标重建数据表。"""
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
