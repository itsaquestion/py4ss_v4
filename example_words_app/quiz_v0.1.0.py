"""
M1（极简版）需求：
- 使用 example_words_app/data/cet4.json，顶层包含两个表头：word 和 definition，
  它们都是以字符串ID为键的字典，形如：
  {"word": {"1001": "apple", ...}, "definition": {"1001": "n.苹果", ...}}
- 随机抽取一个词：先显示中文释义，等待输入英文；判断对错；错则显示正确答案。
- 循环进行；输入 q 退出。
"""

import json
import random
import os

base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "data", "cet4.json")

# 1) 读取 预先准备好的 JSON 文件
# 当然也可以读取excel文件或者csv文件，后面会学
# 暂时先用JSON文件作为数据源
with open(data_path, "r", encoding="utf-8") as f:
    pairs = json.load(f)

# pairs是一个list of dict，可以检查属性
# print(type(pairs))
# print(type(pairs[0]))

print("背单词小程序：输入英文（q 退出）")

while True:
    # 2) random 模块随机抽取一个 tuple
    pair = random.choice(pairs)
    word = pair['word']
    definition = pair['definition']

    print("\n释义：", definition)
    user = input("请输入英文单词：").strip()
    if user.lower() == "q":
        print("已退出。")
        break
    if user.strip().lower() == word.strip().lower():
        print("正确！")
    else:
        print("不对。正确答案：", word)
