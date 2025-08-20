#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime

from yt_dlp import YoutubeDL

def fetch_top_videos(channel_url, max_count):
    """
    用 yt_dlp 抓 YouTube 頻道（或影片列表）前 max_count 支影片的 title 與 videoId。
    回傳 list of dict: [{"title": ..., "id": ...}, ...]
    """
    ydl_opts = {
        "extract_flat": True,      # 只列清單，不下載影片內容
        "skip_download": True,
        "playlistend": max_count,  # 只取到第 max_count 支影片
        "quiet": True,
        "ignoreerrors": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    entries = info.get("entries", [])
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

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {os.path.basename(sys.argv[0])} <YouTube channel/videos URL> <Number of videos>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        num_videos = int(sys.argv[2])
    except ValueError:
        print("Error: <Number of videos> 必須是一個整數。")
        sys.exit(1)

    # 抓前 num_videos 支影片
    videos = fetch_top_videos(url, num_videos)
    if not videos:
        print("Warning: 無法拿到任何影片。請確認網址是否正確且 yt-dlp 能處理這個 URL。")
        sys.exit(1)

    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    out_path = os.path.join(os.getcwd(), filename)

    with open(out_path, "w", encoding="utf-8") as fw:
      for v in videos:
          full_url = f"https://www.youtube.com/watch?v={v['id']}"
          fw.write(f"{v['title']}\n{full_url}\n\n")


    print(f"已抓到前 {len(videos)} 部影片，結果存到：{out_path}")

if __name__ == "__main__":
    main()
