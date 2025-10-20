"""
M4（询问阈值 + 进度显示，KISS）

改动（基于 v0.1.3）：
- 启动时询问阈值 N（回车默认 3）。
- 显示进度：
  - 总体进度：已达标/总数（百分比）。
  - 每次出题时显示该词的进度：correct/N（百分比）。
- 保留：过滤（correct ≥ N 本次不再出现）、中文释义+首字母提示、seen/correct 持久化、q 退出。

运行：在 example_words_app 目录执行 `python quiz_v0.1.4.py`
"""

import json
import random

data_path = 'data/cet4_sample.json'

# 读取原始数据，并为每个词条补充进度字段（若此前不存在）
with open(data_path, 'r', encoding='utf-8') as f:
    pairs = json.load(f)
for p in pairs:
    if 'seen' not in p:
        p['seen'] = 0
    if 'correct' not in p:
        p['correct'] = 0

# 询问阈值（默认 3）
raw = input("请输入达标阈值N（默认3）：").strip()
N = 3 if raw == '' else int(raw)

print("背单词小程序（阈值与进度版）：输入英文（q 退出）")

def overall_progress(pairs, N):
    mastered = sum(1 for x in pairs if x['correct'] >= N)
    total = len(pairs)
    percent = round(mastered * 100 / total, 1) if total > 0 else 0.0
    return mastered, total, percent

# 本次会话的可抽取列表：仅包含 correct < N 的词
active = [p for p in pairs if p['correct'] < N]
if not active:
    m, t, pct = overall_progress(pairs, N)
    print(f"当前已无未达标单词：总体进度 {m}/{t}（{pct}%）")
    exit(0)

while active:
    # 展示总体进度
    m, t, pct = overall_progress(pairs, N)
    print(f"\n总体进度：{m}/{t}（{pct}%）")

    pair = random.choice(active)
    word = pair['word']
    definition = pair['definition']

    print("释义：", definition)
    # 简单首字母提示：例如 apple -> a _ _ _ _
    first = word[0]
    underscores = " ".join("_" for _ in range(len(word) - 1))
    hint = f"{first} {underscores}" if underscores else first
    print("提示：", hint)

    # 该词的进度（相对阈值N）
    c = pair['correct']
    word_pct = round(min(c, N) * 100 / N, 1)
    print(f"该词进度：{c}/{N}（{word_pct}%）")

    user = input("请输入英文单词：").strip()
    if user.lower() == 'q':
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

    # 达到阈值则从 active 中移除
    if pair['correct'] >= N:
        try:
            active.remove(pair)
            print(f"已达阈值（{N}），本次运行中不再出此词：{word}")
        except ValueError:
            pass

if not active:
    m, t, pct = overall_progress(pairs, N)
    print(f"本次运行中，所有未达标单词均已达到设定阈值。总体：{m}/{t}（{pct}%）")

