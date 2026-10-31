# 风格 DNA：从照片里读出风格

同一套引擎，能做出截然不同的网站，靠的就是这份 DNA。DNA 是一份小 YAML，写在新站根目录的 `style-dna.yaml`。规矩是：

> **先有 DNA，再写代码。DNA 里每个决定都要写出处：来自哪张照片、哪个数字，或者用户的哪句话。**

写不出出处的决定，就是 agent 自己的口味，要删掉重想。

---

## 1. DNA 格式

```yaml
trip: "一句话说清这趟旅行"           # 用户确认过的那句话
place: 地点                          # 决定音阶、文字砖、语言混搭
evidence:                            # 从 dna-seed.json 抄过来的关键数字
  tone: mid / chroma: moderate / temperature: neutral / hue_spread: mixed / night_share: 0.24
color:
  paper: "#FFFBF7"    # 出处
  ink: "#121212"      # 出处
  accent: "#F0481A"   # 出处：哪张照片的哪个颜色，做了什么调整
  on_accent: "#FFFBF7"
type:
  display: Archivo    # Google Fonts，必须有 ≥700 的字重（点阵字要靠粗笔画取点）→ THEME.font.family、:root --display
  stretch: expanded   # 宽 / 正常 / 窄 → :root --stretch（125% / 100% / 62%）、THEME.font.stretch
  case: upper         # upper / mixed → :root --case（uppercase / none）、THEME.font.upper（true / false）
  cjk: Noto Sans SC   # 中文、日文配字 → :root --cjk
  why: 为什么是这套字
hero: { word: JAPAN, sub: "Travel / 26 / 11", line: "Tokyo · Osaka · Kobe · Kyoto" }
motion:               # 对应 THEME.motion；缓动曲线写在 :root --ease
  character: 利落 / 柔软 / 机械 / 漂浮 …
  drift: .0032  follow: .075  spring: .06  damp: .82  repel: 60  gather: 950  develop: 1250
texture:
  dots: circle        # 点阵字的粒子形态：circle / square / glyph / line（非 circle 要改 stepDots 的画法；这是旋钮，不算 swaps）
  styles: [orig, ink, dot, block]   # 风格台：原图 + 3 种，至少一种能给出调色板
sound:
  scale: [0,1,5,7,8]  # 音阶名和出处
  base: 62
  presence: 1         # THEME.presence：.5 若有若无 / 1 默认 / 1.5 有存在感
chapters:
  - { en: Towers, zh: 高塔, mood: 仰望, line: "…", photos: [...], ambient: "城市低鸣 + 钟", voice: bell }
swaps: []             # 要替换的默认部件，最多 2 个，每个写清是哪条 DNA 跟默认部件冲突
```

---

## 2. 读照片的顺序

1. **跑脚本**：`prepare_photos.py`，再跑 `analyze_photos.py`。拿到 `dna-seed.json` 和 `contact.jpg`。
2. **看总览图 `contact.jpg`**，回答下面这些问题，答案写成笔记：
   - **题材**：建筑、街道、自然、食物、人、物件，各占多少？
   - **地点和语言**：在哪里？照片里出现了什么文字和招牌？
   - **时间**：白天还是夜晚，晴天还是雨天，有没有季节感？脚本的 `night_guess` 只是猜，以看图为准。
   - **母题**：有没有反复出现的形状、颜色或物件？本站的母题是"塔"和"朱红"。母题最适合拿来定强调色和章节。
   - **质感**：胶片、数码、手机还是扫描？颗粒、锐度、色偏怎样？
   - **拍照的人在看什么**：是仰望、平视还是俯拍，是远景还是近距离？
3. **起草"一句话"**：这趟旅行是什么？例如"在日本抬头看塔、天黑后看招牌"。后面所有决定都要能回到这句话上来。
4. **按下面的映射表**，逐项填 DNA。

---

## 3. 映射表：数字和观察 → 设计决定

每一条都写了"为什么"。遇到表里没有的情况，按"为什么"去推。

### 3.1 颜色

**强调色 accent**

