from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LOCAL_DATA = Path.home() / "data"
LOCAL_DATA_SRC = LOCAL_DATA / "src"

if LOCAL_DATA_SRC.exists():
    sys.path.insert(0, str(LOCAL_DATA_SRC))


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


def make_company_annual_operations_data():
    """从本地 CSMAR 数据切出一张小型公司年度经营表。"""
    from load_data import read_csmar

    basic = read_csmar("上市公司基本信息年度表")
    finidx = read_csmar("财务指标文件")
    mainfin = read_csmar("上市公司主要财务指标")

    basic_cols = [
        "firm_id",
        "year",
        "股票简称",
        "行业名称",
        "所属省份",
        "所属城市",
        "首次上市日期",
        "上市状态",
    ]
    finidx_cols = [
        "firm_id",
        "year",
        "证券代码",
        "统计截止日期",
        "年报公布日期",
        "销售费用",
        "经营活动产生的现金流量净额",
        "资产负债率",
        "营业毛利率",
        "员工数目",
    ]
    mainfin_cols = [
        "firm_id",
        "year",
        "总资产",
        "总负债",
        "营业收入",
        "营业成本",
        "净利润",
    ]

    panel = (
        finidx[finidx_cols]
        .merge(mainfin[mainfin_cols], on=["firm_id", "year"], how="inner")
        .merge(basic[basic_cols], on=["firm_id", "year"], how="inner")
    )

    keep_years = [2018, 2019, 2020]
    target_industries = [
        "计算机、通信和其他电子设备制造业",
        "电气机械及器材制造业",
        "医药制造业",
        "软件和信息技术服务业",
        "汽车制造业",
        "房地产业",
    ]
    required_cols = [
        "股票简称",
        "行业名称",
        "所属省份",
        "所属城市",
        "首次上市日期",
        "上市状态",
        "年报公布日期",
        "销售费用",
        "经营活动产生的现金流量净额",
        "资产负债率",
        "营业毛利率",
        "员工数目",
        "总资产",
        "总负债",
        "营业收入",
        "营业成本",
        "净利润",
    ]

    panel = panel[
        panel["year"].isin(keep_years)
        & panel["行业名称"].isin(target_industries)
        & panel[required_cols].notna().all(axis=1)
    ].copy()

    complete_counts = panel.groupby("firm_id")["year"].nunique()
    complete_firms = complete_counts[complete_counts == len(keep_years)].index
    candidates = panel[panel["firm_id"].isin(complete_firms)].copy()

    chosen_codes = []
    for industry in target_industries:
        industry_codes = (
            candidates[candidates["行业名称"] == industry]
            .drop_duplicates("firm_id")
            .sort_values("firm_id")["firm_id"]
            .head(4)
            .tolist()
        )
        chosen_codes.extend(industry_codes)

    output = (
        candidates[candidates["firm_id"].isin(chosen_codes)]
        .sort_values(["证券代码", "统计截止日期"])
        .loc[
            :,
            [
                "证券代码",
                "股票简称",
                "统计截止日期",
                "年报公布日期",
                "行业名称",
                "所属省份",
                "所属城市",
                "首次上市日期",
                "上市状态",
                "总资产",
                "总负债",
                "营业收入",
                "营业成本",
                "销售费用",
                "净利润",
                "经营活动产生的现金流量净额",
                "资产负债率",
                "营业毛利率",
                "员工数目",
            ],
        ]
        .copy()
    )

    output["证券代码"] = output["证券代码"].astype(str).str.zfill(6)

    amount_cols = [
        "总资产",
        "总负债",
        "营业收入",
        "营业成本",
        "销售费用",
        "净利润",
        "经营活动产生的现金流量净额",
    ]
    for col in amount_cols:
        output[f"{col}_亿元"] = (output[col] / 1e8).round(2)
    output = output.drop(columns=amount_cols).rename(
        columns={"经营活动产生的现金流量净额_亿元": "经营现金流_亿元"}
    )
    output = output[
        [
            "证券代码",
            "股票简称",
            "统计截止日期",
            "年报公布日期",
            "行业名称",
            "所属省份",
            "所属城市",
            "首次上市日期",
            "上市状态",
            "总资产_亿元",
            "总负债_亿元",
            "营业收入_亿元",
            "营业成本_亿元",
            "销售费用_亿元",
            "净利润_亿元",
            "经营现金流_亿元",
            "资产负债率",
            "营业毛利率",
            "员工数目",
        ]
    ]
    output.to_excel(DATA / "company_annual_operations_clean.xlsx", index=False)

    return output


