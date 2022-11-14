import sys
from PyQt5.QtWidgets import QDialog, QApplication
from maindlg import Ui_Dialog


# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow
class MyApp(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置界面
        self.btn.clicked.connect(self.sayHi)  # 绑定点击信号和槽函数

    def sayHi(self):  # click对应的槽函数
        print("hi")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())