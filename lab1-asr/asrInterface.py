# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asrInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QMovie, QIcon
from sympy import re
from recognize import Recognize_Thread
from threading import Thread
import speech_recognition as sr
import os
import win32api


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(344, 550)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 280, 231, 55))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 250, 231, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.voiceFig = QtWidgets.QLabel(self.centralwidget)
        self.voiceFig.setGeometry(QtCore.QRect(85, 50, 161, 121))
        self.voiceFig.setText("")
        self.gif = QMovie("icon/voice.gif")
        self.voiceFig.setMovie(self.gif)
        self.gif.start()
        self.voiceFig.setScaledContents(True)
        self.voiceFig.setObjectName("voiceFig")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 160, 191, 25))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 117, 210);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 340, 231, 55))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 400, 231, 55))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(0, 117, 210);")
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(152, 470, 40, 50))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("QPushButton{color:rgb(0, 0, 0)}"
                                      "QPushButton:hover{color:rgb(0, 117, 210)}"
                                      "QPushButton{background-color:white}"
                                      "QPushButton{border:2px}"
                                      "QPushButton{border-radius:10px}"
                                      "QPushButton{padding:2px 4px}")
        self.pushButton.setObjectName("pushButton")
        self.icon = QIcon("icon/mic.png")
        self.pushButton.setIcon(self.icon)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Use another thread to recognize speech
        self.thread = Recognize_Thread()
        self.thread.signal.connect(self.callback)
        self.pushButton.clicked.connect(self.recognize_speech)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))
        self.label_3.setText(_translate(
            "MainWindow", "1. Enjoy music by saying \"Play music\""))
        self.label_2.setText(_translate("MainWindow", "You can:"))
        self.label.setText(_translate("MainWindow", "Hi! How can I help?"))
        self.label_4.setText(_translate(
            "MainWindow", "2. Take some notes by saying \"Open Notepad\""))
        self.label_5.setText(_translate(
            "MainWindow", "3. Search Internet by asking any questions"))

    def recognize_speech(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "I am listening..."))
        self.label.repaint()
        self.thread.start()

    def callback(self, response):
        _translate = QtCore.QCoreApplication.translate
        print(response)
        if response["success"] is None:
            self.label.setText(_translate("MainWindow", "Recognizing..."))
            self.label.repaint()
        elif response["success"] and response["error"] is None:
            self.label.setText(_translate(
                "MainWindow", response["transcription"].title()))
            self.label.repaint()
            self.execute_command(response["transcription"])
        else:
            self.label.setText(_translate("MainWindow", response["error"]))
            self.label.repaint()

    def execute_command(self, command):
        words = command.lower().split()
        if "play" in words or "music" in words:
            if os.path.exists('.\\test.mp3'):
                win32api.ShellExecute(0, 'open', '.\\test.mp3', '', '', 1)
            else:
                # music not exists, show message on GUI
                self.label.setText(QtCore.QCoreApplication.translate(
                    "MainWindow", "Music not found"))
        elif "open" in words or "notepad" in words:
            if not os.path.exists('.\\note.txt'):
                # create new file
                f = open('.\\note.txt', 'x')
                f.close()
            win32api.ShellExecute(0, 'open', '.\\note.txt', '', '', 0)
        elif command != '':
            # search on Bing
            url = 'https://cn.bing.com/search?q=' + command
            win32api.ShellExecute(0, 'open', url, '', '', 1)
