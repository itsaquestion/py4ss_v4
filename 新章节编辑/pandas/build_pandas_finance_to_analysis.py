from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent
NB_PATH = ROOT / "pandas_finance_to_analysis.ipynb"
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

Pandas 是 Python 中处理表格数据的核心工具。它提供了类似电子表格的数据结构，又可以用代码完成重复、精确、可追踪的数据整理和计算。在经管数据分析中，上市公司财务表、问卷数据、交易数据、地区统计数据等，通常都可以先整理成 pandas 的 `DataFrame`，再继续做统计分析、建模或可视化。
"""
    ),
    md(
        """**Jupyter Notebook 简介**

本章使用 Jupyter Notebook。Notebook 文件扩展名是 `.ipynb`，适合记录数据分析过程：代码、文字说明和运行结果可以放在同一个文件中。"""
    ),
    md(
        """**数据存放约定**

本课程约定：数据文件都放在工作目录下的 `data` 文件夹中。工作目录可以理解为当前项目或当前 notebook 所在的主要目录。读取数据时，可以用相对路径引用文件，例如 `data/finance_teaching_clean.xlsx`。"""
    ),
    md(
        """**本章使用的数据**

本章使用两张教学表：

- `data/finance_teaching_clean.xlsx`：公司年度财务数据。
- `data/company_profile_teaching_clean.xlsx`：公司基本信息。"""
    ),
    md(
        """## 本章知识点安排

**阶段 1：先认识一张表**

读入财务表，查看前几行、后几行、行列数、列名、数据类型和描述统计。先知道表里有什么，再决定后面怎么处理。

**阶段 2：从表里取出自己需要的部分**

围绕“在行与列上操作”展开：选单列、选多列、`iloc`、`loc`、条件筛选、复合条件、同时选行和列、`query()`，以及筛选后查看结果。

**阶段 3：修改表，生成新信息**

用已有列生成新列，做列运算，覆盖已有列，用 `np.where()`、`pd.cut()` 和带筛选的 `.loc` 赋值，排序、排名，并做简单统计。

**阶段 4：处理真实数据中的常见问题**

建立工作副本，检查缺失值和重复值，处理特殊文本，转换数据类型，使用 `dropna()`、`fillna()`、`replace()`、`map()`，并理解链式赋值 warning。

**阶段 5：合并第二张表，补充背景信息**

处理作为编号的证券代码，使用字符串方法和日期方法，整理公司信息表，用 `merge()` 合并，并检查合并结果。

**阶段 6：按行业和年份做比较**

从公司明细表转向分组结论：`groupby()`、多指标 `agg()`、自定义聚合函数、`transform()`、每组取前几名、分组循环和 `concat()`。

**阶段 7：把数据整理成适合分析的形状**

理解长表和宽表，使用 `pivot_table()`、`set_index()`、`reset_index()`，构造 `Series` / `DataFrame`，并导出结果。

**阶段 8：时间序列入门**

让 pandas 识别时间顺序，使用日期索引、日期切片、`shift()`、`diff()`、`pct_change()`、`cumprod()` 和 `resample()`。"""
    ),
    md(
        """**开始前：DataFrame 和 Series**

Pandas 主要处理二维表格。一个 `DataFrame` 可以理解为一张 Excel 表：有行、列、列名和行索引。一个 `Series` 可以理解为一列数据，它由索引和值组成。多个 `Series` 横向放在一起，就形成一个 `DataFrame`。

```text
index + ndarray -> Series
index + Series + Series + ... -> DataFrame
```

![](images/df-dp.png)"""
    ),
    md(
        """**Excel 和 CSV**

常见表格数据主要有两类：

- Excel 文件：扩展名通常是 `.xlsx`。可以保存格式、颜色、多个工作表等信息，适合给人查看和编辑。
- CSV 文件：扩展名是 `.csv`。本质上是纯文本，只保存数据本身，不保存格式。它体积小、通用性强，几乎所有数据软件都能读取。

