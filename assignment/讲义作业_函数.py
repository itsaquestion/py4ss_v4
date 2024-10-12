# 函数作业

# %%
# 实现一个函数my_count()，计算并返回一个列表的元素数量，但不要使用自带的len()函数。
# print(my_count([2,3,4,5])) # 应该输出 4

# 实现一个函数：你自己写一个函数
# 计算一个list中元素的个数
# 思考：这个函数的参数，应该是一个list，返回值应该是这个list的长度

# 注意：这个函数接收1个变量
# 所以参数应该是一个
# 但是参数名你选
# def my_count(a_list):
# def my_count(x):
# def my_count(a, b): 错了

# 思考：大致上是这样
# def my_count(a_list):
# ... # 计算a_list的长度，保存在一个变量
# 例如n中
#     return n 
# 返回值： return 把一个值，返回给外界

# 思考：先写功能，再包装成函数

a_list = [1,2,3,4,5]
# 算长度？

def my_count(a_list):
    n = 0
    for i in a_list:
        n += 1
    
    return n
    # print(n)
# 问：print和return
# print()把变量打印到屏幕上
# return 从函数内部，把一个值返回给外界

# 以后多次使用的时候，就不要再写循环了
my_count([3,4,5,6,7,8])
my_count([3,4,5,6])


# %% 先写计算长度
a_list = [1,2,3,4,5]

n = 0
for i in a_list:
    n+=1
    
print(n)

# %%
# 包装成函数
def my_count(a_list):
    n = 0
    for i in a_list:
        n += 1
    
    return n
    # print() 和return 
    # print()把参数打印到屏幕上
    # return 把某个值，返回到函数外
    
my_count([2,3,4,5,6,7,8])
# 调用函数 函数名()
# 这个函数要求计算一个list的长度
# 最后调用的时候，一定是你传递一个list给函数，函数返回给你一个数字

# %%
    

def my_count(x):
    count = 0
    for i in x: # 写成 for _ in x: 也可以
        count += 1
    return count

print(my_count([2,3,4,5]))  # 输出 4


# %%

# 实现一个函数my_max_len()，找到一个字符串列表中最长的字符串，但不要使用自带的max()函数。
# print(my_max_len(['a','bbb','cc'])) # 应该输出 'bbb'

# 思考：要写一个函数，参数是一个list of string，要求找到最长的string，返回出来

# 收一个参数，返回其中一个元素

# 大致结构：

# def my_max_len(str_list):
#     # 其他代码
#     result = # 找最长的
#     return result

# 先写功能
# 思路：
# 把第一个元素，放在result中
# 把从第2个元素开始，每个元素
# 都和result比较
# 如果比result长，就替换进去
# result就会是最长的那个
str_list = ['a','bbb','c']

result = str_list[0]

# 从第2个元素开始比
for s in str_list[1:]:
    if len(s) > len(result):
        result = s
print(result)

# 包装成函数
def my_max_len(str_list):
    
    result = str_list[0]

    # 从第2个元素开始比
    for s in str_list[1:]:
        if len(s) > len(result):
            result = s
    # print(result)
    return result

my_max_len(['adsfadf','adfadsf','qfadsfadsf'])


# %%
def my_max_len(str_list):
    if not str_list:
        return None
    longest = str_list[0]
    for s in str_list[1:]:
        if len(s) > len(longest):
            longest = s
    return longest

print(my_max_len(['a','bbb','cc']))  # 输出 'bbb'

# %%

# 实现一个函数find_min_max()，一个查找列表中最大和最小值，并返回一个元组.
# print(find_min_max([1, 5, 3, 9, 2, 7]))  # 应该输出 (1, 9)
# print(find_min_max([-5, 0, 10, -10, 5]))  # 应该输出 (-10, 10)

# 思路：问一个列表中最大和最小值
# 接收1个参数：要检查的list
# 返回一个tuple：(最小，最大)



def find_min_max(numbers):
    if not numbers:
        return None
    
    # 先建立最大值和最小值2个变量
    # 把第一个元素放进去
    min_val = max_val = numbers[0]
    
    # 从第二个元素开始遍历
    # 如果比max_val更大，则替换进去
    # 如果比min_val更小，也替换进去
    for num in numbers[1:]:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num
    return (min_val, max_val)
    # 最后返回元组 ()

print(find_min_max([1, 5, 3, 9, 2, 7]))  # 输出 (1, 9)
print(find_min_max([-5, 0, 10, -10, 5]))  # 输出 (-10, 10)
# %%
# 利用不定数量参数，写一个函数my_sum()，可以求任意个变量的和。效果应该如下：
# my_sum(1,2,3,4) == 10
# my_sum(3,4,5) == 12

# 照抄讲义
# 不定长参数，参数名前有个*
# *args，传递的所有变量，都会进入args这个tuple。

# 求和以前写过
def my_sum(*args):
    total = 0
    for num in args: # args是一个元组
        total += num
    return total

print(my_sum(1, 2, 3, 4))  # 输出 10
print(my_sum(3, 4, 5))     # 输出 12
# %%
# 写一个函数work()，要求接受一个字符串的List作为参数，把List中的每一个字符串，去掉第一个字符和最后一个字符，然后转为大写。
# 应该的效果：

# work(['apple','banana','orange']) == ['PPL','ANAN','RANG']


# %%
# 思路：先写功能
# 功能从里层开始写

# 范例
s = 'apple'

# 去掉第一个和最后一个字符
s[1:-1].upper()
# 成功！

# 用列表推导式，把上述算法用到每个元素
str_list = ['apple','banana','orange']

[s[1:-1].upper() for s in str_list ]
# 成功！

# 包装成函数

# 把写好的算法，包装到函数中
# 便于处理外界送过来的参数
def work(str_list):
    return [s[1:-1].upper() for s in str_list ]

work(['asdf','qwer']) # 成功！

# %% 



def work(str_list):
    return [s[1:-1].upper() for s in str_list]

print(work(['apple', 'banana', 'orange']))  # 输出 ['PPL', 'ANAN', 'RANG']