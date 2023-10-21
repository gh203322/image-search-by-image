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

🐳 Docker 镜像地址: `registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.0)`

```shell
docker run -d --gpus all -p 80:8501 registry.cn-beijing.aliyuncs.com/chatchat/chatchat:0.2.0
```

- 该版本镜像大小 `33.9GB`，使用 `v0.2.0`，以 `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04` 为基础镜像
- 该版本内置一个 `embedding` 模型：`m3e-large`，内置 `fastchat+chatglm2-6b-32k`
- 该版本目标为方便一键部署使用，请确保您已经在Linux发行版上安装了NVIDIA驱动程序
- 请注意，您不需要在主机系统上安装CUDA工具包，但需要安装 `NVIDIA Driver` 以及 `NVIDIA Container Toolkit`，请参考[安装指南](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- 首次拉取和启动均需要一定时间，首次启动时请参照下图使用 `docker logs -f <container id>` 查看日志
- 如遇到启动过程卡在 `Waiting..` 步骤，建议使用`docker exec -it <container id> bash` 进入 `/logs/` 目录查看对应阶段日志

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
