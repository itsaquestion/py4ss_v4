# 以下是同学的姓名，学号和考试分数的数据

# names = ["Alice", "Bob", "Clare"]
# ids = [101,102,103]
# scores = [85, 92, 78]
# 构建一个字典data，其中key是名字，value是另一个字典key和value是id和score以及对应的值。
# 构建出来大概是这样： {'Alice': {'id': 1, 'score': 85},  ...}

# 含义：可以用人名来获取id和分数

# data['Alice'] = {'id':, 'socre':}

# 对data按分数排序，高分的在前面。

# 找出分数最高的同学，打印“分数最高的同学是: ??? ，学号是???，分数是： ???。”

# %% 数据
names = ["Alice", "Bob", "Clare"]
ids = [101, 102, 103]
scores = [85, 92, 78]

# %% 构建字典

# %% 字典推导式的版本
data = {names[i]: {"id": ids[i], "score": scores[i]} for i in range(len(names))}


# %% 循环的版本
# 思路：创建一个空字典，把人逐一添加
# 有3个人，遍历0到2
# 把names，ids, scores 对应的数据拿出来，构建出字典
# 

data = {} # 构建空字典

# 遍历0，1，2，把数据添加进空字典


# len(names)：有多少人？2
# range(len(names)) 0,1,2
# for ... 遍历 0,1,2
# 获得数据
# 名称 names[i]
# id: ids[i]
# score: scores[i]
# {'id':ids[i], 'score':scores[i]}
# data[names[i]] = ...
# 对字典普通的赋值
# 其中第一个人：data['Alice'] = {'id':101,'scores':85}

# 用循环来完成对全部人的遍历
for i in range(len(names)):
    data[names[i]] = {"id": ids[i], "score": scores[i]}

print(data)


# %%
# 排序：
# 思路：dict.item() ->
# [(key,value), (key,value), ....]

# %%
data

#%%
list(data.items())[0][1]['score']

# %%


# 定义排序用的函数
def get_score(item):
    return item[1]['score']

get_score(list(data.items())[0])

# %%

# 按分数排序
# data.items() -> [(key,value),...]

# 对上面这个结构，取其中的score来排序
# sorted(data.items(),key=get_score,reverse=True)

# 最后，再转为新的字典
# dict(scorted(...))

sorted_data = dict(sorted(data.items(), key=get_score, reverse=True))

sorted_data

# %%
# 写成匿名函数的版本


sorted_data = dict(sorted(data.items(), key=lambda item: item[1]['score'], reverse=True))


print(sorted_data)

# %%
# 找出分数最高的同学的名字

# 思路：上述数据结构，以名称为key
# 只要知道第一个人的名字即可（已经排序——

# 排序好的数据，keys()是全部人名
# sorted_data.keys()
max_score_name = list(sorted_data.keys())[0]
max_score_name
# %%

data[max_score_name]
# %%
# 使用名字获取对应的id和分数
student_id = data[max_score_name]["id"]

score = data[max_score_name]["score"]

# 打印结果
print(f"分数最高的同学是: {max_score_name}，学号是 {student_id}，分数是： {score}。")


# %%
