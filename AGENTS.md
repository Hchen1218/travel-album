# 给 agent 的说明

这个仓库是一个单文件旅行相册网站（`index.html` + `photos/`），同时也是一个 skill 的模板。

- **想用自己的照片做一个这样的网站**：读 `skills/photo-album/SKILL.md`，按流程走。风格要从用户自己的照片里读出来，不要照抄本站的 JAPAN 风格。
- **想修改本站**：`index.html` 顶部的「风格区」（CSS `:root`、JS `THEME`、`CHAPTERS`、`TEXT_TILES`，以及「声音：风格区」）放的是可变的风格值，其余部分是引擎。改引擎之前，先读 `skills/photo-album/references/components.md` 里对应部件的契约。
- **本地运行**：`python3 -m http.server 8765`，然后访问 http://localhost:8765 。不能用 `file://` 打开，否则读不到照片像素。
- **版权**：`photos/` 里的照片归作者所有，不要复制到别的项目里。
