from PyQt6.QtWidgets import QMessageBox


# вывод ошибки набора дат
def dataError():
    msg = QMessageBox()
    # msg.setIcon(QMessageBox.icon())
    msg.setText("Date-time Error")
    msg.setInformativeText('Начальная дата обработки данных больше конечной')
    msg.setWindowTitle("Error")
    msg.exec()
    # QMessageBox.icon(DeprecationWarning)
