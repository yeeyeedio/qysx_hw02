import requests  # 导入requests库，用于发送HTTP请求
import base64  # 导入base64库，用于编码和解码base64数据
import logging  # 导入logging库，用于记录日志
import traceback  # 导入traceback库，用于打印错误信息

class VehicleDetection:
    def __init__(self, access_token):
        """
        初始化方法，设置访问令牌和车辆检测API的URL
        :param access_token: API访问令牌
        """
        self.access_token = access_token  # 初始化访问令牌
        self.vehicle_detect_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect'  # 车辆检测API的URL

    def detect(self, img_base64):
        """
        检测图像中的车辆
        :param img_base64: 图像的Base64编码字符串
        :return: 检测结果的JSON对象或None（如果失败）
        """
        try:
            # 设置请求参数
            params = {"image": img_base64}
            # 构造完整的请求URL，包括访问令牌
            request_url = self.vehicle_detect_url + "?access_token=" + self.access_token
            # 设置请求头，指定内容类型为表单数据
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            # 发送POST请求，带有参数和请求头，超时时间为30秒
            response = requests.post(request_url, data=params, headers=headers, timeout=30)

            # 如果响应存在且状态码为200（表示成功）
            if response and response.status_code == 200:
                # 返回JSON格式的响应内容
                return response.json()
            else:
                # 否则记录错误日志，包含状态码和返回内容
                logging.error(f"车辆检测API请求失败，返回状态码: {response.status_code}, 返回内容: {response.content}")
                return None
        except requests.RequestException as e:
            # 捕获请求异常，记录错误日志并打印堆栈跟踪
            logging.error(f"车辆检测API请求错误: {e}")
            traceback.print_exc()
            return None
