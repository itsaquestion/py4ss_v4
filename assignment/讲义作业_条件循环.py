# 条件、循环、列表推导式
# %%
# 练习1：小明身高1.75m，体重80.5kg。请根据BMI公式（体重除以身高的平方）帮小明计算他的BMI指数，并根据BMI指数：

# 低于18.5：过轻
# 18.5-25：正常
# 25-28：过重
# 28-32：肥胖
# 高于32：严重肥胖
# 用if-elif判断并打印结果：

height = 1.75
weight = 80.5

# bmi = ?

# if bmi < 18.5:
#     pass
# elif bmi < 25:
#     pass
# elif ...

# else:
#     ...

# 计算BMI指数
bmi = weight / (height ** 2)
print(f'小明的bmi是{bmi:.2f}')

# 用 if-elif 判断，并打印结果
if bmi < 18.5:
    result = "过轻"
elif bmi < 25:
    # 到这里，bmi肯定 >= 18.5
    # 因此，不用写成 bmi >= 18.5 and bmi < 25
# elif bmi >= 18.5 and bmi < 25
# 不需要这么写
    result = "正常"
elif bmi < 28:
    result = "过重"
elif bmi < 32:
    result = "肥胖"
else:
    result = "严重肥胖"

print(f"小明的BMI指数是{bmi:.1f}，体重状况为：{result}")
#  f-string中 {变量名:格式化}
# 格式化写法 .2f = 2位小数

# %% 闰年
# 一般的做法
year = 2005  # 或者任何一年

# (年份能被4整除 and 不能被100整除的) or (能被400整除)

# == : 判断是否相等
# != : 不等
# and
# or
# not
# 都是逻辑运算，因此会返回bool True/False


# 不能被100整除 year % 100 != 0
# != 不等于
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


print(f"{year}年是闰年吗？ {is_leap}")
# %%
# 教学用示范
if year % 400 == 0:
    # 如果能被400整除就是闰年
    is_leap = True
else:
    # 第一个条件
    if year % 4 == 0 and year % 100 != 0:
        is_leap = True
    else:
        is_leap = False

print(f"{year}年{'是' if is_leap else '不是'}闰年")
# %%
# 对一个变量number，判断是否能被2或者3整除

# 按具体的情况，请输出：

# “你输入的数字可以整除 2 和 3”
# “你输入的数字可以整除 2，但不能整除 3”
# “你输入的数字可以整除 3，但不能整除 2”
# “你输入的数字不能整除 2 和 3”
number = 12  # 可以更改为任何整数

# 问最严格的条件
# 放松一个
# 再放松一个
# 再放松一个

if number % 2 == 0 and number % 3 == 0:
    print("你输入的数字可以整除 2 和 3")
elif number % 2 == 0:
    # 判断这个条件，则上一个条件不成立
    print("你输入的数字可以整除 2，但不能整除 3")
elif number % 3 == 0:
    print("你输入的数字可以整除 3，但不能整除 2")
else:
    print("你输入的数字不能整除 2 和 3")
    
# %%
# 嵌套的版本

number = 12  # 可以更改为任何整数

# if 能否被2整除
# 可以被2整除
#       if 能否被3整除
#           能
#       else 不能
# else:
# 不能被2整除
#       if 能否被3整除
#           能
#       else 不能

if number % 2 == 0:
    # 能
    if number % 3 == 0:
        print("你输入的数字可以整除 2 和 3")
    else:
        print("你输入的数字可以整除 2，但不能整除 3")
else:
    # 不能
    if number % 3 == 0:
        print("你输入的数字可以整除 3，但不能整除 2")
    else:
        print("你输入的数字不能整除 2 和 3")

# 小目标：能用逻辑运算，2层if，合格
        
# %%
# 打印 1到10 中的偶数。
# 小提示：如何判断一个数是否是偶数？取余的操作符是%
num = 2
while num <= 10:
    print(num)
    num += 2
    print("这里是循环体里面")

print('这里是循环体的外面')
    
# 框架和例题相同
# 计数器从2开始，自增2

# %%
i = 1
while i <= 10:
    # while后面的条件，仔细看是否有可能不成立
    if i % 2 ==0:
        print(i)
    
    i+=1 # 累加代码必须在循环体内
    # 否则，i就永远=1


# %%
# 利用循环，求1到100的累加，计算完成最后打印出来
# 小提示：你可以建立一个新的变量，用来存放累加的结果
total = 0 # 累加变量

num = 1
while num <= 100:
    total += num # 每次循环，把num 累加到totel
    num += 1
print(total)
# %%
# 求1~100之间能被7整除，但不能同时被5整除的所有整数。For和While版本

# %% for 版本
for num in range(1, 101):
    if (num % 7 == 0) and (num % 5 != 0):
        print(num)

# %% while 版本
num = 1
while num <= 100:
    if num % 7 == 0 and num % 5 != 0:
        print(num)
    num += 1
# %%
# 求列表（或者元组）平均值。

# %% for 版本
score = [70, 90, 78, 85, 97, 94, 65, 80]

total = 0
for num in score: # 遍历其中的每个数
    total += num # 累加到total中

# 稍微结合了while和for的范例

average = total / len(score)
print(f"平均分是：{average:.2f}")
# %% while 版本
total = 0
i = 0 # i = 0,1,2,3,4,5 ... len(score) - 1 
while i < len(score):
    total += score[i]
    i += 1

average = total / len(score)
print(f"平均分是：{average:.2f}")
# %%
# 二分查找
a = [5, 8, 15, 20, 30, 45, 78, 100, 120, 200]
target = 30

left, right = 0, len(a) - 1

while left <= right:
    mid = left + (right - left) // 2
    if a[mid] == target:
        print(f"{target}的位置在 {mid}")
        break
    elif a[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
else:
    print(f"{target}没找到")

# %%
# 使用列表推导式创建一个列表，该列表包含1到20之间所有偶数的平方。
even_squares = [x**2 for x in range(1, 21) if x % 2 == 0]
print(even_squares)

# 遍历1到20
[    for i in range(1,21)     ]

# 添加条件：偶数
[    for i in range(1,21)    if i % 2==0]

# 添加操作：平方
[i ** 2 for i in range(1,21) if i % 2==0]

# %% 
# 提取以下列表中，首字母不是a的单词。
words = ['apple', 'banana', 'ant', 'animal', 'astronaut', 'airplane']
non_a_words = [s for s in words if not s[0]=='a']
print(non_a_words)

# 这是一个list -> list
# 因此，列表推导式

# 首字母不是a？
# 令s为其中一个单词，s[0] != 'a'
