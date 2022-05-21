import subprocess  # 加壳的命令行，这里用来调用一些系统程序、文件
import csv  # csv文件处理
from pathlib import Path  # 判定文件是否存在要用

try:
    # 不能确定正确执行的代码
    filename = 'Allm3u8.csv'

    name = []
    m3u8_teacherTrack = []
    m3u8_pptVideo = []
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取Allm3u8.csv
        header = next(csv_reader)  # 读取第一行每一列的标题
        for row in csv_reader:  # 将 csv 文件中的数据保存到m3u8_teacherTrack、m3u8_pptVideo中
            # 读取name
            name.append(row[0])
            # 读取m3u8_teacherTrack到m3u8_teacherTrack数组中
            m3u8_teacherTrack.append(row[2])
            # 读取m3u8_pptVideo到m3u8_pptVideo数组中
            m3u8_pptVideo.append(row[3])
    # 回显
    print('读取Allm3u8.csv成功')
except:
    print('读取Allm3u8.csv失败')
    exit()

# 预设保存位置在：视频\M3U8，询问用户
saveFold = input('请输入保存位置(回车默认 "视频\M3U8" )：')
if saveFold == '':
    saveFold = "%USERPROFILE%\Videos\M3U8"

numLen = len(name)
print('共计'+str(numLen)+'个录播')
for i in range(0, numLen):

    my_file = Path(saveFold + '\\'+str(name[i]) + '_teacherTrack' + '.mp4')
    if my_file.exists():
        # 查看指定的文件或目录是否存在
        print(str(name[i])+'_teacherTrack' + '.mp4' + '已存在，跳过')
    else:
        print('正在下载第' + str(i+1) + '个视频的teacherTrack')
        p = subprocess.Popen('N_m3u8DL-CLI --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir %s --saveName %s %s' % (saveFold, str(name[i])+'_teacherTrack', str(m3u8_teacherTrack[i])),
                             shell=True)
        return_code = p.wait()  # 等待子进程结束，并返回状态码；

    my_file = Path(saveFold + '\\'+str(name[i]) + '_pptVideo' + '.mp4')
    if my_file.exists():
        # 查看指定的文件或目录是否存在
        print(str(name[i])+'_pptVideo' + '.mp4' + '已存在，跳过')
    else:
        print('正在下载第' + str(i+1) + '个视频的pptVideo')
        p = subprocess.Popen('N_m3u8DL-CLI --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir %s --saveName %s %s' % (saveFold, str(name[i])+'_pptVideo', str(m3u8_pptVideo[i])),
                             shell=True)
        return_code = p.wait()  # 等待子进程结束，并返回状态码；

    my_file = Path(saveFold + '\\'+str(name[i]) + '.mp4')
    if my_file.exists():
        print(str(name[i]) + '.mp4' + '已存在，跳过')
    else:
        print('正在调用ffmpeg合并视频，会很久，请耐心等候')
        p = subprocess.Popen('ffmpeg -i %s.mp4 -i %s.mp4 -filter_complex "pad=3360:1080:color=red[x0];[0:v]scale=w=1920:h=1080[inn0];[x0][inn0]overlay=0:0[x1];[1:v]scale=w=1440:h=1080[inn1];[x1][inn1]overlay=1920:0" %s.mp4' % (saveFold+'\\'+str(name[i])+'_teacherTrack', saveFold+'\\'+str(name[i])+'_pptVideo', saveFold+'\\'+str(name[i])),
                             shell=True)
        # -loglevel quiet 可以关闭ffmpeg输出
        return_code = p.wait()  # 等待子进程结束，并返回状态码；
        print('视频合并成功！')
