import requests
import re,os
import random
import hashlib
import sys
# import keyboard 监听全局快捷键
from aip import AipOcr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PIL import ImageGrab
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui_windowgui import Ui_Form  #导入创建的GUI类
from Secretkey import * #导入秘钥配置文件


#自己建一个mywindows类，mywindow是自己的类名。QtWidgets.QMainWindow：继承该类方法
class mywindow(QtWidgets.QMainWindow, Ui_Form):
    #__init__:析构函数，也就是类被创建后就会预先加载的项目。
    # 马上运行，这个方法可以用来对你的对象做一些你希望的初始化。
    
    def __init__(self):
        #这里需要重载一下mywindow，同时也包含了QtWidgets.QMainWindow的预加载项。
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.Selection = "icon/对号.png"
        self.Unchecked = "icon/未选中.png"
        self.red_logo = 'icon/red_logo.png'
        self.tuichu = ":/newPrefix/icon/退出.png"
        self.logo = ":/newPrefix/icon/logo.png"
        self.guanyu = ":/newPrefix/icon/关于.png" 
        self.jietu = ':/newPrefix/icon/截图按钮.png'  
        self.button_thread = MyBeautifulThread()#实例化按钮多线程
        self.button_thread.trigger.connect(self.button_th)#链接多线程下载
        self.clipboard_thread = MyBeautifulThread()#实例化剪贴板多线程
        self.clipboard_thread.trigger.connect(self.clipboard_th)#链接多线程下载
        # self.Monitor_thread = MyBeautifulThread()#实例化监听多线程
        # self.Monitor_thread.trigger.connect(self.Monitor_th)#链接多线程下载
       
        self.clipboard = QtWidgets.QApplication.clipboard() #实例化监听剪切板
        self.clipboard.dataChanged.connect(self.on_change_clipboard)
        self.tuopan = QtWidgets.QSystemTrayIcon(self) #创建托盘
        self.tuopan.setIcon(QtGui.QIcon(self.logo))  #设置托盘图标        
        # 弹出的信息被点击就会调用messageClicked连接的函数
        #tuopan.messageClicked.connect(self.message)
        # self.toolButton_3.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Q)) #不是全局热键
        #托盘图标被激活
        self.tuopan.activated.connect(self.iconActivated)
        #设置提示信息
        self.tuopan.setToolTip('截图翻译小工具')

        
        #创建托盘的右键菜单
        self.tpMenu = QtWidgets.QMenu()
        self.tpMenu.addAction(QtWidgets.QAction(QtGui.QIcon(self.logo), '主程序', self,triggered=self.show_main))
        self.tpMenu.addAction(QtWidgets.QAction(QtGui.QIcon(self.jietu), '截图 shift+Q ', self,triggered=self.on_ScreenBut_pressed))
        self.tpMenu.addSeparator()
        self.tpMenu.addAction(QtWidgets.QAction(QtGui.QIcon(self.Selection), '开启监听', self,triggered=self.open_monitor))
        self.tpMenu.addAction(QtWidgets.QAction(QtGui.QIcon(self.Unchecked), '关闭监听', self,triggered=self.Close_monitor))
        self.tpMenu.addAction(QtWidgets.QAction(QtGui.QIcon(self.guanyu), '关于', self,triggered=self.about))
        self.tpMenu.addSeparator()
        self.tpMenu.addAction(QtWidgets.QAction(QtGui.QIcon(self.tuichu), '退出', self,triggered=self.quit))
        self.tuopan.setContextMenu(self.tpMenu) #把tpMenu设定为托盘的右键菜单
        # self.tuopan.qaction.setcheckable()
        self.tuopan.show()  #显示托盘   
        
        #托盘创建出来时显示的信息
        self.tuopan.showMessage("", '截图翻译小工具我在这里！', icon=1) #icon的值  0没有图标  1是提示  2是警告  3是错误 

        

        
   


    def open_monitor(self):
        self.checkBox.setChecked(True) #是否勾选
        self.tuopan.setIcon(QtGui.QIcon(self.logo)) 
        self.tuopan.showMessage("", '已开启监听，剪贴板！', icon=1)

    def Close_monitor(self):
        self.checkBox.setChecked(False) #是否勾选
        self.tuopan.setIcon(QtGui.QIcon(self.red_logo)) 
        self.tuopan.showMessage("", '已关闭监听，剪贴板！', icon=1)
        

    def keyPressEvent(self, event):

        '''pyqt非全局快捷键'''
          #QtCore.Qt.Key_+按键名（Escape=Esc）-->事件值
            
        if (event.key() == Qt.Key_Q) and QApplication.keyboardModifiers() == Qt.ShiftModifier:
            print("shift + q")
            self.on_ScreenBut_pressed()

        


    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件
        self.hide()  # 隐藏窗体
      
    def show_main(self):
        self.tabWidget.setCurrentIndex(0)
        self.show()


    def quit(self):
        
        app.exit()

    def about(self):
        self.tabWidget.setCurrentIndex(1)
        self.show()

    def iconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:  #双击 显示或隐藏窗口
            self.tuopan_double_click()
        elif reason == QtWidgets.QSystemTrayIcon.Trigger:    # 单击  #<code>MiddleClick</code>  中键双击
            pass
 
 
