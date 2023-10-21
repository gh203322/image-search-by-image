import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.autograd import Variable
import cv2
import numpy as np
from sklearn.decomposition import PCA

# 图片缩放大小
IMG_SCALE_SIZE_W = 224
IMG_SCALE_SIZE_H = 224

# 加载特征提取模型
FE_MODEL = models.resnet50(pretrained=True)  # 导入ResNet50的预训练模型


"""
获取图片特征向量
参数：
    file：    可以是文件流或者文件路径
"""
def get_img_embedding(file):

    # 读取图片，转换成与目标图片同一尺寸
    source = None
    if isinstance(file, str):
        source = cv2.imread(file)
    elif isinstance(file, bytes):
        nparr = np.fromstring(file, np.uint8)
        source = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    source = cv2.resize(source, (IMG_SCALE_SIZE_W, IMG_SCALE_SIZE_H))

    FE_MODEL.fc = nn.Linear(2048, 2048)  # 重新定义最后一层
    torch.nn.init.eye(FE_MODEL.fc.weight)  # 将二维tensor初始化为单位矩阵

    for param in FE_MODEL.parameters():
        param.requires_grad = False

    # 将 source 转换为 PyTorch Tensor
    source = torch.from_numpy(source.transpose((2, 0, 1))).unsqueeze(0).float()
    x = Variable(source, requires_grad=False)
    with torch.no_grad():
        y = FE_MODEL(x)
    feature_embedding = y.data.numpy()  # 将提取出来的特征向量转化成 numpy 形式便于后面存储
    print('特征向量维度：',feature_embedding.shape)
    return feature_embedding


"""
向量降维
参数：
    embedding：    输入向量
    n_components:  需要降维的目标值，数值型
"""
def de_embedding(embedding, n_components):
    """
    使用PCA降维将特征向量的维度降到目标维度。

    参数:
        features (numpy.ndarray): 包含特征向量的NumPy数组，每行表示一个特征向量。
        target_dimension (int): 目标维度，将特征向量降维到这个维度。

    返回:
        numpy.ndarray: 降维后的特征向量数组。
    """
    pca = PCA(n_components = n_components)
    reduced_features = pca.fit_transform(embedding)
    return reduced_features