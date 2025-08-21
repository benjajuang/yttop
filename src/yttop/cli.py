#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime
from yt_dlp import YoutubeDL

USAGE = "Usage: yttop <YouTube channel/playlist URL> <Number of videos>"

def fetch_top_videos(channel_url: str, max_count: int):
    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "playlistend": max_count,
        "quiet": True,
        "ignoreerrors": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    entries = (info or {}).get("entries", []) or []
    results = []
    for entry in entries:
        if not entry:
            continue
        title = entry.get("title")
        vid = entry.get("id") or entry.get("url")
        if title and vid:
            results.append({"title": title, "id": vid})
        if len(results) >= max_count:
            break
    return results

def write_output(videos, out_dir=None):
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    base_dir = out_dir if out_dir else os.getcwd()
    out_path = os.path.join(base_dir, filename)
    with open(out_path, "w", encoding="utf-8") as fw:
        for v in videos:
            full_url = f"https://www.youtube.com/watch?v={v['id']}"
            fw.write(f"{v['title']}\n{full_url}\n\n")
    return out_path

def parse_args(argv):
    # No args => interactive mode
    if len(argv) == 1:
        return None, None
    # Arg mode
    if len(argv) == 3:
        url = argv[1]
        try:
            count = int(argv[2])
        except ValueError:
            print("Error: <Number of videos> 必須是一個整數。", file=sys.stderr)
            sys.exit(1)
        return url, count
    print(USAGE, file=sys.stderr)
    sys.exit(1)

def interactive_prompt():
    url = input("Enter YouTube channel/playlist URL: ").strip()
    while not url:
        url = input("URL cannot be empty. Enter YouTube channel/playlist URL: ").strip()
    while True:
        count_str = input("Enter number of videos: ").strip()
        try:
            count = int(count_str)
            if count <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer for the number of videos.")
    return url, count

def main():
    url, count = parse_args(sys.argv)
    if url is None and count is None:
        url, count = interactive_prompt()
    videos = fetch_top_videos(url, count)
    if not videos:
        print("Warning: 無法拿到任何影片。請確認網址是否正確且 yt-dlp 能處理這個 URL。", file=sys.stderr)
        sys.exit(1)
    out_path = write_output(videos)
    print(f"已抓到前 {len(videos)} 部影片，結果存到：{out_path}")

if __name__ == "__main__":
    main()
