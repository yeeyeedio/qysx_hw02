from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog  # 导入PyQt5库的相关组件
from PyQt5.QtCore import Qt  # 导入Qt核心模块
from PyQt5.QtGui import QPixmap, QImage  # 导入QPixmap和QImage用于处理图像
import os  # 导入os库，用于处理文件和目录路径
import traceback  # 导入traceback库，用于打印错误信息

class HumanRecognitionMenu(QMainWindow):
    def __init__(self):
        # 调用父类QMainWindow的初始化方法
        super(HumanRecognitionMenu, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('人流量监测')
        # 设置窗口位置和大小
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件和布局
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 设置背景图片
        self.background_label = QLabel(self)
        pixmap = QPixmap(os.path.join('data', 'sc_3.jpg'))  # 加载背景图片
        self.background_label.setPixmap(pixmap)  # 设置背景图片
        self.background_label.setAlignment(Qt.AlignCenter)  # 设置图片居中
        self.background_label.setScaledContents(True)  # 设置图片自动缩放
        self.layout.addWidget(self.background_label)  # 将背景标签添加到布局中

        # 创建按钮
        self.live_monitor_button = QPushButton('实时监控', self)
        self.video_button = QPushButton('视频分析', self)
        self.back_button = QPushButton('返回', self)

        # 连接按钮点击事件到相应的方法
        self.live_monitor_button.clicked.connect(self.enter_live_monitor)
        self.video_button.clicked.connect(self.select_video_file)
        self.back_button.clicked.connect(self.back_to_main_menu)

        # 创建按钮布局，并添加按钮
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.live_monitor_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.video_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # 创建容器部件，并设置布局
        container = QWidget()
        container.setLayout(button_layout)

        # 创建主布局，并将容器部件添加到布局中
        main_layout = QVBoxLayout()
        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        self.background_label.setLayout(main_layout)

    def enter_live_monitor(self):
        """
        进入实时监控界面
        """
        try:
            from menu.live_monitor_menu import LiveMonitorMenu  # 延迟导入LiveMonitorMenu模块
            self.live_monitor_menu = LiveMonitorMenu(mode='crowd')  # 创建LiveMonitorMenu实例，模式设置为'crowd'
            self.live_monitor_menu.show()  # 显示实时监控界面
            self.close()  # 关闭当前窗口
        except Exception as e:
            # 捕获并打印异常
            print("Error occurred while entering live monitor:", e)
            traceback.print_exc()

    def select_video_file(self):
        """
        选择视频文件进行分析
        """
        try:
            # 打开文件对话框选择视频文件
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "Video Files (*.mp4 *.avi);;All Files (*)", options=options)
            if fileName:
                from menu.video_analysis_menu import VideoAnalysisMenu  # 延迟导入VideoAnalysisMenu模块
                self.video_analysis_menu = VideoAnalysisMenu(fileName, mode='crowd')  # 创建VideoAnalysisMenu实例，传入选择的视频文件和模式
                self.video_analysis_menu.show()  # 显示视频分析界面
                self.close()  # 关闭当前窗口
        except Exception as e:
            # 捕获并打印异常
            print("Error occurred while selecting video file:", e)
            traceback.print_exc()

    def back_to_main_menu(self):
        """
        返回主菜单界面
        """
        self.close()  # 关闭当前窗口
        from menu.main_menu import MainMenu  # 延迟导入MainMenu模块
        self.main_menu = MainMenu()  # 创建MainMenu实例
        self.main_menu.show()  # 显示主菜单界面
