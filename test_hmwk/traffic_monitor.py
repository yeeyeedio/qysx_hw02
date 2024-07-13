import cv2  # 导入cv2库用于视频捕捉和图像处理
import base64  # 导入base64库用于编码和解码base64数据
import logging  # 导入logging库用于记录日志
import threading  # 导入threading库用于多线程操作
from PyQt5.QtCore import QThread, pyqtSignal, QTimer  # 导入QThread、pyqtSignal和QTimer用于线程和定时器操作
from PyQt5.QtGui import QImage, QPainter, QColor  # 导入QImage、QPainter和QColor用于图像处理
from api_baidu.vehicle_detection import VehicleDetection  # 从api_baidu导入VehicleDetection类
from api_baidu.human_recognition import HumanRecognition  # 从api_baidu导入HumanRecognition类

# 配置日志记录
logging.basicConfig(filename='traffic_monitor.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# 使用线程锁来确保线程安全
result_lock = threading.Lock()

class VehicleDetectionThread(QThread):
    # 定义线程信号
    result_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, img_base64, access_token, semaphore):
        # 调用父类QThread的初始化方法
        super(VehicleDetectionThread, self).__init__()
        self.detector = VehicleDetection(access_token)  # 初始化车辆检测器
        self.img_base64 = img_base64  # 保存图像的base64编码
        self.semaphore = semaphore  # 信号量，用于限制并发数量

    def run(self):
        with self.semaphore:
            try:
                result = self.detector.detect(self.img_base64)  # 调用车辆检测API
                if result:
                    self.result_signal.emit(result)  # 发送检测结果信号
                else:
                    self.error_signal.emit("车辆检测API请求失败")  # 发送错误信号
            except Exception as e:
                self.error_signal.emit(f"车辆检测线程异常: {str(e)}")  # 发送异常信号
                logging.error(f"车辆检测线程异常: {str(e)}")  # 记录异常日志

class CrowdCountingThread(QThread):
    # 定义线程信号
    result_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, img_base64, access_token, semaphore):
        # 调用父类QThread的初始化方法
        super(CrowdCountingThread, self).__init__()
        self.counter = HumanRecognition(access_token)  # 初始化人流量统计器
        self.img_base64 = img_base64  # 保存图像的base64编码
        self.semaphore = semaphore  # 信号量，用于限制并发数量

    def run(self):
        with self.semaphore:
            try:
                result = self.counter.count(self.img_base64)  # 调用人流量统计API
                if result:
                    self.result_signal.emit(result)  # 发送统计结果信号
                else:
                    self.error_signal.emit("人流量统计API请求失败")  # 发送错误信号
            except Exception as e:
                self.error_signal.emit(f"人流量统计线程异常: {str(e)}")  # 发送异常信号
                logging.error(f"人流量统计线程异常: {str(e)}")  # 记录异常日志

