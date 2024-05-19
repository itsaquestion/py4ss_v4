### 2. 数据准备

在本节中，我们将使用Seaborn（sns）库自带的数据集来演示因子分析的数据准备过程。Seaborn库提供了一些内置的示例数据集，方便我们进行数据分析和可视化。

#### 2.1 数据导入与清洗

我们首先将导入Seaborn库，并加载其中的一个示例数据集。然后，我们将对数据进行简单的清洗，包括处理缺失值、异常值等。这样做是为了确保我们分析的数据质量和准确性。

```python
import seaborn as sns

# 加载示例数据集
data = sns.load_dataset("iris")

# 查看数据前几行
print(data.head())

# 检查缺失值
print(data.isnull().sum())

# 处理缺失值（如果有的话）
# 这里示例数据集没有缺失值，所以不需要处理
```

#### 2.2 变量选择

在进行因子分析之前，我们需要选择合适的变量。在这个示例中，我们将选择鸢尾花数据集中的花萼长度（sepal_length）、花萼宽度（sepal_width）、花瓣长度（petal_length）和花瓣宽度（petal_width）这四个变量进行分析。

```python
# 选择需要分析的变量
selected_vars = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
print(selected_vars.head())
```

通过以上操作，我们完成了数据的准备工作，现在可以进入下一步，使用主成分分析和因子分析方法来探索数据的潜在结构了。