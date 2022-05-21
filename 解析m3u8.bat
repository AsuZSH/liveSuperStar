@echo off
@chcp>nul 2>nul 936

rem 接收URL
set URL=
set /p URL=请输入 URL: 

rem 之前数据移到temp文件夹
@mkdir>nul 2>nul "temp\"
@move>nul 2>nul Allm3u8.csv "temp\"

echo 加载中，请稍后

rem python获取视频信息到Allm3u8.csv
python allM3U8Analysis.py "%URL%"

echo 解析任务已完成，相关信息已经保存到Allm3u8.csv和AllErrorURL.csv