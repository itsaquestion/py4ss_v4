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

**阶段 1：数据读取与初步查看**

读入财务表，查看前几行、后几行、行列数、列名、数据类型和描述统计。先知道表里有什么，再决定后面怎么处理。

**阶段 2：行列选择与条件筛选**

围绕“在行与列上操作”展开：选单列、选多列、`iloc`、`loc`、条件筛选、复合条件、同时选行和列、`query()`，以及筛选后查看结果。

**阶段 3：变量生成与数据修改**

用已有列生成新列，做列运算，覆盖已有列，用 `np.where()`、`pd.cut()` 和带筛选的 `.loc` 赋值，排序、排名，并做简单统计。

**阶段 4：常见数据问题处理**

建立工作副本，检查缺失值和重复值，处理特殊文本，转换数据类型，使用 `dropna()`、`fillna()`、`replace()`、`map()`，并理解链式赋值 warning。

**阶段 5：多表合并与背景信息补充**

处理作为编号的证券代码，使用字符串方法和日期方法，使用 `concat()` 追加同结构表，整理公司信息表，用 `merge()` 合并，并检查合并结果。

**阶段 6：分组汇总与组内比较**

从公司明细表转向分组结论：`groupby()`、多指标 `agg()`、自定义聚合函数、`transform()`、每组取前几名和分组循环。

**阶段 7：数据重塑与结果表构造**

理解长表和宽表，使用 `pivot_table()`、`set_index()`、`reset_index()`，构造 `Series` / `DataFrame`，并导出结果。

