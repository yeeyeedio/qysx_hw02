import sys  # 导入sys库，用于与解释器交互

from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QApplication  # 导入PyQt5库的相关组件
from PyQt5.QtCore import Qt, QTimer  # 导入Qt核心模块和QTimer定时器
from PyQt5.QtGui import QPixmap, QImage, QColor, QPalette  # 导入QPixmap、QImage用于处理图像，QColor和QPalette用于设置颜色
import collections  # 导入collections模块，用于创建双端队列
import logging  # 导入logging库，用于记录日志
import traceback  # 导入traceback库，用于打印错误信息
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # 导入FigureCanvas用于嵌入matplotlib图表
from matplotlib.figure import Figure  # 导入Figure用于创建图表

class LiveMonitorMenu(QMainWindow):
    def __init__(self, mode='vehicle'):
        # 调用父类QMainWindow的初始化方法
        super(LiveMonitorMenu, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('实时监控')
        # 设置窗口位置和大小
        self.setGeometry(100, 100, 1200, 800)  # 增大窗口尺寸
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
        self.image_label.setFixedSize(800, 450)  # 固定监控视频的尺寸

        self.vehicle_count_label = QLabel(self)
        self.vehicle_count_label.setAlignment(Qt.AlignCenter)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.data_queue = collections.deque(maxlen=20)  # 限制折线图显示的数据点数量

        self.toggle_button = QPushButton('开始/停止', self)
        self.back_button = QPushButton('返回', self)

        self.toggle_button.setCheckable(True)  # 设置按钮可切换状态
        self.toggle_button.clicked.connect(self.toggle_monitoring)  # 连接按钮点击事件到相应的方法
        self.back_button.clicked.connect(self.back_to_main_menu)

        # 创建按钮布局，并添加按钮
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.vehicle_count_label, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.layout.addLayout(button_layout)
        self.layout.setAlignment(Qt.AlignCenter)

        # 隐藏折线图和标签，初始时按钮居中
        self.image_label.hide()
        self.vehicle_count_label.hide()
        self.canvas.hide()

        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setAlignment(Qt.AlignCenter)

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        self.button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.central_layout.addStretch()
        self.central_layout.addLayout(self.button_layout)
        self.central_layout.addStretch()

        self.layout.addLayout(self.central_layout)
        self.layout.setAlignment(Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)

    def toggle_monitoring(self):
        """
        切换监控状态
        """
        try:
            from traffic_monitor import TrafficMonitor  # 延迟导入TrafficMonitor模块
            if not self.monitor:
                self.monitor = TrafficMonitor(self.update_image, self.update_text, self.update_vehicle_count, mode=self.mode)
                self.monitor.start_monitoring()
            if self.toggle_button.isChecked():
                self.monitor.start_monitoring()
                self.timer.start(1000)  # 每秒更新一次折线图
                self.image_label.show()  # 显示监控视频
                self.vehicle_count_label.show()  # 显示车辆计数
                self.canvas.show()  # 显示折线图
                logging.info("开始实时监控")
            else:
                self.monitor.toggle_pause()
                self.timer.stop()
                logging.info("暂停实时监控")
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
        更新日志文本
        :param text: 要记录的文本
        """
        print(text)
        logging.info(text)

    def update_vehicle_count(self, count):
        """
        更新车辆计数
        :param count: 当前车辆数量
        """
        self.data_queue.append(count)
        self.vehicle_count_label.setText(f"当前人数: {count}" if self.mode == 'crowd' else f"当前车辆数量: {count}")

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

    def back_to_main_menu(self):
        """
        返回主菜单界面
        """
        if self.monitor:
            self.monitor.stop_monitoring()
            self.monitor = None
        self.timer.stop()
        self.data_queue.clear()
        self.canvas.hide()  # 隐藏折线图
        self.close()
        from menu.main_menu import MainMenu  # 延迟导入MainMenu模块
        self.main_menu = MainMenu()  # 创建MainMenu实例
        self.main_menu.show()  # 显示主菜单界面

if __name__ == "__main__":
    app = QApplication(sys.argv)
    live_monitor_menu = LiveMonitorMenu("vehicle")
    live_monitor_menu.show()
    sys.exit(app.exec_())
