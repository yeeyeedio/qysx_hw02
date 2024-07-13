from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget  # 导入PyQt5库的相关组件
from PyQt5.QtCore import Qt  # 导入Qt核心模块
from PyQt5.QtGui import QPixmap  # 导入QPixmap用于处理图像
import os  # 导入os库，用于处理文件和目录路径

class MainMenu(QMainWindow):
    def __init__(self):
        # 调用父类QMainWindow的初始化方法
        super(MainMenu, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('主菜单')
        # 设置窗口位置和大小
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件和布局
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 设置背景图片
        self.background_label = QLabel(self)
        pixmap = QPixmap(os.path.join('data', 'sc_hos.jpg'))  # 加载背景图片
        self.background_label.setPixmap(pixmap)  # 设置背景图片
        self.background_label.setAlignment(Qt.AlignCenter)  # 设置图片居中
        self.layout.addWidget(self.background_label)  # 将背景标签添加到布局中

        # 创建按钮
        self.vehicle_detection_button = QPushButton('车辆检测', self)
        self.crowd_monitor_button = QPushButton('人流量监测', self)
        self.back_button = QPushButton('返回', self)

        # 连接按钮点击事件到相应的方法
        self.vehicle_detection_button.clicked.connect(self.enter_vehicle_detection)
        self.crowd_monitor_button.clicked.connect(self.enter_crowd_monitor)
        self.back_button.clicked.connect(self.back_to_login)

        # 创建按钮布局，并添加按钮
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.vehicle_detection_button)
        button_layout.addWidget(self.crowd_monitor_button)
        button_layout.addWidget(self.back_button)
        button_layout.setAlignment(Qt.AlignCenter)

        # 将按钮布局设置为背景标签的布局
        self.background_label.setLayout(button_layout)

    def enter_vehicle_detection(self):
        """
        进入车辆检测界面
        """
        from menu.vehicle_detection_menu import VehicleDetectionMenu  # 延迟导入VehicleDetectionMenu模块
        self.vehicle_detection_menu = VehicleDetectionMenu()  # 创建VehicleDetectionMenu实例
        self.vehicle_detection_menu.show()  # 显示车辆检测界面
        self.close()  # 关闭当前窗口

    def enter_crowd_monitor(self):
        """
        进入人流量监测界面
        """
        from menu.human_recognition_menu import HumanRecognitionMenu  # 延迟导入HumanRecognitionMenu模块
        self.crowd_monitor_menu = HumanRecognitionMenu()  # 创建HumanRecognitionMenu实例
        self.crowd_monitor_menu.show()  # 显示人流量监测界面
        self.close()  # 关闭当前窗口

    def back_to_login(self):
        """
        返回登录界面
        """
        from menu.login_menu import LoginMenu  # 延迟导入LoginMenu模块
        self.login_menu = LoginMenu()  # 创建LoginMenu实例
        self.login_menu.show()  # 显示登录界面
        self.close()  # 关闭当前窗口
