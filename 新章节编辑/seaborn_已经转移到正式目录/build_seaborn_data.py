from pathlib import Path
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LOCAL_DATA_SRC = Path.home() / "data" / "src"

if LOCAL_DATA_SRC.exists():
    sys.path.insert(0, str(LOCAL_DATA_SRC))


def _take_evenly_spaced_firms(df, n):
    """按资产规模分布均匀取样，避免只取到同一类公司。"""
    firm_size = (
        df[df["year"] == df["year"].min()]
        .drop_duplicates("firm_id")
        .sort_values("总资产")
    )
    if len(firm_size) <= n:
        return firm_size["firm_id"].tolist()

    positions = np.linspace(0, len(firm_size) - 1, n).round().astype(int)
    return firm_size.iloc[positions]["firm_id"].tolist()


def make_visualization_sample():
    from load_data import read_csmar

    basic = read_csmar("上市公司基本信息年度表")
    finidx = read_csmar("财务指标文件")
    mainfin = read_csmar("上市公司主要财务指标")

    years = list(range(2018, 2024))
    target_industries = [
        "计算机、通信和其他电子设备制造业",
        "电气机械及器材制造业",
        "医药制造业",
        "软件和信息技术服务业",
        "汽车制造业",
        "房地产业",
    ]

    panel = (
        finidx[
            [
                "firm_id",
                "year",
                "证券代码",
                "统计截止日期",
                "资产负债率",
                "营业毛利率",
                "员工数目",
            ]
        ]
        .merge(
            mainfin[["firm_id", "year", "总资产", "营业收入", "净利润"]],
            on=["firm_id", "year"],
            how="inner",
        )
        .merge(
            basic[["firm_id", "year", "股票简称", "行业名称", "所属省份"]],
            on=["firm_id", "year"],
            how="inner",
        )
    )

    required_cols = [
        "证券代码",
        "统计截止日期",
        "资产负债率",
        "营业毛利率",
        "员工数目",
        "总资产",
        "营业收入",
        "净利润",
        "股票简称",
        "行业名称",
        "所属省份",
    ]
    panel = panel[
        panel["year"].isin(years)
        & panel["行业名称"].isin(target_industries)
        & panel[required_cols].notna().all(axis=1)
    ].copy()

    complete_counts = panel.groupby("firm_id")["year"].nunique()
    complete_firms = complete_counts[complete_counts == len(years)].index
    candidates = panel[panel["firm_id"].isin(complete_firms)].copy()
    stable_industry = candidates.groupby("firm_id")["行业名称"].nunique()
    stable_firms = stable_industry[stable_industry == 1].index
    candidates = candidates[candidates["firm_id"].isin(stable_firms)].copy()

    base_year = candidates[candidates["year"] == min(years)].copy()
    base_year["总资产_亿元"] = base_year["总资产"] / 1e8
    base_year["营业收入_亿元"] = base_year["营业收入"] / 1e8
    moderate_firms = base_year[
        base_year["总资产_亿元"].between(5, 500)
        & base_year["营业收入_亿元"].between(1, 300)
    ]["firm_id"]
    candidates = candidates[candidates["firm_id"].isin(moderate_firms)].copy()

    target_counts = {
        "计算机、通信和其他电子设备制造业": 32,
        "电气机械及器材制造业": 27,
        "医药制造业": 24,
        "软件和信息技术服务业": 19,
        "汽车制造业": 15,
        "房地产业": 11,
    }
    chosen_firms = []
    for industry, n in target_counts.items():
        industry_panel = candidates[candidates["行业名称"] == industry]
        chosen_firms.extend(_take_evenly_spaced_firms(industry_panel, n=n))

    output = (
        candidates[candidates["firm_id"].isin(chosen_firms)]
        .sort_values(["行业名称", "证券代码", "统计截止日期"])
        .loc[
            :,
            [
                "证券代码",
                "股票简称",
                "统计截止日期",
                "year",
                "行业名称",
                "所属省份",
                "总资产",
                "营业收入",
                "净利润",
                "资产负债率",
                "营业毛利率",
                "员工数目",
            ],
        ]
        .rename(columns={"year": "年份"})
        .copy()
    )

    output["证券代码"] = output["证券代码"].astype(str).str.zfill(6)
    output["统计截止日期"] = pd.to_datetime(output["统计截止日期"])
    for col in ["总资产", "营业收入", "净利润"]:
        output[f"{col}_亿元"] = (output[col] / 1e8).round(2)
    output["资产负债率"] = output["资产负债率"].round(4)
    output["营业毛利率"] = output["营业毛利率"].round(4)
    output["员工数目"] = output["员工数目"].astype(int)

    output = output[
        [
            "证券代码",
            "股票简称",
            "统计截止日期",
            "年份",
            "行业名称",
            "所属省份",
            "总资产_亿元",
            "营业收入_亿元",
            "净利润_亿元",
            "资产负债率",
            "营业毛利率",
            "员工数目",
        ]
    ].reset_index(drop=True)

    DATA.mkdir(exist_ok=True)
    output.to_excel(DATA / "company_visualization_sample.xlsx", index=False)
    return output


if __name__ == "__main__":
    sample = make_visualization_sample()
    print("company_visualization_sample.xlsx", sample.shape)
    print(sample.groupby("行业名称")["证券代码"].nunique())
    print(sample["年份"].min(), sample["年份"].max())
