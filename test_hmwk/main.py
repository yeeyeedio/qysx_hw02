from PyQt5.QtWidgets import QApplication  # 导入QApplication用于创建Qt应用程序
import sys  # 导入sys库，用于与解释器交互
from menu.login_menu import LoginMenu  # 从menu包中导入LoginMenu类

if __name__ == '__main__':
    # 创建Qt应用程序实例
    app = QApplication(sys.argv)
    # 创建LoginMenu实例
    window = LoginMenu()
    # 显示登录窗口
    window.show()
    # 运行应用程序
    sys.exit(app.exec_())
