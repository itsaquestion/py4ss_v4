"""
M2（记录进度演示版，单文件，KISS）

目标（第一部分，仅记录进度）：
- 显示中文释义与首字母提示；用户输入英文，判断对错。
- 每题结束后更新该词条的 `seen`（出现次数）和 `correct`（正确次数），并将整个列表写回原始 JSON 文件。
- 不做过滤/阈值，只演示“如何记录并持久化进度”。

运行：在 example_words_app 目录执行 `python quiz_v0.1.2.py`
"""

import json
import random


data_path = 'data/cet4_sample.json'



print("背单词小程序（记录进度演示版）：输入英文（q 退出）")

# 读取原始数据，并为每个词条补充进度字段（若此前不存在）
with open(data_path, 'r', encoding='utf-8') as f:
    pairs = json.load(f)

for p in pairs:
    if 'seen' not in p:
        p['seen'] = 0
    if 'correct' not in p:
        p['correct'] = 0

while True:
    pair = random.choice(pairs)
    word = pair['word']
    definition = pair['definition']

    print("\n释义：", definition)
    # 简单首字母提示：例如 apple -> a _ _ _ _
    first = word[0]
    underscores = " ".join("_" for _ in range(len(word) - 1))
    hint = f"{first} {underscores}" if underscores else first
    print("提示：", hint)
    # 显示当前词条的进度（便于观察 JSON 中 seen/correct 的变化）
    print(f"进度：已练 {pair.get('seen',0)} 次，答对 {pair.get('correct',0)} 次")

    user = input("请输入英文单词：").strip()
    if user.lower() == 'q':
        # 退出前保存一下（虽然每题后也会保存）
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(pairs, f, ensure_ascii=False, indent=2)
        print("已退出，进度已保存。")
        break

    if user.strip() == word.strip():
        print("正确！")
        is_correct = True
    else:
        print("不对。正确答案：", word)
        is_correct = False

    # 更新进度（每题答完都计入 seen；答对则 correct+1）
    pair['seen'] = pair.get('seen', 0) + 1
    if is_correct:
        pair['correct'] = pair.get('correct', 0) + 1

    # 每题后保存更新（演示 JSON 写回）
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    # 本版不移除任何词；第二部分再添加“过滤达标词”的逻辑


