---
name: photo-album
description: >-
  把一文件夹旅行照片做成一个单文件的互动相册网站：照片环、会躲鼠标并染上照片颜色的点阵大字、横滑章节页、实时风格台、点阵显影的单张大图和放大镜，以及每章不同的现场合成声音。风格从用户自己的照片里读出来，所以每个人做出来都不一样。
  Turn a folder of travel photos into a single-file interactive photo-album website (photo ring, particle type tinted by photos, chapters, live print styles, a particle-developing photo viewer with loupe, per-chapter synthesized sound) whose visual and sonic style is derived from the user's own photos. Use when someone wants a travel album, photo journal or portfolio site "like this one" or "in this style".
---

# Photo Album：照片即材料的旅行相册

本仓库的 `index.html` 既是作品，也是模板。这份 skill 教你做两件事：读懂它为什么长这样，然后用**另一个人的照片**做出一个同样完成度、风格却完全属于那些照片的网站。

## 先记住这一句

> **不变的是引擎和原理，变的是风格 DNA。** 风格 DNA 从照片里读出来，跟用户确认后，再填进模板的旋钮里。

五条原理，详见 `references/principles.md`。动手之前先读一遍：

1. **照片是唯一的原材料**：所有颜色、形状、声音都从像素里算出来。
2. **外壳克制**：纸、墨、一个来自照片的强调色、一套字体。
3. **一切都有物理感**：惯性、回弹、飞行、显影，没有硬切。
4. **每章一种情绪**：同时落在画面、交互、声音三个层面。
5. **单文件、零构建、零音频文件**：执行 `python3 -m http.server` 就能跑。

## 文件地图

| 文件 | 什么时候读 |
|---|---|
| `references/principles.md` | 开始前，必读 |
| `references/style-dna.md` | 第 2–3 步，必读。照片 → DNA 的映射表，以及确认问题 |
| `references/examples.md` | 第 2 步。本站的 DNA，加 3 份截然不同的示例 |
| `references/components.md` | 第 4 步。每个部件的契约、旋钮和可替换形式 |
| `references/sound.md` | 第 4 步。乐器、音阶、每章声音配方、音量预算 |
| `scripts/prepare_photos.py` | 第 1 步。生成 `photos/sq` 和 `photos/full` |
| `scripts/analyze_photos.py` | 第 1 步。生成 `dna-seed.json` 和 `contact.jpg` |
| `../../index.html` | 模板。顶部的「风格区」是要填的地方，其余是引擎 |

## 流程

### 第 0 步：确认输入

- 照片文件夹：8–40 张都可以。不到 24 张时，照片环会循环补满四条边；不到 8 张的话，首页建议换成照片堆（见 `components.md` 第 1 节）。超过 40 张，首页会很挤，可以挑选一下。
- 新站放在哪个文件夹。**不要在本仓库里覆盖 JAPAN 站。**
- 照片版权归用户。如果混有别人的作品（比如用其他风格 skill 生成的图），记下作者和许可，后面写进 `credit` 和 `license`。

### 第 1 步：整理和测量照片

```bash
python3 skills/photo-album/scripts/prepare_photos.py <照片文件夹> --out <新站文件夹>
python3 skills/photo-album/scripts/analyze_photos.py <新站文件夹>/photos/full --out <新站文件夹>/.dna
```

- 第一个脚本会打印每张照片的 `src`、`w`、`h`，后面填 `CHAPTERS` 时要用。
- 脚本需要 Pillow（`pip install pillow`）。

### 第 2 步：读照片，起草 DNA

1. 打开 `.dna/contact.jpg` 亲眼看。只看数字是读不出题材、地点、母题和质感的。
2. 读 `.dna/dna-seed.json` 的 `summary`、`accent_candidates`、`paper_ink` 和 `chapter_draft_by_color`。
3. 按 `references/style-dna.md` 的格式，在新站根目录写 `style-dna.yaml`。规矩：
   - **每个决定都写出处**：来自哪张照片、哪个数字，或者用户的哪句话；
   - 强调色只能从照片里来；
   - 起草两套方向：A 贴近照片本来的气质，B 在母题或反差上更大胆。
4. **防撞衫检查**（`style-dna.md` 第 6 节）：跟 `examples.md` 里的 JAPAN DNA 比，至少 4 项不同。

### 第 3 步：跟用户确认，最多 4 个问题，一次一个

问题清单在 `style-dna.md` 第 5 节。每个问题都附上你的推荐答案和理由，用户回答"按你的来"也可以。

跳过的标准：用户原话里**直接**给出了答案，才跳过。比如用户说"不要声音"，就跳过第 4 题。如果只能从原话里推测，比如"散心"推出"声音轻一点"，那就仍然要问，只是把推测写成你的推荐答案。

问完之后定稿 `style-dna.yaml`。

### 第 4 步：搭站

