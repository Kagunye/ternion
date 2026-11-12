#!/bin/sh
# Hero clip: first 3.2 s of the source (crane lifting a container on white),
# cursor painted out (it sits on plain white background),
# source site's nav bar cropped off, mirrored so the crane
# sits on the right, shadows nudged toward the Ternion navy, then played
# forward + reversed for a seamless loop. No audio.
# Usage: sh tools/process_video.sh "<source.mp4>"
set -e
SRC="$1"
OUT="$(dirname "$0")/../static/video"
FILTER="[0:v]trim=0:3.2,setpts=PTS-STARTPTS,format=rgb24,drawbox=x=440:y=171:w=33:h=28:color=0xFCFCFC@1:t=fill,drawbox=x=452:y=198:w=17:h=5:color=0xFCFCFC@1:t=fill,crop=740:330:0:130,hflip,curves=r='0/0.03 0.25/0.25 1/1':g='0/0.12 0.25/0.27 1/1':b='0/0.30 0.25/0.36 1/1',split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]"
ffmpeg -v error -y -i "$SRC" -filter_complex "$FILTER" -map "[v]" -an -c:v libx264 -crf 22 -preset slow -pix_fmt yuv420p -movflags +faststart "$OUT/hero.mp4"
ffmpeg -v error -y -i "$SRC" -filter_complex "$FILTER" -map "[v]" -an -c:v libvpx-vp9 -crf 34 -b:v 0 "$OUT/hero.webm"
ffmpeg -v error -y -i "$OUT/hero.mp4" -frames:v 1 -q:v 3 "$OUT/hero-poster.jpg"
ls -la "$OUT"
