"""Download every paper in papers.csv into papers/. Re-run any time: files already there are skipped.

Uses curl (ships with Windows 10+). IACR ePrint serves PDFs behind a browser check, so those
are listed at the end for you to download by hand into papers/ with the printed file name.
Usage: python download.py
"""
import csv
import pathlib
import re
import shutil
import subprocess
import time

HERE = pathlib.Path(__file__).parent
OUT = HERE / "papers"
# Some hosts (HAL) challenge browser user agents, others (RHUL) block curl's: try both.
AGENTS = ["curl/8", "Mozilla/5.0", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"]


def file_name(row):
    first = re.sub(r"[^A-Za-z]", "", row["authors"].split(",")[0])  # "El Maouaki" -> ElMaouaki
    words = re.sub(r"[^A-Za-z0-9 ]", "", row["title"]).split()[:6]
    return f"{row['id']}_{first}{row['year']}_{'_'.join(words)}.pdf"


def is_pdf(path):
    data = path.read_bytes()
    return data[:5] == b"%PDF-" and b"%%EOF" in data[-2048:]  # header + trailer: catches cut-off downloads


def fetch(url, dest):
    if url.startswith("local:"):
        src = HERE / url[len("local:"):]
        if src.exists():
            shutil.copy(src, dest)
        return dest.exists()
    for agent in AGENTS:
        subprocess.run(["curl", "-sL", "--retry", "2", "--max-time", "180", "-A", agent, "-o", str(dest), url])
        if dest.exists() and is_pdf(dest):
            return True
        time.sleep(2)
    dest.unlink(missing_ok=True)
    return False


def main():
    OUT.mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(HERE / "papers.csv", encoding="utf-8")))
    manual = []
    for row in rows:
        dest = OUT / file_name(row)
        if dest.exists() and is_pdf(dest):
            print(f"[have] {dest.name}")
            continue
        ok = fetch(row["pdf_url"], dest)
        print(f"[{'ok' if ok else 'MISS'}] {dest.name}")
        if not ok:
            manual.append((dest.name, row["page_url"]))
        time.sleep(3)  # arXiv asks automated clients for <= 1 request / 3 s
    print(f"\n{len(rows) - len(manual)}/{len(rows)} PDFs in {OUT}")
    if manual:
        print("Download these by hand (open the link, save the PDF into papers/ under this name):")
        for name, page in manual:
            print(f"  {name}\n    {page}")


if __name__ == "__main__":
    main()
