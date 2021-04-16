
# pip install PyQt6
# pyuic6 messenger.ui -o clientui.py

# В этом py файле описана логика взаимодействия с интерфейсом


from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QFileDialog
# импорт функций из других файлов
from clientui import Ui_MainWindow
from drctryChoice import Ui_drctryChoice
from takeFiles import Ui_takeFiles
from datetime import datetime
from errors import *
import secProcessing
import n7Proccesing
import os


class Passport(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # описание работы главного окна
        self.setupUi(self)
        self.runPassport.pressed.connect(self.onClick)
        self.openDirectory.pressed.connect(self.openDrctry)
        self.openFileDirectory.pressed.connect(self.openFileDrctry)
        self.runSevend.pressed.connect(self.onClick7_d)
        self.dateEdit_2.setDate(QtCore.QDate(int(str(datetime.today()).split(' ')[0].split('-')[0]),
                                             int(str(datetime.today()).split(' ')[0].split('-')[1]),
                                             int(str(datetime.today()).split(' ')[0].split('-')[2])))
        self.dateEdit_2.setDisplayFormat("dd.MM.yyyy")
        self.dateEdit.setDate(QtCore.QDate(2020, 1, 1))
        self.dateEdit.setDisplayFormat("dd.MM.yyyy")

    def openFileDrctry(self):
        # описание работы всплывающей формы выбора директории с файлами ПРИЗМА
        self.inst = QtWidgets.QWidget()
        ui_drctry = Ui_takeFiles()
        ui_drctry.setupUi(self.inst)
        # запись в 2 файла -> 2 кластера, чтобы данные о папке сохранялись в отрыве от работы программы
        try:
            with open('path1files.ini', 'r') as f:
                ui_drctry.lineEdit.setText(f.read())
        except:
            ui_drctry.lineEdit.setText("")
        try:
            with open('path2files.ini', 'r') as f2:
                ui_drctry.lineEdit_2.setText(f2.read())
        except:
            ui_drctry.lineEdit_2.setText("")
        ui_drctry.pushButton.clicked.connect(lambda: Ui_takeFiles.getFileDirectory(ui_drctry, 'path1files'))
                                                            # Ui_takeFiles.getFileDirectory аналог getPassDirectory,
                                                            # но в файле takesFiles.py
        ui_drctry.pushButton_2.clicked.connect(lambda: Ui_takeFiles.getFileDirectory(ui_drctry, 'path2files'))
        self.inst.show()

    def openDrctry(self):
        # описание работы всплывающей формы выбора директории сохранения паспорта, картинок, файлов и т.д.
        self.inst = QtWidgets.QWidget()
        ui_drctry = Ui_drctryChoice()
        ui_drctry.setupUi(self.inst)
        ui_drctry.pushButton.clicked.connect(self.getPassDirectory)
        try:
            with open('pathpass.ini', 'r') as f:
                ui_drctry.lineEdit.setText(f.read())
        except:
            ui_drctry.lineEdit.setText("")
        self.inst.show()

    def getPassDirectory(self):
        # Сам выбор папки, да знаю, что немного косой, и можно было бы убрать из этого файла в другой
        self.inst = QtWidgets.QWidget()
        ui_drctry = Ui_drctryChoice()
        ui_drctry.setupUi(self.inst)
        dirlist = QFileDialog.getExistingDirectory(self)
        ui_drctry.lineEdit.setText(dirlist)
        with open('pathpass.ini', 'w') as f:
            f.write(dirlist)
        self.inst.show()
        print(dirlist)

    def onClick(self):
        # описание работы кнопки получения паспорта
        strtDate = self.dateEdit.dateTime().toString('dd MM yyyy')
        endDate = self.dateEdit_2.dateTime().toString('dd MM yyyy')
        lst = []
        with open('pathpass.ini', 'r') as f:
            dirlist = f.read()
        piclist = dirlist + '/Pics'
        with open('path1files.ini', 'r') as f:
            file1cl = f.read()
        with open('path2files.ini', 'r') as f:
            file2cl = f.read()
        if ~os.path.exists(piclist):
            try:
                os.mkdir(piclist)
            except OSError:
                print("Создать директорию %s не удалось" % piclist)
            else:
                print("Успешно создана директория %s " % piclist)
        lst.append(strtDate.split(" "))
        lst.append(endDate.split(" "))
        # проверяем нормальные даты или нет, если да, то графики и ворд файл строятся
        try:
            secProcessing.secProccesing(int(lst[0][0]), int(lst[0][1]), int(lst[0][2]), int(lst[1][0]), int(lst[1][1]),
                                    int(lst[1][2]), dirlist, piclist, file1cl, file2cl)
        except ZeroDivisionError:
            dataError()

    def onClick7_d(self):
        # работы кнопки получения информации по 7-му диноду
        strtDate = self.dateEdit.dateTime().toString('dd MM yyyy')
        endDate = self.dateEdit_2.dateTime().toString('dd MM yyyy')
        lst = []
        with open('pathpass.ini', 'r') as f:
            dirlist = f.read()
        piclist = dirlist + '/Pics'
        with open('path1files.ini', 'r') as f:
            file1cl = f.read()
        with open('path2files.ini', 'r') as f:
            file2cl = f.read()
        if ~os.path.exists(piclist):
            try:
                os.mkdir(piclist)
            except OSError:
                print("Создать директорию %s не удалось" % piclist)
            else:
                print("Успешно создана директория %s " % piclist)
        lst.append(strtDate.split(" "))
        lst.append(endDate.split(" "))
        # смотри коммент выше
        try:
            n7Proccesing.n7Proccesing(int(lst[0][0]), int(lst[0][1]), int(lst[0][2]), int(lst[1][0]), int(lst[1][1]),
                                      int(lst[1][2]), dirlist, piclist, file1cl, file2cl)
        except KeyError:
            dataError()


# запуск основного окна
app = QtWidgets.QApplication([])
window = Passport()
window.show()
app.exec()

# Не удаляй, код должен остаться, если сломается takeFiles.py

# def getFileDirectory(self, filename):
#     dirlist = QFileDialog.getExistingDirectory(self)
#     if filename == 'path1files':
#         self.lineEdit.setText(dirlist)
#     else:
#         self.lineEdit_2.setText(dirlist)
#     with open(filename + '.ini', 'w') as f:
#         f.write(dirlist)
#     print(dirlist)