#响应托盘双击，最大最小化界面
    def tuopan_double_click(self):
        if self.isMinimized() or not self.isVisible():
            #若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
            self.showNormal()
            self.activateWindow()
        else:
            #若不是最小化，则最小化
            self.showMinimized()     


    def on_pushButton_pressed(self):
        '''一键识别翻译'''
    
        if self.textEdit.toPlainText():
            self.button_thread.start()  
        else:
            self.statusBar().showMessage("请输入内容！")

    def on_checkBox_pressed(self):
        if self.checkBox.isChecked()== False:
            self.tuopan.setIcon(QtGui.QIcon(self.logo))  
        else:
            self.tuopan.setIcon(QtGui.QIcon(self.red_logo))

    def on_ScreenBut_pressed(self):
        '''截屏功能'''
        print("执行截屏功能")
        
        window.hide()
       
        screenshot.run()
       
        window.show() #图片数据写入剪贴板
    
       
        print("截屏完毕")
        
    def on_textclearBut_pressed(self):
        
        self.textEdit.clear()


    def on_showclearBut_pressed(self):
        self.textBrowser.clear()

  

    def button_th(self):
        '''为翻译按钮增加多线程'''
        neirong = self.textEdit.toPlainText()
        jieguo = re.match(r'^file:///.*?[jpg|png|bmp]$',neirong)
        if jieguo:
            path = neirong[8:]
            wb_list = text_sb.Distinguish(path)
            self.show_text(wb_list)
        else:
            if 'file:///' not in neirong:
                dst = translate.trans_results(neirong)
                self.textBrowser.append("翻译结果".center(105,"*"))
                self.textBrowser.append(dst)
            else:
                self.statusBar().showMessage("你拖拽的文件格式有问题！")
    

    def show_text(self,wb_list):
        q = ' '.join(wb_list)
        self.textBrowser.append("识别内容".center(105,"*"))
        self.textBrowser.append(q)
        dst = translate.trans_results(q)
        self.textBrowser.append("翻译结果".center(105,"*"))
        self.textBrowser.append(dst)
        self.statusBar().showMessage("翻译成功！")

    def clipboard_th(self):
        '''截图翻译线程'''
        
        wb_list = text_sb.Distinguish()
        if wb_list:
            self.show_text(wb_list)
            # os.remove("ocr.png")



    def on_change_clipboard(self):
        '''监听剪切板'''
        
        if self.checkBox.isChecked()== True:
            # print('我被选中')
            im = ImageGrab.grabclipboard()
            print(im)
            if 'image' in str(im):
                im.save("ocr.png")
                self.clipboard_thread.start()
        else:
            print('关闭监听')    


class Text_Distinguish():
    '''图像识别'''
    def __init__(self):
        self.__APP_ID = img_APP_ID 
        self.__API_KEY = img_API_KEY
        self.__SECRET_KEY = img_ECRET_KEY
        self.client = AipOcr(self.__APP_ID, self.__API_KEY, self.__SECRET_KEY)
          

    def Distinguish(self,path = "ocr.png"):
        wb_list = []
        try:
            with open(path,"rb") as f:
                image = f.read()
                text = self.client.basicGeneral(image)
                words_result = text["words_result"]
                for i in words_result:
                    wb_list.append(i["words"])
            return wb_list
        except:
            print('没有找到图片')
            return None