def make_dirty_financial_indicators_data(operations_df):
    """从披露财务指标切出一张待清洗的公司年度财务指标表。"""
    from load_data import read_csmar

    indicators = read_csmar("披露财务指标")

    teaching_codes = operations_df["证券代码"].astype(str).str.zfill(6).unique()
    selected = indicators[
        indicators["股票代码"].astype(str).str.zfill(6).isin(teaching_codes)
        & indicators["year"].between(2018, 2020)
    ].copy()

    selected = selected[
        [
            "股票代码",
            "股票简称",
            "统计截止日期",
            "非经常性损益",
            "归属于上市公司股东的扣除非经常性损益的净利润",
            "加权平均净资产收益率",
            "扣除非经常性损益后的加权平均净资产收益率",
            "基本每股收益",
        ]
    ].rename(
        columns={
            "股票代码": "证券代码",
            "归属于上市公司股东的扣除非经常性损益的净利润": "扣非净利润",
            "扣除非经常性损益后的加权平均净资产收益率": "扣非净资产收益率",
        }
    )

    selected["证券代码"] = selected["证券代码"].astype(str).str.zfill(6)
    selected["非经常性损益_亿元"] = (selected["非经常性损益"] / 1e8).round(2)
    selected["扣非净利润_亿元"] = (selected["扣非净利润"] / 1e8).round(2)
    selected = selected.drop(columns=["非经常性损益", "扣非净利润"])
    selected = selected.sort_values(["证券代码", "统计截止日期"]).head(45).reset_index(drop=True)

    dirty = selected.copy()
    object_cols = [
        "证券代码",
        "统计截止日期",
        "非经常性损益_亿元",
        "扣非净利润_亿元",
        "加权平均净资产收益率",
        "扣非净资产收益率",
        "基本每股收益",
    ]
    dirty[object_cols] = dirty[object_cols].astype("object")

    dirty.loc[0, "证券代码"] = int(dirty.loc[0, "证券代码"])
    dirty.loc[1, "证券代码"] = f" {dirty.loc[1, '证券代码']} "
    dirty.loc[2, "统计截止日期"] = dirty.loc[2, "统计截止日期"].strftime("%Y/%m/%d")
    dirty.loc[3, "统计截止日期"] = "2020-13-31"
    dirty.loc[4, "非经常性损益_亿元"] = "--"
    dirty.loc[5, "扣非净利润_亿元"] = f"{dirty.loc[5, '扣非净利润_亿元']:,.2f}"
    dirty.loc[6, "加权平均净资产收益率"] = f"{dirty.loc[6, '加权平均净资产收益率']:.2f}%"
    dirty.loc[7, "扣非净资产收益率"] = ""
    dirty.loc[8, "基本每股收益"] = "缺失"
    dirty.loc[10, "股票简称"] = f" {dirty.loc[10, '股票简称']} "
    dirty.loc[len(dirty)] = dirty.loc[0]

    dirty.to_excel(DATA / "financial_indicators_dirty.xlsx", index=False)

    return dirty


if __name__ == "__main__":
    finance_df, company_df = make_clean_intro_data()
    operations_df = make_company_annual_operations_data()
    indicators_df = make_dirty_financial_indicators_data(operations_df)
    print("finance_teaching_clean.xlsx", finance_df.shape)
    print("company_profile_teaching_clean.xlsx", company_df.shape)
    print("company_annual_operations_clean.xlsx", operations_df.shape)
    print("financial_indicators_dirty.xlsx", indicators_df.shape)