class TrafficMonitor:
    def __init__(self, update_image_callback, update_text_callback, update_vehicle_count_callback, mode='vehicle'):
        self.update_image_callback = update_image_callback  # 更新图像回调函数
        self.update_text_callback = update_text_callback  # 更新文本回调函数
        self.update_vehicle_count_callback = update_vehicle_count_callback  # 更新车辆计数回调函数
        self.cap = None  # 视频捕捉对象
        self.timer = QTimer()  # 定时器对象
        self.timer.timeout.connect(self.update_frame)  # 连接定时器超时信号到更新帧方法
        self.vehicle_access_token = '24.7c009f00db2ab5b048bda2cd1b9305cf.2592000.1723336808.282335-93691061'  # 车辆检测API的访问令牌
        self.human_recognition_token = '24.67c209eede6c3d6af90aad6b37839d50.2592000.1723336931.282335-93462147'  # 人流量统计API的访问令牌
        self.frame_count = 0  # 帧计数
        self.detections = []  # 检测结果列表
        self.is_paused = False  # 暂停标志
        self.mode = mode  # 'vehicle'或'crowd'模式
        self.last_count = 0  # 保持显示最近的API返回结果
        self.api_semaphore = threading.Semaphore(2)  # 限制并发数量为2

    def start_monitoring(self):
        """
        启动实时监控
        """
        logging.info("启动实时监控")
        print("启动实时监控")
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)  # 打开默认摄像头
        if not self.cap.isOpened():
            self.update_text_callback("无法打开摄像头")
            logging.error("无法打开摄像头")
            print("无法打开摄像头")
            return
        self.is_paused = False
        self.timer.start(30)  # 每30毫秒更新一次帧

    def select_video_file(self, video_file):
        """
        选择视频文件进行分析
        """
        logging.info(f"选择视频文件: {video_file}")
        print(f"选择视频文件: {video_file}")
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(video_file)  # 打开视频文件
        if not self.cap.isOpened():
            self.update_text_callback("无法打开视频文件")
            logging.error("无法打开视频文件")
            print("无法打开视频文件")
            return
        self.is_paused = False
        self.timer.start(30)  # 每30毫秒更新一次帧

    def stop_monitoring(self):
        """
        停止监控
        """
        logging.info("停止监控")
        print("停止监控")
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None

    def toggle_pause(self):
        """
        切换暂停状态
        """
        if self.is_paused:
            self.timer.start(30)
        else:
            self.timer.stop()
        self.is_paused = not self.is_paused

    def update_frame(self):
        """
        更新视频帧
        """
        if not self.is_paused:
            ret, frame = self.cap.read()
            if not ret:
                self.update_text_callback("无法捕获视频帧")
                logging.error("无法捕获视频帧")
                print("无法捕获视频帧")
                return

            self.frame_count += 1
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将帧转换为RGB格式
            height, width, channel = frame_rgb.shape
            step = channel * width
            qimg = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)

            qimg_with_detections = qimg.copy()
            painter = QPainter(qimg_with_detections)
            painter.setPen(QColor(0, 255, 0))
            with result_lock:
                for detection in self.detections:
                    if self.mode == 'vehicle':
                        vehicle_type, left, top, width, height = detection
                        painter.drawRect(left, top, width, height)  # 绘制矩形
                        painter.drawText(left, top - 10, vehicle_type)  # 绘制车辆类型文本
                    else:
                        person_count, left, top, width, height = detection
                        painter.drawRect(left, top, width, height)  # 绘制矩形
                        painter.drawText(left, top - 10, str(person_count))  # 绘制人数文本
            painter.end()

            self.update_image_callback(qimg_with_detections)

            if self.frame_count % 15 == 0:
                _, buffer = cv2.imencode('.jpg', frame)  # 将帧编码为JPEG格式
                img_base64 = base64.b64encode(buffer).decode()

                if self.mode == 'vehicle':
                    self.vehicle_detection_thread = VehicleDetectionThread(img_base64, self.vehicle_access_token, self.api_semaphore)
                    self.vehicle_detection_thread.result_signal.connect(self.process_vehicle_detection_result)
                    self.vehicle_detection_thread.error_signal.connect(self.update_text_callback)
                    self.vehicle_detection_thread.start()
                else:
                    self.crowd_counting_thread = CrowdCountingThread(img_base64, self.human_recognition_token, self.api_semaphore)
                    self.crowd_counting_thread.result_signal.connect(self.process_crowd_counting_result)
                    self.crowd_counting_thread.error_signal.connect(self.update_text_callback)
                    self.crowd_counting_thread.start()

    def process_vehicle_detection_result(self, result):
        """
        处理车辆检测结果
        """
        vehicle_info = result.get('vehicle_info', [])
        new_detections = []
        result_text = "车辆检测结果:\n"
        vehicle_count = 0
        for vehicle in vehicle_info:
            vehicle_type = vehicle.get('type', '未知')
            location = vehicle.get('location', {})
            left = location.get('left', 0)
            top = location.get('top', 0)
            width = location.get('width', 0)
            height = location.get('height', 0)
            new_detections.append((vehicle_type, left, top, width, height))
            result_text += f"类型: {vehicle_type}, 位置: 左上({left}, {top}), 宽: {width}, 高: {height}\n"
            vehicle_count += 1

        with result_lock:
            self.detections = new_detections
            self.update_text_callback(result_text)
            self.update_vehicle_count_callback(vehicle_count)
            logging.info(f"检测到 {vehicle_count} 辆车辆")
            print(f"检测到 {vehicle_count} 辆车辆")

    def process_crowd_counting_result(self, result):
        """
        处理人流量统计结果
        """
        with result_lock:
            if result:
                person_num = result.get('person_num', 0)
                self.last_count = person_num  # 更新最近结果
                new_detections = [(person_num, 0, 0, 0, 0)]
                result_text = f"人流量统计结果: {person_num} 人"
                self.detections = new_detections
                self.update_text_callback(result_text)
                self.update_vehicle_count_callback(person_num)
                logging.info(f"检测到 {person_num} 人")
                print(f"检测到 {person_num} 人")
            else:
                # 保持上次结果
                result_text = f"人流量统计结果: {self.last_count} 人"
                self.update_text_callback(result_text)
                self.update_vehicle_count_callback(self.last_count)
                logging.info(f"保持最近的检测结果: {self.last_count} 人")
                print(f"保持最近的检测结果: {self.last_count} 人")
