import os, inspect, sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(current_dir)
sys.path.append("../")
# See https://blog.csdn.net/bornfree5511/article/details/115197553

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Uis.uSyncMainUI18 import Ui_MainWindow
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np

# import helloworld
from PyQt5 import QtCore, QtGui, QtWidgets

# --Content 01 added for tab 3 start here (by cmj on 20210928)--
from PyQt5.QtGui import *

# --Contents 01 added for tab 3 end here (by cmj on 20210928)--
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from lib.share import SI
import UserManage

from UserMainWindow import UserMainWindowClass

from FieldValue import FieldValueClass
from ShortcutsManager import ShortcutsManagerClass


# needs socket and struct library
from socket import *
from struct import *


#Any errors and hangs (or an infinite loop) in a daemon process will not affect the main process, 
#and it will only be terminated once the main process exits. (i.e. will only be terminating with the main process.)
#Best way is to set up a Queue to have all the child processes communicate to the parent process so that we can join them and clean up nicely.


import multiprocessing as mp
import time
import queue
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
import functools
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView



class GlobalShortcuts(QObject):
    def __init__(self):
        super(GlobalShortcuts, self).__init__()

    def globalShortcutsSlot(self, keys: str):
        print(keys)


class Communicate(QObject):
    closeApp = pyqtSignal()


# --Contents 02 added for tab 3 start here (by cmj on 20210928)--
def hhmmss(ms):
    h, r = divmod(ms, 360000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))


class ShortcutsWindow(ShortcutsManagerClass):
    def __init__(self):
        super(ShortcutsWindow, self).__init__()

        self.setWindowTitle("Shortcuts Configuration Window")

        # self.widget = QWidget()

        ##https://pythonpyqt.com/pyqt-events/

        self.c = Communicate()
        # widget.currentItemChanged.connect(self.index_changed)
        # widget.currentTextChanged.connect(self.text_changed)

        # self.setCentralWidget(widget)

    def closeEvent(self, event):
        """
        Override the closeEvent method of QWidget in your main window.
        https://stackoverflow.com/questions/9249500/pyside-pyqt-detect-if-user-trying-to-close-window
        """
        # do stuff
        if True:
            print("shortcut configuration window closed")
            self.c.closeApp.emit()
            event.accept()  # let the window close
        else:
            event.ignore()


class ViewerWindow(QMainWindow):
    state = pyqtSignal(bool)

    def closeEvent(self, e):
        # Emit the window state, to update the viewer toggle button.
        self.state.emit(False)


class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()


# --Contents 02 added for tab 3 end here (by cmj on 20210928)--


