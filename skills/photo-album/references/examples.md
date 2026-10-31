# 示例：同一套流程，四种截然不同的结果

第一份是本仓库 JAPAN 站的真实 DNA。后三份是虚构的，用来示范：照片证据不同，流程得出的决定会差多远。

**它们不是可以套用的成品。** 新站的 DNA 必须从新照片里读出来，然后过 `style-dna.md` 第 6 节的防撞衫检查。

---

## A. JAPAN（本仓库，真实）

```yaml
trip: "在日本抬头看塔，天黑以后看招牌，走累了吃一口好的"
place: 日本（东京、大阪、神户、京都）
evidence:   # analyze_photos.py 实测
  tone: mid / contrast: normal / chroma: moderate / temperature: neutral
  hue_spread: mixed, dominant_hue: 19° / night_share: .24 / portrait_share: .8
  accent_candidates: torii #DA754D (17°), old-tower #5A85C8 (217°), drugstore #CEB556 (48°)
color:
  paper: "#FFFBF7"   # tone 为 mid、夜景少 → 浅纸；带一点暖，呼应木头和朱红
  ink: "#121212"
  accent: "#F0481A"  # torii 的 #DA754D 提纯，色相 17° → 14°。母题：鸟居、东京塔、神户塔都是这个橙红，全站的签名
  on_accent: "#FFFBF7"
type:
  display: Archivo, stretch: expanded (--stretch 125%), case: upper (--case uppercase, upper:true)
  cjk: Noto Sans SC
  why: 一半照片是招牌、车站、塔。宽体全大写像站牌和霓虹字，经得住点阵化
hero: { word: JAPAN, sub: "Travel / 26 / 11", line: "Tokyo · Osaka · Kobe · Kyoto" }
motion: { character: 利落, drift: .0032, follow: .075, spring: .06, damp: .82, repel: 60, gather: 950, develop: 1250 }
texture:
  dots: circle
  styles: [orig, ink, dot, block]   # 油墨橙黑双色像日式版画和海报；网点像招牌灯箱；色块给出调色板
sound: { scale: "[0,1,5,7,8] 都节音阶", base: 62, presence: 1 }
chapters:
  - { en: Towers,       zh: 高塔, mood: 仰望, ambient: 城市低鸣 + 钟,     voice: bell }
  - { en: Neon,         zh: 霓虹, mood: 喧闹, ambient: 112BPM 合成器琶音, voice: synth }
  - { en: Vermilion,    zh: 朱红, mood: 祝福, ambient: 稀疏拨弦,          voice: pluck }
  - { en: Green,        zh: 绿荫, mood: 歇脚, ambient: 风 + 鸟鸣,         voice: wood }
  - { en: Wander,       zh: 漫游, mood: 无目的, ambient: 海浪 + 铺底,     voice: high pluck }
  - { en: Small things, zh: 小事, mood: 满足, ambient: lo-fi 电钢 + 黑胶,  voice: keys }
swaps: []
```

---

## B. 冰岛冬天（虚构）

```yaml
trip: "在冰岛的冬天，追一整周的光"
evidence:
  tone: dark / contrast: soft / chroma: muted / temperature: cool
  hue_spread: concentrated, dominant_hue: 205° / night_share: .55
  accent_candidates: aurora #5BE3A6 (153°), ice #9CC9E8 (205°)
color:
  paper: "#0E1215"   # tone 偏暗、夜景过半 → 深色纸（paper_dark_option），让极光和雪发亮
  ink: "#EEF3F6"
  accent: "#4DF0A8"  # 来自 aurora 的 #5BE3A6，提亮。整组照片几乎是冷蓝单色，极光是唯一的反差点，而且确实出现在 4 张照片里
type:
  display: Big Shoulders Display (800), case: upper
  cjk: Noto Sans SC
  why: 窄而高，像冰柱和玄武岩柱；冷、克制
hero: { word: ICELAND, sub: "Winter / 25 / 12", line: "Reykjavík · Vík · Jökulsárlón · Mývatn" }
motion: { character: 漂浮, drift: .0012, follow: .04, spring: .025, damp: .92, repel: 80, gather: 1400, develop: 2000 }
texture:
  dots: line      # 粒子画成随速度拉长的短线，像风里的雪（旋钮，不算 swaps）
  styles: [orig, line, cyan, block]   # 线稿：边缘像冰裂；蓝晒：照片调色板里本来就有深冰蓝；色块保留
sound: { scale: "[0,2,4,6,7,9,11] 利底亚", base: 57, presence: .6 }
chapters:
  - { en: Black sand, zh: 黑沙, ambient: 低通海浪 + 低持续音,          voice: bell (低八度) }
  - { en: Ice,        zh: 冰,   ambient: 高通噪声风 + 随机冰裂,        voice: 新乐器 ice (高通噪声 + 极短包络) }
  - { en: Aurora,     zh: 极光, ambient: 三个慢 LFO 的正弦铺底,         voice: riser (很慢) }
  - { en: Warm rooms, zh: 暖屋, ambient: 黑胶 + 电钢,                  voice: keys }
swaps:
  - ring → 无限网格漂移   # 动效性格是"漂浮"；四条边带的环形流动太"城市"，跟漫天飘雪的整面墙冲突
```

