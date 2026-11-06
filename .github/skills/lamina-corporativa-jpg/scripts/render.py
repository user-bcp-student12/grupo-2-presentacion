"""Renderiza una lámina HTML a JPG 1920x1080 (Full HD, 16:9).

Uso:
    python render.py entrada.html salida.jpg [--quality 95]

Usa Edge o Chrome en modo headless y Pillow para garantizar el tamaño exacto.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

W, H = 1920, 1080

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_browser() -> str:
    for p in BROWSERS:
        if os.path.exists(p):
            return p
    for name in ("msedge", "chrome", "google-chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("No se encontró Edge/Chrome. Instálalo o ajusta BROWSERS en render.py.")


def render(html: Path, out: Path, quality: int) -> None:
    browser = find_browser()
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "slide.png"
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={W},{H + 200}",
            f"--user-data-dir={tmp}",
            "--virtual-time-budget=3000",
            f"--screenshot={png}",
            html.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        if not png.exists():
            sys.exit("El navegador no generó la captura.")
        img = Image.open(png).convert("RGB")
        # La ventana es más alta que la lámina; se recorta al área exacta.
        img = img.crop((0, 0, W, H))
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, "JPEG", quality=quality, subsampling=0, optimize=True)
    print(f"OK {out} ({W}x{H})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--quality", type=int, default=95)
    a = ap.parse_args()
    render(a.html, a.out, a.quality)
