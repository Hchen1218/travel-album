#!/usr/bin/env python3
"""量照片：给"风格 DNA"提供可计算的那一半信号。

  python3 analyze_photos.py [照片文件夹，默认 photos/full] [--out 输出文件夹，默认当前目录]

输出两样东西：
  dna-seed.json  每张照片的 5 个主色、明暗、反差、饱和度、冷暖、色相集中度；
                 整组照片的总体判断（tone / chroma / temperature / hue_spread / night_share）、
                 强调色候选（每个都注明来自哪张照片）、纸色和墨色建议、按颜色粗分的章节草案
  contact.jpg    全部照片的缩略图总览，每张下面带 5 个主色，给 agent 自己"看图"用

脚本只量，不做设计决定。怎么把这些数字变成颜色、字体、动效和声音，见 references/style-dna.md。
需要 Pillow（pip install pillow）。
"""
import argparse, colorsys, json, math, random, sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("需要 Pillow：pip install pillow")

EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
lum = lambda c: (c[0] * .299 + c[1] * .587 + c[2] * .114) / 255
hexof = lambda c: "#" + "".join(f"{round(v):02X}" for v in c)


def kmeans(px, k=5, iters=10):
    """和网站里 lbPalette 同一个做法：按亮度分位数起步，结果稳定、不随机。"""
    px = sorted(px, key=lum)
    C = [list(px[int(q * (len(px) - 1))]) for q in [(i + .5) / k for i in range(k)]]
    for _ in range(iters):
        S = [[0, 0, 0, 0] for _ in C]
        for p in px:
            j = min(range(len(C)), key=lambda j: (C[j][0] - p[0]) ** 2 + (C[j][1] - p[1]) ** 2 + (C[j][2] - p[2]) ** 2)
            s = S[j]; s[0] += p[0]; s[1] += p[1]; s[2] += p[2]; s[3] += 1
        C = [[s[0] / s[3], s[1] / s[3], s[2] / s[3]] if s[3] else C[j] for j, s in enumerate(S)]
    n = [0] * len(C)
    for p in px:
        n[min(range(len(C)), key=lambda j: sum((C[j][i] - p[i]) ** 2 for i in range(3)))] += 1
    return sorted(({"hex": hexof(c), "rgb": [round(v) for v in c], "share": round(n[j] / len(px), 3)} for j, c in enumerate(C)),
                  key=lambda d: -d["share"])


