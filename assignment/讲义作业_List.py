# 5.1.4 List 练习

# %% 题目1

# 创建一个名为my_list的列表，包含以下元素：1, 3, 5, 7, 9。然后创建一个变量element，将其赋值为列表中的第四个元素。

my_list = [1, 3, 5, 7, 9]
element = my_list[3]
print(element)

# %% 题目2
# 创建一个名为my_list的列表，包含以下元素：2, 4, 6, 8。使用append方法将10添加到列表的末尾，然后创建一个变量length，将其赋值为列表的长度。

my_list = [2, 4, 6, 8]
my_list.append(10)
print(my_list)
length = len(my_list)
print(length)

# %% 题目3

# 创建一个名为my_list的列表，包含以下元素：1, 9, 3, 7。使用insert方法在9和3之间插入一个值为5的元素，然后创建一个变量max_value，将其赋值为列表中的最大值。

my_list = [1, 9, 3, 7]
my_list.insert(2, 5)
print(my_list)
max_value = max(my_list)
print(max_value)
# %% 题目4

# 创建一个名为my_list的列表，包含以下元素：2.2, 3.3, 1.1, 4.4。使用remove方法删除元素1.1，然后创建一个变量min_value，将其赋值为列表中的最小值。

my_list = [2.2, 3.3, 1.1, 4.4]
my_list.remove(1.1)
print(my_list)
min_value = min(my_list)
print(min_value)

# 5.1.6 List 练习（切片和其他）

# %% 题目1
# 创建一个名为my_list的列表，包含以下元素：1, 2, 3, 4, 5。使用切片获取前三个元素，并存储在新列表first_three中。

my_list = [1, 2, 3, 4, 5]
first_three = my_list[:3] 
print(first_three)

# %% 题目2
# 创建一个名为my_list的列表，包含以下元素：1, 2, 3, 4, 5, 6, 7, 8, 9, 10。使用切片和步长来创建一个新列表even_numbers，其中包含my_list中的所有偶数。

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = my_list[1::2]
print(even_numbers)
# %% 题目3
# 创建一个名为my_list的列表，包含以下元素：‘a’, ‘b’, ‘c’, ‘d’, ‘e’。使用切片创建一个新列表reversed_list，它是my_list的一个反转版本。

my_list = ['a', 'b', 'c', 'd', 'e']
reversed_list = my_list[::-1]
print(reversed_list)


# %% 题目4
# 创建两个列表，名为list1和list2，分别包含以下元素：
# list1: [1, 2, 3, 4]
# list2: [5, 6, 7, 8]
# 使用切片和+操作符创建一个新列表merged_list，它包含list1的前两个元素和list2的后两个元素。

list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]
merged_list = list1[:2] + list2[2:]
print(merged_list)
# %% 题目5
# 创建一个名为my_list的列表，包含以下元素：‘apple’, ‘banana’, ‘cherry’, ‘date’, ‘elderberry’。使用切片和列表连接来替换中间的三个元素为一个新的子列表[‘fig’, ‘grape’, ‘honeydew’]。

my_list = ['apple', 'banana', 'cherry', 'date', 'elderberry']
my_list[1:4] = ['fig', 'grape', 'honeydew']
print(my_list)
# %%
