@echo off
@chcp>nul 2>nul 936

rem ����URL
set URL=
set /p URL=������ URL: 

rem ֮ǰ�����Ƶ�temp�ļ���
@mkdir>nul 2>nul "temp\"
@move>nul 2>nul Allm3u8.csv "temp\"

echo �����У����Ժ�

rem python��ȡ��Ƶ��Ϣ��Allm3u8.csv
python allM3U8Analysis.py "%URL%"

echo ������������ɣ������Ϣ�Ѿ����浽Allm3u8.csv��AllErrorURL.csv