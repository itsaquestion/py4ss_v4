from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
NB_PATH = ROOT / "pandas_目标驱动极简版_干净起步.ipynb"


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
        """# Pandas 入门：先从一张现实但干净的表开始

这一版先避开脏数据清洗。第一阶段只使用年度财务表，目标是做出一份 2020 年公司表现排名。

财务表中有 `证券代码`，但第一阶段暂时不处理它：编号列不参与计算，先从更直观的列开始练习 pandas 的基本操作。第二阶段再正式处理证券代码，并把财务表和公司信息表合并。"""
    ),
    md(
        """## 阶段 1：用一张财务表做出 2020 年公司表现排名

先读入 `finance_teaching_clean.xlsx`。这张表每行是一家公司某一年的财务数据。"""
    ),
    code(
        """import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 20)

finance_raw = pd.read_excel("data/finance_teaching_clean.xlsx")
finance_raw.head()"""
    ),
    md("""`证券代码` 是编号，不是财务指标。第一阶段先把它放到一边，集中练习选行、选列、计算和排序。"""),
    code(
        """finance = finance_raw.drop(columns=["证券代码"])
finance.head()"""
    ),
    md("""先看这张表的基本结构。"""),
    code(
        """print("行列数：", finance.shape)
print("列名：", finance.columns.tolist())

finance.info()"""
    ),
    md("""选出我们关心的几列。"""),
    code(
        """finance[["证券简称", "年份", "营业收入_亿元", "净利润_亿元"]].head()"""
    ),
    md("""筛选 2020 年的数据。"""),
    code(
        """finance_2020 = finance[finance["年份"] == 2020]
finance_2020.head()"""
    ),
    md("""在原有列的基础上计算新指标。"""),
    code(
        """finance["净利率"] = finance["净利润_亿元"] / finance["营业收入_亿元"]
finance["资产收益率"] = finance["净利润_亿元"] / finance["总资产_亿元"]
finance["是否盈利"] = finance["净利润_亿元"] > 0

finance[["证券简称", "年份", "净利率", "资产收益率", "是否盈利"]].head()"""
    ),
    md("""重新筛选 2020 年，并按营业收入排序。"""),
    code(
        """finance_2020_rank = (
    finance[finance["年份"] == 2020]
    .sort_values("营业收入_亿元", ascending=False)
)

finance_2020_rank[[
    "证券简称", "营业收入_亿元", "净利润_亿元", "净利率", "资产收益率", "资产负债率"
]].head(10)"""
    ),
    md("""做几个简单统计，了解 2020 年样本公司的整体情况。"""),
    code(
        """finance_2020[["总资产_亿元", "营业收入_亿元", "净利润_亿元", "资产负债率"]].describe()"""
    ),
    code(
        """print("公司数量：", finance_2020["证券简称"].nunique())
print("营业收入平均值：", finance_2020["营业收入_亿元"].mean())
print("营业收入最大值：", finance_2020["营业收入_亿元"].max())"""
    ),
    md(
        """阶段 1 小结：这一阶段只讲基础功能，包括读取、临时放下暂不处理的列、查看、选列、筛行、列运算、排序和简单统计。"""
    ),
    md(
        """## 阶段 2：处理证券代码，并加入公司信息

现在要把财务排名和公司信息表合并。合并时需要可靠的连接键，所以这一阶段必须认真处理 `证券代码`：把它作为字符串，并补齐到 6 位。"""
    ),
    code(
        """def read_code(x):
    return str(x).strip().zfill(6)

finance_with_code = pd.read_excel(
    "data/finance_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)

company = pd.read_excel(
    "data/company_profile_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)

finance_with_code.head()"""
    ),
    md("""先在带代码的财务表中重新生成阶段 1 用过的指标。"""),
    code(
        """finance_with_code["净利率"] = finance_with_code["净利润_亿元"] / finance_with_code["营业收入_亿元"]
finance_with_code["资产收益率"] = finance_with_code["净利润_亿元"] / finance_with_code["总资产_亿元"]
finance_with_code["是否盈利"] = finance_with_code["净利润_亿元"] > 0

finance_2020_rank_with_code = (
    finance_with_code[finance_with_code["年份"] == 2020]
    .sort_values("营业收入_亿元", ascending=False)
)

finance_2020_rank_with_code.head()"""
    ),
    md("""从公司信息表中选出需要合并的列。"""),
    code(
        """company_small = company[["证券代码", "行业名称", "省份", "城市", "上市日期"]]
company_small.head()"""
    ),
    md("""把 2020 年排名表和公司信息表合并。"""),
    code(
        """rank_with_info = finance_2020_rank_with_code.merge(
    company_small,
    on="证券代码",
    how="left",
)

rank_with_info[[
    "证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利润_亿元", "净利率"
]].head(10)"""
    ),
    md("""合并后可以提出更具体的问题。例如：2020 年营业收入前十的公司分别来自哪些行业？"""),
    code(
        """rank_with_info.head(10)["行业名称"].value_counts()"""
    ),
    md(
        """阶段 2 小结：这一阶段带出证券代码的字符串处理、补齐 6 位、第二张表、选列、`merge`，以及合并后的分类统计。"""
    ),
    md(
        """## 阶段 3：按行业汇总，重建一张分析表

现在不再只看公司名单，而是比较行业。目标是得到一张行业层面的汇总表。"""
    ),
    code(
        """analysis_df = finance_with_code.merge(company_small, on="证券代码", how="left")
analysis_df.head()"""
    ),
    md("""按行业汇总 2020 年的数据。"""),
    code(
        """industry_2020 = (
    analysis_df[analysis_df["年份"] == 2020]
    .groupby("行业名称")
    .agg(
        公司数=("证券简称", "nunique"),
        平均营业收入_亿元=("营业收入_亿元", "mean"),
        平均净利率=("净利率", "mean"),
        平均资产负债率=("资产负债率", "mean"),
    )
    .sort_values("平均营业收入_亿元", ascending=False)
)

industry_2020"""
    ),
    md("""如果希望看到每个行业收入最高的公司，可以用分组循环。"""),
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
    md("""最后，把三年营业收入重建成一张公司层面的宽表，便于比较收入变化。"""),
    code(
        """revenue_wide = analysis_df.pivot_table(
    index=["证券代码", "证券简称", "行业名称"],
    columns="年份",
    values="营业收入_亿元",
)

revenue_wide["收入增长率_2018_2020"] = revenue_wide[2020] / revenue_wide[2018] - 1

company_summary = revenue_wide.reset_index().sort_values("收入增长率_2018_2020", ascending=False)
company_summary.head(10)"""
    ),
    md("""保存阶段成果。"""),
    code(
        """finance_2020_rank_with_code.to_excel("data/finance_2020_rank.xlsx", index=False)
industry_2020.to_excel("data/industry_2020_clean_summary.xlsx")
company_summary.to_excel("data/company_clean_summary.xlsx", index=False)

print("已保存三个阶段成果")"""
    ),
    md(
        """阶段 3 小结：这一阶段带出 `groupby().agg()`、分组循环、`concat`、`pivot_table` 和结果保存。"""
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
