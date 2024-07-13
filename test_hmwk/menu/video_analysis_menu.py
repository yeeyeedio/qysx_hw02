import sys  # 导入sys库，用于与解释器交互
import os  # 导入os库，用于处理文件和目录路径
import traceback  # 导入traceback库，用于打印错误信息
import logging  # 导入logging库，用于记录日志
import collections  # 导入collections模块，用于创建双端队列
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QApplication  # 导入PyQt5库的相关组件
from PyQt5.QtCore import Qt, QTimer  # 导入Qt核心模块和QTimer定时器
from PyQt5.QtGui import QPixmap, QImage, QColor, QPalette  # 导入QPixmap、QImage用于处理图像，QColor和QPalette用于设置颜色
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # 导入FigureCanvas用于嵌入matplotlib图表
from matplotlib.figure import Figure  # 导入Figure用于创建图表

class VideoAnalysisMenu(QMainWindow):
    def __init__(self, video_file, mode='vehicle'):
        # 调用父类QMainWindow的初始化方法
        super(VideoAnalysisMenu, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('视频分析')
        # 设置窗口位置和大小
        self.setGeometry(100, 100, 800, 600)
        self.video_file = video_file  # 保存视频文件路径
        self.mode = mode  # 设置监控模式

        # 设置背景颜色
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setAutoFillBackground(True)
        palette = self.central_widget.palette()
        palette.setColor(QPalette.Window, QColor(236, 223, 207))  # 设置背景颜色
        self.central_widget.setPalette(palette)

        self.layout = QVBoxLayout(self.central_widget)

        self.monitor = None  # 初始化监控器对象

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.result_text = QLabel(self)
        self.result_text.setAlignment(Qt.AlignCenter)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.data_queue = collections.deque(maxlen=20)  # 限制折线图显示的数据点数量

        self.toggle_button = QPushButton('开始/停止', self)
        self.back_button = QPushButton('返回', self)

        self.toggle_button.setCheckable(True)  # 设置按钮可切换状态
        self.toggle_button.clicked.connect(self.toggle_monitoring)  # 连接按钮点击事件到相应的方法
        self.back_button.clicked.connect(self.back_to_previous_menu)

        # 创建按钮布局，并添加按钮
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.result_text, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.layout.addLayout(button_layout)
        self.layout.setAlignment(Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)

        self.canvas.hide()  # 初始时隐藏折线图

    def toggle_monitoring(self):
        """
        切换监控状态
        """
        try:
            from traffic_monitor import TrafficMonitor  # 延迟导入TrafficMonitor模块
            if not self.monitor:
                self.monitor = TrafficMonitor(self.update_image, self.update_text, self.update_vehicle_count, mode=self.mode)
                self.monitor.select_video_file(self.video_file)  # 选择视频文件
            if self.toggle_button.isChecked():
                self.monitor.start_monitoring()
                self.timer.start(1000)  # 每秒更新一次折线图
                self.canvas.show()  # 显示折线图
            else:
                self.monitor.toggle_pause()
                self.timer.stop()
        except Exception as e:
            print("Error occurred while toggling monitoring:", e)
            logging.error(f"Error occurred while toggling monitoring: {e}")
            traceback.print_exc()

    def update_image(self, qimg):
        """
        更新监控视频的图像
        :param qimg: QImage对象
        """
        self.image_label.setPixmap(QPixmap.fromImage(qimg))

    def update_text(self, text):
        """
        更新结果文本
        :param text: 要显示的文本
        """
        self.result_text.setText(text)

    def update_vehicle_count(self, count):
        """
        更新车辆计数
        :param count: 当前车辆数量
        """
        self.data_queue.append(count)
        self.result_text.setText(f"当前人数: {count}" if self.mode == 'crowd' else f"当前车辆数量: {count}")

    def update_plot(self):
        """
        更新折线图
        """
        self.ax.clear()
        self.ax.plot(list(self.data_queue), color='blue', marker='o', linestyle='-', linewidth=2, markersize=5)
        self.ax.set_facecolor('lightgrey')  # 设置图表背景颜色
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # 设置网格线
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        # 保留刻度线和Y轴坐标标签
        self.ax.tick_params(axis='both', which='both')
        self.canvas.draw()

    def back_to_previous_menu(self):
        """
        返回上一级菜单界面
        """
        if self.monitor:
            self.monitor.stop_monitoring()
            self.monitor = None
        self.timer.stop()
        self.data_queue.clear()
        self.canvas.hide()  # 隐藏折线图
        self.close()
        if self.mode == 'crowd':
            from menu.human_recognition_menu import HumanRecognitionMenu
            self.crowd_monitor_menu = HumanRecognitionMenu()
            self.crowd_monitor_menu.show()
        else:
            from menu.vehicle_detection_menu import VehicleDetectionMenu
            self.vehicle_detection_menu = VehicleDetectionMenu()
            self.vehicle_detection_menu.show()

if __name__ == "__main__":
    # 创建Qt应用程序实例
    app = QApplication(sys.argv)
    # 创建VideoAnalysisMenu实例，传入视频文件和模式
    video_analysis_menu = VideoAnalysisMenu("video.mp4", "vehicle")
    # 显示视频分析界面
    video_analysis_menu.show()
    # 运行应用程序
    sys.exit(app.exec_())