class my_ComboBox(QMainWindow, Ui_MainWindow):
    def __init__(self, mainWindow):
        print("__init__ is called")
        super().__init__()
        self.setupUi(mainWindow)
        self.initUI()
        # --Contents 03 added for tab 3 start here (by cmj on 20210929)--
        self.turnonButton.clicked.connect(self.setup_camera)
        #self.recordButton.clicked.connect(self.recording)
        # Setup the playlist.
        self.playlist = QMediaPlaylist()
        self.playbackPlayer.setPlaylist(self.playlist)
        # Connect control buttons/slides for media player.
        self.videoPlay.pressed.connect(self.playbackPlayer.play)
        self.videoPause.pressed.connect(self.playbackPlayer.pause)
        self.videoStop.pressed.connect(self.playbackPlayer.stop)
        self.VideoVA.valueChanged.connect(self.playbackPlayer.setVolume)
        #self.previousButton.pressed.connect(self.playlist.previous)
        #self.nextButton.pressed.connect(self.playlist.next)
        self.model = PlaylistModel(self.playlist)
        self.PlaybackList.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.PlaybackList.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)
        self.playbackPlayer.durationChanged.connect(self.update_duration)
        self.playbackPlayer.positionChanged.connect(self.update_position)
        self.VideoProgress.valueChanged.connect(self.playbackPlayer.setPosition)
        self.action_Open_media.triggered.connect(self.open_media)
        # --Contents 03 added for tab 3 end here (by cmj on 20210929)--
        # most important code for integration
        self.EventRedefinition.clicked.connect(self.callShortCutsConfiguration)
        self.VEventRedefinitio.clicked.connect(self.callShortCutsConfiguration)
        self.actionNew_Participant_Info.triggered.connect(
            self.actionNew_Participant_InfoExcute
        )
        self.setAcceptDrops(True)
        
        ## update the shortcut definition.
        # self.ShortcutConfigureWidget=ShortcutsWindow()
        self.shortcutsManager = ShortcutsWindow()
        self.shortcutsManager.c.closeApp.connect(self.updateShortConfigureInfo)

        self.fieldValueList = self.shortcutsManager.getAllInfo()
        self.initiateShortConfigureInfo()


        # https://stackoverflow.com/questions/9249500/pyside-pyqt-detect-if-user-trying-to-close-window
        # capture the ShortConfigureWindow close event.
        # self.ShortcutConfigureWidget.aboutToQuit.connect(self.updateShortConfigureInfo)
        # self.ShortcutConfigureWidget.lastWindowClosed.connect(self.updateShortConfigureInfo)

        ## put menu actions here.
        self.action_Quit.triggered.connect(mainWindow.close)
        self.action4_Camera_Annotation.triggered.connect(self.callShortCutsConfiguration)
        self.action_Help.triggered.connect(self.HelpDialog)
        # self.show() # comment out this line will remove the unncessary new window titled 'python'
        self.BP_Collection.stateChanged.connect(self.main)




    def Plot_BP(self, q):
        self.plot = pg.PlotWidget()
        vbox = QVBoxLayout()
        self.BP_Preview_2.setLayout(vbox)
        vbox.addWidget(self.plot)
        self.plotter()
        q = mp.Queue()  # 主进程实例化一个进程queue
        self.prcss_chld_gt_BP.start()
    def plotter(self):
        self.data = np.full([3000,],0)  #change to how many starter points in graph (how many points for 30s)。 0.01s讀取一次數據，那麽30s可以讀取30/0.01=3000個點
        self.ptr = 0
        self.curve = self.plot.getPlotItem().plot()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(10)  #（單位：ms）change to how many ms to be waited before plotting a point。每0.01s讀取一次數據，就是每10ms讀取一次數據。
    def updater(self):
        self.data[:-1] = self.data[1:]  # shift data in the array one sample left
        self.data[-1] = self.q.get()[-1]
        self.curve.setData(self.data)
        self.ptr += 1
        self.curve.setPos(self.ptr, 0)



    def main(self, checked):
        """The main process"""
        q = mp.Queue()  #q在main process里定义为Queue就ok了。

        #主程序 - 画图
        workr = mp.Process(target=self.Plot_BP, args=(self, q)) 

        #子程序1 - 检查读取Brain Products的数据是否正常，如果q里面为空的话立马在q里面put终止程序。  （在背景运行）
        wdog = mp.Process(target=self.watchdog, args=(q,))
        # run the watchdog as daemon so it terminates with the main process
        wdog.daemon = True

        #子程序2 - 读取Brain Products的数据 （在背景运行）
        prcss_chld_gt_BP = mp.Process(target=self.dataGeneratorBrainProducts, args=(q, "zsq"))  # 将q传递给子进程,由子进程往主进程传递数据 
        # run the data generator as daemon so it terminates with the main process
        prcss_chld_gt_BP.daemon = True


        if checked:
            workr.start()
            print ("[MAIN]: starting process P1")
            wdog.start()
            print ("[MAIN]: starting process P2")

            # Poll the queue
            while True:
                msg = q.get()   #start to feed q into process arguments.
                if msg == "KILL data generator": 
                    print ("[MAIN]: Terminating data generator.")
                    workr.terminate()
                    time.sleep(0.1)
                    if not workr.is_alive():
                        print ("[MAIN]: data generator is a goner.")
                        workr.join(timeout=1.0)
                        print ("[MAIN]: Joined data generator successfully!")
                        q.close()
                    else:
                        prcss_chld_gt_BP.start()
                        print ("[CHILD1]: starting process P3")
                        break # prcss_chld_gt_BP process daemon gets terminated；   # watchdog process daemon gets terminated


        else:  #这里else的话直接关闭所有process，用不到watchdog，也用不着识别是否有BP的信号。
            print ("[MAIN]: Terminating data generator.")
            workr.terminate()
            time.sleep(0.1)
            if not workr.is_alive():
                print ("[MAIN]: data generator is a goner.")
                workr.join(timeout=1.0)
                print ("[MAIN]: Joined data generator successfully!")
                q.close()

    
    

    def watchdog(q):  #This check the queue for updates and send a signal to it when the child process isn't sending anything for too long
        while True:
            try:
                msg = q.get(timeout=100.0)  #set a waiting time..
            except queue.Empty as e:
                print ("[WATCHDOG]: Looks like BP is not connected...")
                q.put("KILL data generator")

                

    

    #define the target function of child process 1:
    def dataGeneratorBrainProducts(q, data):
        # Main RDA routine
        # Create a tcpip socket
        con = socket(AF_INET, SOCK_STREAM)
        # Connect to recorder host via 32Bit RDA-port
        # adapt to your host, if recorder is not running on local machine
        # change port to 51234 to connect to 16Bit RDA-port
        con.connect(("localhost", 51244))
        # Flag for main loop
        finish = False
        # data buffer for calculation, empty in beginning, 0.1s
        data1s = []
        # block counter to check overflows of tcpip buffer
        lastBlock = -1

        while not finish:
            # Get message header as raw array of chars
            rawhdr = RecvData(con, 24)   #(一打开Recorder，最先接收到的数据都是header. 每次接收到的数据一开始都是headers.)（header就包括下面的message size, message type等等一些基本信息。）
            # Split array into usefull information id1 to id4 are constants
            (id1, id2, id3, id4, msgsize, msgtype) = unpack('<llllLL', rawhdr)
            # Get data part of message, which is of variable size
            rawdata = RecvData(con, msgsize - 24)     #（raw data其实就是接收到的信息减去前面24bytes的headers）

            # Perform action dependend on the message type
            if msgtype == 1:
                # Start message, extract eeg properties and display them
                (channelCount, samplingInterval, resolutions, channelNames) = GetProperties(rawdata)
                # reset block counter
                lastBlock = -1
                print ("Start")
                print ("Number of channels: " + str(channelCount))
                print ("Sampling interval: " + str(samplingInterval))
                print ("Resolutions: " + str(resolutions))
                print ("Channel Names: " + str(channelNames))

            elif msgtype == 4:
                # Data message, extract data and markers
                (block, points, markerCount, data, markers) = GetData(rawdata, channelCount)   #rawdata里面有data，rawdata包含了data，markers，markercount，pointcount等等信息。
                # Check for overflow
                if lastBlock != -1 and block > lastBlock + 1:
                    print ("*** Overflow with " + str(block - lastBlock) + " datablocks ***" )
                lastBlock = block
                # Print markers, if there are some in actual block
                if markerCount > 0:
                    for m in range(markerCount):
                        print ("Marker " + markers[m].description + " of type " + markers[m].type)
                # Put data at the end of actual buffer
                data1s.extend(data)
                # If more than 0.01s of data is collected, calculate average power, print it and reset data buffer
                if len(data1s) > channelCount * 10000 / samplingInterval:   #100000/4000=2.5. --> 0.01s里有2.5次数据记录。
                    index = int(len(data1s) - channelCount * 100000 / samplingInterval)
                    data1s = data1s[index:]
                    avg = 0
                    # Do not forget to respect the resolution !!!
                    for i in range(len(data1s)):
                        avg = avg + data1s[i]*data1s[i]*resolutions[i % channelCount]*resolutions[i % channelCount]
                    avg = avg / len(data1s)
                    print ("Average power: " + str(avg))
                    #data = time.time() * np.random.normal()
                    # time.sleep(3)
                    q.put(
                        ("multiprocess queue test", avg)
                    )  # put一次只能传递一个数据对象，多个对象必须使用列表 元组 字典等传递
                    data1s = []
            
            elif msgtype == 3:
                # Stop message, terminate program
                print ("Stop")
                finish = True
        # Close tcpip connection
        con.close()
    #---------------------BP data--------------------
    """
    Simple Python RDA client for the RDA tcpip interface of the BrainVision Recorder
    It reads all the information from the recorded EEG,
    prints EEG and marker information to the console and calculates and
    prints the average power every second

    Brain Products GmbH
    Gilching/Freiburg, Germany
    www.brainproducts.com
    """
    # Marker class for storing marker information
    class Marker:
        def __init__(self):
            self.position = 0
            self.points = 0
            self.channel = -1
            self.type = ""
            self.description = ""

    # 其实这个就是接收规定大小的所有的值，是个loop，接收到达到规定的size为止
    def RecvData(socket, requestedSize):
        returnStream = bytes(0)
        while len(returnStream) < requestedSize:
            databytes = socket.recv(requestedSize - len(returnStream))
            if databytes == []:
                raise RuntimeError #, "connection broken"
            returnStream += databytes
        return returnStream

    # Helper function for splitting a raw array of
    # zero terminated strings (C) into an array of python strings嗯嗯
    #很有意思的，怎么split String
    def SplitString(raw):
        stringlist = []
        s = ""
        for i in range(len(raw)):
            if raw[i:i+1] != bytes('\x00','utf-8'):   #如果有连续的不等于\x00的东东，就把它们连在一起
                s = s + raw[i:i+1].decode('utf-8', 'ignore')
            else:     #一直到碰到\x00了，就把之前的都作为一个项放到list里面去。逻辑上没错。
                stringlist.append(s)
                s = ""  #然后把s重置
        return stringlist

    # Helper function for extracting eeg properties from a raw data array
    # read from tcpip socket
    def GetProperties(rawdata):
        # Extract channel count and sampling interval.
        (channelCount, samplingInterval) = unpack('<Ld', rawdata[:12])   #channel count 和 samplign interval在rawdata的前12位中([0,11))。
        # Extract resolutions
        resolutions = []
        for c in range(channelCount):  #0-31
            index = 12 + c * 8         #12, 20, 28, 36,....., 360
            restuple = unpack('<d', rawdata[index:index+8])     #[12:20), [20:28),.........
            resolutions.append(restuple[0])  
        
        # Extract channel names
        channelNames = SplitString(rawdata[12 + 8 * channelCount:])    #channel names在最后。就是rawdata[360:]
        return (channelCount, samplingInterval, resolutions, channelNames)

    # Helper function for extracting eeg and marker data from a raw data array
    # read from tcpip socket       
    def GetData(rawdata, channelCount):
        # Extract blockcount, pointscount and markercount
        (block, points, markerCount) = unpack('<LLL', rawdata[:12])      #这些信息都是在rawdata开头的地方[0:12)
        #point是得到data的一个点，就是一个横截面儿。例如sampling rate是250就是1s接收250次信号数据就是1s接收250个点。每一次是一共接收channel count*points个数据。
        # Extract eeg data as array of floats
        data = []
        for i in range(points * channelCount):  #对于1s内得到的rawdata就是[0,8000)，对于2s内得到的rawdata就是[0,16000)。
            index = 12 + 4 * i  #(12,16,20,24,.....32012)
            value = unpack('<f', rawdata[index:index+4])  #[12:16), [16,20).....
            data.append(value[0])

        # Extract markers
        markers = []
        index = 12 + 4 * points * channelCount
        for m in range(markerCount):
            markersize = unpack('<L', rawdata[index:index+4])

            ma = Marker()
            (ma.position, ma.points, ma.channel) = unpack('<LLl', rawdata[index+4:index+16])
            typedesc = SplitString(rawdata[index+16:index+markersize[0]])
            ma.type = typedesc[0]
            ma.description = typedesc[1]

            markers.append(ma)
            index = index + markersize[0]
        return (block, points, markerCount, data, markers)
    #-----------------------------------------------




    def HelpDialog(self):
        print('help triggered')

    def closeApp(self):
        sys.exit('quit')


    def updateShortConfigureInfo(self):
        print("updateShortConfigureInfo")
        self.shortcutsManager = None
        self.updatedShortcutsManager = ShortcutsWindow()
        # self.shortcutsManager.c.closeApp.connect(self.updateShortConfigureInfo)

        self.updatedFieldValueList = self.updatedShortcutsManager.getAllInfo()

        shortcutsExistingInfo = ""

        if self.fieldValueList is not None:
            for index in range(0, len(self.updatedFieldValueList)):
                fieldValue = self.updatedFieldValueList[index]
                shortcutsExistingInfo = (
                    shortcutsExistingInfo
                    + str(fieldValue.key, encoding="utf-8")
                    + "  "
                    + str(fieldValue.description, encoding="utf-8")
                    + "\n<br>"
                )
        else:
            print("fieldValueList is none")
            shortcutsExistingInfo = "快捷键未定义。"

        self._translate = QtCore.QCoreApplication.translate
        self.EventList.setHtml(
            self._translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Arial'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">定义好的事件快捷键：</span></p>\n'
                " %s",
            )
            % shortcutsExistingInfo
        )
        self.EventList.show()
        print(shortcutsExistingInfo)
        self.shortcutsManager = self.updatedShortcutsManager
        self.updatedShortcutsManager = None

    def initiateShortConfigureInfo(self):
        print("initiateShortConfigureInfo")
        # self.shortcutsManager = ShortcutsWindow()
        # self.shortcutsManager.c.closeApp.connect(self.updateShortConfigureInfo)

        self.fieldValueList = self.shortcutsManager.getAllInfo()

        shortcutsExistingInfo = ""

        if self.fieldValueList is not None:
            for index in range(0, len(self.fieldValueList)):
                fieldValue = self.fieldValueList[index]
                shortcutsExistingInfo = (
                    shortcutsExistingInfo
                    + str(fieldValue.key, encoding="utf-8")
                    + "  "
                    + str(fieldValue.description, encoding="utf-8")
                    + "\n<br>"
                )
        else:
            print("fieldValueList is none")
            shortcutsExistingInfo = "快捷键未定义。"

        self._translate = QtCore.QCoreApplication.translate
        self.EventList.setHtml(
            self._translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Arial'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">定义好的事件快捷键：</span></p>\n'
                " %s",
            )
            % shortcutsExistingInfo
        )
        self.EventList.show()
        print(shortcutsExistingInfo)

    def callShortCutsConfiguration(self):
        # print("---")
        self.shortcutsManager.show()
        # self.ShortcutConfigureWidget.show()

    def initUI(self):
        pass

    def actionNew_Participant_InfoExcute(self):
        SI.userManage = UserManage.UserManageForm()
        SI.userManage.show()

    # --Contents added for tab 3 start here (by cmj on 20210928)--
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.playlist.addMedia(QMediaContent(url))
        self.model.layoutChanged.emit()
        # If not playing, seeking to first of newly added + play.
        if self.playbackPlayer.state() != QMediaPlayer.PlayingState:
            i = self.playlist.mediaCount() - len(e.mimeData().urls())
            self.playlist.setCurrentIndex(i)
            self.playbackPlayer.play()

    def open_media(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "mp3 Audio (*.mp3);mp4 Video (*.mp4);Movie files (*.mov);All files (*.*)",
        )
        if path:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.model.layoutChanged.emit()

    def update_duration(self, duration):
        print("!", duration)
        print("?", self.playbackPlayer.duration())
        self.VideoProgress.setMaximum(duration)
        if duration >= 0:
            self.totaltimelabel2.setText(hhmmss(duration))

    def update_position(self, position):
        if position >= 0:
            self.currenttimelabel2.setText(hhmmss(position))
        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.VideoProgress.blockSignals(True)
        self.VideoProgress.setValue(position)
        self.VideoProgress.blockSignals(False)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.PlaybackList.setCurrentIndex(ix)

    def erroralert(self, *args):
        print(args)

    # --Contents added for tab 3 end here (by cmj on 20210928)--