| 规则 | 为什么 |
|---|---|
| 只从 `accent_candidates` 或某张照片的 `vivid_spots` 里选 | 原理 1 |
| 优先选**母题**的颜色：在几个章节里都出现、或者最能代表这个地方的颜色 | 它会出现在 logo、文字砖、点阵字、油墨效果里，是整个站的签名 |
| 可以把饱和度和明度提高，让它在纸上站得住；色相偏移不超过 ±8° | 照片里的颜色经过光线和压缩会发灰，提纯以后仍然是"那个颜色" |
| 在 paper 上做大字时，对比度要 ≥ 3:1 | `on_accent` 选 paper 或 ink 里对比更高的那个 |

示例：本站从鸟居的 `#DA754D`（色相 17°）提纯成 `#F0481A`。

**纸和墨 paper / ink**

| 证据 | 决定 | 为什么 |
|---|---|---|
| `tone` 是 bright 或 mid，`night_share` < .5 | 浅色纸，用 `paper_light` | 照片是主角，浅纸最不抢戏 |
| `tone` 是 dark，或 `night_share` ≥ .5 | 深色纸（`paper_dark_option`），墨变浅色 | 夜景放在白纸上会像一个个黑洞；深色底让光源发亮 |
| `temperature` 是 warm 或 cool | 纸带一点同向的色温，偏离纯白不超过 6 | 让外壳跟照片站在同一种光线下 |

**整组照片的色相分布 hue_spread**

| 证据 | 决定 | 为什么 |
|---|---|---|
| varied（照片颜色四散） | 外壳更克制：一个强调色，其余全中性 | 照片已经够吵了 |
| concentrated（照片几乎是一个色系） | 两种选法：<br>1. 强调色取这个色系里最纯的一点，做成近似单色的站；<br>2. 取照片里罕见的对比色点，前提是它确实在照片里出现过 | 要么顺着照片走，要么从照片里找反差，都不能凭空加色 |

### 3.2 字体

| 照片的性格 | display 方向 | Google Fonts 例子 |
|---|---|---|
| 城市、招牌、交通、建筑 | 宽体无衬线，全大写 | Archivo（wdth 125）、Unbounded、Syne |
| 冷、极简、北方、高海拔 | 窄体，或细中带粗的衬线 | Archivo（wdth 62）、Big Shoulders Display、Fraunces |
| 自然、慢、海边 | 人文衬线或圆润无衬线，大小写混排 | Fraunces、Young Serif、DM Serif Display、Nunito |
| 市集、热闹、食物、高饱和 | 粗圆体或胖体 | Rubik、Baloo 2、Bricolage Grotesque |
| 胶片、复古、旧物 | 等宽或打字机体 | Space Mono、IBM Plex Mono、Courier Prime |

**硬性要求**
- 首页点阵大字用 `THEME.font`，字重必须 ≥ 700。笔画太细的话，`wordPoints` 取不到足够的点，字会散。
- 中文配 Noto Sans SC 或 Noto Serif SC，日文配 Noto Sans JP，韩文配 Noto Sans KR，跟 display 的衬线与否保持一致。
- 只用一套 display 加一套正文（或者 display 兼任正文），不要三套。

### 3.3 动效（THEME.motion）

| 性格 | 证据 | drift | follow | spring / damp | repel | gather / develop |
|---|---|---|---|---|---|---|
| 利落（本站） | 城市，反差 normal 或 hard | .0032 | .075 | .06 / .82 | 60 | 950 / 1250 |
| 柔软 | 自然、海边，反差 soft | .0018 | .05 | .035 / .88 | 75 | 1200 / 1700 |
| 漂浮 | 雾、雪、水下，tone 偏亮、低饱和 | .0012 | .04 | .025 / .92 | 85 | 1400 / 2000 |
| 机械 | 工业、地铁、夜景、hard contrast | .005 | .11 | .09 / .74 | 50 | 750 / 900 |

`repel` 是点阵字躲开鼠标的半径（px）：性格越软，半径越大，散开的范围也越大。

缓动曲线 `:root --ease` 跟着变，JS 会自动读取它：
- 利落：`cubic-bezier(.7,0,.2,1)`
- 柔软：`cubic-bezier(.4,0,.2,1)`
- 机械：`steps()`，或者 `cubic-bezier(.9,0,.1,1)`

