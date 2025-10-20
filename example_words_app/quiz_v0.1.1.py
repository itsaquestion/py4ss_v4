"""
M1（极简版）需求（含首字母提示）：
- 使用 example_words_app/data/cet4_sample.json
- 随机抽取一个词：先显示中文释义，再显示首字母+下划线提示（下划线数=单词长度-1）；
  等待输入英文；判断对错；错则显示正确答案。
- 循环进行；输入 q 退出。
"""

import json
import random
import os

# 1) 读取 预先准备好的 JSON 文件
# 当然也可以读取excel文件或者csv文件，后面会学
# 暂时先用JSON文件作为数据源

data_path = 'data/cet4_sample.json'

with open(data_path, "r", encoding="utf-8") as f:
    pairs = json.load(f)

print("背单词小程序：输入英文（q 退出）")

while True:
    # 2) random 模块随机抽取一个词
    pair = random.choice(pairs)
    word = pair['word']
    definition = pair['definition']

    # 显示中文释义
    print("\n释义：", definition)

    # 新增：显示首字母 + 下划线提示（下划线数量 = 单词长度 - 1）
    # 例如：apple -> a _ _ _ _
    if len(word) >= 1:
        first_letter = word[0]
        underscores = " ".join("_" for _ in range(len(word) - 1))
        hint = f"{first_letter} {underscores}" if underscores else first_letter
        print("提示：", hint)

    # 读取用户输入
    user = input("请输入英文单词：").strip()
    if user.lower() == "q":
        print("已退出。")
        break

    if user.strip() == word.strip():
        print("正确！")
    else:
        print("不对。正确答案：", word)