def measure(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    W, H = im.size
    small = im.resize((64, 64), Image.BILINEAR)
    px = list(small.getdata())
    Ls = [lum(p) for p in px]
    L = sum(Ls) / len(Ls)
    contrast = math.sqrt(sum((x - L) ** 2 for x in Ls) / len(Ls))
    sats, warm, hx, hy, hn, vivid = [], 0, 0, 0, 0, []
    for r, g, b in px:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        sats.append(s * v)                       # 暗处的"饱和"不算数
        warm += (r - b) / 255
        if s > .25 and v > .2:                    # 只拿有颜色的像素算色相
            hx += math.cos(h * 2 * math.pi) * s; hy += math.sin(h * 2 * math.pi) * s; hn += s
        if s > .5 and v > .45:
            vivid.append((r, g, b))
    # 面积小但很鲜艳的颜色（比如天空里的一座橙色塔），整体 k-means 会把它平均掉，单独再聚一次
    spots = []
    if len(vivid) >= 40:
        for c in kmeans(vivid, k=min(3, len(vivid) // 40)):
            spots.append({**c, "share": round(c["share"] * len(vivid) / len(px), 3)})
    conc = math.hypot(hx, hy) / hn if hn else 0  # 1 = 全是一个色相，0 = 色相四散
    hue = (math.degrees(math.atan2(hy, hx)) % 360) if hn else None
    bright = sorted(Ls)[int(.97 * len(Ls))]
    return {
        "file": path.name, "src": path.stem, "w": W, "h": H,
        "orientation": "portrait" if H > W * 1.05 else "landscape" if W > H * 1.05 else "square",
        "palette": kmeans(px),
        "luminance": round(L, 3), "contrast": round(contrast, 3),
        "saturation": round(sum(sats) / len(sats), 3),
        "warmth": round(warm / len(px), 3),
        "hue": None if hue is None else round(hue), "hue_concentration": round(conc, 3),
        "night_guess": L < .36 and bright > .5,         # 整体暗、但有亮的光源：夜景（只是猜，要看图确认）
        "vivid_spots": spots,
        "_hue_vec": [hx, hy, hn],
    }


def label(v, cuts, names):
    for c, n in zip(cuts, names):
        if v < c:
            return n
    return names[-1]


def accent_candidates(photos, n=6):
    """有分量、够鲜艳的颜色，按色相去重。每个都记住它来自哪张照片——强调色必须能说出出处。"""
    pool = []
    for p in photos:
        for c in p["palette"] + p["vivid_spots"]:
            h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c["rgb"]))
            if s > .45 and v > .4 and c["share"] >= .02:
                pool.append({"hex": c["hex"], "from": p["src"], "hue": round(h * 360), "chroma": round(s * v, 3),
                             "share": c["share"], "score": round((s * v) ** 2 * (.15 + c["share"]) ** .5, 3)})
    pool.sort(key=lambda d: -d["score"])
    out = []
    for c in pool:
        if all(min(abs(c["hue"] - o["hue"]), 360 - abs(c["hue"] - o["hue"])) > 22 for o in out):
            out.append(c)
        if len(out) == n:
            break
    return out


def paper_ink(photos, temperature):
    """纸：带一点照片整体冷暖的近白；墨：照片里最暗的低饱和色，压到近黑。"""
    tint = {"warm": (255, 251, 246), "cool": (246, 249, 252), "neutral": (250, 250, 248)}[temperature]
    darks = [c["rgb"] for p in photos for c in p["palette"] if lum(c["rgb"]) < .25]
    if darks:
        d = min(darks, key=lum)
        ink = [round(18 + (v - sum(d) / 3) * .25) for v in d]
    else:
        ink = [18, 18, 18]
    return {"paper_light": hexof(tint), "ink": hexof([max(0, min(60, v)) for v in ink]),
            "paper_dark_option": hexof([max(8, v) for v in ink]), "ink_on_dark_option": hexof(tint)}


def chapter_draft(photos):
    """只按颜色和明暗粗分；agent 还要结合地点、题材、时间重新分。"""
    n = len(photos)
    k = max(2, min(7, round(n / 4)))
    feat = []
    for p in photos:
        hue = math.radians(p["hue"] or 0) if p["hue"] is not None else 0
        feat.append([p["luminance"] * 2, p["saturation"] * 3, p["warmth"] * 2,
                     math.cos(hue) * p["hue_concentration"], math.sin(hue) * p["hue_concentration"]])
    random.seed(7)
    C = [feat[i][:] for i in random.sample(range(n), k)]
    for _ in range(30):
        A = [min(range(k), key=lambda j: sum((f[i] - C[j][i]) ** 2 for i in range(5))) for f in feat]
        for j in range(k):
            m = [feat[i] for i in range(n) if A[i] == j]
            if m:
                C[j] = [sum(x[i] for x in m) / len(m) for i in range(5)]
    groups = [[photos[i]["src"] for i in range(n) if A[i] == j] for j in range(k)]
    return [g for g in groups if g]


def contact_sheet(photos, folder, out, cell=220, cols=6):
    rows = math.ceil(len(photos) / cols)
    pad, cap = 14, 46
    sheet = Image.new("RGB", (cols * (cell + pad) + pad, rows * (cell + cap + pad) + pad), (244, 242, 238))
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.load_default(size=13)
    except TypeError:
        font = ImageFont.load_default()
    for i, p in enumerate(photos):
        x, y = pad + (i % cols) * (cell + pad), pad + (i // cols) * (cell + cap + pad)
        im = ImageOps.exif_transpose(Image.open(folder / p["file"])).convert("RGB")
        im.thumbnail((cell, cell))
        sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
        sx = x
        for c in p["palette"]:
            w = max(2, round(cell * c["share"]))
            dr.rectangle([sx, y + cell + 4, sx + w, y + cell + 16], fill=tuple(c["rgb"]))
            sx += w
        dr.text((x, y + cell + 22), f"{i + 1:02d} {p['src']}"[:30], fill=(30, 30, 30), font=font)
    sheet.save(out, quality=86)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path, nargs="?", default=Path("photos/full"))
    ap.add_argument("--out", type=Path, default=Path("."))
    a = ap.parse_args()
    files = sorted(p for p in a.src.iterdir() if p.suffix.lower() in EXT)
    if not files:
        sys.exit(f"{a.src} 里没有照片")
    photos = []
    for f in files:
        print(f"量 {f.name}", file=sys.stderr)
        photos.append(measure(f))

    avg = lambda k: sum(p[k] for p in photos) / len(photos)
    L, S, Wm = avg("luminance"), avg("saturation"), avg("warmth")
    hx, hy, hn = (sum(p["_hue_vec"][i] for p in photos) for i in range(3))
    Cn = math.hypot(hx, hy) / hn if hn else 0      # 整组照片放在一起，色相集中还是四散
    for p in photos:
        del p["_hue_vec"]
    temperature = label(Wm, [-.03, .05], ["cool", "neutral", "warm"])
    summary = {
        "count": len(photos),
        "tone": label(L, [.32, .55], ["dark", "mid", "bright"]),
        "contrast": label(avg("contrast"), [.17, .25], ["soft", "normal", "hard"]),
        "chroma": label(S, [.1, .2], ["muted", "moderate", "vivid"]),
        "temperature": temperature,
        "hue_spread": label(Cn, [.3, .55], ["varied", "mixed", "concentrated"]),
        "dominant_hue": round(math.degrees(math.atan2(hy, hx)) % 360) if hn else None,
        "night_share": round(sum(p["night_guess"] for p in photos) / len(photos), 2),
        "portrait_share": round(sum(p["orientation"] == "portrait" for p in photos) / len(photos), 2),
        "raw": {"luminance": round(L, 3), "saturation": round(S, 3), "warmth": round(Wm, 3), "hue_concentration": round(Cn, 3)},
    }
    seed = {
        "summary": summary,
        "accent_candidates": accent_candidates(photos),
        "paper_ink": paper_ink(photos, temperature),
        "chapter_draft_by_color": chapter_draft(photos),
        "photos": photos,
    }
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "dna-seed.json").write_text(json.dumps(seed, ensure_ascii=False, indent=1))
    contact_sheet(photos, a.src, a.out / "contact.jpg")
    print(json.dumps({"summary": summary, "accent_candidates": seed["accent_candidates"], "paper_ink": seed["paper_ink"]},
                     ensure_ascii=False, indent=1))
    print(f"\n写好了 {a.out / 'dna-seed.json'} 和 {a.out / 'contact.jpg'}", file=sys.stderr)


if __name__ == "__main__":
    main()
