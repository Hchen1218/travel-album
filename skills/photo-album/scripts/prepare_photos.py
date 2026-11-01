#!/usr/bin/env python3
"""把一文件夹原始照片整理成网站要的两套图，并打印 CHAPTERS 用的宽高。

  photos/sq/<名字>.jpg    640×640 居中裁切的方图，用在首页照片环上
  photos/full/<名字>.jpg  长边 1600，保留原始比例，用在章节页和大图上

用法：
  python3 prepare_photos.py <原始照片文件夹> [--out 网站根目录] [--full 1600] [--sq 640]

需要 Pillow（pip install pillow）。会按 EXIF 方向转正，文件名转成小写短横线。
最后会调用 bake_tints.py 生成 photos/tints.js（直接双击 index.html 打开时，首页点阵字靠它染色）。
输出的 JSON 可以直接抄进 index.html 的 CHAPTERS。
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("需要 Pillow：pip install pillow")

EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "photo"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("--out", type=Path, default=Path("."))
    ap.add_argument("--full", type=int, default=1600)
    ap.add_argument("--sq", type=int, default=640)
    a = ap.parse_args()

    files = sorted(p for p in a.src.iterdir() if p.suffix.lower() in EXT)
    if not files:
        sys.exit(f"{a.src} 里没有照片")
    full_dir, sq_dir = a.out / "photos" / "full", a.out / "photos" / "sq"
    full_dir.mkdir(parents=True, exist_ok=True)
    sq_dir.mkdir(parents=True, exist_ok=True)

    out, used = [], set()
    for p in files:
        try:
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        except Exception as e:
            print(f"跳过 {p.name}：{e}", file=sys.stderr)
            continue
        name = base = slug(p.stem)
        k = 2
        while name in used:
            name, k = f"{base}-{k}", k + 1
        used.add(name)

        full = im.copy()
        full.thumbnail((a.full, a.full), Image.LANCZOS)
        full.save(full_dir / f"{name}.jpg", quality=86, optimize=True, progressive=True)
        ImageOps.fit(im, (a.sq, a.sq), Image.LANCZOS).save(sq_dir / f"{name}.jpg", quality=84, optimize=True, progressive=True)
        out.append({"src": name, "w": full.width, "h": full.height, "from": p.name})
        print(f"{p.name} → {name}  {full.width}×{full.height}", file=sys.stderr)

    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from bake_tints import bake
    bake(a.out)


if __name__ == "__main__":
    main()
