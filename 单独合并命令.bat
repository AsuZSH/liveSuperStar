ffmpeg -i 1.mp4 -i 2.mp4 -filter_complex "pad=3360:1080:color=red[x0];[0:v]scale=w=1920:h=1080[inn0];[x0][inn0]overlay=0:0[x1];[1:v]scale=w=1440:h=1080[inn1];[x1][inn1]overlay=1920:0" out.mp4
pause