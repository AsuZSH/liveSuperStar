# %%

# 因为存在JavaScript动态加载，需要 PhantomJS：https://phantomjs.org/download.html
import time  # 使用延时
import re  # 字符串正则
import csv  # 进行 .CSV 文件读写
from selenium import webdriver  # 动态网页获取 pip install selenium==2.48.0
from getM3U8_info import getM3U8_info  # 调用getM3U8_info
import subprocess  # 加壳的命令行，这里用来调用一些系统程序、文件
from pathlib import Path  # 判定文件是否存在要用
from inputimeout import inputimeout, TimeoutOccurred  # 输入超时检测

# example:python3 cmd.py http://www.jiaxingren.com/folder24/folder147/folder149/folder170/2018-10-25/416269.html
# websiteUrl = "http://newesxidian.chaoxing.com/live/viewNewCourseLive1?isStudent=1&liveId=11094984"  # 正常

# 配置设定

# websiteUrl: 网课地址
# savaFold: 保存位置
# oneOrAll: 1:当前录播, 2:全部录播
# ifDownload: 1:下载, 2:仅解析
# if_m3u8_mobile: 是否处理m3u8_mobile, 1:处理, 2:不处理
# if_m3u8_teacherTrack: 是否处理m3u8_teacherTrack, 1:处理, 2:不处理
# if_m3u8_pptVideo: 是否处理m3u8_pptVideo, 1:处理, 2:不处理
# ifCompose: 1:结束后进行视频拼接, 2:仅下载

websiteUrl = input('请输入课程录播链接：')
savaFold = input('请输入保存位置: ')
print('请输入解析设置')
oneOrAll = input('    1:当前链接, 2:课程全部: ')
ifDownload = input('    解析完成后是否下载(1:下载, 2:仅解析信息输出到 .csv 文件): ')
if ifDownload == '1':
    print('视频流选择(建议优先"1 2 2")：')
    if_m3u8_mobile = input('    是否下载mobile(超星自动拼接老师和PPT, 质量一般)(1:是, 2:否): ')
    if_m3u8_teacherTrack = input('    是否下载teacherTrack(1:是, 2:否): ')
    if_m3u8_pptVideo = input('    是否下载pptVideo(1:是, 2:否): ')
    if if_m3u8_teacherTrack == '1' and if_m3u8_pptVideo == '1':
        print('    teacherTrack与pptVideo可进行视频拼接：左侧老师、右侧PPT，需要Nvidia显卡支持')
        print('        Nvidia驱动下载：https://developer.nvidia.com/cuda-downloads')
        print('        如果不知道上面在说什么，选否')
        ifCompose = input(
            '    是否进行视频拼接(1:是, 2:否): ')
    else:
        ifCompose = '2'
print()
# 抓取 直播ID
print('正在获取信息')
try:
    browser = webdriver.PhantomJS()
except:
    exit('    获取失败, 请重试')
browser.get(websiteUrl)
live_id_info_list = []
while live_id_info_list == []:
    try:
        # 不能确定是否正确执行的代码
        live_id_info_list = browser.find_elements_by_xpath(
            '//*[@class="w_tab_btn w_live_btn"]')
    except:
        time.sleep(2)
# 将 直播id 数量存到num_id
num_id = len(live_id_info_list)
# 课程名称 class_name
class_name = browser.find_element_by_xpath(
    '/html/body/div[1]/div/div[1]/ul/li[1]/a').get_attribute("textContent")[3:]

# %%
# m3u8地址解析 开始


