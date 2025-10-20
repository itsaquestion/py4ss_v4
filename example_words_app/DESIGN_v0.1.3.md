# 设计文档 v0.1.3（按正确次数过滤）

## 新特性（基于 v0.1.2 增量）
- 增加简单过滤：当某单词的 `correct` ≥ N（默认 3）时，本次练习不再出现。
- 其他保持不变：
  - 显示中文释义 + 首字母提示（如 `apple -> a _ _ _ _`）。
  - 每题后更新 `seen`/`correct` 并写回同一个 JSON 文件。
  - 输入 `q` 退出。

## 大致怎么做（保持极简）
- 常量：脚本顶部设定 `N = 3`。
- 启动：读取 `example_words_app/data/cet4_sample.json`，为每个词条补齐 `seen`/`correct` 字段。
- 构造本次会话的可抽取列表：`active = [p for p in pairs if p['correct'] < N]`。
- 循环：
  1) `random.choice(active)` 抽题；打印释义、首字母提示与当前进度。
  2) `input()` 获取答案；正确则 `correct += 1`；每题后 `seen += 1`。
  3) 用 `json.dump` 把 `pairs` 写回原 JSON 文件。
  4) 若该词 `correct >= N`，则 `active.remove(pair)`，本次运行中不再出现。
- 若 `active` 为空，则提示“本次已无未达标单词”。

## 运行方式
- 切换目录：`cd example_words_app`
- 运行脚本：`python quiz_v0.1.3.py`

## 备注
- 如需改为“strictly > N 才过滤”，把判断改成 `correct > N` 即可；当前实现使用 `>= N`，更常见也更直观。
