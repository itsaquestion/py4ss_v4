# 5.4.10 Dict小练习
# %%
# 题目1：创建字典 创建一个名为 person_info 的字典，其中包含以下键值对：
# 'name': 'Alice'
# 'age': 25
# 'city': 'New York'

person_info = {"name": "Alice", "age": 25, "city": "New York"}

print(person_info)

# %%
# 题目2：访问字典中的值 使用刚刚创建的 person_info 字典。编写一个Python语句来访问键 ‘age’ 对应的值，并将其存储在一个名为 age_value 的变量中。
age_value = person_info['age']
print(age_value)


# %%

# 题目3：添加键值对 在 person_info 字典中添加一个新的键值对，其中键为 ‘occupation’，值为 ‘Engineer’。
person_info['occupation'] = 'Engineer'
print(person_info)

# %%

# 题目4：修改字典中的值 修改 person_info 字典中键 ‘city’ 对应的值为 ‘San Francisco’。
person_info['city'] = 'San Francisco'

print(person_info)

# %%
# 题目5：删除键值对和获取所有键 首先，删除 person_info 字典中键 ‘age’ 及其对应的值。然后获取该字典中所有的键，并将它们存储在一个名为 keys_list 的列表中。

# 如果person_info里有age，才删除
# 否则，不做操作

if 'age' in person_info:
    del person_info['age']
    
keys_list = person_info.keys()
print(keys_list)

# 如果执行删除的代码2次，第一次会成功，age就不存在了
# 执行第二次，会删除一个“不存在的key”，因此会报错

# %%
