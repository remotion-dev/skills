#!/usr/bin/env bash
# Editorial pass for a cinematic trailer: trim + color grade + music + VO mix.
# Designed to beat the Cowork 45s bash timeout by running in stages.
#
# Usage:
#   ./editorial_pass.sh <project_dir>
#
# Expected files in <project_dir>:
#   scene1-cold-open.mp4 ... scene8-title-card.mp4
#   vo/vo-01-cold-open.mp3 ... vo/vo-05-resolution.mp3
#   edit/<music_track>.mp3   (only one, will be auto-detected)
#
# Produces: <project_dir>/TRAILER-DIRECTORS-CUT.mp4

set -e
PROJECT="${1:-$(pwd)}"
cd "$PROJECT"

# Standard grades (locked from production runs)
GRADE_WARM="colorbalance=rs=.06:bs=-.08,eq=contrast=1.10:saturation=0.92:gamma=0.96,vignette=angle=PI/5"
GRADE_COOL="colorbalance=rs=.04:bs=.02,eq=contrast=1.15:saturation=0.85:gamma=0.92,vignette=angle=PI/5"
GRADE_HERO="colorbalance=rs=.05:bs=-.05,eq=contrast=1.08:saturation=0.95:gamma=0.97,vignette=angle=PI/5"

mkdir -p cut
MUSIC=$(ls edit/*.mp3 | head -1)
if [ -z "$MUSIC" ]; then
  echo "ERROR: no music track found in edit/ — drop an MP3 there first" >&2
  exit 1
fi
echo "Using music: $MUSIC"

# --- Stage 1: trim + grade scenes 1-4 ---
echo "Stage 1: trim + grade scenes 1-4..."
ffmpeg -y -loglevel error \
 -i scene1-cold-open.mp4 -i scene2-arrival.mp4 -i scene3-war-room.mp4 -i scene4-hustle-montage.mp4 \
 -filter_complex "\
[0:v]trim=0.5:4.5,setpts=PTS-STARTPTS,$GRADE_WARM[v0];\
[1:v]trim=2:6,setpts=PTS-STARTPTS,$GRADE_WARM[v1];\
[2:v]trim=1:4,setpts=PTS-STARTPTS,$GRADE_WARM[v2];\
[3:v]trim=0:3,setpts=PTS-STARTPTS,$GRADE_WARM[v3];\
[v0][v1][v2][v3]concat=n=4:v=1:a=0[v]" \
 -map "[v]" -c:v libx264 -crf 22 -preset ultrafast -pix_fmt yuv420p -an cut/part1.mp4

# --- Stage 2: trim + grade scenes 5-8 ---
echo "Stage 2: trim + grade scenes 5-8..."
ffmpeg -y -loglevel error \
 -i scene5-buyer-couple.mp4 -i scene6-crisis-desk.mp4 -i scene7-kitchen-resolution.mp4 -i scene8-title-card.mp4 \
 -filter_complex "\
[0:v]trim=5:10,setpts=PTS-STARTPTS,$GRADE_WARM[v4];\
[1:v]trim=1:9,setpts=PTS-STARTPTS,$GRADE_COOL[v5];\
[2:v]trim=2:10,setpts=PTS-STARTPTS,$GRADE_HERO[v6];\
[3:v]trim=0:5,setpts=PTS-STARTPTS[v7];\
[v4][v5][v6][v7]concat=n=4:v=1:a=0[v]" \
 -map "[v]" -c:v libx264 -crf 22 -preset ultrafast -pix_fmt yuv420p -an cut/part2.mp4

# --- Stage 3: concat (instant, no re-encode) ---
echo "Stage 3: concat the two halves..."
cat > cut/concat.txt <<EOF
file 'part1.mp4'
file 'part2.mp4'
EOF
ffmpeg -y -loglevel error -f concat -safe 0 -i cut/concat.txt -c copy cut/silent-cut.mp4

# --- Stage 4: mix music + VOs onto silent cut ---
echo "Stage 4: mix audio (music + 5 VOs)..."
ffmpeg -y -loglevel error \
 -i cut/silent-cut.mp4 \
 -i "$MUSIC" \
 -i vo/vo-01-cold-open.mp3 -i vo/vo-02-arrival.mp3 -i vo/vo-03-buyer-found.mp3 \
 -i vo/vo-04-dialogue-scene6.mp3 -i vo/vo-05-resolution.mp3 \
 -filter_complex "\
[1:a]volume=0.32,afade=t=in:st=0:d=1.5,afade=t=out:st=37:d=3,atrim=end=40[music];\
[2:a]adelay=500|500,volume=1.5[a1];\
[3:a]adelay=4500|4500,volume=1.5[a2];\
[4:a]adelay=15000|15000,volume=1.5[a3];\
[5:a]adelay=23000|23000,volume=1.7[a4];\
[6:a]adelay=30000|30000,volume=1.5[a5];\
[music][a1][a2][a3][a4][a5]amix=inputs=6:duration=longest:normalize=0,alimiter=limit=0.95[aout]" \
 -map 0:v -map "[aout]" \
 -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart \
 TRAILER-DIRECTORS-CUT.mp4

echo "---"
echo "Done. Output:"
ls -lh TRAILER-DIRECTORS-CUT.mp4
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 TRAILER-DIRECTORS-CUT.mp4