if __name__ == '__main__':
    app = QApplication(sys.argv)

    #----------------Set color dark--------------------
    #app.setStyle("Fusion")
    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    #palette = QPalette()
    #palette.setColor(QPalette.Window, QColor(53, 53, 53))
    #palette.setColor(QPalette.WindowText, Qt.white)
    #palette.setColor(QPalette.Base, QColor(25, 25, 25))
    #palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    #palette.setColor(QPalette.ToolTipBase, Qt.white)
    #palette.setColor(QPalette.ToolTipText, Qt.white)
    #palette.setColor(QPalette.Text, Qt.white)
    #palette.setColor(QPalette.Button, QColor(53, 53, 53))
    #palette.setColor(QPalette.ButtonText, Qt.white)
    #palette.setColor(QPalette.BrightText, Qt.red)
    #palette.setColor(QPalette.Link, QColor(42, 130, 218))
    #palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    #palette.setColor(QPalette.HighlightedText, Qt.black)
    #app.setPalette(palette)
    #app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    #---------------------------------------------------
    
    app.setQuitOnLastWindowClosed(True)
    # test
    userMainWindow = UserMainWindowClass()
    form = my_ComboBox(userMainWindow)
    # userMainWindow = UserMainWindowClass()
    globalShortcuts = GlobalShortcuts()
    userMainWindow.globalShortcutsSignal.connect(globalShortcuts.globalShortcutsSlot)
    # shortcutsManager = ShortcutsManagerClass(userMainWindow)
    userMainWindow.show()

    # mainWindow.show()
    sys.exit(app.exec_())
