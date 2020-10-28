'''
下载 macOS 常用 kexts
要求：
Python 版本 3.X
pip 插件 requests 和 pyperclip
下载工具：迅雷，wget，aria2 至少有一个
说明：
1、默认使用迅雷下载，使用迅雷下载是调用迅雷，然后迅雷访问剪切板。
2、手动输入当前 OpenCore 的版本，请输入正确格式，默认为 0.6.2，可手动更改。
3、可修改下载目录。
4、下载的 kext 是根据 dict_url 字典里的数据下载，请自行添加或修改。
'''
#import os
import subprocess
import requests
import pyperclip  # 剪切板

# 自定义 OpenCore 版本
oc_ver = input("输入当前 OpenCore 版本（默认为 0.6.2）:")
if oc_ver == '':
    oc_ver = '0.6.2'

# 下载目录
download_dir = '~/Downloads'

# GitHub 地址
base_url = 'https://github.com'

'''
定义 url 字典，在 GitHub 里下载下载文件
'''
dict_url = {
    'OpenCore': 'https://github.com/acidanthera/OpenCorePkg/releases/latest',
    'Lilu': 'https://github.com/acidanthera/Lilu/releases/latest',
    'VirtualSMC': 'https://github.com/acidanthera/VirtualSMC/releases/latest',
    'AppleALC': 'https://github.com/acidanthera/AppleALC/releases/latest',
    'WhateverGreen': 'https://github.com/acidanthera/WhateverGreen/releases/latest',
    'AirportBrcmFixup': 'https://github.com/acidanthera/AirportBrcmFixup/releases/latest',
    'BrcmPatchRAM': 'https://github.com/acidanthera/BrcmPatchRAM/releases/latest',
    'BT4LEContinuityFixup': 'https://github.com/acidanthera/BT4LEContinuityFixup/releases/latest',
    'HibernationFixup': 'https://github.com/acidanthera/HibernationFixup/releases/latest',
    'NoTouchID': 'https://github.com/al3xtjames/NoTouchID/releases/latest',
    'PS2Controller': 'https://github.com/acidanthera/VoodooPS2/releases/latest',
    'RealtekRTL8111': 'https://github.com/Mieze/RTL8111_driver_for_OS_X/releases/latest',
    'USBInjectAll': 'https://github.com/Sniki/OS-X-USB-Inject-All/releases/latest',
    'Black80211':'https://github.com/usr-sse2/Black80211-Catalina', # intel WiFi
    
}


'''
全局变量，存储下载的网页源文件
'''
html = ''

def get_internet_ver(url):
    '''
    获取 GitHub 里的版本
    '''
    response = requests.get(url)

    global html
    html = response.text
    # print (html)
    html = html.split("\n")
    ver = ""
    for ver in html:
        ver = ver.strip()
        if len(ver) < 30:
            continue
        if ver.find("/tree/") != -1:
            ver = ver[ver.find("/tree/") + 6:]
            ver = ver[:ver.find('" ')]
            break
    return ver


def get_ver(kext_name):
    '''
    获取 macOS 系统里的 kext 版本
    '''
    if kext_name == 'OpenCore':
        return oc_ver
    cmd = 'kextstat | grep ' + kext_name
    #ver = os.popen(cmd).read()
    ver = subprocess.os.popen(cmd).readline()
    if ver == '':
        # 获取不到版本时
        return 'kext_is_not_installed'
    ver = ver[ver.find('(')+1:ver.find(')')]
    return ver


def check_ver(internet_ver, ver):
    '''
    比较版本
    '''
    # 下掉版本中的 v 字符
    rst = False
    if internet_ver == ver:
        return rst

    internet_ver = internet_ver.replace('v', '')
    internet_ver = internet_ver.replace('V', '')
    internet_ver = internet_ver.split('.')
    ver = ver.split('.')

    n = len(internet_ver)
    for i in range(0, n):
        if internet_ver[i] > ver[i]:
            rst = True
            break
    return rst


def get_dowload_url(kext_name, v_type):
    '''
    获取下载链接
    '''
    ver = get_ver(kext_name)
    if ver == 'kext_is_not_installed':
        # 获取不到版本时
        return 'kext_is_not_installed'
    url = dict_url[kext_name]
    internet_ver = get_internet_ver(url)

    # ver = '0.0.0' # 测试
    rst = check_ver(internet_ver, ver)
    global html
    if rst == True:
        for url in html:
            tmp = url.lower() # 临时字符串， 全部转换成小写
            index = tmp.find('/download/') # 查找 ‘/download/’ 所在位置
            if index != -1:
                ss = ''
                if v_type == '1':
                    ss = 'release'
                else:
                    ss = 'debug'

                if kext_name == 'RealtekRTL8111': # 特例 RealtekRTL8111 不分 debug 和 release 版本
                    ss = '.zip'

                if tmp.find(ss, index) != -1: # 在‘/download/’ 所在位置后 开始查找
                    url = base_url + url[url.find('"/') + 1:url.find('.zip') + 4]
                    return url

    return ''


def download_file(tool, v_type):
    '''
    下载文件
    '''
    for kext_name in dict_url:
        url = get_dowload_url(kext_name, v_type)
        if url == 'kext_is_not_installed':
            continue
        if url != '':
            cmd = ''
            if tool == '1':
                cmd = 'wget -P ' + download_dir + ' ' + url
            elif tool == '3':
                cmd = 'aria2c -d ' + download_dir + ' ' + url

            # os.system(cmd)
            print('开始下载：' + kext_name)
            subprocess.os.system(cmd)
            print('成功下载：' + kext_name)
        else:
            print(kext_name + ' 已是最新版本\n' )


def get_dowload_urls(tool, v_type):
    '''
    下载文件的 URL 集合
    '''
    urls = ''
    for kext_name in dict_url:
        url = get_dowload_url(kext_name, v_type)
        if url == 'kext_is_not_installed':
            continue
        if url != '':
            if tool == '2':
                urls = urls + '\n' + url
            else:
                urls = urls + ' ' + url
        else:
            print(kext_name + ' 已是最新版本\n')

    return urls


def thunder_download(tool, v_type):
    '''
    用迅雷下载
    '''
    urls = get_dowload_urls(tool, v_type)
    urls = urls.lstrip()
    if urls == '':
        print('没有更新')
        return ''

    pyperclip.copy(urls)
    cmd = '/Applications/Thunder.app/Contents/MacOS/Thunder '

    # os.system(cmd)
    subprocess.os.system(cmd)


print("输入序号：")
print("1 使用 wget 下载")
print("2 使用 迅雷 下载(默认)")
print("3 使用 aria2 下载")
tool = input("选择下载工具:")


print("输入版本：")
print("1 Release 版（默认）")
print("2 Debug 版")
v_type = input("选择版本:")
if v_type != '2':
    v_type = '1'

if tool != '1' and tool != '3':
    tool='2'
    thunder_download(tool, v_type)
else:
    download_file(tool, v_type)