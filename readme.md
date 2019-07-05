# ScreenTranslation

1. 一款截图翻译小工具，自带截屏功能`快捷键shift+q`，**文本识别**，**自动识别中英文**，**翻译功能**调用百度接口！
2. 可监听剪贴板，支持其他第三方任意截屏软件，截屏至剪贴板即可自动翻译！支持系统小托盘图标！
3. 代码需要配置秘钥文件才能运行，其他依赖包可`pip install` 自行安装！
4. 程序有发行版本，可直接下载使用！

### 一、使用方法及运行环境

#### 1、推荐python3.6以上版本编译器！

#### 2、需要在cmd命令下安装以下依赖包！

```python
pip install requests #安装requests模块，用于翻译接口！
```

```python
pip install baidu-aip #百度接口OCR模块，用于图像识别
```

```python
pip install PyQt5 #Gui界面模块
```

```python
pip install Pillow #用于剪贴板图片，保存本地磁盘
```

#### 3、配置Secretkey.py秘钥文件

##### 			**①获取文本识别秘钥注册网址** :http://ai.baidu.com/tech/ocr/general

```python
'''这里是百度图像识别秘钥，需要自己去注册获得秘钥'''

img_APP_ID = '替换你注册获取到的秘钥'
img_API_KEY = '替换你注册获取到的秘钥'
img_ECRET_KEY = '替换你注册获取到的秘钥'
```

##### 	**②获取百度翻译秘钥注册网址**:**http://api.fanyi.baidu.com/api/trans/product/index**

```python
'''这里是百度翻译秘钥，需要自己去注册获得秘钥'''

fy_APP_ID = "替换你注册获取到的秘钥"
fy_Secret_key = "替换你注册获取到的秘钥"
```

#### 4、运行jtfy4.0.py主程序！

### 二、发行版本

- 若安装环境或运行报错，可直接下载发行版本使用！
- 下载地址: https://github.com/lyjxhxn/ScreenTranslation/releases

### 三、程序界面

![](https://s2.ax1x.com/2019/06/21/Vx0SSJ.png)



![https://s2.ax1x.com/2019/06/21/VxwMIU.png](https://s2.ax1x.com/2019/06/21/VxwMIU.png)

