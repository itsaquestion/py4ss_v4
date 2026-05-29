from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
NB_PATH = ROOT / "pandas_极简讲义.ipynb"


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
        """# Pandas 极简入门：上市公司数据

这一节用两张小表介绍 pandas 的基本功能：

- `company_info_example.xlsx`：公司基本信息，每家公司一行。
- `financial_data_example.xlsx`：年度财务数据，每家公司每年一行。

这两张表来自真实上市公司数据的抽样，并故意保留了少量常见问题：证券代码格式、缺失值、重复行、数字列混入文本等。"""
    ),
    md(
        """## 1. 读取数据

证券代码是编号，不是可以计算大小的数字。读取时先把它作为字符串处理，并补齐到 6 位。"""
    ),
    code(
        """import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 20)

def read_code(x):
    return str(x).strip().zfill(6)

company = pd.read_excel(
    "data/company_info_example.xlsx",
    converters={"证券代码": read_code},
)

finance = pd.read_excel(
    "data/financial_data_example.xlsx",
    converters={"证券代码": read_code},
)

company.head()"""
    ),
    code("""finance.head()"""),
    md(
        """## 2. 先看数据

拿到一张表后，通常先看行列数、列名、数据类型、缺失值和几个样本行。"""
    ),
    code(
        """print(company.shape)
print(company.columns.tolist())

company.info()"""
    ),
    code(
        """print(finance.shape)
print(finance.dtypes)

finance.isna().sum()"""
    ),
    md(
        """`value_counts()` 适合快速查看分类变量的分布。"""
    ),
    code("""company["行业名称"].value_counts(dropna=False).head(10)"""),
    md(
        """## 3. 选择行和列

`[]` 常用于选列，`.loc` 按行列标签选择，`.iloc` 按整数位置选择。"""
    ),
    code("""company[["证券代码", "证券简称", "行业名称", "省份"]].head()"""),
    code("""company.loc[company["省份"] == "广东省", ["证券代码", "证券简称", "城市"]].head()"""),
    code("""finance.iloc[:5, :5]"""),
    md(
        """## 4. 清洗常见脏数据

先处理文本两端空格、日期类型、缺失值、重复行，以及数字列中混入的文本。"""
    ),
    code(
        """company["证券简称"] = company["证券简称"].str.strip()
company["上市日期"] = pd.to_datetime(company["上市日期"], errors="coerce")
company["成立日期"] = pd.to_datetime(company["成立日期"], errors="coerce")

company[company["行业名称"].isna() | company["城市"].isna()]"""
    ),
    code(
        """# 这里为了演示，行业用“未分类”填补，城市用“未知”填补。
company["行业名称"] = company["行业名称"].fillna("未分类")
company["城市"] = company["城市"].fillna("未知")

company.isna().sum()"""
    ),
    code(
        """# 财务表里有一行重复记录。
print("重复行数量：", finance.duplicated().sum())
finance = finance.drop_duplicates()

# 数字列里可能混入逗号、-- 等文本。先统一转成字符串清理，再转回数值。
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
    md(
        """## 5. 列运算和类型转换

Pandas 的常见用法是基于已有列生成新列。"""
    ),
    code(
        """finance["统计截止日期"] = pd.to_datetime(finance["统计截止日期"], errors="coerce")
finance["年份"] = finance["统计截止日期"].dt.year

finance["总资产_亿元"] = finance["总资产"] / 1e8
finance["营业收入_亿元"] = finance["营业收入"] / 1e8
finance["净利率"] = finance["净利润"] / finance["营业收入"]
finance["是否盈利"] = finance["净利润"] > 0

finance["负债率等级"] = pd.cut(
    finance["资产负债率"],
    bins=[0, 0.4, 0.7, 1.0],
    labels=["低", "中", "高"],
)

finance[["证券代码", "年份", "总资产_亿元", "营业收入_亿元", "净利率", "是否盈利", "负债率等级"]].head()"""
    ),
    md(
        """## 6. 排序、筛选和分组统计

下面找出 2020 年营业收入最高的几家公司。"""
    ),
    code(
        """finance_2020 = finance[finance["年份"] == 2020]

finance_2020.sort_values("营业收入", ascending=False)[
    ["证券代码", "证券简称", "营业收入_亿元", "净利率"]
].head(10)"""
    ),
    md(
        """`groupby()` 用于“按组计算”。例如按年份统计平均资产负债率、营业收入总额和盈利公司数量。"""
    ),
    code(
        """finance.groupby("年份").agg(
    平均资产负债率=("资产负债率", "mean"),
    营业收入合计_亿元=("营业收入_亿元", "sum"),
    盈利公司数=("是否盈利", "sum"),
)"""
    ),
    md(
        """## 7. 合并两张表

公司基本信息表有行业和省份，财务表有年度指标。两张表可以按 `证券代码` 合并。"""
    ),
    code(
        """merged = finance.merge(
    company[["证券代码", "行业名称", "省份", "城市", "上市日期"]],
    on="证券代码",
    how="left",
)

merged.head()"""
    ),
    code(
        """industry_summary = (
    merged[merged["年份"] == 2020]
    .groupby("行业名称")
    .agg(
        公司数=("证券代码", "nunique"),
        平均营业收入_亿元=("营业收入_亿元", "mean"),
        平均净利率=("净利率", "mean"),
    )
    .sort_values("平均营业收入_亿元", ascending=False)
)

industry_summary"""
    ),
    md(
        """## 8. 保存结果

清洗和合并后的结果可以保存为 Excel 或 CSV。一般保存普通表格时使用 `index=False`。"""
    ),
    code(
        """merged.to_excel("data/merged_finance_company.xlsx", index=False)
print("已保存：data/merged_finance_company.xlsx")"""
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