### 3.4 质感：点阵粒子和风格台

| 证据 | 粒子形态 | 风格台的 3 种效果 |
|---|---|---|
| 城市、印刷感、招牌（本站） | circle | 油墨双色、网点、色块 |
| 夜景、霓虹，`night_share` 高 | circle（发光） | 网点、扫描线、色块 |
| 自然、植物、蓝天 | circle 或 line | 蓝晒 cyanotype、木刻双色、色块 |
| 食物、物件、高饱和 | square | 像素马赛克、riso 双色、色块 |
| 胶片、复古 | glyph（字符） | ASCII、颗粒油墨、色块 |
| 雪、雾、极简 | line | 线稿（边缘检测）、单色网点、色块 |

规则：
- "色块"（k-means 调色板）建议永远保留。它是"照片是原材料"最直接的证明，大图侧栏的调色板也跟它呼应。
- 新效果的写法见 `components.md` 的"风格台"一节。

### 3.5 声音

详见 `sound.md`，这里只列 DNA 级别的决定：
- **音阶**：按地点选。
- **整体速度**：跟着动效性格走。
- **每章的乐器**：跟着那一章的情绪走。
- **presence**：环境声的总音量，填进 `THEME.presence`（.5 若有若无，1 默认，1.5 有存在感）。

### 3.6 首页和文案

| 项目 | 规则 |
|---|---|
| `hero.word` | 地点名，或者一个能概括这趟旅行的词。最好不超过 9 个字母，超过时要带空格，`wordPoints` 会拆成两行。用户的母语不是拉丁字母时，也优先用拉丁字母大字，点阵效果最好；本地文字放进文字砖 |
| `hero.sub` | `Travel / YY / MM` 这类格式，信息要短 |
| `hero.line` | 去过的地方，用 `·` 连接 |
| `TEXT_TILES` | 两块：a 是强调色底，放一句英文短诗；b 是墨色底，放本地文字和统计数字 |
| 章节导语 | 一句话，用第一人称的感受，不做说明 |
| 图注 | 16 个字以内，写感受，不写"这是 XX" |

---

## 4. 章节怎么分

- 一般分 4–7 章，每章 3–6 张。照片少于 12 张时分 2–3 章，每章至少 2 张。宁可少分一章，也不要出现只有 1 张的章。
- **按情绪和母题分，不按日期分。** `chapter_draft_by_color` 只是按颜色粗分的草案。要结合看图得到的题材、地点、昼夜重新分。
- 每章起一个英文单词或词组（en）、两个汉字（zh，或用户的语言），再配一句导语。
- 章节顺序要像一天或一段旅程：从远到近、从白天到夜晚、从大到小。本站的顺序是：塔，霓虹，朱红，绿荫，漫游，小事。

---

## 5. 跟用户确认：最多 4 个问题，一次只问一个

每个问题都带 agent 的推荐答案和理由，用户可以只回答"按你的来"。

1. **"这趟旅行，用一句话说是什么？"** 附上 agent 起草的那句话，以及据此定的 hero.word、hero.sub。
2. **"章节这样分可以吗？"** 列出每章的名字、情绪词和照片编号（对应 contact.jpg 上的编号）。
3. **"风格选 A 还是 B？"** 给两套 DNA 方向，每套用 3 行描述：
   - 色板，写成 `paper / ink / accent`，accent 注明出处；
   - 字体和动效性格；
   - 声音（音阶加两种代表乐器）。

   A 贴近照片的本来气质，B 往母题或反差上更大胆一些。
4. **"声音要有存在感，还是若有若无？"**

用户已经在需求里说清楚的问题，跳过不问。

---

## 6. 防撞衫检查（定稿前必须做）

把 DNA 跟本仓库的 JAPAN DNA（见 `examples.md`）逐项对比：paper、accent 色相、display 字体、动效性格、粒子形态、风格台效果、音阶、主要乐器。

- **至少 4 项要不同。** 做不到的话，说明你在套模板而不是在读照片，回到第 2 步重看。
- 唯一的例外：照片确实也是日本城市。这时也要在母题、强调色或章节上找到不同点。