在数据分析中，Excel 和 CSV 都常见。拿不准保存成什么格式时，CSV 往往更通用；需要给人直接打开查看时，Excel 更方便。"""
    ),
    md(
        """## 阶段 1：先认识一张表

目标：读入年度财务表，知道这张表有多少行、多少列，每一列大致是什么含义。"""
    ),
    md(
        """**读取数据，并看表的样子**

1. `pd.read_excel("文件路径")`：读取 Excel 文件，得到一张 `DataFrame`。

2. `head()` / `tail()`：分别查看开头和末尾，默认显示 5 行；`head(10)` / `tail(10)` 可以指定行数。"""
    ),
    code(
        """import pandas as pd  # 表格数据处理
import numpy as np  # 数值和缺失值处理

pd.set_option("display.max_columns", 30)  # 最多显示 30 列
pd.set_option("display.float_format", "{:.4f}".format)  # 小数显示为 4 位

finance_raw = pd.read_excel("data/finance_teaching_clean.xlsx")  # 读取 Excel
finance_raw.head()  # 查看前 5 行"""
    ),
    code(
        """finance_raw.tail()  # 查看后 5 行"""
    ),
    md(
        """**查看表的结构和数值概况**

1. `shape`：查看行数和列数。

2. `columns.tolist()`：查看列名，并转换成普通列表，显示起来更直接。

3. `dtypes` / `info()`：查看数据类型；`info()` 还会显示每列的非缺失值数量。

4. `describe()`：查看数值列的样本数、均值、标准差、最小值、四分位数和最大值。"""
    ),
    code(
        """finance_raw.shape  # 查看行数和列数"""
    ),
    code(
        """finance_raw.columns.tolist()  # 查看列名列表"""
    ),
    code(
        """finance_raw.dtypes  # 查看每列数据类型"""
    ),
    code(
        """finance_raw.info()  # 查看表结构摘要"""
    ),
    code(
        """finance_raw.describe()  # 查看数值列描述统计"""
    ),
    md(
        """**建立工作副本**

拿到原始数据后，建议复制一张工作副本。后面的筛选、删除、修改都在副本上做；如果处理过程中改错了，还可以回到原始表重新开始。

1. `drop(columns=[...])`：删除指定列。很多 pandas 操作会返回一张新表，原表通常不会自动改变。

2. `.copy()`：复制出工作副本。这里先暂时放下 `证券代码`，集中处理财务指标。"""
    ),
    code(
        """finance = finance_raw.drop(columns=["证券代码"]).copy()  # 删除暂不用的列并复制副本
finance.head()  # 查看工作副本"""
    ),
    md(
        """阶段 1 小结：拿到表格后，先用 `head()`、`tail()`、`shape`、`columns`、`dtypes`、`info()` 和 `describe()` 看结构、类型和大致分布。

**练习**：完成最后的阶段 1 练习。"""
    ),
    md(
        """## 阶段 2：从表里取出自己需要的部分

目标：从财务表中切出自己要看的行和列，形成 2020 年值得进一步观察的公司名单。"""
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
        """`.iloc` 按整数位置选择，基本格式是：

```python
df.iloc[行位置, 列位置]
```

行位置和列位置都从 0 开始，可以使用切片。它适合快速查看“第几行、第几列”。"""
    ),
    code(
        """finance.iloc[:5, :4]"""
    ),
    md(
        """`.loc` 按标签选择，基本格式是：

```python
df.loc[行标签, 列标签]
```

这里的“行标签”可以是索引标签，也可以是一个筛选条件；“列标签”可以是一个列名，也可以是列名列表。"""
    ),
    code(
        """finance.loc[
    finance["年份"] == 2020,
    ["证券简称", "营业收入_亿元", "净利润_亿元", "资产负债率"],
].head()"""
    ),
    md(
        """`.loc` 也可以用标签切片。要注意：`.loc` 的标签切片包含结束点，这和 Python 列表切片不同。"""
    ),
    code(
        """finance.loc[0:3, "证券简称":"营业收入_亿元"]"""
    ),
    md(
        """条件筛选会得到一组 `True` / `False`。把这组结果放到 `.loc` 的行位置，就可以保留满足条件的行。

复合条件要用 `&`、`|`、`~`，每个条件外面加括号。"""
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
        """`query()` 也用于条件筛选。它把筛选条件写成字符串，列名可以直接出现在字符串里。条件较短时，这种写法很方便。"""
    ),
    code(
        """finance.query("年份 == 2020 and 净利润_亿元 > 0").head()"""
    ),
    md(
        """阶段 2 小结：想从表中取出一部分数据，可以按列名选列，用 `iloc` 按位置选，用 `loc` 按标签或条件选；条件较短时，`query()` 也很方便。筛选之后用 `head()`、`tail()` 和行数看一眼结果。

完成本阶段后，请做最后“练习”中的阶段 2 练习。"""
    ),
    md(
        """## 阶段 3：修改表，生成新信息

目标：在原始财务指标基础上，生成更适合比较的新变量，并得到 2020 年公司表现排名。"""
    ),
    md(
        """用已有列生成新列，是 pandas 中最常见的操作之一。写法和给字典增加新键类似：

```python
df["新列"] = 表达式
```

表达式可以来自一列，也可以来自多列共同计算。"""
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
        """`pd.cut()` 可以把连续数值分成几个区间，常用于生成“高、中、低”这类分组变量。

也可以按条件给新列赋值。`np.where(条件, 条件成立时的值, 条件不成立时的值)` 适合二选一；`.loc[条件, 列名] = 新值` 适合对满足条件的行局部修改。"""
    ),
    code(
        """finance["负债水平"] = "正常"
finance.loc[finance["资产负债率"] >= 0.7, "负债水平"] = "较高"

finance[["证券简称", "年份", "资产负债率", "负债水平"]].head()"""
    ),
    md(
        """修改筛选后的数据时，优先使用 `.loc[条件, 列名] = 新值`。下面这种连续使用 `[]` 的写法容易触发 warning，也容易让人分不清修改的是原表还是临时切出来的表：

```python
finance[finance["资产负债率"] >= 0.7]["负债水平"] = "较高"
```

这类写法通常称为链式赋值。课堂和作业中建议直接写成 `.loc`。"""
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
        """排序适合查看结果。需要把排名作为一列继续使用时，可以用 `rank()`。"""
    ),
    code(
        """finance_2020_rank["收入排名"] = (
    finance_2020_rank["营业收入_亿元"]
    .rank(ascending=False, method="min")
    .astype(int)
)

finance_2020_rank[["证券简称", "营业收入_亿元", "收入排名"]].head(10)"""
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
        """为了展示结果，也可以重命名结果表中的列。"""
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
        """阶段 3 小结：我们得到了 `finance_2020_rank`。这一阶段带出了列运算、新增列、按条件赋值、`np.where()`、`pd.cut()`、排序、排名和简单统计。

完成本阶段后，请做最后“练习”中的阶段 3 练习。"""
    ),
    md(
        """## 阶段 4：处理真实数据中的常见问题

目标：把会影响计算和后续合并的常见问题先处理掉。真实数据不一定很脏，但经常会出现缺失值、重复行、特殊文本、数字被读成文本等情况。"""
    ),
    md(
        """先重新读取带证券代码的财务表。证券代码是编号，适合作为字符串处理。"""
    ),
    code(
        """def read_code(x):
    return str(x).strip().zfill(6)

finance_code = pd.read_excel(
    "data/finance_teaching_clean.xlsx",
    converters={"证券代码": read_code},
)
finance_code["净利率"] = finance_code["净利润_亿元"] / finance_code["营业收入_亿元"]
finance_code["资产收益率"] = finance_code["净利润_亿元"] / finance_code["总资产_亿元"]
finance_code["是否盈利"] = finance_code["净利润_亿元"] > 0
finance_code["负债水平"] = np.where(finance_code["资产负债率"] >= 0.7, "较高", "正常")

finance_code.head()"""
    ),
    md(
        """为了集中演示，这里从干净财务表复制出一份练习用的小表，再人为放入几个真实数据里常见的问题。"""
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
        """检查缺失值和重复行。"""
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
        """缺失值可以删除，也可以填补。怎么处理取决于分析目的。这里演示两种常见做法。

`dropna()` 会删除包含缺失值的行或列；`fillna()` 会把缺失值替换成指定数值。"""
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
        """`dropna()` 可以用参数控制删除规则。`subset` 指定检查哪些列，`axis=1` 可以按列删除，`how="all"` 表示整行或整列全部缺失时才删除。"""
    ),
    code(
        """dropna_demo = pd.DataFrame({
    "A": [1, np.nan, np.nan],
    "B": [2, np.nan, np.nan],
    "C": [np.nan, np.nan, np.nan],
})

display(dropna_demo)
display(dropna_demo.dropna(how="all"))
display(dropna_demo.dropna(axis=1, how="all"))"""
    ),
    md(
        """`map()` 适合把一组取值映射成另一组取值。常见写法是先准备一个字典，再把原来的取值替换成新的标签。"""
    ),
    code(
        """debt_map = {"正常": "低风险", "较高": "需关注", "未知": "待确认"}
fill_missing["负债风险"] = fill_missing["负债水平"].map(debt_map)

fill_missing[["证券简称", "负债水平", "负债风险"]].head()"""
    ),
    md(
        """`replace()` 适合替换特殊值。现实数据里常见 `999`、`-1`、`--` 等特殊编码。和 `map()` 相比，`replace()` 更常用于把少数异常取值替换掉。"""
    ),
    code(
        """special = pd.Series([1, 2, 999, -1, 5], name="原始值")
special.replace({999: np.nan, -1: 0})"""
    ),
    md(
        """### 副本、视图和链式赋值

直接修改数据时，建议优先使用：

```python
df.loc[条件, 列名] = 新值
```

筛选出一部分数据再修改时，显式使用 `.copy()` 生成工作副本。这样更容易判断后续操作影响的是哪一张表。连续使用 `df[条件]["列"] = 新值` 这类链式赋值，pandas 往往会给出 warning。"""
    ),
    md(
        """阶段 4 小结：这一阶段带出了 `isna()`、`dropna()`、`axis`、`how`、`fillna()`、`duplicated()`、`drop_duplicates()`、`replace()`、`pd.to_numeric()`、`map()`、工作副本和链式赋值 warning。

完成本阶段后，请做最后“练习”中的阶段 4 练习。"""
    ),
    md(
        """## 阶段 5：合并第二张表，补充背景信息

目标：把财务表和公司信息表合并，让财务指标带上行业、省份、城市、上市日期等背景信息。"""
    ),
    md(
        """证券代码是编号，适合作为字符串处理。读取时把它转成字符串，并补齐到 6 位。"""
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
        """公司信息表中有文本列和日期列，可以做几个轻量处理。"""
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
        """字符串列可以使用 `.str` 调用字符串方法。常见格式是：

```python
df["文本列"].str.contains("关键词", na=False)
```

`na=False` 表示遇到缺失值时按“不包含关键词”处理。下面用它找出行业名称中包含“制造”的公司，或找出简称中包含 `ST` 的公司。"""
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
        """日期列先用 `pd.to_datetime()` 转成日期类型，再用 `.dt` 提取年份、月份、季度等信息。常见格式是：

```python
df["日期列"] = pd.to_datetime(df["日期列"])
df["年份"] = df["日期列"].dt.year
```

下面根据上市日期提取年份、月份、季度，再筛选较早上市的公司。"""
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
        """重新在带证券代码的财务表中生成前面用到的财务指标。"""
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
        """合并前把右表整理成需要的列。"""
    ),
    code(
        """company_small = company[
    ["证券代码", "行业名称", "省份", "城市", "上市市场", "上市日期", "上市年份", "是否ST"]
]

company_small.head()"""
    ),
    md(
        """`merge()` 用于按共同字段合并两张表。最常见的写法是：

```python
left.merge(right, on="共同列名", how="left")
```

这里的 `left` 是左表，`right` 是右表，`on` 指定用哪一列匹配。合并后要检查行数和关键列缺失，确认匹配结果符合预期。"""
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
        """`how` 决定合并后保留哪些行。`left` 保留左表中的行，`inner` 保留两表都能匹配的行，`outer` 保留两表行的并集。实际分析中，先确认哪一张表是主表，再选择合适的合并方式。"""
    ),
    code(
        """merge_how_demo = pd.DataFrame({
    "how": ["left", "inner", "outer"],
    "行数": [
        len(finance_2020_rank_code.merge(company_small, on="证券代码", how="left")),
        len(finance_2020_rank_code.merge(company_small, on="证券代码", how="inner")),
        len(finance_2020_rank_code.merge(company_small, on="证券代码", how="outer")),
    ],
})

merge_how_demo"""
    ),
    md(
        """两个表的连接键列名不同时，可以用 `left_on` 和 `right_on`。下面做一个简短演示。"""
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
        """阶段 5 小结：我们得到了 `rank_with_info`。这一阶段带出了证券代码处理、字符串方法、日期方法、`value_counts()`、`merge()`、`how` 和合并检查。

完成本阶段后，请做最后“练习”中的阶段 5 练习。"""
    ),
    md(
        """## 阶段 6：按行业和年份做比较

目标：从公司层面的明细表，上升到行业和年份层面的比较。"""
    ),
    code(
        """analysis_df = finance_code.merge(company_small, on="证券代码", how="left")
analysis_df.head()"""
    ),
    md(
        """`groupby()` 用于“先分组，再计算”。常见写法是：

```python
df.groupby("分组列").agg(新列名=("被计算列", "统计方法"))
```

下面先做一个普通的行业汇总。"""
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
        """也可以同时按行业和年份分组。多个分组列放在列表中，例如 `groupby(["行业名称", "年份"])`。"""
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
        """`agg()` 可以同时计算多个统计量，也可以使用自定义函数。自定义函数接收一列数据，返回一个统计结果。"""
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
        """`transform()` 可以把分组结果带回到每一行。`agg()` 通常得到每组一行，`transform()` 得到和原表等长的一列，因此适合做组内比较。

下面计算 2020 年每家公司是否高于本行业平均营业收入。"""
    ),
    code(
        """industry_compare_2020 = analysis_df[analysis_df["年份"] == 2020].copy()
industry_compare_2020["行业平均收入_亿元"] = (
    industry_compare_2020
    .groupby("行业名称")["营业收入_亿元"]
    .transform("mean")
)
industry_compare_2020["高于行业平均"] = (
    industry_compare_2020["营业收入_亿元"] > industry_compare_2020["行业平均收入_亿元"]
)

industry_compare_2020[[
    "行业名称", "证券简称", "营业收入_亿元", "行业平均收入_亿元", "高于行业平均"
]].head(10)"""
    ),
    md(
        """每组取前几名的常用做法是：排序、分组、再 `head()`。"""
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
        """`concat()` 还可以横向或纵向拼接表。横向拼接时，它会按索引对齐。和按当前显示顺序直接粘贴相比，按索引对齐更适合保留行标签的含义。"""
    ),
    code(
        """left = pd.Series(["A", "B", "C"], index=[1, 2, 3], name="name")
right = pd.Series([90, 80, 70], index=[3, 2, 1], name="score")

pd.concat([left, right], axis=1)"""
    ),
    md(
        """按当前行顺序拼接时，可以先重置索引。"""
    ),
    code(
        """pd.concat(
    [left.reset_index(drop=True), right.reset_index(drop=True)],
    axis=1,
)"""
    ),
    md(
        """阶段 6 小结：这一阶段带出了 `groupby()`、多指标 `agg()`、自定义聚合、`transform()`、每组取前几名、分组循环和 `concat()`。

完成本阶段后，请做最后“练习”中的阶段 6 练习。"""
    ),
    md(
        """## 阶段 7：把数据整理成适合分析的形状

目标：把明细表改造成更适合回答问题的表。分析时可以根据问题重新组织数据形状。"""
    ),
    md(
        """`pivot_table()` 可以把长表整理成宽表。基本思路是指定：哪些列作为行索引，哪一列展开成新列，哪一列作为单元格里的值。

下面把公司年度营业收入整理成宽表，每家公司一行，每一年一列。"""
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
        """`set_index()` 和 `reset_index()` 常用于在“普通列”和“索引”之间切换。索引用来标识行；需要把索引重新当作普通变量使用时，可以 `reset_index()`。"""
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
        """保存结果。Excel 适合给人看，CSV 更通用。默认情况下，pandas 会把索引也保存成文件中的一列。普通表格通常使用 `index=False`。索引本身有意义时，可以先用 `reset_index()` 把它变成普通列，再保存。"""
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
        """阶段 7 小结：这一阶段带出了 `pivot_table()`、`set_index()`、`reset_index()`、构造 `Series` / `DataFrame`，以及保存 Excel 和 CSV。

完成本阶段后，请做最后“练习”中的阶段 7 练习。"""
    ),
    md(
        """## 阶段 8：时间序列入门

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
        """日期作为索引后，可以直接按日期字符串切片。`prices.loc["2020-02"]` 表示取出 2020 年 2 月的数据；`prices.loc["2020-02-10":"2020-02-20"]` 表示取出一个日期区间。"""
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
        """`resample()` 可以把高频数据汇总到较低频率。它要求索引是日期时间类型。常见写法是 `df.resample("ME").last()`，表示按月分组并取每个月最后一个观测。"""
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
        """阶段 8 小结：这一阶段带出了 `date_range()`、日期索引、按日期切片、`shift()`、`diff()`、`pct_change()`、`cumprod()` 和 `resample()`。

完成本阶段后，请做最后“练习”中的阶段 8 练习。"""
    ),
    md(
        """## 练习

下面的练习继续使用本章两张表。建议每完成一步都看一眼结果，例如使用 `head()`、`tail()`、`shape` 或者简单统计。题目中的变量名是建议变量名，便于课堂核对。

### 阶段 1 练习：先认识一张表

**练习 1.1**：查看财务表结构

读取 `finance_teaching_clean.xlsx`，赋值给变量 `finance_ex1`。显示前 5 行和后 5 行，打印行列数、列名列表和各列数据类型。

**练习 1.2**：查看关键财务指标的分布

在 `finance_ex1` 中选择 `营业收入_亿元`、`净利润_亿元`、`总资产_亿元`、`资产负债率` 四列，赋值给变量 `key_finance_ex1`。显示这四列的描述统计，并打印 2020 年样本行数。

### 阶段 2 练习：从表里取出自己需要的部分

**练习 2.1**：找出低负债且盈利的公司

暂时删除 `证券代码` 列，结果赋值给变量 `finance_no_code_ex2`。筛选 2020 年同时满足以下条件的公司：`净利润_亿元 > 0`、`资产负债率 < 0.6`。结果赋值给变量 `low_debt_profit_2020`，只保留 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`资产负债率` 四列，并按 `资产负债率` 从低到高排序。打印结果行数，并显示前 5 行。

**练习 2.2**：选出收入和资产都较高的公司

在 2020 年公司中，筛选 `营业收入_亿元` 高于当年中位数、并且 `总资产_亿元` 高于当年中位数的公司，赋值给变量 `large_revenue_asset_2020`。显示 `证券简称`、`营业收入_亿元`、`总资产_亿元`、`资产负债率`，并查看前 5 行和后 5 行。

### 阶段 3 练习：修改表，生成新信息

**练习 3.1**：找出收入高但净利率较低的公司

在 `finance_no_code_ex2` 中新增 `净利率 = 净利润_亿元 / 营业收入_亿元`。筛选 2020 年 `营业收入_亿元` 高于当年中位数、同时 `净利率` 低于当年中位数的公司，赋值给变量 `high_revenue_low_margin`。这个结果代表“规模不小、利润率相对偏低”的公司。再为 2020 年公司按营业收入生成 `收入排名`。显示 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`净利率`、`收入排名`，并查看前 5 行和后 5 行。

**练习 3.2**：给公司打上资产规模标签

用 `pd.cut()` 根据 `总资产_亿元` 生成 `资产规模`：`0-100` 为“小”，`100-1000` 为“中”，`1000` 以上为“大”。统计 2020 年不同 `资产规模` 的公司数量，赋值给变量 `size_counts_2020`。要求输出计数结果。

**练习 3.3**：按条件生成负债水平

在 `finance_no_code_ex2` 中新增 `负债水平`，先全部赋值为“正常”，再用 `.loc` 把 `资产负债率 >= 0.7` 的行改为“较高”。显示 `证券简称`、`年份`、`资产负债率`、`负债水平` 四列的前 8 行，并统计不同 `负债水平` 的数量。

### 阶段 4 练习：处理真实数据中的常见问题

**练习 4.1**：清洗一张带问题的小表

重新读取带代码的财务表，读取时把 `证券代码` 处理成 6 位字符串。取前 12 行，复制为 `dirty_ex1`。为练习清洗操作，加入以下情况：把第 2 行 `营业收入_亿元` 改成缺失值；把第 3 行 `净利润_亿元` 改成 `"--"`；把第 4 行 `总资产_亿元` 改成带逗号的字符串；再重复添加第 1 行。完成缺失值检查、重复行检查、去重、数值转换。最终结果赋值给变量 `dirty_ex1_clean`，要求 `总资产_亿元` 和 `净利润_亿元` 都是数值列。

**练习 4.2**：替换特殊值并填补缺失

在 `dirty_ex1_clean` 中，把 `净利润_亿元` 的缺失值填为 0，把 `营业收入_亿元` 的缺失值填为该列中位数。新增 `是否盈利` 列：`净利润_亿元 > 0` 为 `True`，否则为 `False`。输出每列缺失值数量，并显示 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`是否盈利`。

**练习 4.3**：用映射生成风险标签

根据 `资产负债率` 新增 `负债水平`：大于等于 0.7 为“较高”，否则为“正常”。再用 `map()` 把“较高”映射为“需关注”，把“正常”映射为“低风险”，生成 `负债风险`。统计不同 `负债风险` 的数量。

### 阶段 5 练习：合并公司信息并解释排名

**练习 5.1**：处理证券代码并合并行业信息

重新读取 `finance_teaching_clean.xlsx` 和 `company_profile_teaching_clean.xlsx`。读取时把 `证券代码` 处理成 6 位字符串。筛选 2020 年财务数据，与公司信息表按 `证券代码` 合并，赋值给变量 `finance_company_2020`。检查合并前后行数是否一致，并检查 `行业名称` 是否有缺失。

**练习 5.2**：找出制造业中收入最高的公司

在 `finance_company_2020` 中筛选 `行业名称` 包含“制造”的公司，赋值给变量 `manufacturing_2020`。按 `营业收入_亿元` 从高到低排序，显示前 8 行。结果应包含 `证券代码`、`证券简称`、`行业名称`、`省份`、`营业收入_亿元`、`净利润_亿元`。

**练习 5.3**：比较早上市公司和较晚上市公司

把公司表中的 `上市日期` 转为日期格式，并生成 `上市年份`。在 `finance_company_2020` 中新增 `上市阶段`：`上市年份 < 2000` 标记为“较早上市”，否则标记为“较晚上市”。分别计算两组公司的平均 `营业收入_亿元` 和平均 `净利率`。

### 阶段 6 练习：按行业和年份汇总

**练习 6.1**：行业年度摘要表

把财务表和公司信息表合并为 `analysis_ex6`。按 `行业名称` 和 `年份` 分组，计算 `公司数`、`营业收入合计_亿元`、`平均净利率`、`平均资产负债率`，赋值给变量 `industry_year_summary`。显示前 12 行。

**练习 6.2**：每个行业找两家公司

在 2020 年数据中，按 `行业名称` 分组，找出每个行业 `营业收入_亿元` 最高的 2 家公司，赋值给变量 `top2_revenue_by_industry`。结果只保留 `行业名称`、`证券代码`、`证券简称`、`营业收入_亿元`、`净利率`，并按行业名称和营业收入排序。

**练习 6.3**：计算行业内部收入差距

自定义函数 `value_range(x)`，返回 `x.max() - x.min()`。按 `行业名称` 分组，计算 2020 年各行业营业收入的均值和收入差距，赋值给变量 `industry_gap_2020`。按收入差距从高到低排序。

**练习 6.4**：判断公司是否高于行业平均

在 2020 年数据中，用 `groupby()` 和 `transform()` 计算每家公司所在行业的平均营业收入，生成 `行业平均收入_亿元`。再生成 `高于行业平均`，表示该公司营业收入是否高于所在行业平均值。显示 `行业名称`、`证券简称`、`营业收入_亿元`、`行业平均收入_亿元`、`高于行业平均`，并查看前 10 行。

### 阶段 7 练习：重建分析表

**练习 7.1**：构造公司收入宽表

用 `pivot_table()` 把 `analysis_ex6` 整理为每家公司一行、年份为列、值为 `营业收入_亿元` 的宽表，赋值给变量 `revenue_wide_ex7`。计算 `收入增长率_2018_2020 = 2020 / 2018 - 1`，按增长率从高到低排序，显示前 10 行。

**练习 7.2**：构造公司综合摘要表

基于 `analysis_ex6` 构造 `company_profile_summary`，每家公司一行，至少包含：`证券代码`、`证券简称`、`行业名称`、`省份`、`2018` 年营业收入、`2020` 年营业收入、`收入增长率_2018_2020`、`2020` 年资产负债率。按 `收入增长率_2018_2020` 从高到低排序，显示前 10 行。

**练习 7.3**：核对公司摘要表

检查 `company_profile_summary` 的行数是否等于公司数量。再按 `行业名称` 统计公司数量，并显示统计结果。最后显示 `company_profile_summary` 的前 5 行和后 5 行。

### 阶段 8 练习：时间序列入门

**练习 8.1**：构造价格序列并计算收益率

构造 2021 年 1 月到 2021 年 6 月的工作日日期。使用随机数生成一列日收益率 `return`，从初始价格 100 出发构造价格 `price`。把结果赋值给以日期为索引的变量 `price_df`，并新增 `lag_price`、`diff`、`pct_return` 三列。显示前 8 行。

**练习 8.2**：按月份观察价格变化

从 `price_df` 中筛选 2021 年 3 月的数据，赋值给变量 `march_price`。显示前 5 行和后 5 行。然后用 `resample("ME").last()` 得到月末价格，赋值给变量 `month_end_price_ex8`。

**练习 8.3**：从月末价格计算月收益

基于 `month_end_price_ex8` 计算月收益率，赋值给变量 `month_return_ex8`。找出月收益率最高的月份和最低的月份，并打印对应月份和收益率。"""
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
