# ScreenTranslation

1. 一款截图翻译小工具，自带截屏功能`快捷键shift+q`，**文本识别**，**自动识别中英文**，**翻译功能**调用百度接口！
2. 可监听剪贴板，支持其他第三方任意截屏软件，截屏至剪贴板即可自动翻译！支持系统小托盘图标！
3. 代码需要配置秘钥文件才能运行，其他依赖包可`pip install` 自行安装！
4. 程序有发行版本，可直接下载使用！

#### 获取秘钥方法

**1. 文本识别注册网址** :http://ai.baidu.com/tech/ocr/general

````````
'''这里是百度图像识别秘钥，需要自己去注册获得秘钥'''

img_APP_ID = '替换你注册获取到的秘钥'
img_API_KEY = '替换你注册获取到的秘钥'
img_ECRET_KEY = '替换你注册获取到的秘钥'

````````



**2. 翻译功能注册网址**:http://api.fanyi.baidu.com/api/trans/product/index

````
'''这里是百度翻译秘钥，需要自己去注册获得秘钥'''

fy_APP_ID = "替换你注册获取到的秘钥"
fy_Secret_key = "替换你注册获取到的秘钥"
````

#### 程序界面

![](https://s2.ax1x.com/2019/06/21/Vx0SSJ.png)

![](https://s2.ax1x.com/2019/06/21/VxwMIU.png)
