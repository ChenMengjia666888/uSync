import sys
from PyQt5.QtWidgets import QTextEdit, QWidget, QMessageBox, QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import QCoreApplication
import sqliteCRUB

from PyQt5.QtGui import QImage, QPainter, QPixmap
import cv2
import numpy as np
import cv2, imutils


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 750, 550)
        # w = QWidget()
        self.resize(750, 550)
        self.move(300, 300)

        subjectIDLabel = QLabel("被试名：", self)
        subjectIDLabel.move(10, 50)

        self.subjectIDEntry = QLineEdit("", self)
        self.subjectIDEntry.move(70, 50)
        self.label = QLabel(self)

        cap = cv2.VideoCapture(0)
        img, self.image = cap.read()
        # cv2.imshow("Frame", frame)
        self.image = imutils.resize(self.image, height=420)
        self.tmp = self.image
        image = imutils.resize(self.image, width=420)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(
            frame,
            frame.shape[1],
            frame.shape[0],
            frame.strides[0],
            QImage.Format_RGB888,
        )
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.move(50, 90)

        btn = QPushButton("确认", self)
        btn.move(50, 400)
        btn.clicked.connect(self.saveUserDB)

        btnCancel = QPushButton("关闭", self)
        btnCancel.move(200, 400)
        btnCancel.clicked.connect(QCoreApplication.instance().quit)
        self.setWindowTitle("Video Preview by uSync software")

        self.show()

    def saveUser(self, event):
        print("1111")
        outfile = open("user-account.txt", "a")
        outfile.write(self.subjectIDEntry.text())
        outfile.close()

    def saveUserDB(self, event):
        print("saveUserDB")
        sqliteCRUB.AddInitialDB()
        sqliteCRUB.AddParticipant2DB(self.subjectIDEntry.text(), "-", "-")

    def closeEvent(self, event):

        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
