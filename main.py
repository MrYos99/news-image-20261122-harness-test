"""Harness probe: Pillow + TTF availability in the make.fun entry sandbox.

The verdict is encoded in the artifact itself, so the harness
reproduction carries it:
  RED   -> Pillow is NOT importable (stdlib-only fallback drew this)
  BLUE  -> Pillow imports, but the shipped TTF font cannot be loaded
  GREEN -> Pillow imports AND the shipped DejaVuSerif.ttf loads
Every branch writes a valid 1024x1024 PNG to /output/entry.png
and exits 0, so a missing library can never crash the probe.
"""
import os
import struct
import sys
import zlib

W = H = 1024


def out_path():
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def _crc32(data):
    return zlib.crc32(data) & 0xFFFFFFFF


def _chunk(kind, data):
    c = struct.pack(">I", len(data)) + kind + data
    return c + struct.pack(">I", _crc32(kind + data))


def png_bytes(rgb):
    # rgb: W*H*3 bytes, one scanline per row, filter byte 0 each row.
    raw = b"".join(b"\x00" + rgb[y * W * 3:(y + 1) * W * 3] for y in range(H))
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(raw, 9))
        + _chunk(b"IEND", b"")
    )


def write_png(path, rgb):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png_bytes(rgb))


def solid_rgb(r, g, b):
    return bytes([r, g, b]) * (W * H)


def main():
    path = out_path()
    try:
        from PIL import Image, ImageDraw, ImageFont
        import PIL
    except Exception as exc:
        # No Pillow at all: stdlib-only red image. Log the import error
        # so the harness run log says WHY it is missing, not just that.
        print("PROBE: PIL import failed:", repr(exc))
        write_png(path, solid_rgb(176, 30, 36))
        print("PROBE: PIL missing -> RED")
        return 0
    # Pillow is importable. Try the TTF shipped in the repo.
    here = os.path.dirname(os.path.abspath(__file__))
    ttf = os.path.join(here, "DejaVuSerif.ttf")
    try:
        font = ImageFont.truetype(ttf, 48)
        font_small = ImageFont.truetype(ttf, 28)
        ttf_ok = True
    except Exception as exc:
        print("PROBE: TTF load failed:", exc)
        ttf_ok = False
    if not ttf_ok:
        img = Image.new("RGB", (W, H), (29, 58, 110))
        d = ImageDraw.Draw(img)
        d.text((60, 460), "PIL OK, TTF FAIL", fill=(255, 255, 255))
        d.text((60, 540), "Pillow " + PIL.__version__, fill=(255, 255, 255))
        img.save(path, format="PNG")
        print("PROBE: PIL ok, TTF fail -> BLUE")
        return 0
    img = Image.new("RGB", (W, H), (27, 120, 55))
    d = ImageDraw.Draw(img)
    d.text((60, 440), "PIL OK, TTF OK", font=font, fill=(255, 255, 255))
    d.text((60, 520), "Pillow " + PIL.__version__, font=font_small, fill=(255, 255, 255))
    d.text((60, 570), "DejaVuSerif.ttf loaded from repo", font=font_small, fill=(255, 255, 255))
    img.save(path, format="PNG")
    print("PROBE: PIL ok, TTF ok -> GREEN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
