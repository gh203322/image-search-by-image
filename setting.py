# -*- coding: UTF-8 -*-


import os

# 程序配置
# 应用启动端口
API_PORT  = os.environ.get('API_PORT')
if not API_PORT:
    API_PORT = 7000

# 向量数据库地址（必要配置参数）
MILVUS_HOST  = os.environ.get('MILVUS_HOST')
MILVUS_HOST = '222.85.214.245'
# 向量数据库端口
MILVUS_PORT = os.environ.get('MILVUS_PORT')
if not MILVUS_PORT:
    # MILVUS_PORT = 19530
    MILVUS_PORT = 11088
# 向量数据库用户名
MILVUS_USER  = os.environ.get('MILVUS_USER')
# 向量数据库密码
MILVUS_PASSWORD  = os.environ.get('MILVUS_PASSWORD')
# 向量数据库token
MILVUS_HOST_TOKEN  = os.environ.get('MILVUS_HOST_TOKEN')

# 图片库路径
IMAGE_POOL_PATH = os.environ.get('IMAGE_POOL_PATH')
# 增量图片路径
IMAGE_INC_PATH = os.environ.get('IMAGE_INC_PATH')
# 图片缓存目录
IMAGE_CACHE_PATH = os.environ.get('IMAGE_CACHE_PATH')
if not IMAGE_CACHE_PATH:
    IMAGE_CACHE_PATH = f"image_cache_path"
# 支持搜索的图片的格式
IMAGE_SUFFIXS = ['.jpg','.jpeg','.png','.JPG','.JPEG','.PNG','.gif']
# 图片检索返回的默认相似图片数量
IMAGE_SEARCH_LIMIT = 10
