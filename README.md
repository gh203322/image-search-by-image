<div style="text-align: center;">
  <p align="center" style="font-size: 32px; font-weight: bold;">🌘 一种基于图向量和向量数据库的图片搜索引擎。</p>
</div>

![](img/logo.png)

--- 

## 介绍

💡 一种利用图片特征向量及向量数据库进行向量相似检索的技术。

📺 实现原理

![实现原理图](img/langchain+chatglm.png)

本项目实现原理如下图所示，过程包括加载图片 -> 读取图片 -> 特征提取 -> 存储到向量数据库 -> 待检索图片 -> 在图片向量库中匹配出与待检索图片向量最相似的 `top k`个 -> 匹配到相似结果 -> 返回结果。

---

##  使用
### Docker 部署 

1、通过已有的基础镜像启动  
🐳 Docker 基础镜像地址: `registry.cn-chengdu.aliyuncs.com/mrrobot_public/bogv-base:1.1`

```docker-compose.yml
version: '3.5'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.2.11
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"

  attu:
    container_name: milvus-attu
    image: zilliz/attu:v2.2.6
    environment:
      MILVUS_URL: milvus-standalone:19530
    ports:
      - "19531:3000"
    depends_on:
      - "standalone"

  # API接口
  bogv:
    container_name: bogv-api
    image: registry.cn-chengdu.aliyuncs.com/mrrobot_public/bogv-base:1.1
    restart: always
    ports:
      - "11090:7000"
    volumes:
      - /etc/localtime:/etc/localtime
      - ./:/app
    environment:
      - TZ=Asia/Shanghai
      - MILVUS_HOST=milvus-standalone
      - MILVUS_PORT=19530
    working_dir: /app  # 设置容器的工作目录
    command: sh -c "python main.py"
    privileged: true

networks:
  default:
    name: milvus
```

2、通过在线下载依赖的方式构建镜像并启动
```docker-compose.yml
version: '3.5'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.2.11
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"

  attu:
    container_name: milvus-attu
    image: zilliz/attu:v2.2.6
    environment:
      MILVUS_URL: milvus-standalone:19530
    ports:
      - "19531:3000"
    depends_on:
      - "standalone"

  # API接口
  bogv:
    container_name: bogv-api
    image: python:3.7
    restart: always
    ports:
      - "7000:7000"
    volumes:
      - /etc/localtime:/etc/localtime
      - ./:/app
    environment:
      - TZ=Asia/Shanghai
      - MILVUS_HOST=milvus-standalone
      - MILVUS_PORT=19530
    working_dir: /app  # 设置容器的工作目录
    command: sh -c "pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt && python main.py"
    privileged: true

networks:
  default:
    name: milvus
```

### API介绍

```python
llm_model_dict={
                "chatglm2-6b": {
                        "local_model_path": "/Users/xxx/Downloads/chatglm2-6b",
                        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
                        "api_key": "EMPTY"
                    },
                }
```

- 请确认已下载至本地的 Embedding 模型本地存储路径写在 `embedding_model_dict` 对应模型位置，如：


```shell
$ streamlit run webui.py
```
