import requests
from requests.exceptions import HTTPError, RequestException

class HttpUtils:
    @staticmethod
    def get(url, params=None, headers=None, timeout=10):
        """
        发送 GET 请求

        :param url: 请求的 URL
        :param params: 查询参数（字典）
        :param headers: 请求头（字典）
        :param timeout: 超时时间（秒）
        :return: 响应内容（JSON 格式）
        """
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()  # 返回 JSON 格式的内容
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")
        return None

    @staticmethod
    def post(url, data=None, json=None, headers=None, timeout=10):
        """
        发送 POST 请求

        :param url: 请求的 URL
        :param data: 表单数据（字典）
        :param json: JSON 数据（字典）
        :param headers: 请求头（字典）
        :param timeout: 超时时间（秒）
        :return: 响应内容（JSON 格式）
        """
        try:
            response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()  # 返回 JSON 格式的内容
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")
        return None

# 示例用法
if __name__ == "__main__":
    # GET 请求示例
    url_get = "https://jsonplaceholder.typicode.com/posts/1"
    response_get = HttpUtils.get(url_get)
    print("GET Response:", response_get)

    # POST 请求示例
    url_post = "https://jsonplaceholder.typicode.com/posts"
    data_post = {
        "title": 'foo',
        "body": 'bar',
        "userId": 1
    }
    response_post = HttpUtils.post(url_post, json=data_post)
    print("POST Response:", response_post)
