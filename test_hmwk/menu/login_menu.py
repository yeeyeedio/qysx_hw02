from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout  # 导入PyQt5库的相关组件
from PyQt5.QtCore import Qt  # 导入Qt核心模块
from PyQt5.QtGui import QPixmap  # 导入QPixmap用于处理图像
import os  # 导入os库，用于处理文件和目录路径

class LoginMenu(QMainWindow):
    def __init__(self):
        # 调用父类QMainWindow的初始化方法
        super(LoginMenu, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('用户登录')
        # 设置窗口位置和大小
        self.setGeometry(100, 100, 800, 600)

        # 创建中央部件和布局
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 设置背景图片
        self.background_label = QLabel(self)
        pixmap = QPixmap(os.path.join('data', 'sc_imu.jpg'))  # 加载背景图片
        self.background_label.setPixmap(pixmap)  # 设置背景图片
        self.background_label.setAlignment(Qt.AlignCenter)  # 设置图片居中
        self.layout.addWidget(self.background_label)  # 将背景标签添加到布局中

        # 创建用户名输入框
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('用户名')  # 设置占位文本
        self.username_input.setFixedWidth(300)  # 设置输入框固定宽度
        # 创建密码输入框
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('密码')  # 设置占位文本
        self.password_input.setEchoMode(QLineEdit.Password)  # 设置输入框为密码模式
        self.password_input.setFixedWidth(300)  # 设置输入框固定宽度

        # 创建登录和注册按钮
        self.login_button = QPushButton('登录', self)
        self.register_button = QPushButton('注册', self)

        # 连接按钮点击事件到相应的方法
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        # 创建表单布局，并添加输入框和按钮
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        form_layout.setAlignment(Qt.AlignCenter)

        # 创建容器部件，并设置布局
        container = QWidget()
        container.setLayout(form_layout)

        # 创建主布局，并将容器部件添加到布局中
        main_layout = QVBoxLayout()
        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        self.background_label.setLayout(main_layout)

    def login(self):
        """
        用户登录
        """
        username = self.username_input.text()  # 获取用户名输入
        password = self.password_input.text()  # 获取密码输入

        if not username or not password:
            QMessageBox.warning(self, '错误', '用户名/密码不能为空')  # 显示警告消息框
            return

        # 检查用户名和密码是否匹配
        with open('users.txt', 'r') as f:
            for line in f:
                user, pwd = line.strip().split(',')
                if user == username and pwd == password:
                    self.enter_main_menu()  # 进入主菜单
                    return

        QMessageBox.warning(self, '错误', '用户名/密码错误')  # 显示警告消息框

    def register(self):
        """
        用户注册
        """
        username = self.username_input.text()  # 获取用户名输入
        password = self.password_input.text()  # 获取密码输入

        if not username or not password:
            QMessageBox.warning(self, '错误', '用户名/密码不能为空')  # 显示警告消息框
            return

        # 检查用户名是否已存在
        with open('users.txt', 'r') as f:
            for line in f:
                user, _ = line.strip().split(',')
                if user == username:
                    QMessageBox.warning(self, '错误', '用户名已存在')  # 显示警告消息框
                    return

        # 添加新用户
        with open('users.txt', 'a') as f:
            f.write(f'{username},{password}\n')  # 将新用户信息写入文件

        QMessageBox.information(self, '成功', '注册成功')  # 显示信息消息框

    def enter_main_menu(self):
        """
        进入主菜单界面
        """
        from menu.main_menu import MainMenu  # 延迟导入MainMenu模块
        self.main_menu = MainMenu()  # 创建MainMenu实例
        self.main_menu.show()  # 显示主菜单界面
        self.close()  # 关闭当前窗口
