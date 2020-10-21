# Kexts_Download
 在GitHub中自动下载常用 macOS kext

## 要求：
### 1、Python 版本 3.X
    查看 python 版本
```
 python -V
```
### 2、pip 插件 requests 和 pyperclip
    安装 requests 和 pyperclip
```
 python -m pip install requests
 python -m pip install pyperclip
```
### 3、至少有一个下载工具：迅雷，wget，aria2
## 说明：
### 1、默认使用迅雷下载，使用迅雷下载是调用迅雷，然后迅雷访问剪切板。
### 2、手动输入当前 OpenCore 的版本，请输入正确格式，默认为 0.6.2，可手动更改。
### 3、可修改下载目录。
### 4、下载的 kext 是根据 dict_url 字典里的数据下载，请自行添加或修改。
