echo off
@chcp>nul 2>nul 936

rem 接收URL
set URL=
set /p URL=请输入 URL: 

rem 保存文件夹
set saveFold="%USERPROFILE%\Videos\M3U8"
rem 默认下载地址, 回车直接使用, 可自定义
set /p saveFold=请输入保存路径(回车默认 "视频\M3U8" ): 

rem 之前数据移到temp文件夹
@mkdir>nul 2>nul "temp\"
@move>nul 2>nul Allm3u8.csv "temp\"

echo 加载中，请稍后

rem python获取视频信息到Allm3u8.csv
python allM3U8.py "%URL%"

rem 读取csv
setlocal enabledelayedexpansion
for /f "tokens=1-3 delims=," %%i in (Allm3u8.csv) do (
    set Filename=%%i
    set m3u8URL=%%k
    
    rem 创建路径
    @mkdir>nul 2>nul %saveFold%
    rem 开始下载m3u8
    N_m3u8DL-CLI --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir !saveFold! --saveName !Filename! !m3u8URL!
)
    
    rem pause