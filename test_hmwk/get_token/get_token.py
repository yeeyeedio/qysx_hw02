# get_token.py
import requests
import json


# 图像识别的API密钥
# api_key = 'WmMa00WsNNcMUz49D4m3SBNw'
# secret_key = 'e69NQdmsmloOUzKfHuZ3Lam9X9N7CgBF'
# token = '24.7c009f00db2ab5b048bda2cd1b9305cf.2592000.1723336808.282335-93691061'

# 人体检测和属性识别的API密钥
# api_key = 'i8xLgGDZoTf72DZjCtWg6191'
# secret_key = 'J1XSkTin5dZt1Pq64urU0ocTQIyFsfAE'
# token = '24.67c209eede6c3d6af90aad6b37839d50.2592000.1723336931.282335-93462147'

# 任意选取一个API密钥即可完成所有调用
def get_access_token():
    """
    获取访问令牌的函数。通过API Key和Secret Key向百度AI开放平台请求获取访问令牌。

    Returns:
        str: 返回获取的访问令牌，如果失败则返回None。
    """
    # 使用图像识别的API密钥和Secret Key
    api_key = 'i8xLgGDZoTf72DZjCtWg6191'
    secret_key = 'J1XSkTin5dZt1Pq64urU0ocTQIyFsfAE'
    # 获取访问令牌的URL
    token_url = 'https://aip.baidubce.com/oauth/2.0/token'

    # 拼接完整的URL，包含请求参数
    url = f"{token_url}?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"

    # 设置请求头
    headers = {
        'Content-Type': 'application/json',  # 指定内容类型为JSON
        'Accept': 'application/json'  # 接受返回的内容类型为JSON
    }

    # 发送POST请求以获取访问令牌
    response = requests.request("POST", url, headers=headers)

    # 判断请求是否成功
    if response.status_code == 200:
        # 解析返回的JSON响应
        token_info = response.json()
        # 返回访问令牌
        return token_info.get('access_token')
    else:
        # 如果请求失败，打印错误信息
        print(f"Error: Unable to get access token, {response.text}")
        # 返回None表示获取失败
        return None


if __name__ == '__main__':
    # 获取访问令牌并打印
    token = get_access_token()
    print(token)