if oneOrAll == '2':
    print('    获取课程信息成功, 课程名:' + class_name + ', 数量:' + str(num_id))
    # 检查是否有已存在的解析文件，ifSkipAnalysis 1：跳过解析，2：不跳过
    ifSkipAnalysis = ''  # 先赋值空，如果解析文件存在，就while，否则赋值'2'
    # 监测解析是否存在
    my_file = Path(savaFold+'\\'+class_name+'\\'+'Allm3u8.csv')
    if my_file.exists():
        # 解析文件存在，获取输入
        while ifSkipAnalysis != '1' and ifSkipAnalysis != '2':
            try:
                # 15秒内未完成输入，则超时
                ifSkipAnalysis = inputimeout(
                    prompt='        检测到当前目录已存在解析文件，是否跳过解析步骤？\n            15秒后自动选"否"(1:是, 2:否)：', timeout=15)
            except TimeoutOccurred:
                ifSkipAnalysis = '2'
    else:
        ifSkipAnalysis = '2'
    # 检测结束
    if ifSkipAnalysis == '2':
        # 创建文件夹
        p = subprocess.Popen('md>nul 2>nul %s' % (savaFold+'\\'+class_name),
                             stdout=None, shell=True)
        return_code = p.wait()  # 等待子进程结束，并返回状态码；

        # 清除可能的已有的解析文件，在新的Allm3u8.csv写入表头
        # 删除旧的ErrorURL.csv
        p = subprocess.Popen('del>nul 2>nul %s' % (savaFold+'\\'+class_name+'\\'+'ErrorURL.csv'),
                             stdout=None, shell=True)
        return_code = p.wait()  # 等待子进程结束，并返回状态码；
        # 删除旧的Allm3u8.csv
        p = subprocess.Popen('del>nul 2>nul %s' % (savaFold+'\\'+class_name+'\\'+'Allm3u8.csv'),
                             stdout=None, shell=True)
        return_code = p.wait()  # 等待子进程结束，并返回状态码；
        # 新的Allm3u8.csv，写入表头
        with open(savaFold+'\\'+class_name+'\\'+'Allm3u8.csv', 'a', newline='') as file:
            Allm3u8TempWriter = csv.writer(file)
            Allm3u8TempWriter.writerow(
                ['录播名称', 'm3u8_mobile', 'm3u8_teacherTrack', 'm3u8_pptVideo'])

        # 提示
        print('        网页加载需要较长时间，请等待(一般每个20秒之内)。。。')
        print('        请不要在程序运行时打开 .csv 文件')
        # for循环，循环处理各视频
        for i in range(1, num_id+1):
            # 输出当前序号
            print('    当前处理：第' + str(i) + '/' + str(num_id) + '个视频')
            # 制作live_info_xpath
            live_info_xpath = '//*[@id="signleCourseList"]/li[' + \
                str(i) + ']/div/a'
            # 获取 id 对应信息live_info_temp
            live_info_temp = browser.find_element_by_xpath(
                live_info_xpath).get_attribute("href")

            # name 直接可用
            # 制作name_xpath
            name_xpath = '//*[@id="signleCourseList"]/li[' + str(i) + ']/p'
            # 获取 name 对应信息name
            name = browser.find_element_by_xpath(
                name_xpath).get_attribute("textContent")
            name = name.replace(" ", "")
            HTML_info_temp = browser.page_source

            # 检索文字设定：live_info_inse
            live_info_inse = re.compile(
                r'([1-9][0-9]{4,})', re.S)  # 正则匹配

            # 检索结果，输出列表：live_temp
            live_temp = re.findall(live_info_inse, live_info_temp)

            # 检索结果处理
            try:
                live_id = str(live_temp[0])

                # 获得M3U8
                # 检索文字设定：URL_inse
                URL_inse = re.compile(
                    r'[a-zA-z]+://[^\s]*liveId=\b', re.S)  # 正则匹配
                # 检索结果，输出URL前缀列表：URL_temp
                URL_temp = re.findall(URL_inse, websiteUrl)
                # 拼接URL前缀 id
                websiteUrl = str(URL_temp)[2:-2] + live_id
                # 获取m3u8所有信息
                m3u8_info = getM3U8_info.getM3U8_info(websiteUrl)

                # 检索文字设定：
                m3u8_info_mobile_temp = re.compile(
                    r'"mobile":".*?.m3u8', re.S)  # 正则匹配 m3u8_info_mobile_temp
                m3u8_info_teacherTrack_temp = re.compile(
                    r'"teacherTrack":".*?.m3u8', re.S)  # 正则匹配 m3u8_info_teacherTrack_temp
                m3u8_info_pptVideo_temp = re.compile(
                    r'"pptVideo":".*?.m3u8', re.S)  # 正则匹配 m3u8_info_pptVideo_temp

                # 检索结果，输出三个列表：
                m3u8_All = re.findall(
                    m3u8_info_mobile_temp, m3u8_info)  # 输出列表：m3u8_All
                m3u8_teacherTrack_temp = re.findall(
                    m3u8_info_teacherTrack_temp, m3u8_info)  # 输出列表：m3u8_teacherTrack_temp
                m3u8_pptVideo_temp = re.findall(
                    m3u8_info_pptVideo_temp, m3u8_info)  # 输出列表：m3u8_pptVideo_temp

                # 检索结果处理
                # 根据最终 待选 m3u8_All 数量是否 >=1 判断其有效性
                if len(m3u8_All) >= 1:
                    # 将最终的三个 m3u8 放到m3u8_mobile、m3u8_teacherTrack、m3u8_pptVideo
                    m3u8_mobile = str(m3u8_All[0])[10:]
                    m3u8_teacherTrack = str(m3u8_teacherTrack_temp[0])[16:]
                    m3u8_pptVideo = str(m3u8_pptVideo_temp[0])[12:]
                else:
                    m3u8_mobile = 'null'
                    m3u8_teacherTrack = 'null'
                    m3u8_pptVideo = 'null'

                # 写入 .csv
                # 文件名，保存位置，三个m3u8 正常数据写入Allm3u8.csv
                if m3u8_mobile != 'null':
                    with open(savaFold+'\\'+class_name+'\\'+'Allm3u8.csv', 'a', newline='') as file:
                        Allm3u8TempWriter = csv.writer(file)
                        Allm3u8TempWriter.writerow(
                            [name, m3u8_mobile, m3u8_teacherTrack, m3u8_pptVideo])
                    print('        处理成功！')
                # 时间，文件名，m3u8 错误数据写入 ErrorURL.csv
                else:
                    with open(savaFold+'\\'+class_name+'\\'+'ErrorURL.csv', 'a', newline='') as AllErrorGet:
                        ErrorURLWriter = csv.writer(AllErrorGet)
                        ErrorURLWriter.writerow(
                            [str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), name, websiteUrl, '视频流不存在'])
                    print('        处理失败，已记录，视频流不存在')
            except:
                with open(savaFold+'\\'+class_name+'\\'+'ErrorURL.csv', 'a', newline='') as AllErrorGet:
                    ErrorURLWriter = csv.writer(AllErrorGet)
                    ErrorURLWriter.writerow(
                        [str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), name, websiteUrl, '超星未上传'])
                print('        处理失败，已记录，可能超星尚未上传')
        # 任务结束，关闭浏览器
        browser.close()
        print('解析任务结束！')

