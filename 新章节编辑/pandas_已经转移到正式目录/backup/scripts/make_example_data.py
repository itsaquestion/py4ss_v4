from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def format_code(value):
    return str(int(value)).zfill(6)


def make_example_data():
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
        "批发业",
    ]

    candidates = basic[
        basic["行业名称"].isin(target_industries)
        & basic["证券代码"].isin(fin.loc[fin["年份"].between(2018, 2020), "证券代码"])
    ].copy()

    chosen_codes = []
    for industry in target_industries:
        part = candidates[candidates["行业名称"] == industry].sort_values("证券代码").head(4)
        chosen_codes.extend(part["证券代码"].tolist())

    chosen_codes = chosen_codes[:30]

    company = (
        basic[basic["证券代码"].isin(chosen_codes)]
        .sort_values("证券代码")
        .loc[
            :,
            [
                "证券代码",
                "公司全称",
                "上市市场编码",
                "行业代码",
                "行业名称",
                "省份",
                "城市",
                "公司上市日期",
                "公司成立日期",
            ],
        ]
        .copy()
    )

    name_map = (
        fin[fin["证券代码"].isin(chosen_codes)]
        .sort_values(["证券代码", "统计截止日期"])
        .drop_duplicates("证券代码")
        .set_index("证券代码")["证券简称"]
    )
    company.insert(1, "证券简称", company["证券代码"].map(name_map))

    company["证券代码"] = company["证券代码"].map(format_code)
    company = company.rename(
        columns={
            "上市市场编码": "上市市场",
            "公司上市日期": "上市日期",
            "公司成立日期": "成立日期",
        }
    )

    company["上市状态"] = np.where(company["证券简称"].str.contains("ST", na=False), "ST", "正常上市")

    # Controlled dirty values for teaching.
    company.loc[company.index[3], "行业名称"] = np.nan
    company.loc[company.index[7], "城市"] = np.nan
    company.loc[company.index[12], "上市日期"] = "2017/03/15"
    company.loc[company.index[18], "证券简称"] = " " + str(company.loc[company.index[18], "证券简称"]) + " "

    finance = (
        fin[fin["证券代码"].isin(chosen_codes) & fin["年份"].between(2018, 2020)]
        .sort_values(["证券代码", "年份"])
        .loc[
            :,
            [
                "证券代码",
                "证券简称",
                "统计截止日期",
                "年份",
                "总资产",
                "总负债",
                "净资产",
                "营业总收入",
                "净利润",
                "资产负债率",
            ],
        ]
        .copy()
    )
    finance["证券代码"] = finance["证券代码"].map(format_code)
    finance = finance.rename(columns={"营业总收入": "营业收入"})
    finance[["总资产", "净利润"]] = finance[["总资产", "净利润"]].astype("object")

    # Add dirty values that are common in spreadsheets.
    finance.loc[finance.index[5], "营业收入"] = np.nan
    finance.loc[finance.index[14], "净利润"] = "--"
    finance.loc[finance.index[25], "总资产"] = f"{finance.loc[finance.index[25], '总资产']:,.0f}"
    finance.loc[finance.index[37], "统计截止日期"] = "2020/12/31"

    duplicate_row = finance.iloc[[10]].copy()
    finance = pd.concat([finance, duplicate_row], ignore_index=True)

    company.to_excel(DATA / "company_info_example.xlsx", index=False)
    finance.to_excel(DATA / "financial_data_example.xlsx", index=False)

    return company, finance


if __name__ == "__main__":
    company_df, finance_df = make_example_data()
    print("company_info_example.xlsx", company_df.shape)
    print("financial_data_example.xlsx", finance_df.shape)
