import os
import hashlib
import requests
import cv2


# 获取路径下所有的文件
def get_files_by_suffix(path, suffix_list):
    file_list = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext in suffix_list:
                file_path = os.path.join(root, filename)
                file_list.append(file_path)
    return file_list


# 获取文件名
def get_file_name(file_path):
    file_name = ""
    file_name = file_name + os.path.basename(file_path)  # 获取文件名
    name_without_ext = os.path.splitext(file_name)[0]  # 去除文件扩展名
    return name_without_ext


# 获取文件名
def get_file_name_with_suffix(file_path):
    file_name = ""
    file_name = file_name + os.path.basename(file_path)  # 获取文件名
    return file_name


# 获取文件md5
def calculate_md5(obj):
    # 创建一个MD5哈希对象
    md5_hash = hashlib.md5()


    if isinstance(obj, str):
        # 打开文件并逐块更新哈希对象
        with open(obj, "rb") as file:
            while True:
                # 读取文件块
                file_chunk = file.read(4096)  # 4096字节块大小，你可以根据需要调整
                # 如果没有更多数据块，则退出循环
                if not file_chunk:
                    break
                # 更新哈希对象
                md5_hash.update(file_chunk)
    elif isinstance(obj, bytes):
        # 更新哈希对象以计算字节数组的 MD5 哈希值
        md5_hash.update(obj)

    # 返回MD5哈希值的十六进制表示
    return md5_hash.hexdigest()


# 通过url地址获取文件流
def get_bytes_from_url(url):
    try:
        # 发送 HTTP GET 请求以获取图像，同时禁用 SSL 证书验证
        response = requests.get(url, verify=False)

        # 检查响应状态码，确保请求成功
        if response.status_code == 200:
            # 获取图像的字节数据
            image_bytes = response.content
            return image_bytes
        else:
            print(f"HTTP GET request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# 通过文件路径获取文件流
def get_bytes_from_path(path):
    try:
        # 使用OpenCV读取图像文件
        image = cv2.imread(path)

        if image is not None:
            # 从文件路径中获取文件的后缀名
            file_extension = os.path.splitext(path)[1]

            # 将图像转换为字节数组
            _, image_bytes = cv2.imencode(file_extension, image)
            return image_bytes.tobytes()
        else:
            print("Failed to read the image.")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# 将逗号分隔的字符串拆分为数组
def split_comma_separated_string(input_string):
    """
    将逗号分隔的字符串拆分为数组
    :param input_string: 逗号分隔的字符串
    :return: 包含拆分结果的数组
    """
    if not input_string:
        return []  # 如果输入为空字符串，返回空数组

    # 使用逗号作为分隔符拆分字符串
    result = input_string.split(',')

    return result