# 仅解析当前链接
elif oneOrAll == '1':
    savaFold = savaFold + '\\' + '单集'
    # 创建文件夹
    p = subprocess.Popen('md>nul 2>nul %s' % (savaFold+'\\'+class_name),
                         stdout=None, shell=True)
    return_code = p.wait()  # 等待子进程结束，并返回状态码；

    # 清除可能的已有文件，在新的Allm3u8.csv写入表头
    # 删除旧的Allm3u8.csv
    p = subprocess.Popen('del>nul 2>nul %s' % (savaFold+'\\'+class_name+'\\'+'Allm3u8.csv'),
                         stdout=None, shell=True)
    return_code = p.wait()  # 等待子进程结束，并返回状态码；
    with open(savaFold+'\\'+class_name+'\\'+'Allm3u8.csv', 'a', newline='') as file:
        Allm3u8TempWriter = csv.writer(file)
        Allm3u8TempWriter.writerow(
            ['录播名称', 'm3u8_mobile', 'm3u8_teacherTrack', 'm3u8_pptVideo'])

    # 获取当前liveId，currentliveId[0]
    currentliveId_inse = re.compile(
        r'\d+$', re.S)  # 正则匹配设定 currentliveId_inse
    currentliveId = re.findall(
        currentliveId_inse, websiteUrl)  # 输出列表：currentliveId

    # 查找livdId对应录播名
    i = 1
    live_id = ''
    while i <= num_id+1 and currentliveId[0] != live_id:
        live_info_xpath = '//*[@id="signleCourseList"]/li[' + \
            str(i) + ']/div/a'
        # 获取 id 对应信息live_info_temp
        live_info_temp = browser.find_element_by_xpath(
            live_info_xpath).get_attribute("href")
        live_info_inse = re.compile(
            r'([1-9][0-9]{4,})', re.S)  # 正则匹配
        # 检索结果，输出列表：live_temp
        live_temp = re.findall(live_info_inse, live_info_temp)
        live_id = str(live_temp[0])
        i = i+1
        # 处理name
        # 制作name_xpath
    i = i - 1
    name_xpath = '//*[@id="signleCourseList"]/li[' + str(i) + ']/p'
    # 获取 name 对应信息name
    name = browser.find_element_by_xpath(
        name_xpath).get_attribute("textContent")
    name = name.replace(" ", "")

    # 获取m3u8所有信息
    try:
        m3u8_info = getM3U8_info.getM3U8_info(websiteUrl)

        # 检索文字设定：
        m3u8_info_mobile_temp = re.compile(
            r'"mobile":".*?.m3u8', re.S)  # 正则匹配 m3u8_info_mobile_temp
        m3u8_info_teacherTrack_temp = re.compile(
            r'"teacherTrack":".*?.m3u8', re.S)  # 正则匹配 m3u8_info_teacherTrack_temp
        m3u8_info_pptVideo_temp = re.compile(
            r'"pptVideo":".*?.m3u8', re.S)  # 正则匹配 m3u8_info_pptVideo_temp

        # 检索结果，输出三个列表：
        m3u8_All = re.findall(
            m3u8_info_mobile_temp, m3u8_info)  # 输出列表：m3u8_All
        m3u8_teacherTrack_temp = re.findall(
            m3u8_info_teacherTrack_temp, m3u8_info)  # 输出列表：m3u8_teacherTrack_temp
        m3u8_pptVideo_temp = re.findall(
            m3u8_info_pptVideo_temp, m3u8_info)  # 输出列表：m3u8_pptVideo_temp

        # 检索结果处理
        # 根据最终 待选 m3u8_All 数量是否 >=1 判断其有效性
        if len(m3u8_All) >= 1:
            # 将最终的三个 m3u8 放到m3u8_mobile、m3u8_teacherTrack、m3u8_pptVideo
            m3u8_mobile = str(m3u8_All[0])[10:]
            m3u8_teacherTrack = str(m3u8_teacherTrack_temp[0])[16:]
            m3u8_pptVideo = str(m3u8_pptVideo_temp[0])[12:]
        else:
            m3u8_mobile = 'null'
            m3u8_teacherTrack = 'null'
            m3u8_pptVideo = 'null'

        # 写入 .csv
        # 文件名，保存位置，三个m3u8 正常数据写入Allm3u8.csv
        if m3u8_mobile != 'null':
            with open(savaFold+'\\'+class_name+'\\'+'Allm3u8.csv', 'a', newline='') as file:
                Allm3u8TempWriter = csv.writer(file)
                Allm3u8TempWriter.writerow(
                    [name, m3u8_mobile, m3u8_teacherTrack, m3u8_pptVideo])
            print('    获取当前链接信息成功：' + name)
        # 时间，文件名，m3u8 错误数据写入 ErrorURL.csv
        else:
            with open(savaFold+'\\'+class_name+'\\'+'ErrorURL.csv', 'a', newline='') as AllErrorGet:
                ErrorURLWriter = csv.writer(AllErrorGet)
                ErrorURLWriter.writerow(
                    [str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), name, websiteUrl, '视频流不存在'])
            exit('处理失败，已记录，视频流不存在')
    except:
        with open(savaFold+'\\'+class_name+'\\'+'ErrorURL.csv', 'a', newline='') as AllErrorGet:
            ErrorURLWriter = csv.writer(AllErrorGet)
            ErrorURLWriter.writerow(
                [str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), name, websiteUrl, '超星未上传'])
        exit('处理失败，已记录，可能超星尚未上传')

    print('解析任务结束！')
