# 个人主页维护

内容源文件为 `index.jemdoc` 和 `src/` 下的 jemdoc 文件。请修改源文件后重新生成 HTML，不单独编辑生成结果。

使用 Python 3（仅依赖标准库）：

```bash
python3 jemdoc.py index.jemdoc biography.jemdoc
python3 -m unittest discover -s tests -v
```

Windows 若 Python 3 命令为 `python` 或 `py -3`，将上述 `python3` 替换为对应命令。

`biography.jemdoc` 与主页共用 `src/biography.jemdoc`。`backup/` 保留历史文件，但在 GitHub Pages 配置中排除发布。

提交时包含源文件、生成的 HTML 及必要的样式变更；推送到 `main` 后由 GitHub Pages 发布。

论文正式出版信息核对来源：

- TroLLoc：https://doi.org/10.1007/s41635-026-00177-1
- CU.POKer：https://doi.org/10.1109/TCAD.2021.3096458

奖学金时间已由本人确认为 2018 - 2022。DAC Young Fellow Award 按当前要求不添加。
