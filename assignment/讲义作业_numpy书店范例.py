# %%
# 数据准备
import numpy as np

# 书籍的单价列表
price_list = [120, 85, 100, 75, 95]
# 将列表转换为numpy数组
prices = np.array(price_list)

# 书籍的销售数量列表
quantity_list = [30, 15, 20, 10, 25]
# 将列表转换为numpy数组
quantities = np.array(quantity_list)

# 书籍名称 # 这个是新增，原来的代码中遗漏了
book_names = np.array(['微观经济学', '宏观经济学', '金融学', '会计学','Python数据分析'])


print("书籍价格数组:", prices)
print("销售数量数组:", quantities)

# 计算每本书未折扣前的总销售额
total_sales = prices * quantities
print("未折扣前的总销售额:", total_sales)

# 书籍的折扣比率
discount_rates = np.array([0.1, 0.05, 0.15, 0.05, 0.1])  # 10%, 5%, 15%, 5%, 10%

final_prices = total_sales * (1 - discount_rates)
print("折扣后的销售额:", final_prices)


# %%

# 12.1.4 练习题
# 12.1.4.1 题目 1: 价格调整
# 假设书店决定对所有书籍价格进行统一调整，增加5元。请使用numpy数组操作来更新prices数组，并打印新的价格数组。

prices_adjusted = prices + 5
print(prices_adjusted)


# 提示： 使用向量化操作来增加数组中的每一个元素。

# %%
# 12.1.4.2 题目 2: 销售筛选
# 书店想要了解哪些书籍的销售额在折扣后仍然超过2000元。使用布尔索引来筛选出这些书籍的价格和名称，并打印结果。

total_sales_adjusted = prices_adjusted * quantities * ( 1 - discount_rates)
print("调整后的总销售额:", total_sales_adjusted)

total_sales_adjusted > 2000

print("销售额在折扣后仍然超过2000元有:",book_names[total_sales_adjusted > 2000])


# 提示： 先计算折后总销售额，然后创建一个布尔数组用于筛选。

# %%
# 12.1.4.3 题目 3: 总结统计
# 请计算并打印以下统计信息： - 所有书籍的销售总数。 - 折扣后每本书平均的销售额。 - 折扣率最高的书籍的名称和价格。


print('所有书籍的销售总数:', quantities.sum())
print('折扣后每本书平均的销售额', total_sales_adjusted.mean())

# 获得最大值所在的index
max_discount_index = np.argmax(discount_rates)


print('折扣率最高的书籍是:', book_names[max_discount_index], '价格:', prices_adjusted[max_discount_index])


# 提示： 使用sum(), mean()函数，以及argmax()来找到折扣率最高的书籍。
