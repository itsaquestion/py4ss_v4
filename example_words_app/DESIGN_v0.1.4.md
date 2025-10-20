# 设计文档 v0.1.4（阈值与进度显示）

## 新特性（基于 v0.1.3 增量）
- 启动时询问达标阈值 `N`（回车默认 3）。
- 显示两类进度：
  - 总体进度：已达标/总数 + 百分比。
  - 该词进度：`correct/N` + 百分比（每次出题时显示）。
- 过滤：当 `correct ≥ N`，本次练习不再出现该词。
- 其他保持不变：中文释义 + 首字母提示、每题后写回 `seen/correct`、`q` 退出。

## 实现要点（KISS）
- 读取 `example_words_app/data/cet4_sample.json`，缺失 `seen/correct` 的词条补 0。
- 询问阈值：`raw = input(...); N = 3 if raw == '' else int(raw)`。
- 构造 `active = [p for p in pairs if p['correct'] < N]`。
- 每轮：
  1) 计算总体进度（已达标数/总数与百分比）并打印。
  2) `random.choice(active)` 出题；打印释义、首字母提示、该词的 `correct/N` 与百分比。
  3) 判定对错；答对 `correct += 1`；每题 `seen += 1`；`json.dump` 写回。
  4) 若该词 `correct ≥ N`，从 `active` 移除并提示不再出现。
- `active` 为空则提示本次全部达标并打印总体进度。

## 运行方式
- `cd example_words_app`
- `python quiz_v0.1.4.py`

## 备注
- 为保持入门友好，保持单文件、直写原 JSON、逻辑顺序清晰可读。
