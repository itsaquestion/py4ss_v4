"""
M3（过滤版，KISS）

目标：在 v0.1.2 基础上，新增“按正确次数过滤”的最小实现。
- 默认阈值 N = 3；当某词的 correct ≥ N 时，本次练习不再出现。
- 保留：中文释义 + 首字母提示；记录并写回 seen/correct；q 退出。

运行：在 example_words_app 目录执行 `python quiz_v0.1.3.py`
"""

import json
import random


data_path = 'data/cet4_sample.json'
N = 3  # 过滤阈值：correct ≥ N 的词本次不再出现（可按需改成 2、4 等）

# 读取原始数据，并为每个词条补充进度字段（若此前不存在）
with open(data_path, 'r', encoding='utf-8') as f:
    pairs = json.load(f)
for p in pairs:
    if 'seen' not in p:
        p['seen'] = 0
    if 'correct' not in p:
        p['correct'] = 0

print("背单词小程序（过滤版）：输入英文（q 退出）")

# 本次会话的可抽取列表：仅包含 correct < N 的词
active = [p for p in pairs if p['correct'] < N]
if not active:
    print("当前已无未达标单词（或均已达到阈值）。")
    exit(0)

while active:
    pair = random.choice(active)
    word = pair['word']
    definition = pair['definition']

    print("\n释义：", definition)
    # 简单首字母提示：例如 apple -> a _ _ _ _
    first = word[0]
    underscores = " ".join("_" for _ in range(len(word) - 1))
    hint = f"{first} {underscores}" if underscores else first
    print("提示：", hint)
    print(f"进度：已练 {pair['seen']} 次，答对 {pair['correct']} 次")

    user = input("请输入英文单词：").strip()
    if user.lower() == 'q':
        # 退出前保存（虽然每题后也会保存）
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(pairs, f, ensure_ascii=False, indent=2)
        print("已退出，进度已保存。")
        break

    if user == word:
        print("正确！")
        pair['correct'] += 1
    else:
        print("不对。正确答案：", word)

    pair['seen'] += 1

    # 每题后保存更新
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)

    # 若达到阈值，本次会话中不再出此词
    if pair['correct'] >= N:
        try:
            active.remove(pair)
            print(f"已达阈值（{N}），本次运行中不再出此词：{word}")
        except ValueError:
            pass

if not active:
    print("本次运行中，所有未达标单词均已达到设定阈值。做得好！")