跟 JAPAN 不同的地方：纸、强调色色相、字体、动效、粒子、风格台、音阶、乐器，8 项全不同。

---

## C. 墨西哥城市集（虚构）

```yaml
trip: "在墨西哥城的市集里，吃了一整天"
evidence:
  tone: bright / contrast: hard / chroma: vivid / temperature: warm
  hue_spread: varied / night_share: .05
  accent_candidates: papel-picado #E8358C (330°), chili #D8432A (8°), lime #8CC63F (88°), wall #2F6FD6 (217°)
color:
  paper: "#FFF8EE"   # 偏暖的纸
  ink: "#1A1410"
  accent: "#E8358C"  # 照片颜色四散 → 只能留一个强调色。选剪纸彩旗的粉，因为它在 3 个章节里反复出现，最能代表这里。辣椒红跟 JAPAN 的橙太近，放弃
type:
  display: Rubik (900), case: mixed
  cjk: Noto Sans SC
  why: 圆、胖、热闹，像手绘招牌
hero: { word: MERCADO, sub: "CDMX / 26 / 03", line: "Coyoacán · Roma · La Merced · Xochimilco" }
motion: { character: 弹跳, drift: .004, follow: .09, spring: .08, damp: .7, repel: 70, gather: 800, develop: 1000 }
texture:
  dots: square    # 像瓷砖、像剪纸
  styles: [orig, riso, pixel, block]   # riso 双色像街头海报；像素马赛克像瓷砖墙
sound: { scale: "[0,2,4,5,7,9,11] 大调", base: 64, presence: 1.4 }
chapters:
  - { en: Chiles,   zh: 辣椒, ambient: 带通噪声人声 + 马林巴切分, voice: 新乐器 marimba }
  - { en: Walls,    zh: 墙,   ambient: 木琴稀疏,                 voice: wood }
  - { en: Flowers,  zh: 花船, ambient: 水声 + 拨弦,              voice: pluck }
  - { en: Sweets,   zh: 甜,   ambient: 钢鼓 + 轻打击,            voice: 新乐器 steel drum }
swaps: []
```

---

## D. 上海梅雨夜（虚构）

```yaml
trip: "梅雨季的上海，下班后一个人走回家"
evidence:
  tone: dark / contrast: normal / chroma: muted / temperature: cool
  hue_spread: mixed / night_share: .8
  accent_candidates: sign #F2B33D (40°), neon #E0475C (352°), taxi #3DBFA3 (167°)
color:
  paper: "#15171A"   # 夜景占 80% → 深色纸
  ink: "#E6E3DD"
  accent: "#F2B33D"  # 来自路牌、便利店灯箱的琥珀色。湿地面上反复出现它的倒影，是这组照片的母题
type:
  display: Space Mono (700), case: upper
  cjk: Noto Serif SC
  why: 等宽体像出租车计价器、地铁屏幕；中文用宋体，留一点老城的书卷气
hero: { word: PLUM RAIN, sub: "Shanghai / 26 / 06", line: "Wukang Rd · Bund · Jing'an · Lujiazui" }   # 超过 9 个字母，带空格，会拆成两行
motion: { character: 机械, drift: .005, follow: .11, spring: .09, damp: .74, repel: 50, gather: 750, develop: 900 }
texture:
  dots: circle（发光）
  styles: [orig, scan, ascii, block]   # 扫描线像雨夜里的屏幕；ASCII 像计价器
sound: { scale: "[0,3,5,7,10] 小调五声", base: 57, presence: .7 }
chapters:
  - { en: Puddles,    zh: 水洼, ambient: 雨声（高通噪声 + 随机雨滴）+ 电钢, voice: keys }
  - { en: Signs,      zh: 灯牌, ambient: 合成器琶音（慢，80BPM）,          voice: synth }
  - { en: Plane trees, zh: 梧桐, ambient: 风 + 雨点,                    voice: pluck }
  - { en: Last train, zh: 末班, ambient: 低持续音 + 远处的钟,            voice: bell }
swaps:
  - 大图显影 → 扫描线显影   # 质感是"屏幕、扫描线"，点阵由粗到细像印刷，跟雨夜屏幕的气质冲突
```

---

## 看出来了什么

- **证据不同，决定就不同。**深色纸、强调色、字体、动效、音阶，每一项都能追溯到 evidence 里的数字，或者看图得到的母题。
- **强调色永远只有一个，永远来自照片。**照片颜色四散（C）时更要克制；照片接近单色（B）时，就去找唯一的反差点。
- **替换部件是例外，不是常规。**四份里只有两份各换了一个部件，而且都写了是哪条 DNA 跟默认部件冲突。