class Translate():
    '''文本翻译'''
    def __init__(self):
        self.__APP_ID = fy_APP_ID
        self.__Secret_key = fy_Secret_key
        self.api = "https://fanyi-api.baidu.com/api/trans/vip/translate"

    


    def recognition_language(self,q):
        '''利用百度接口判断中英文'''
        q = q[:32]
        headers = {'Host': 'fanyi.baidu.com',
                    'Origin': 'https://fanyi.baidu.com',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Mobile Safari/537.36'}
        url = 'https://fanyi.baidu.com/langdetect'
        data = {'query':q}
        response = requests.post(url, headers=headers, data=data,verify = False).json()
        # print(response)
        lan = response.get('lan')
        return lan



    def trans_results(self,q):
        lan = self.recognition_language(q)
        if lan == 'en':
            # print("我是英文")
            language_from = "en"
            language_to = "zh"
        else:
            language_from = "zh"
            language_to = "en"
            # print("我是中文")
            
        salt = str(random.random())[8:]
        #拼接appid=2015063000000001+q=apple+salt=1435660288+密钥=12345678
        params = self.__APP_ID + q + salt + self.__Secret_key
        encrypt = hashlib.md5(bytes(params,encoding='utf-8')).hexdigest()
        data = {"q":q,
                "from":language_from,
                "to":language_to,
                "appid":self.__APP_ID,
                "salt":salt,
                "sign":encrypt}

        html = requests.post(self.api,data=data,verify = False).json()
        trans_result = html["trans_result"][0]
        dst = trans_result["dst"]
        return dst
    

class MyBeautifulThread(QtCore.QThread):
    '''多线程'''
    trigger = QtCore.pyqtSignal()
 
    def __init__(self):
        super(MyBeautifulThread, self).__init__()

    def run(self):
        self.trigger.emit()




def toRectF(rect):
    return QRectF(
        rect.x(),
        rect.y(),
        rect.width(),
        rect.height()
    )


def toRect(rectF):
    return QRect(
        rectF.x(),
        rectF.y(),
        rectF.width(),
        rectF.height()
    )


def normalizeRect(rect):
    x = rect.x()
    y = rect.y()
    w = rect.width()
    h = rect.height()
    if w < 0:
        x = x + w
        w = -w
    if h < 0:
        y = y + h
        h = -h
    return QRectF(x, y, w, h)

# def screenShot():

#    '''监听全局快捷键'''
#    if keyboard.wait(hotkey='shift+q') == None:
#        print('快捷键被按下')



class WScreenshot(QWidget):
    @classmethod
    def run(cls):
        cls.win = cls()
        cls.win.getScreen()
        cls.win.show()
      
       
    def __init__(self,):
        super(WScreenshot, self).__init__()

        # self.saveDir = u'D:/'
        # self.saveName = u'W截图-{}'.format(QDateTime().currentDateTime().toString("yyyyMMdd-hh-mm-ss"))
        self.saveFormat = 'png'
        self.picQuality = 100
        self.clipboard = QApplication.clipboard() #实例化剪贴板
        self.setWindowTitle(u'截图窗体')
        self.showFullScreen()  # 全屏显示
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # self.screenShot_thread = MyBeautifulThread()#实例化热键多线程
        # self.screenShot_thread.trigger.connect(self.screenShot)#链接热键多线程下载
       


    def getScreen(self):
         # 屏幕 和 屏幕信息
        
        self.screen = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

        self.screenSize = self.screen.rect().size()
        self.screenRect = toRectF(self.screen.rect())
        # -点
        self.screenTopLeft = self.screenRect.topLeft()
        self.screenBottomLeft = self.screenRect.bottomLeft()
        self.screenTopRight = self.screenRect.topRight()
        self.screenBottomRight = self.screenRect.bottomRight()
        # -上下左右限
        self.screenLeft = self.screenRect.left()
        self.screenRight = self.screenRect.right()
        self.screenTop = self.screenRect.top()
        self.screenBottom = self.screenRect.bottom()

        # A:start(x,y)        D:(x+w,y)
        #     -----------------
        #     |               |
        #     |               |
        #     -----------------
        # B:(x,y+h)           C:end(x+w,y+h)

        # 设置 self.screen 为窗口背景
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(self.screen))
        self.setPalette(palette)

        # 调节器层
        self.adjustment_original = QPixmap(self.screenSize)  # 初始调节器
        self.adjustment_original.fill(QColor(0, 0, 0, 64))
        self.adjustment = QPixmap()  # 调节器
        # self.adjustment = self.adjustment_original.copy()  # 调节器

        # 画布层
        self.canvas_original = QPixmap(self.screenSize)  # 初始画布
        self.canvas_original.fill(Qt.transparent)
        self.canvas_saved = self.canvas_original.copy()  # 保存已经画好的图案
        self.canvas = QPixmap()  # 画布

        # self.canvas = self.canvas_original.copy()  # 画布
        # self.canvas_saved = self.canvas.copy()
        # 输出
        self.output = QPixmap()

        # 当前功能状态
        self.isMasking = False
        self.hasMask = False
        self.isMoving = False
        self.isAdjusting = False
        self.isDrawing = False
        self.hasPattern = False
        self.mousePos = ''
        self.isShifting = False

        # 蒙版 和 蒙版信息
        self.maskRect = QRectF()
        self.maskRect_backup = QRectF()

        # 以下 16 个变量随self.maskRect变化而变化
        self.maskTopLeft = QPoint()
        self.maskBottomLeft = QPoint()
        self.maskTopRight = QPoint()
        self.maskBottomRight = QPoint()
        self.maskTopMid = QPoint()
        self.maskBottomMid = QPoint()
        self.maskLeftMid = QPoint()
        self.maskRightMid = QPoint()

        self.rectTopLeft = QRectF()
        self.rectBottomLeft = QRectF()
        self.rectTopRight = QRectF()
        self.rectBottomRight = QRectF()
        self.rectTop = QRectF()
        self.rectBottom = QRectF()
        self.rectLeft = QRectF()
        self.rectRight = QRectF()

        self.adjustmentLineWidth = 2
        self.adjustmentWhiteDotRadius = 6
        self.adjustmentBlueDotRadius = 4
        self.blue = QColor(30, 120, 255)
        self.setCursor(Qt.CrossCursor)  # 设置鼠标样式 十字

        self.setMouseTracking(True)

        # 鼠标事件点
        self.start = QPoint()
        self.end = QPoint()

        # self.test()

    def test(self):
        self.hasMask = True
        self.isMasking = True
        self.maskRect = QRectF(100, 100, 600, 800)
        self.updateMaskInfo()
        self.update()

    def toMask(self):
        rect = QRectF(self.start, self.end)

        if self.isShifting:
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            absW = abs(w)
            absH = abs(h)
            wIsLonger = True if absW > absH else False
            if w > 0:
                if h > 0:
                    end = QPoint(x + absW, y + absW) if wIsLonger else QPoint(x + absH, y + absH)
                else:
                    end = QPoint(x + absW, y - absW) if wIsLonger else QPoint(x + absH, y - absH)
            else:
                if h > 0:
                    end = QPoint(x - absW, y + absW) if wIsLonger else QPoint(x - absH, y + absH)
                else:
                    end = QPoint(x - absW, y - absW) if wIsLonger else QPoint(x - absH, y - absH)

            rect = QRectF(self.start, end)

        self.maskRect = QRectF(
            rect.x() + min(rect.width(), 0),
            rect.y() + min(rect.height(), 0),
            abs(rect.width()),
            abs(rect.height())
        )

        # 修正超出屏幕、碰撞
        if self.isShifting:
            self.fixCollision()

        self.updateMaskInfo()
        self.update()

    # 修复碰撞。针对 isShifting 的情况
    def fixCollision(self):
        vector = self.end - self.start
        vX = vector.x()
        vY = vector.y()
        resStart = self.maskRect.topLeft()
        resEnd = self.maskRect.bottomRight()
        mLeft = self.maskRect.left()
        mRight = self.maskRect.right()
        mTop = self.maskRect.top()
        mBottom = self.maskRect.bottom()
        # w < h
        if self.maskRect.left() <= self.screenLeft:
            newW = mRight - self.screenLeft
            if vY > 0:
                resStart = QPoint(self.screenLeft, mTop)
                resEnd = resStart + QPoint(newW, newW)
            else:
                resStart = resEnd + QPoint(-newW, -newW)
        elif self.maskRect.right() >= self.screenRight:
            newW = self.screenRight - mLeft
            if vY > 0:
                resEnd = resStart + QPoint(newW, newW)
            else:
                resEnd = QPoint(self.screenRight, mBottom)
                resStart = resEnd + QPoint(-newW, -newW)
        # w > h
        elif self.maskRect.top() <= self.screenTop:
            newW = mBottom - self.screenTop
            if vX > 0:
                resStart = QPoint(mLeft, self.screenTop)
                resEnd = resStart + QPoint(newW, newW)
            else:
                resStart = resEnd + QPoint(-newW, -newW)
        elif self.maskRect.bottom() >= self.screenBottom:
            newW = self.screenBottom - mTop
            if vX > 0:
                resEnd = resStart + QPoint(newW, newW)
            else:
                resEnd = QPoint(mRight, self.screenBottom)
                resStart = resEnd + QPoint(-newW, -newW)
        self.maskRect = QRectF(resStart, resEnd)

    def toAdjust(self):

        mRect = self.maskRect_backup
        mStart = mRect.topLeft()
        mStartX = mStart.x()
        mStartY = mStart.y()
        mEnd = mRect.bottomRight()
        mEndX = mEnd.x()
        mEndY = mEnd.y()
        resStart = mStart
        resEnd = mEnd
        if not self.isShifting:

            if self.mousePos == 'TL':
                resStart = self.end
            elif self.mousePos == 'BL':
                resStart = QPoint(self.end.x(), mStartY)
                resEnd = QPoint(mEndX, self.end.y())
            elif self.mousePos == 'TR':
                resStart = QPoint(mStartX, self.end.y())
                resEnd = QPoint(self.end.x(), mEndY)
            elif self.mousePos == 'BR':
                resEnd = self.end
            elif self.mousePos == 'T':
                resStart = QPoint(mStartX, self.end.y())
            elif self.mousePos == 'B':
                resEnd = QPoint(mEndX, self.end.y())
            elif self.mousePos == 'L':
                resStart = QPoint(self.end.x(), mStartY)
            elif self.mousePos == 'R':
                resEnd = QPoint(self.end.x(), mEndY)
        else:
            print(self.mousePos)
            if self.mousePos == 'T':
                resStart = QPoint(mStartX, self.end.y())
                newW = mEndY - self.end.y()
                resEnd = resStart + QPoint(newW, newW)
            elif self.mousePos == 'B':
                newW = self.end.y() - mStartY
                resEnd = resStart + QPoint(newW, newW)
            elif self.mousePos == 'L':
                resStart = QPoint(self.end.x(), mStartY)
                newW = mEndX - self.end.x()
                resEnd = resStart + QPoint(newW, newW)
            elif self.mousePos == 'R':
                newW = self.end.x() - mStartX
                resEnd = resStart + QPoint(newW, newW)
            elif self.mousePos == 'TL':
                newW = mEndX - self.end.x()
                newH = mEndY - self.end.y()
                newW = newW if newW > newH else newH
                resStart = resEnd + QPoint(-newW, -newW)
            elif self.mousePos == 'BR':
                newW = self.end.x() - mStartX
                newH = self.end.y() - mStartY
                newW = newW if newW > newH else newH
                resEnd = resStart + QPoint(newW, newW)
            elif self.mousePos == 'TR':
                newW = self.end.x() - mStartX
                newH = mEndY - self.end.y()
                newW = newW if newW > newH else newH
                resStart = mRect.bottomLeft()
                resEnd = resStart + QPoint(newW, -newW)
            elif self.mousePos == 'BL':
                newW = mEndX - self.end.x()
                newH = self.end.y() - mStartY
                newW = newW if newW > newH else newH
                resStart = mRect.topRight()
                resEnd = resStart + QPoint(-newW, newW)

        self.maskRect = normalizeRect(QRectF(resStart, resEnd))

        self.fixCollision()

        self.updateMaskInfo()
        self.update()

    def toMove(self):
        mStart = self.maskRect_backup.topLeft()
        mStartX = mStart.x()
        mStartY = mStart.y()
        mEnd = self.maskRect_backup.bottomRight()
        mEndX = mEnd.x()
        mEndY = mEnd.y()
        mWidth = self.maskRect_backup.width()
        mHeight = self.maskRect_backup.height()
        mWHPoint = QPoint(mWidth, mHeight)
        vector = self.end - self.start
        vX = vector.x()
        vY = vector.y()

        resStart = mStart + vector
        resStartX = resStart.x()
        resStartY = resStart.y()
        resEnd = mEnd + vector
        resEndX = resEnd.x()
        resEndY = resEnd.y()

        if resStartX <= self.screenLeft and resStartY <= self.screenTop:
            resStart = self.screenTopLeft
            resEnd = resStart + mWHPoint
        elif resEndX >= self.screenRight and resEndY >= self.screenBottom:
            resEnd = self.screenBottomRight
            resStart = resEnd - mWHPoint
        elif resStartX <= self.screenLeft and resEndY >= self.screenBottom:
            resStart = QPoint(self.screenLeft, self.screenBottom - mHeight)
            resEnd = resStart + mWHPoint
        elif resEndX >= self.screenRight and resStartY <= self.screenTop:
            resStart = QPoint(self.screenRight - mWidth, self.screenTop)
            resEnd = resStart + mWHPoint
        elif resStartX <= self.screenLeft:
            resStart = QPoint(self.screenLeft, mStartY + vY)
            resEnd = resStart + mWHPoint
        elif resStartY <= self.screenTop:
            resStart = QPoint(mStartX + vX, self.screenTop)
            resEnd = resStart + mWHPoint
        elif resEndX >= self.screenRight:
            resEnd = QPoint(self.screenRight, mEndY + vY)
            resStart = resEnd - mWHPoint
        elif resEndY >= self.screenBottom:
            resEnd = QPoint(mEndX + vX, self.screenBottom)
            resStart = resEnd - mWHPoint
        self.maskRect = normalizeRect(QRectF(resStart, resEnd))
        self.updateMaskInfo()
        self.update()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.start = QMouseEvent.pos()
            self.end = self.start
            if self.hasMask:
                self.maskRect_backup = self.maskRect
                if self.mousePos == 'mask':
                    self.isMoving = True
                else:
                    self.isAdjusting = True
            else:
                self.isMasking = True

        if QMouseEvent.button() == Qt.RightButton:
            if self.isMasking or self.hasMask:
                self.isMasking = False
                self.hasMask = False
                self.maskRect = QRectF(0, 0, 0, 0)
                self.updateMaskInfo()
                self.update()
            else:
                self.close()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.isMasking = False
            self.isMoving = False
            self.isAdjusting = False
            self.isDrawing = False

    def mouseDoubleClickEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            if self.mousePos == 'mask':
                self.save()
                self.close()

    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        self.end = pos

        if self.isMasking:
            self.hasMask = True
            self.toMask()
        elif self.isMoving:
            self.toMove()
        elif self.isAdjusting:
            self.toAdjust()

        # 设置鼠标样式
        if self.isDrawing:
            pass
        else:
            if self.hasMask:
                if self.isMoving:
                    self.setCursor(Qt.SizeAllCursor)
                if self.isAdjusting:
                    pass
                else:
                    self.setMouseShape(pos)
            else:
                self.mousePos = ''
                self.setCursor(Qt.CrossCursor)  # 设置鼠标样式 十字

    def setMouseShape(self, pos):
        # 设置鼠标样式
        if self.rectTopLeft.contains(pos):
            self.setCursor(Qt.SizeFDiagCursor)
            self.mousePos = 'TL'
        elif self.rectBottomLeft.contains(pos):
            self.setCursor(Qt.SizeBDiagCursor)
            self.mousePos = 'BL'
        elif self.rectBottomRight.contains(pos):
            self.setCursor(Qt.SizeFDiagCursor)
            self.mousePos = 'BR'
        elif self.rectTopRight.contains(pos):
            self.setCursor(Qt.SizeBDiagCursor)
            self.mousePos = 'TR'
        elif self.rectLeft.contains(pos):
            self.setCursor(Qt.SizeHorCursor)
            self.mousePos = 'L'
        elif self.rectTop.contains(pos):
            self.setCursor(Qt.SizeVerCursor)
            self.mousePos = 'T'
        elif self.rectBottom.contains(pos):
            self.setCursor(Qt.SizeVerCursor)
            self.mousePos = 'B'
        elif self.rectRight.contains(pos):
            self.setCursor(Qt.SizeHorCursor)
            self.mousePos = 'R'
        elif self.maskRect.contains(pos):
            self.setCursor(Qt.SizeAllCursor)
            self.mousePos = 'mask'

    def updateMaskInfo(self):
        # 蒙版点
        self.maskTopLeft = self.maskRect.topLeft()
        self.maskBottomLeft = self.maskRect.bottomLeft()
        self.maskTopRight = self.maskRect.topRight()
        self.maskBottomRight = self.maskRect.bottomRight()
        self.maskTopMid = (self.maskTopLeft + self.maskTopRight) / 2
        self.maskBottomMid = (self.maskBottomLeft + self.maskBottomRight) / 2
        self.maskLeftMid = (self.maskTopLeft + self.maskBottomLeft) / 2
        self.maskRightMid = (self.maskTopRight + self.maskBottomRight) / 2
        # 除蒙版区外的 8 个区域
        self.rectTopLeft = QRectF(self.screenTopLeft, self.maskTopLeft)
        self.rectBottomLeft = QRectF(self.screenBottomLeft, self.maskBottomLeft)
        self.rectTopRight = QRectF(self.screenTopRight, self.maskTopRight)
        self.rectBottomRight = QRectF(self.screenBottomRight, self.maskBottomRight)
        self.rectTop = QRectF(QPoint(self.maskRect.left(), self.screenTop), self.maskTopRight)
        self.rectBottom = QRectF(self.maskBottomLeft, QPoint(self.maskRect.right(), self.screenBottom))
        self.rectLeft = QRectF(QPoint(self.screenLeft, self.maskRect.top()), self.maskBottomLeft)
        self.rectRight = QRectF(self.maskTopRight, QPoint(self.screenRight, self.maskRect.bottom()))

    def paintEvent(self, QPaintEvent):

        painter = QPainter()

        # 开始在 画布层 上绘画。如果正在绘画，绘制图案, 否则不绘制
        if self.isDrawing:
            if self.hasPattern:
                self.canvas = self.canvas_saved.copy()
            else:
                self.canvas = self.canvas_original.copy()
            painter.begin(self.canvas)
            self.paintCanvas(painter)
            painter.end()
            # 把 画布层 绘画到窗口上
            painter.begin(self)
            painter.drawPixmap(self.screenRect, self.canvas)
            painter.end()

        # 开始在 空白调节器层 上绘画。如果有蒙版，绘制调节器形状, 否则不绘制
        else:
            self.adjustment = self.adjustment_original.copy()
            painter.begin(self.adjustment)
            self.paintAdjustment(painter)
            painter.end()
            # 把 调节器层 绘画到窗口上
            painter.begin(self)
            painter.drawPixmap(toRect(self.screenRect), self.adjustment)
            painter.end()

    def paintAdjustment(self, painter):
        if self.hasMask:
            painter.setRenderHint(QPainter.Antialiasing, True)  # 反走样
            painter.setPen(Qt.NoPen)
            # 在蒙版区绘制屏幕背景
            painter.setBrush(QBrush(self.screen))
            painter.drawRect(self.maskRect)
            # 绘制线框
            lineWidth = self.adjustmentLineWidth
            painter.setBrush(self.blue)
            painter.drawRect(
                QRectF(
                    self.maskTopLeft + QPoint(-lineWidth, -lineWidth),
                    self.maskTopRight + QPoint(lineWidth, 0))
            )
            painter.drawRect(
                QRectF(
                    self.maskBottomLeft + QPoint(-lineWidth, 0),
                    self.maskBottomRight + QPoint(lineWidth, lineWidth)
                )
            )
            painter.drawRect(
                QRectF(
                    self.maskTopLeft + QPoint(-lineWidth, -lineWidth),
                    self.maskBottomLeft + QPoint(0, lineWidth)
                )
            )
            painter.drawRect(
                QRectF(
                    self.maskTopRight + QPoint(0, -lineWidth),
                    self.maskBottomRight + QPoint(lineWidth, lineWidth)
                )
            )
            if self.maskRect.width() > 150 and self.maskRect.height() > 150:
                # 绘制点
                points = [
                    self.maskTopLeft, self.maskTopRight, self.maskBottomLeft, self.maskBottomRight,
                    self.maskLeftMid, self.maskRightMid, self.maskTopMid, self.maskBottomMid
                ]
                # -白点
                whiteDotRadiusPoint = QPoint(self.adjustmentWhiteDotRadius, self.adjustmentWhiteDotRadius)
                painter.setBrush(Qt.white)
                for point in points:
                    painter.drawEllipse(QRectF(point - whiteDotRadiusPoint, point + whiteDotRadiusPoint))
                # -蓝点
                blueDotRadius = QPoint(self.adjustmentBlueDotRadius, self.adjustmentBlueDotRadius)
                painter.setBrush(self.blue)
                for point in points:
                    painter.drawEllipse(QRectF(point - blueDotRadius, point + blueDotRadius))

            # 绘制尺寸
            maskSize = (abs(int(self.maskRect.width())), abs(int(self.maskRect.height())))
            painter.setFont(QFont('Monaco', 7, QFont.Bold))
            painter.setPen(Qt.transparent)  # 透明获得字体Rect
            textRect = painter.drawText(
                QRectF(self.maskTopLeft.x() + 10, self.maskTopLeft.y() - 25, 100, 20),
                Qt.AlignLeft | Qt.AlignVCenter,
                '{} x {}'.format(*maskSize)
            )
            painter.setBrush(QColor(0, 0, 0, 128))  # 黑底
            padding = 5
            painter.drawRect(
                QRectF(
                    textRect.x() - padding,
                    textRect.y() - padding * 0.4,
                    textRect.width() + padding * 2,
                    textRect.height() + padding * 0.4
                )
            )
            painter.setPen(Qt.white)
            painter.drawText(
                textRect,
                Qt.AlignLeft | Qt.AlignVCenter,
                '{} x {}'.format(*maskSize)
            )
            painter.setPen(Qt.NoPen)

    def paintCanvas(self, painter):
        pass

    def keyPressEvent(self, event):
        '''全局快捷键'''
          #QtCore.Qt.Key_+按键名（Escape=Esc）-->事件值
        if event.key() == Qt.Key_Escape:
            cls.win.close()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()
        if QKeyEvent.key() == Qt.Key_Return or QKeyEvent.key() == Qt.Key_Enter:  # 大键盘、小键盘回车
            if self.hasMask:
                self.save()
            self.close()
        if QKeyEvent.modifiers() & Qt.ShiftModifier:
            self.isShifting = True

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Shift:
            self.isShifting = False

    def save(self):
        self.output = self.screen.copy()
        
        if self.hasPattern:
            painter = QPainter(self.output)
            painter.drawPixmap(self.canvas)
        self.output = self.output.copy(toRect(self.maskRect))
        self.clipboard.setPixmap(self.output) #写入剪贴板
        # self.output.save(
        #     u'{saveName}'.format(
        #         saveName = 'ocr.png'
        #         # format = self.saveFormat.lower()
        #     ),
        #     self.saveFormat,
        #     self.picQuality
        # )


if __name__ == '__main__': #如果整个程序是主程序
     # QApplication相当于main函数，也就是整个程序（很多文件）的主入口函数。
     # 对于GUI程序必须至少有一个这样的实例来让程序运行。
    
    app = QtWidgets.QApplication(sys.argv)
    #生成 mywindow 类的实例。
    window = mywindow()
    #有了实例，就得让它显示，show()是QWidget的方法，用于显示窗口。
    
    screenshot = WScreenshot()
    window.setFixedSize(window.width(), window.height()) #禁止窗口大小化
  
   
    window.show()
    text_sb = Text_Distinguish()
    translate = Translate()
    
    
    # 调用sys库的exit退出方法，条件是app.exec_()，也就是整个窗口关闭。
    # 有时候退出程序后，sys.exit(app.exec_())会报错，改用app.exec_()就没事
    # https://stackoverflow.com/questions/25719524/difference-between-sys-exitapp-exec-and-app-exec
    sys.exit(app.exec_())
    