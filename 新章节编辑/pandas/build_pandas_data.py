from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def make_clean_intro_data():
    basic = pd.read_excel(DATA / "source_sample_basic_info.xlsx")
    fin = pd.read_excel(DATA / "source_sample_fin_data.xlsx")

    fin["年份"] = pd.to_datetime(fin["统计截止日期"]).dt.year

    target_industries = [
        "货币金融服务",
        "房地产业",
        "软件和信息技术服务业",
        "计算机、通信和其他电子设备制造业",
        "汽车制造业",
        "电气机械及器材制造业",
        "医药制造业",
    ]

    fin_complete = fin[
        fin["年份"].between(2018, 2020)
        & fin[["总资产", "营业总收入", "净利润", "资产负债率"]].notna().all(axis=1)
    ].copy()

    counts = fin_complete.groupby("证券代码")["年份"].nunique()
    complete_codes = counts[counts == 3].index

    candidates = basic[
        basic["证券代码"].isin(complete_codes)
        & basic["行业名称"].isin(target_industries)
    ].copy()

    chosen_codes = []
    for industry in target_industries:
        chosen_codes.extend(
            candidates[candidates["行业名称"] == industry]
            .sort_values("证券代码")
            .head(4)["证券代码"]
            .tolist()
        )
    chosen_codes = chosen_codes[:28]

    finance = (
        fin_complete[fin_complete["证券代码"].isin(chosen_codes)]
        .sort_values(["证券代码", "年份"])
        .loc[:, ["证券代码", "证券简称", "年份", "总资产", "营业总收入", "净利润", "资产负债率"]]
        .copy()
    )

    finance["总资产_亿元"] = (finance["总资产"] / 1e8).round(2)
    finance["营业收入_亿元"] = (finance["营业总收入"] / 1e8).round(2)
    finance["净利润_亿元"] = (finance["净利润"] / 1e8).round(2)
    finance["资产负债率"] = finance["资产负债率"].round(4)

    finance_teaching = finance[
        ["证券代码", "证券简称", "年份", "总资产_亿元", "营业收入_亿元", "净利润_亿元", "资产负债率"]
    ].copy()

    company = (
        basic[basic["证券代码"].isin(chosen_codes)]
        .sort_values("证券代码")
        .loc[:, ["证券代码", "上市市场编码", "行业名称", "省份", "城市", "公司上市日期"]]
        .copy()
    )
    names = (
        finance.drop_duplicates("证券代码")
        .set_index("证券代码")["证券简称"]
    )
    company.insert(1, "证券简称", company["证券代码"].map(names))
    company["证券代码"] = company["证券代码"].map(lambda x: str(int(x)).zfill(6))
    company = company.rename(
        columns={
            "上市市场编码": "上市市场",
            "公司上市日期": "上市日期",
        }
    )
    company["上市日期"] = pd.to_datetime(company["上市日期"])
    company_profile = company[
        ["证券代码", "证券简称", "行业名称", "省份", "城市", "上市市场", "上市日期"]
    ].copy()

    finance_teaching.to_excel(DATA / "finance_teaching_clean.xlsx", index=False)
    company_profile.to_excel(DATA / "company_profile_teaching_clean.xlsx", index=False)

    return finance_teaching, company_profile


if __name__ == "__main__":
    finance_df, company_df = make_clean_intro_data()
    print("finance_teaching_clean.xlsx", finance_df.shape)
    print("company_profile_teaching_clean.xlsx", company_df.shape)