**阶段 8：时间序列数据入门**

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
        """## 阶段 1：数据读取与初步查看

拿到一张新表时，先不要急着计算。第一步是确认数据是否读对了：表有多大、有哪些列、每列大致是什么类型、数值范围是否看起来合理。本阶段先读入年度财务表，并建立对这张表的整体认识。"""
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
        """## 阶段 2：行列选择与条件筛选

多数情况下，我们要处理的数据只是现有数据的一部分，所以需要先按分析要求把数据切出来。比如在这张财务表中，如果想观察 2020 年盈利、收入数据完整、负债率相对不高的公司，就要先筛选出这些公司，再只保留后面要比较的财务列。

范例：选出 2020 年、净利润为正、营业收入不缺失、资产负债率低于 0.7 的公司，作为下一步观察的名单。"""
    ),
    md(
        """**DataFrame 和 Series 的结构**

在 pandas 中，一张表可以拆成几个部分来看：

1. `df.index`：行索引，用来标识每一行。

2. `df.columns`：列名，用来标识每一列。

3. `df.values`：表格中的值。

4. `df["A"]`：从 DataFrame 中取出一列，会得到一个 `Series`。`Series` 也有自己的 `index` 和 `values`。

![](images/df_structure_breakdown.png)"""
    ),
    md(
        """**选择列**

1. `df["列名"]`：用列名选择单列，返回 `Series`。`Series` 可以理解为一列数据。

2. `df[[列名列表]]`：用列名的 list 选择多列，返回 `DataFrame`。这里可以用上前面学过的 list 写法，例如 `["证券简称", "年份"]`。

3. `type()`：查看对象类型。这里用它区分 `Series` 和 `DataFrame`。"""
    ),
    code(
        """one_col = finance["营业收入_亿元"]  # 用列名选择单列
one_col.head()  # 查看单列数据"""
    ),
    code(
        """type(one_col)  # 查看单列对象类型"""
    ),
    code(
        """some_cols = finance[["证券简称", "年份", "营业收入_亿元"]]  # 用列名 list 选择多列
some_cols.head()  # 查看多列数据"""
    ),
    code(
        """type(some_cols)  # 查看多列对象类型"""
    ),
    code(
        """finance[["证券简称", "年份", "营业收入_亿元", "净利润_亿元"]].head()  # 查看多列结果"""
    ),
    md(
        """**按位置和标签选择**

1. `.iloc[行位置, 列位置]`：按整数位置选择。行和列都使用从 0 开始的顺序位置。

2. `.iloc` 切片：写法和列表切片类似，`起点:终点` 表示从起点取到终点之前，不包括终点。例如 `:5` 表示位置 0 到 4。

3. `.loc[行标签, 列标签]`：按标签选择。行标签可以是索引标签，也可以是筛选条件；列标签可以是一个列名，也可以是列名列表。

4. `.loc` 标签切片：按标签切片时包含结束点，这和 Python 列表切片不同。"""
    ),
    code(
        """finance.iloc[:5, :4]  # 前 5 行、前 4 列"""
    ),
    code(
        """# 查看 2020 年公司的几个关键财务列。
finance.loc[
    finance["年份"] == 2020,  # 行位置：筛选 2020 年
    ["证券简称", "营业收入_亿元", "净利润_亿元", "资产负债率"],  # 列位置：保留指定列
].head()  # 查看前 5 行"""
    ),
    code(
        """finance.loc[0:3, "证券简称":"营业收入_亿元"]  # 标签切片包含结束点"""
    ),
    md(
        """**条件筛选**

1. `df["列"] == 值`：生成一组 `True` / `False`，可以放到 `.loc` 的行位置，保留满足条件的行。

2. `&` / `|` / `~`：分别表示“并且”“或者”“取反”。复合条件中，每个条件外面都要加括号。

3. `.notna()`：判断是否不是缺失值。筛选时常用来保留关键列有值的行。

4. `len()`：查看结果有多少行。筛选后通常要看一下行数和前后几行。"""
    ),
    code(
        """# 筛选出 2020 年、盈利、收入不缺失且负债率较低的公司。
good_2020 = finance.loc[
    (finance["年份"] == 2020)  # 条件 1：2020 年
    & (finance["净利润_亿元"] > 0)  # 条件 2：净利润为正
    & (finance["营业收入_亿元"].notna())  # 条件 3：营业收入不是缺失值
    & (finance["资产负债率"] < 0.7),  # 条件 4：资产负债率小于 0.7
    ["证券简称", "营业收入_亿元", "净利润_亿元", "资产负债率"],  # 保留指定列
]

good_2020.head()  # 查看筛选结果"""
    ),
    code(
        """len(good_2020)  # 查看筛选结果行数"""
    ),
    code(
        """good_2020.tail()  # 查看筛选结果末尾"""
    ),
    md(
        """**用字符串写筛选条件**

1. `query("条件")`：把筛选条件写成字符串，列名可以直接出现在字符串里。条件较短时，这种写法很方便。

2. `and` / `or` / `not`：在 `query()` 字符串里可以表示“并且”“或者”“取反”。"""
    ),
    code(
        """finance.query("年份 == 2020 and 净利润_亿元 > 0").head()  # 用 query 筛选"""
    ),
    md(
        """阶段 2 小结：想从表中取出一部分数据，可以按列名选列，用 `iloc` 按位置选，用 `loc` 按标签或条件选；条件较短时，`query()` 也很方便。筛选之后用 `head()`、`tail()` 和行数看一眼结果。

**练习**：完成最后的阶段 2 练习。"""
    ),
    md(
        """## 阶段 3：变量生成与数据修改

选出需要的数据后，很多分析还要把原始字段转换成更接近问题的变量。比如营业收入和净利润可以说明规模和利润，但要比较盈利能力，还需要计算净利率；要观察财务风险，也可以把资产负债率转换成负债水平标签。

范例：在原始财务指标基础上生成净利率、资产收益率、资产规模、负债水平等新变量，并整理出 2020 年公司表现排名。"""
    ),
    md(
        """**用已有列生成新列**

1. `df["新列"] = 表达式`：新增一列，写法和给字典增加新键类似。

2. `列运算`：表达式可以来自一列，也可以来自多列共同计算。例如净利率可以由净利润除以营业收入得到。

3. `比较运算`：例如 `df["净利润_亿元"] > 0` 会得到一列 `True` / `False`，可以直接作为新列。

4. `pd.cut()`：把连续数值分成几个区间，常用于生成“高、中、低”这类分组变量。"""
    ),
    code(
        """# 从原始财务列生成几个更适合比较的新变量。
finance["净利率"] = finance["净利润_亿元"] / finance["营业收入_亿元"]  # 用两列计算新列
finance["资产收益率"] = finance["净利润_亿元"] / finance["总资产_亿元"]  # 用两列计算新列
finance["是否盈利"] = finance["净利润_亿元"] > 0  # 比较结果生成布尔列
finance["资产规模"] = pd.cut(
    finance["总资产_亿元"],  # 要分箱的连续变量
    bins=[0, 100, 1000, np.inf],  # 分箱边界
    labels=["小", "中", "大"],  # 每个区间的标签
)

finance[["证券简称", "年份", "净利率", "资产收益率", "是否盈利", "资产规模"]].head()  # 查看新列"""
    ),
    md(
        """**按条件修改数据**

1. `np.where(条件, 条件成立时的值, 条件不成立时的值)`：适合二选一地生成新列。

2. `.loc[条件, 列名] = 新值`：适合对满足条件的行局部修改。

3. `df[条件]["列"] = 新值`：这类连续使用 `[]` 的写法称为链式赋值。pandas 不一定能判断你想修改原表还是临时结果，因此容易触发 warning；有时 warning 后原表并没有被修改。

4. `df.loc[条件, "列"] = 新值`：需要修改原表时，课堂和作业中建议使用这种写法。"""
    ),
    code(
        """# 根据资产负债率生成负债水平标签。
finance["负债水平"] = np.where(
    finance["资产负债率"] >= 0.7,  # 条件
    "较高",  # 条件成立时的值
    "正常",  # 条件不成立时的值
)

finance[["证券简称", "年份", "资产负债率", "负债水平"]].head()  # 查看条件生成结果"""
    ),
    code(
        """# 用 .loc 把高负债公司标记为重点关注。
finance["重点关注"] = False  # 先给整列一个默认值
finance.loc[finance["资产负债率"] >= 0.7, "重点关注"] = True  # 按条件局部修改
finance[["证券简称", "年份", "资产负债率", "重点关注"]].head()  # 查看局部修改结果"""
    ),
    md(
        """**排序和排名**

1. `sort_values()`：按一列或多列排序。`ascending=False` 表示从大到小排序；多列排序时可以给 `ascending` 传入列表。

2. `rank()`：生成排名。排序适合查看结果；如果需要把排名作为一列继续使用，可以用 `rank()`。

3. `.astype(int)`：把结果转换为整数类型。排名本身常常希望显示为整数。"""
    ),
    code(
        """# 得到 2020 年公司表现排名表。
finance_2020_rank = (
    finance[finance["年份"] == 2020]  # 筛选 2020 年
    .sort_values(["营业收入_亿元", "净利率"], ascending=[False, False])  # 按收入和净利率降序
)

finance_2020_rank[[
    "证券简称", "营业收入_亿元", "净利润_亿元", "净利率", "资产收益率", "资产负债率", "负债水平"
]].head(10)  # 查看排名靠前的公司"""
    ),
    code(
        """# 把营业收入排名保存成一列，便于后续继续使用。
finance_2020_rank["收入排名"] = (
    finance_2020_rank["营业收入_亿元"]
    .rank(ascending=False, method="min")  # 按营业收入从大到小排名
    .astype(int)  # 转成整数
)

finance_2020_rank[["证券简称", "营业收入_亿元", "收入排名"]].head(10)  # 查看排名列"""
    ),
    code(
        """# 查看排名尾部，理解结果的另一端。
finance_2020_rank[[
    "证券简称", "营业收入_亿元", "净利润_亿元", "净利率", "资产负债率"
]].tail(5)  # 查看排名尾部"""
    ),
    md(
        """**简单统计和展示列名**

1. `nunique()`：计算不重复取值数量。这里用于计算公司数量。

2. `mean()` / `max()`：分别计算平均值和最大值。

3. `describe()`：查看多列描述统计。

4. `rename(columns={...})`：重命名列。常用于把结果表整理成更适合展示的样子。"""
    ),
    code(
        """# 计算 2020 年样本中的公司数量。
finance_2020 = finance[finance["年份"] == 2020]  # 取出 2020 年样本
finance_2020["证券简称"].nunique()  # 计算公司数量"""
    ),
    code(
        """finance_2020["营业收入_亿元"].mean()  # 计算营业收入平均值"""
    ),
    code(
        """finance_2020["营业收入_亿元"].max()  # 计算营业收入最大值"""
    ),
    code(
        """finance_2020[["营业收入_亿元", "净利润_亿元", "资产负债率", "净利率"]].describe()  # 查看多列描述统计"""
    ),
    code(
        """rank_display = finance_2020_rank.rename(
    columns={
        "营业收入_亿元": "营业收入",  # 改短列名
        "净利润_亿元": "净利润",  # 改短列名
    }
)

rank_display[["证券简称", "营业收入", "净利润", "净利率"]].head()  # 查看展示表"""
    ),
    md(
        """阶段 3 小结：我们得到了 `finance_2020_rank`。这一阶段带出了列运算、新增列、按条件赋值、`np.where()`、`pd.cut()`、排序、排名和简单统计。

**练习**：完成最后的阶段 3 练习。"""
    ),
    md(
        """## 阶段 4：常见数据问题处理

真实数据进入统计和合并前，通常要先检查会影响结果的问题。比如收入缺失会影响均值，重复记录会影响计数，数字列里混入 `--` 或带逗号的文本会影响计算，空字符串也可能让分类结果看起来正常但实际不完整。

范例：用一张带问题的小表，找出并处理缺失值、重复行、特殊文本、数字被读成文本、空字符串和标签映射。"""
    ),
    md(
        """**构造清洗样本**

1. `.copy()`：复制一份工作副本。清洗时先在副本上操作，可以保留原始表。

2. `.astype("object")`：把列临时转成可以混放文本和数字的类型，便于演示数字列里混入特殊文本的情况。

3. `np.nan`：表示缺失值。"""
    ),
    code(
        """# 从原始财务表复制出一份练习用的小表，并人为放入几类常见问题。
dirty = finance_raw.head(12).copy()  # 复制工作副本
dirty["负债水平"] = np.where(dirty["资产负债率"] >= 0.7, "较高", "正常")  # 生成演示用标签列
dirty[["总资产_亿元", "净利润_亿元"]] = dirty[["总资产_亿元", "净利润_亿元"]].astype("object")

dirty.loc[1, "营业收入_亿元"] = np.nan  # 放入缺失值
dirty.loc[2, "净利润_亿元"] = "--"  # 数字列混入特殊文本
dirty.loc[3, "总资产_亿元"] = "15,285.79"  # 数字列混入带逗号文本
dirty.loc[4, "负债水平"] = ""  # 文本列出现空字符串
dirty.loc[len(dirty)] = dirty.loc[0]  # 复制第 1 行，制造一行重复记录

dirty.head()  # 查看带问题的小表"""
    ),
    md(
        """**检查缺失值和重复行**

1. `isna()`：判断每个位置是否为缺失值。

2. `sum()`：对 `True` / `False` 求和时，`True` 会按 1 计算，因此 `isna().sum()` 可以统计每列缺失值数量。

3. `duplicated()`：判断每一行是否和前面的行重复。"""
    ),
    code(
        """dirty.isna().sum()  # 统计每列缺失值数量"""
    ),
    code(
        """dirty.duplicated().sum()  # 统计重复行数量"""
    ),
    md(
        """**删除重复行并清理特殊文本**

1. `drop_duplicates()`：删除重复行。

2. `.str.replace()`：使用字符串方法替换文本内容。这里把数字字符串中的逗号去掉。

3. `.mask(条件, 新值)`：把满足条件的位置替换成新值。

4. `pd.to_numeric(errors="coerce")`：把数据转成数值；无法转换的内容会变成缺失值。"""
    ),
    code(
        """dirty = dirty.drop_duplicates().copy()  # 删除重复行，并复制为新的工作表
len(dirty)  # 查看删除重复后的行数"""
    ),
    code(
        """# 把总资产列里带逗号的文本清理成真正的数值。
dirty["总资产_亿元"] = (
    dirty["总资产_亿元"]
    .astype(str)  # 先统一转成字符串
    .str.replace(",", "", regex=False)  # 去掉逗号
)
dirty["总资产_亿元"] = pd.to_numeric(dirty["总资产_亿元"], errors="coerce")  # 转成数值

dirty[["证券简称", "总资产_亿元"]].head()  # 查看转换结果"""
    ),
    code(
        """# 把净利润列里的特殊文本清理成缺失值，再转成数值。
dirty["净利润_亿元"] = dirty["净利润_亿元"].mask(dirty["净利润_亿元"] == "--", np.nan)  # 特殊文本替换为缺失值
dirty["净利润_亿元"] = pd.to_numeric(dirty["净利润_亿元"], errors="coerce")  # 转成数值

dirty[["证券简称", "净利润_亿元"]].head()  # 查看转换结果"""
    ),
    md(
        """**删除或填补缺失值**

1. `dropna(subset=[...])`：只检查指定列，删除这些列中有缺失值的行。

2. `fillna()`：把缺失值替换成指定数值。

3. `median()`：计算中位数。用中位数填补数值列，是一种常见演示做法。

4. `replace()`：替换指定取值。这里把空字符串替换成“未知”。"""
    ),
    code(
        """drop_missing = dirty.dropna(subset=["营业收入_亿元", "净利润_亿元"])  # 删除关键列缺失的行
drop_missing.head()  # 查看删除缺失后的结果"""
    ),
    code(
        """# 填补缺失值，并替换文本列中的空字符串。
fill_missing = dirty.copy()  # 复制一份用于填补缺失的表
fill_missing["营业收入_亿元"] = fill_missing["营业收入_亿元"].fillna(
    fill_missing["营业收入_亿元"].median()  # 用中位数填补营业收入缺失
)
fill_missing["净利润_亿元"] = fill_missing["净利润_亿元"].fillna(0)  # 用 0 填补净利润缺失
fill_missing["负债水平"] = fill_missing["负债水平"].replace({"": "未知"})  # 替换空字符串

fill_missing.isna().sum()  # 检查填补后的缺失值数量"""
    ),
    md(
        """**控制 `dropna()` 的删除规则**

1. `subset`：指定检查哪些列。

2. `axis=1`：按列删除。默认 `axis=0` 是按行删除。

3. `how="all"`：整行或整列全部缺失时才删除。"""
    ),
    code(
        """# 构造一张小表，演示 dropna() 的参数。
dropna_demo = pd.DataFrame({
    "A": [1, np.nan, np.nan],
    "B": [2, np.nan, np.nan],
    "C": [np.nan, np.nan, np.nan],
})

dropna_demo  # 查看演示表"""
    ),
    code(
        """dropna_demo.dropna(how="all")  # 删除全部缺失的行"""
    ),
    code(
        """dropna_demo.dropna(axis=1, how="all")  # 删除全部缺失的列"""
    ),
    md(
        """**映射和替换**

1. `map()`：把一组取值映射成另一组取值。常见写法是先准备一个字典，再把原来的取值替换成新的标签。

2. `replace()`：替换特殊值。和 `map()` 相比，`replace()` 更常用于把少数异常取值替换掉。"""
    ),
    code(
        """debt_map = {"正常": "低风险", "较高": "需关注", "未知": "待确认"}  # 定义映射规则
fill_missing["负债风险"] = fill_missing["负债水平"].map(debt_map)  # 根据负债水平生成风险标签

fill_missing[["证券简称", "负债水平", "负债风险"]].head()  # 查看映射结果"""
    ),
    code(
        """special = pd.Series([1, 2, 999, -1, 5], name="原始值")  # 构造包含特殊编码的 Series
special.replace({999: np.nan, -1: 0})  # 替换特殊值"""
    ),
    md(
        """### 副本、视图和链式赋值

直接修改数据时，建议优先使用：

```python
df.loc[条件, 列名] = 新值
```

筛选出一部分数据再修改时，显式使用 `.copy()` 生成工作副本。这样更容易判断后续操作影响的是哪一张表。连续使用 `df[条件]["列"] = 新值` 这类链式赋值，pandas 往往会给出 warning，也可能没有改到原表。"""
    ),
    md(
        """阶段 4 小结：这一阶段带出了 `isna()`、`dropna()`、`axis`、`how`、`fillna()`、`duplicated()`、`drop_duplicates()`、`replace()`、`pd.to_numeric()`、`map()`、工作副本和链式赋值 warning。

**练习**：完成最后的阶段 4 练习。"""
    ),
    md(
        """## 阶段 5：多表合并与背景信息补充

很多问题需要把不同表的信息放在一起看。财务表可以说明公司表现，公司信息表可以补充行业、地区和上市时间；两张表都包含证券代码，就可以用它把同一家公司对应起来。

范例：把 2020 年公司表现排名和公司信息表合并，让排名结果带上行业、省份、城市、上市日期等背景信息。"""
    ),
    md(
        """**读取连接键，并处理编号列**

1. `连接键`：两张表中用来匹配记录的列。这里用 `证券代码` 把财务表和公司信息表连起来。

2. `converters={...}`：读取 Excel 时指定某些列的转换规则。

3. `str(x).strip().zfill(6)`：把代码转成字符串，去掉两端空格，并补齐到 6 位。证券代码是编号，不适合作为普通数值处理。"""
    ),
    code(
        """# 读取两张表，并把证券代码处理成 6 位字符串。
def read_code(x):
    return str(x).strip().zfill(6)  # 转字符串、去空格、补齐 6 位

finance_code = pd.read_excel(
    "data/finance_teaching_clean.xlsx",
    converters={"证券代码": read_code},  # 读取时处理证券代码
)

company = pd.read_excel(
    "data/company_profile_teaching_clean.xlsx",
    converters={"证券代码": read_code},  # 读取时处理证券代码
)

finance_code.head()  # 查看财务表"""
    ),
    code(
        """company.head()  # 查看公司信息表"""
    ),
    md(
        """**纵向追加同结构表**

1. `pd.concat([表1, 表2, ...], ignore_index=True)`：把列结构相同或相近的表纵向接在一起。

2. `ignore_index=True`：拼接后重新生成连续索引。追加多张同结构表时，通常使用这个参数。

3. `concat()` 和 `merge()` 解决的问题不同：`concat()` 是把记录追加到一起，`merge()` 是按连接键把不同信息匹配到同一行。"""
    ),
    code(
        """# 把两个年度的财务记录纵向追加到一起。
finance_2019 = finance_code.loc[finance_code["年份"] == 2019].copy()  # 取出 2019 年记录
finance_2020_for_concat = finance_code.loc[finance_code["年份"] == 2020].copy()  # 取出 2020 年记录

finance_two_years = pd.concat(
    [finance_2019, finance_2020_for_concat],  # 要追加的表
    ignore_index=True,  # 重新生成连续索引
)

finance_two_years[["证券代码", "证券简称", "年份", "营业收入_亿元"]].head()  # 查看追加结果"""
    ),
    code(
        """finance_two_years["年份"].value_counts().sort_index()  # 检查追加后的年度记录数"""
    ),
    md(
        """**处理文本列和日期列**

1. `.str.strip()`：去掉文本两端空格。

2. `pd.to_datetime()`：把日期列转换成 pandas 能识别的日期类型。

3. `.dt.year` / `.dt.month` / `.dt.quarter`：从日期列中提取年份、月份、季度。

4. `.str.contains("关键词", na=False)`：判断文本是否包含关键词；`na=False` 表示缺失值按“不包含”处理。

5. `value_counts()`：统计每个取值出现的次数。"""
    ),
    code(
        """# 整理公司信息表中的文本列和日期列。
company = company.copy()  # 复制工作副本
company["证券简称"] = company["证券简称"].str.strip()  # 去掉简称两端空格
company["行业名称"] = company["行业名称"].str.strip()  # 去掉行业名称两端空格
company["上市日期"] = pd.to_datetime(company["上市日期"])  # 转换为日期类型
company["上市年份"] = company["上市日期"].dt.year  # 提取上市年份
company["是否ST"] = company["证券简称"].str.contains("ST", na=False)  # 判断简称是否包含 ST

company.head()  # 查看处理后的公司信息表"""
    ),
    code(
        """company["行业名称"].value_counts()  # 统计各行业公司数量"""
    ),
    code(
        """# 筛选行业名称中包含“制造”的公司。
manufacturing = company.loc[
    company["行业名称"].str.contains("制造", na=False),  # 文本包含“制造”
    ["证券代码", "证券简称", "行业名称", "省份"],  # 保留指定列
]

manufacturing.head()  # 查看制造业相关公司"""
    ),
    code(
        """len(manufacturing)  # 统计制造业相关公司数量"""
    ),
    code(
        """manufacturing.tail()  # 查看筛选结果尾部"""
    ),
    code(
        """# 筛选简称中包含 ST 的公司。
st_companies = company.loc[
    company["证券简称"].str.contains("ST", na=False),  # 文本包含 ST
    ["证券代码", "证券简称", "行业名称", "上市年份"],  # 保留指定列
]

st_companies  # 查看 ST 公司"""
    ),
    code(
        """# 提取上市月份和季度，并筛选较早上市的公司。
company["上市月份"] = company["上市日期"].dt.month  # 提取月份
company["上市季度"] = company["上市日期"].dt.quarter  # 提取季度

old_listed = company.loc[
    company["上市年份"] < 2000,  # 筛选 2000 年以前上市
    ["证券代码", "证券简称", "行业名称", "上市日期", "上市年份", "上市月份", "上市季度"],  # 保留指定列
].sort_values("上市日期")  # 按上市日期排序

old_listed.head()  # 查看较早上市公司"""
    ),
    code(
        """old_listed.tail()  # 查看较早上市公司尾部"""
    ),
    md(
        """**准备合并用的两张表**

1. 左表：财务表。这里保留 2020 年公司表现排名。

2. 右表：公司信息表。合并前只保留后面分析需要的背景列。

3. 合并前先整理左右表，可以减少合并后的无关列。"""
    ),
    code(
        """# 重新在带证券代码的财务表中生成前面用到的财务指标。
finance_code["净利率"] = finance_code["净利润_亿元"] / finance_code["营业收入_亿元"]  # 生成净利率
finance_code["资产收益率"] = finance_code["净利润_亿元"] / finance_code["总资产_亿元"]  # 生成资产收益率
finance_code["是否盈利"] = finance_code["净利润_亿元"] > 0  # 生成盈利标记
finance_code["负债水平"] = np.where(finance_code["资产负债率"] >= 0.7, "较高", "正常")  # 生成负债水平

finance_2020_rank_code = (
    finance_code[finance_code["年份"] == 2020]  # 筛选 2020 年
    .sort_values("营业收入_亿元", ascending=False)  # 按营业收入降序
)

finance_2020_rank_code.head()  # 查看左表"""
    ),
    code(
        """company_small = company[
    ["证券代码", "行业名称", "省份", "城市", "上市市场", "上市日期", "上市年份", "是否ST"]  # 保留需要的背景列
]

company_small.head()  # 查看右表"""
    ),
    md(
        """**合并并检查结果**

1. `merge()`：按共同字段合并两张表。

2. `on="共同列名"`：指定用哪一列匹配。

3. `how="left"`：保留左表所有行，把右表能匹配的信息接上来。

4. 合并后检查：通常检查合并前后行数、关键列缺失数量，并看几行结果。"""
    ),
    code(
        """rank_with_info = finance_2020_rank_code.merge(
    company_small,
    on="证券代码",  # 按证券代码匹配
    how="left",  # 保留左表所有行
)

rank_with_info[[
    "证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利率", "上市年份"
]].head(10)  # 查看合并结果"""
    ),
    code(
        """len(finance_2020_rank_code)  # 合并前行数"""
    ),
    code(
        """len(rank_with_info)  # 合并后行数"""
    ),
    code(
        """rank_with_info["行业名称"].isna().sum()  # 检查行业名称缺失数量"""
    ),
    code(
        """rank_with_info[[
    "证券代码", "证券简称", "行业名称", "省份", "营业收入_亿元", "净利率", "上市年份"
]].tail(5)  # 查看合并结果尾部"""
    ),
    md(
        """**合并方式和不同列名的连接键**

1. `how="left"`：保留左表中的行。

2. `how="inner"`：只保留两表都能匹配的行。

3. `how="outer"`：保留两表行的并集。

4. `left_on` / `right_on`：两张表的连接键列名不同时，分别指定左表和右表的连接键。"""
    ),
    code(
        """# 比较不同 how 参数得到的行数。
merge_how_demo = pd.DataFrame({
    "how": ["left", "inner", "outer"],
    "行数": [
        len(finance_2020_rank_code.merge(company_small, on="证券代码", how="left")),  # left 合并行数
        len(finance_2020_rank_code.merge(company_small, on="证券代码", how="inner")),  # inner 合并行数
        len(finance_2020_rank_code.merge(company_small, on="证券代码", how="outer")),  # outer 合并行数
    ],
})

merge_how_demo  # 查看不同合并方式的行数"""
    ),
    code(
        """# 演示左右表连接键列名不同时的合并。
company_key_demo = company_small.rename(columns={"证券代码": "公司代码"})  # 改右表连接键列名

demo_merge = finance_2020_rank_code.merge(
    company_key_demo,
    left_on="证券代码",  # 左表连接键
    right_on="公司代码",  # 右表连接键
    how="left",  # 保留左表所有行
)

demo_merge[["证券代码", "公司代码", "行业名称"]].head()  # 查看不同列名连接键"""
    ),
    md(
        """阶段 5 小结：我们得到了 `rank_with_info`。这一阶段带出了证券代码处理、`concat()`、字符串方法、日期方法、`value_counts()`、`merge()`、`how` 和合并检查。

**练习**：完成最后的阶段 5 练习。"""
    ),
    md(
        """## 阶段 6：分组汇总与组内比较

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
        """分组循环适合处理每组内部较复杂的逻辑。循环得到的结果可以复用前面学过的 `concat()` 合并回来。"""
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
        """`concat()` 横向拼接时，会按索引对齐。和按当前显示顺序直接粘贴相比，按索引对齐更适合保留行标签的含义。"""
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
        """阶段 6 小结：这一阶段带出了 `groupby()`、多指标 `agg()`、自定义聚合、`transform()`、每组取前几名和分组循环。

**练习**：完成最后的阶段 6 练习。"""
    ),
    md(
        """## 阶段 7：数据重塑与结果表构造

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

**练习**：完成最后的阶段 7 练习。"""
    ),
    md(
        """## 阶段 8：时间序列数据入门

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

**练习**：完成最后的阶段 8 练习。"""
    ),
    md(
        """## 练习

下面的练习继续使用本章两张表。建议每完成一步都看一眼结果，例如使用 `head()`、`tail()`、`shape` 或者简单统计。题目中的变量名是建议变量名，便于课堂核对。

### 阶段 1 练习：数据读取与初步查看

**练习 1.1**：查看财务表结构

读取 `finance_teaching_clean.xlsx`，赋值给变量 `finance_ex1`。显示前 5 行和后 5 行，打印行列数、列名列表和各列数据类型。

**练习 1.2**：查看关键财务指标的分布

在 `finance_ex1` 中选择 `营业收入_亿元`、`净利润_亿元`、`总资产_亿元`、`资产负债率` 四列，赋值给变量 `key_finance_ex1`。显示这四列的描述统计，并打印 2020 年样本行数。

### 阶段 2 练习：行列选择与条件筛选

**练习 2.1**：找出低负债且盈利的公司

暂时删除 `证券代码` 列，结果赋值给变量 `finance_no_code_ex2`。筛选 2020 年同时满足以下条件的公司：`净利润_亿元 > 0`、`资产负债率 < 0.6`。结果赋值给变量 `low_debt_profit_2020`，只保留 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`资产负债率` 四列，并按 `资产负债率` 从低到高排序。打印结果行数，并显示前 5 行。

**练习 2.2**：选出收入和资产都较高的公司

在 2020 年公司中，筛选 `营业收入_亿元` 高于当年中位数、并且 `总资产_亿元` 高于当年中位数的公司，赋值给变量 `large_revenue_asset_2020`。显示 `证券简称`、`营业收入_亿元`、`总资产_亿元`、`资产负债率`，并查看前 5 行和后 5 行。

### 阶段 3 练习：变量生成与数据修改

**练习 3.1**：找出收入高但净利率较低的公司

在 `finance_no_code_ex2` 中新增 `净利率 = 净利润_亿元 / 营业收入_亿元`。筛选 2020 年 `营业收入_亿元` 高于当年中位数、同时 `净利率` 低于当年中位数的公司，赋值给变量 `high_revenue_low_margin`。这个结果代表“规模不小、利润率相对偏低”的公司。再为 2020 年公司按营业收入生成 `收入排名`。显示 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`净利率`、`收入排名`，并查看前 5 行和后 5 行。

**练习 3.2**：给公司打上资产规模标签

用 `pd.cut()` 根据 `总资产_亿元` 生成 `资产规模`：`0-100` 为“小”，`100-1000` 为“中”，`1000` 以上为“大”。统计 2020 年不同 `资产规模` 的公司数量，赋值给变量 `size_counts_2020`。要求输出计数结果。

**练习 3.3**：按条件生成负债水平

在 `finance_no_code_ex2` 中新增 `负债水平`，先全部赋值为“正常”，再用 `.loc` 把 `资产负债率 >= 0.7` 的行改为“较高”。显示 `证券简称`、`年份`、`资产负债率`、`负债水平` 四列的前 8 行，并统计不同 `负债水平` 的数量。

### 阶段 4 练习：常见数据问题处理

**练习 4.1**：清洗一张带问题的小表

重新读取带代码的财务表，读取时把 `证券代码` 处理成 6 位字符串。取前 12 行，复制为 `dirty_ex1`。为练习清洗操作，加入以下情况：把第 2 行 `营业收入_亿元` 改成缺失值；把第 3 行 `净利润_亿元` 改成 `"--"`；把第 4 行 `总资产_亿元` 改成带逗号的字符串；再重复添加第 1 行。完成缺失值检查、重复行检查、去重、数值转换。最终结果赋值给变量 `dirty_ex1_clean`，要求 `总资产_亿元` 和 `净利润_亿元` 都是数值列。

**练习 4.2**：替换特殊值并填补缺失

在 `dirty_ex1_clean` 中，把 `净利润_亿元` 的缺失值填为 0，把 `营业收入_亿元` 的缺失值填为该列中位数。新增 `是否盈利` 列：`净利润_亿元 > 0` 为 `True`，否则为 `False`。输出每列缺失值数量，并显示 `证券简称`、`营业收入_亿元`、`净利润_亿元`、`是否盈利`。

**练习 4.3**：用映射生成风险标签

根据 `资产负债率` 新增 `负债水平`：大于等于 0.7 为“较高”，否则为“正常”。再用 `map()` 把“较高”映射为“需关注”，把“正常”映射为“低风险”，生成 `负债风险`。统计不同 `负债风险` 的数量。

### 阶段 5 练习：多表合并与背景信息补充

**练习 5.1**：处理证券代码并合并行业信息

重新读取 `finance_teaching_clean.xlsx` 和 `company_profile_teaching_clean.xlsx`。读取时把 `证券代码` 处理成 6 位字符串。筛选 2020 年财务数据，与公司信息表按 `证券代码` 合并，赋值给变量 `finance_company_2020`。检查合并前后行数是否一致，并检查 `行业名称` 是否有缺失。

**练习 5.2**：找出制造业中收入最高的公司

在 `finance_company_2020` 中筛选 `行业名称` 包含“制造”的公司，赋值给变量 `manufacturing_2020`。按 `营业收入_亿元` 从高到低排序，显示前 8 行。结果应包含 `证券代码`、`证券简称`、`行业名称`、`省份`、`营业收入_亿元`、`净利润_亿元`。

**练习 5.3**：比较早上市公司和较晚上市公司

把公司表中的 `上市日期` 转为日期格式，并生成 `上市年份`。在 `finance_company_2020` 中新增 `上市阶段`：`上市年份 < 2000` 标记为“较早上市”，否则标记为“较晚上市”。分别计算两组公司的平均 `营业收入_亿元` 和平均 `净利率`。

### 阶段 6 练习：分组汇总与组内比较

**练习 6.1**：行业年度摘要表

把财务表和公司信息表合并为 `analysis_ex6`。按 `行业名称` 和 `年份` 分组，计算 `公司数`、`营业收入合计_亿元`、`平均净利率`、`平均资产负债率`，赋值给变量 `industry_year_summary`。显示前 12 行。

**练习 6.2**：每个行业找两家公司

在 2020 年数据中，按 `行业名称` 分组，找出每个行业 `营业收入_亿元` 最高的 2 家公司，赋值给变量 `top2_revenue_by_industry`。结果只保留 `行业名称`、`证券代码`、`证券简称`、`营业收入_亿元`、`净利率`，并按行业名称和营业收入排序。

**练习 6.3**：计算行业内部收入差距

自定义函数 `value_range(x)`，返回 `x.max() - x.min()`。按 `行业名称` 分组，计算 2020 年各行业营业收入的均值和收入差距，赋值给变量 `industry_gap_2020`。按收入差距从高到低排序。

**练习 6.4**：判断公司是否高于行业平均

在 2020 年数据中，用 `groupby()` 和 `transform()` 计算每家公司所在行业的平均营业收入，生成 `行业平均收入_亿元`。再生成 `高于行业平均`，表示该公司营业收入是否高于所在行业平均值。显示 `行业名称`、`证券简称`、`营业收入_亿元`、`行业平均收入_亿元`、`高于行业平均`，并查看前 10 行。

### 阶段 7 练习：数据重塑与结果表构造

**练习 7.1**：构造公司收入宽表

用 `pivot_table()` 把 `analysis_ex6` 整理为每家公司一行、年份为列、值为 `营业收入_亿元` 的宽表，赋值给变量 `revenue_wide_ex7`。计算 `收入增长率_2018_2020 = 2020 / 2018 - 1`，按增长率从高到低排序，显示前 10 行。

**练习 7.2**：构造公司综合摘要表

基于 `analysis_ex6` 构造 `company_profile_summary`，每家公司一行，至少包含：`证券代码`、`证券简称`、`行业名称`、`省份`、`2018` 年营业收入、`2020` 年营业收入、`收入增长率_2018_2020`、`2020` 年资产负债率。按 `收入增长率_2018_2020` 从高到低排序，显示前 10 行。

**练习 7.3**：核对公司摘要表

检查 `company_profile_summary` 的行数是否等于公司数量。再按 `行业名称` 统计公司数量，并显示统计结果。最后显示 `company_profile_summary` 的前 5 行和后 5 行。

### 阶段 8 练习：时间序列数据入门

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