else:
    exit('视频范围，输入有误，已退出')

# m3u8地址解析 结束

# %%
# 下载任务，开始

if ifDownload == '1':  # 开始下载
    print('开始执行下载')

    try:
        # 不能确定正确执行的代码
        filename = savaFold+'\\'+class_name+'\\'+'Allm3u8.csv'

        name = []
        m3u8_teacherTrack = []
        m3u8_pptVideo = []
        m3u8_mobile = []
        with open(filename) as csvfile:
            csv_reader = csv.reader(csvfile)  # 使用csv.reader读取Allm3u8.csv
            header = next(csv_reader)  # 读取第一行每一列的标题
            for row in csv_reader:  # 将 csv 文件中的数据保存到m3u8_teacherTrack、m3u8_pptVideo中
                # 读取name
                name.append(row[0])
                # 读取m3u8_mobile到m3u8_mobile数组中
                m3u8_mobile.append(row[1])
                # 读取m3u8_teacherTrack到m3u8_teacherTrack数组中
                m3u8_teacherTrack.append(row[2])
                # 读取m3u8_pptVideo到m3u8_pptVideo数组中
                m3u8_pptVideo.append(row[3])
    except:
        exit('    读取Allm3u8.csv失败，已退出')
    numLen = len(name)
    print('    共计'+str(numLen)+'个录播')
    # 逐个下载，若已存在，则跳过
    for i in range(0, numLen):
        # 处理 m3u8_mobile
        print('        正在处理第' + str(i+1) +
              '/' + str(numLen) + '个录播')
        if if_m3u8_mobile == '1':
            my_file = Path(savaFold+'\\'+class_name+'\\' + '视频' + '\\' +
                           str(name[i]) + '_mobile' + '.mp4')
            if my_file.exists():
                # 查看指定的文件或目录是否存在
                print('            mobile已存在，跳过')
            else:
                print('            正在下载mobile')
                p = subprocess.Popen('N_m3u8DL-CLI --maxThreads 32 --minThreads 2 --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir %s --saveName %s %s' % (savaFold+'\\'+class_name+'\\'+'视频', str(name[i])+'_mobile', str(m3u8_mobile[i])),
                                     shell=True)
                return_code = p.wait()  # 等待子进程结束，并返回状态码；
        # 处理 m3u8_teacherTrack
        if if_m3u8_teacherTrack == '1':
            my_file = Path(savaFold+'\\'+class_name+'\\' + '视频' + '\\' +
                           str(name[i]) + '_teacherTrack' + '.mp4')
            if my_file.exists():
                # 查看指定的文件或目录是否存在
                print('            teacherTrack已存在，跳过')
            else:
                print('            正在下载teacherTrack')
                p = subprocess.Popen('N_m3u8DL-CLI --maxThreads 32 --minThreads 2 --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir %s --saveName %s %s' % (savaFold+'\\'+class_name+'\\'+'视频', str(name[i])+'_teacherTrack', str(m3u8_teacherTrack[i])),
                                     shell=True)
                return_code = p.wait()  # 等待子进程结束，并返回状态码；
        # 处理 m3u8_pptVideo
        if if_m3u8_pptVideo == '1':
            my_file = Path(savaFold+'\\'+class_name+'\\' + '视频' + '\\' +
                           str(name[i]) + '_pptVideo' + '.mp4')
            if my_file.exists():
                # 查看指定的文件或目录是否存在
                print('            pptVideo已存在，跳过')
            else:
                print('            正在下载pptVideo')
                p = subprocess.Popen('N_m3u8DL-CLI --maxThreads 32 --minThreads 2 --disableIntegrityCheck --enableDelAfterDone --retryCount 2 --workDir %s --saveName %s %s' % (savaFold+'\\'+class_name+'\\'+'视频', str(name[i])+'_pptVideo', str(m3u8_pptVideo[i])),
                                     shell=True)
                return_code = p.wait()  # 等待子进程结束，并返回状态码；
    print('下载任务结束！')
