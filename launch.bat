echo off
@chcp>nul 2>nul 936

rem ����URL
set URL=
set /p URL=������ URL: 

rem �����ļ���
set saveFold="%USERPROFILE%\Videos\M3U8"
rem Ĭ�����ص�ַ, �س�ֱ��ʹ��, ���Զ���
set /p saveFold=�����뱣��·��(�س�Ĭ�� "��Ƶ\M3U8" ): 

rem ֮ǰ�����Ƶ�temp�ļ���
@mkdir>nul 2>nul "temp\"
@move>nul 2>nul Allm3u8.csv "temp\"

echo �����У����Ժ�

rem python��ȡ��Ƶ��Ϣ��Allm3u8.csv
python allM3U8.py "%URL%"

rem ��ȡcsv
setlocal enabledelayedexpansion
for /f "tokens=1-3 delims=," %%i in (Allm3u8.csv) do (
    set Filename=%%i
    set m3u8URL=%%k
    
    rem ����·��
    @mkdir>nul 2>nul %saveFold%
    rem ��ʼ����m3u8
    N_m3u8DL-CLI --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir !saveFold! --saveName !Filename! !m3u8URL!
)
    
    rem pause