1. 把本仓库的 `index.html` 复制到新站文件夹。照片在第 1 步已经放进新站的 `photos/` 了。**不要把本仓库的照片带过去。**
2. 按 DNA 填「风格区」，这些地方都有 `风格区` 注释，搜得到：

   | 位置 | 填什么 |
   |---|---|
   | `<title>`、Google Fonts 的 `<link>` | display 字体和中日文配字 |
   | CSS `:root` | `--bg`、`--ink`、`--accent`、`--on-accent`、`--cjk`、`--display`、`--stretch`、`--case`、`--ph`、`--ease` |
   | JS `THEME` | 标题、logo、年份、hero、字体（`upper` 要和 `--case` 一致）、音阶、`presence`、`motion` |
   | `CHAPTERS` | 章节和照片：`src`、`w`、`h`、`cap`，第三方作品加 `credit` 和 `license` |
   | `TEXT_TILES` | 两块文字砖 |
   | 「声音：风格区」 | `RING_SND`（首页旋律和乐器）、`LB_SND`、`VOICE`、`SCENES`，按 `sound.md` 的配方给每章重写 |

3. 风格台：按 DNA 的 `texture.styles` 保留或改写效果函数。接口和效果配方见 `components.md` 第 4 节。
4. DNA 的 `swaps` 里有替换项时，按 `components.md` 对应部件的"同级替代"去改。**最多 2 个，并且保持对外接口不变。**
5. 全局搜一遍本站特有的残留，搜到就换掉。要不分大小写地搜：

   ```bash
   grep -niE "japan|日本|旅の|tokyo|osaka|kobe|kyoto|高塔|霓虹|朱红|都节|东京塔|国际橙" index.html
   ```

   风格区注释里描述 JAPAN 的话，比如"宽体无衬线，像车站和招牌"，也要改成新站自己的理由。
6. 写一份新站自己的 `README.md`：怎么在本地运行、怎么换照片、署名与版权。结构可以参考本仓库的 README。

### 第 5 步：验收

起本地服务器（`python3 -m http.server 8765`），在浏览器里逐条检查。

**功能**
- [ ] 首页：照片环会流动，可推动，带惯性；点阵大字躲鼠标；悬停照片时变成章节名并染上照片颜色
- [ ] 每一章都能进入，横滑带惯性，照片保持原始比例
- [ ] 风格台 1–4 都能出图；色块效果给出调色板
- [ ] 大图：粒子飞出，由粗到细显影；左右切换；1–4 换风格；放大镜能放到看见像素；取色正常；Esc、返回键、点空白处都能关闭；`#/ch/N/M/view` 直接打开正常
- [ ] 声音：第一次点击后自动开启；每章环境声不同；大图事件音齐全；每章峰值在 0.10–0.32（测法见 `sound.md` 第 6 节）

**体验**
- [ ] 手机宽度（375px）下没有横向滚动；大图变成底部抽屉；按住照片能拖放大镜
- [ ] 开启 `prefers-reduced-motion` 时，动画退化成直接切换，功能完整
- [ ] 键盘可以走完全部流程（Tab、Enter、方向键、1–4、Esc）
- [ ] 控制台没有错误

**风格**
- [ ] 随便指一个颜色，都能说出来自哪张照片（原理 1）
- [ ] 把照片换成灰块后，页面很空（原理 2）
- [ ] 闭上眼也能听出是哪一章（原理 4）
- [ ] 跟 JAPAN 站并排放，一眼就能看出不是同一个站

最后截图给用户看，并请用户自己听一遍声音。测量只能保证声音不爆、不哑，好不好听要人耳判断。

## 踩过的坑

- **双击 `index.html` 用 `file://` 打开时**，浏览器不让读像素：点阵取色、风格台和大图都会失效。必须起本地服务器。
- **canvas 默认宽度是 300**。如果你按"尺寸变了才重设"的逻辑去改 canvas，而目标尺寸恰好是 150 × 2（dpr），就永远不会触发重设。要另外记住上一次的尺寸（参考 `LP.L`）。
- **合成触摸事件时，`setPointerCapture` 可能抛错**，要用 try/catch 包起来。
- **从 window 上派发的 keydown，`e.target` 不是 Node**，判断之前先用 `instanceof Node`。
- **有的预览面板在后台时会暂停 `requestAnimationFrame`**，动画看起来像"卡住"。验证时先截一张图把页面唤醒，或者直接读状态变量来确认。
- **某一章的拨弦叠上环境声，峰值曾经冲到 0.56。** 要降这一章乐器的力度 `v`，不要动压缩器。
- **测声音峰值时数字跳得厉害**：环境声是随机排的，幕布转场还有一声风。测法见 `sound.md` 第 6 节，要多测几次取中位数。
- **验证脚本连续改网址时**，两次之间至少等 1.2 秒，让幕布转场走完。引擎已经处理了"转场途中又跳到大图"的竞态，但等转场走完的结果最稳定。
- **点阵大字用细字重时取不到足够的点。** display 字重要 ≥ 700。

## 署名

- 照片环和点阵大字的交互结构，参考了 Framer 模板 Squareo（Iconic Graphics）的思路。代码、设计和素材都是本仓库原创。
- 新站沿用这套结构时，建议在 README 里保留这句来源说明。
- 本仓库的照片归原作者所有，不随 skill 授权。