elif ifDownload == '2':  # 不进行下载
    print('\n所需资源已经保存在：' + savaFold + '，请查看！\n失败录播信息保存在' +
          savaFold+'\\'+class_name+'\\'+'ErrorURL.csv' + '，请检查！')
    exit('未选择下载，已退出')
else:  # 输入有误
    exit('是否下载，输入有误，已退出')

# 下载任务，结束
# %%

# 合并任务开始
if ifCompose == '1':  # 执行合并
    print('开始执行视频合并任务')
    for i in range(0, numLen):
        print('    正在处理第' + str(i+1) +
              '/' + str(numLen) + '个录播')
        my_file = Path(savaFold+'\\' + class_name + '\\' +
                       '视频' + '\\'+str(name[i]) + '.mp4')
        if my_file.exists():
            print('        已存在，跳过')
        else:
            print('        正在调用ffmpeg合并视频，会很久，请耐心等候')
            # 调用GPU硬件加速视频拼接
            p = subprocess.Popen('ffmpeg -hwaccel cuda -i %s.mp4 -i %s.mp4 -filter_complex "pad=3360:1080:color=red[x0];[0:v]scale=w=1920:h=1080[inn0];[x0][inn0]overlay=0:0[x1];[1:v]scale=w=1440:h=1080[inn1];[x1][inn1]overlay=1920:0" -c:v hevc_nvenc %s.mp4' % (savaFold+'\\'+class_name+'\\'+'视频'+'\\'+str(name[i])+'_teacherTrack', savaFold+'\\'+class_name+'\\'+'视频'+'\\'+str(name[i])+'_pptVideo', savaFold+'\\'+class_name+'\\'+'视频'+'\\'+str(name[i])),
                                 shell=True)
            # -loglevel quiet fatal 可以关闭ffmpeg输出
            return_code = p.wait()  # 等待子进程结束，并返回状态码；
            if return_code == '0':
                print('            视频合并成功！')
            else:
                # 清除ffmpeg合并失败创建的文件
                # p = subprocess.Popen('del>nul 2>nul %s' % (savaFold+'\\'+class_name+'\\'+'视频'+'\\'+str(name[i])+'.mp4'),
                #                      stdout=None, shell=True)
                return_code = p.wait()  # 等待子进程结束，并返回状态码；
                print('            合并失败，请检查设备是否支持！')
    print('视频合并任务结束！')
elif ifCompose == '2':  # 不进行合并
    print('未选择合并任务，已跳过')
else:  # 输入有误
    exit('是否合并，输入有误，已退出')
# 合并任务结束

# 所有任务结束，输出提示
print('\n所需资源已经保存在：' + savaFold + '，请查看！\n失败录播信息保存在' +
      savaFold+'\\'+class_name+'\\'+'ErrorURL.csv' + '，请检查！(如ErrorURL.csv不存在，则全部成功！)')
input('任务完成，回车退出程序')
# %%
