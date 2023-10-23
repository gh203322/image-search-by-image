# -*- coding: UTF-8 -*-

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
import base64
import setting as ST
import milvus as MV
import feature as FT
import utils as UT

app = FastAPI()


"""
restful成功返回
参数：
    data：    json数据
"""
def sucess(data,msg):
    # 返回json数据的方法
    if not msg:
        msg = "请求成功"
    data = {
        "msg": msg,
        "code":200,
        "data":data
    }
    return JSONResponse(data)


"""
restful失败返回
参数：
    msg：    失败信息
"""
def fail(msg):
    # 返回json数据的方法
    if len(msg) == 0:
        msg = "请求失败"

    data = {
        "msg": msg,
        "code":500,
        "data":""
    }
    return JSONResponse(data)


#********************************************图像处理 Api 清单**********************************************#

# 请求参数接收类，继承自 BaseModel 的类
class UploadModel(BaseModel):
    key: Optional[str] = None
    imgPath: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None

# 请求参数接收类，继承自 BaseModel 的类
class SearchModel(BaseModel):
    url: Optional[str] = None
    path: Optional[str] = None
    base64: Optional[str] = None
    limit: Optional[int] = None

# 操作参数接收类，继承自 BaseModel 的类
class OperateModel(BaseModel):
    id: Optional[str] = None


"""
相似图库新增图片-通过文件流
参数：
    file：   图片的文件流
"""
@app.post("/api/image/sim/add/file")
async def img_add_with_file(file: UploadFile = File(...), key: str = Form(None), imgPath: str = Form(None)):

    # 检查文件扩展名以确保它是图像文件
    if not file.filename.lower().endswith(tuple(ST.IMAGE_SUFFIXS)):
        return fail("错误！只支持以下格式的图像："+",".join(ST.IMAGE_SUFFIXS))

    # 获取图片特征向量
    file_bytes = await file.read()
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口存储图片
    if np_embedding is not None and np_embedding.size > 0:
        datas = []
        if not key:
            key = UT.calculate_md5(file_bytes)
        data = MV.create_a_data(key, imgPath, np_embedding.flatten())
        datas.append(data)
        # 插入数据
        insert_res = MV.insert_data(MV.EB_TB_NAME, datas)
        if insert_res:
            return sucess(insert_res,'存储图片成功！')
    return fail('存储图片失败！')


"""
相似图库新增图片-通过url
参数：
    url：   图片的url
"""
@app.post("/api/image/sim/add/url")
def img_add_with_url(params: UploadModel):
    # 检查文件扩展名以确保它是图像文件
    if not UT.get_file_name_with_suffix(params.url).lower().endswith(tuple(ST.IMAGE_SUFFIXS)):
        return fail("错误！只支持以下格式的图像：" + ",".join(ST.IMAGE_SUFFIXS))

    # 获取图片特征向量
    file_bytes = UT.get_bytes_from_url(params.url)
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口存储图片
    if np_embedding is not None and np_embedding.size > 0:
        datas = []
        if not params.key:
            key = UT.calculate_md5(file_bytes)
        data = MV.create_a_data(params.key, params.imgPath, np_embedding.flatten())
        datas.append(data)
        # 插入数据
        insert_res = MV.insert_data(MV.EB_TB_NAME, datas)
        if insert_res:
            return sucess(insert_res, '存储图片成功！')
    return fail('存储图片失败！')


"""
相似图库新增图片-通过文件路径
参数：
    path：   图片的路径
"""
@app.post("/api/image/sim/add/path")
def img_add_with_path(params: UploadModel):
    # 检查文件扩展名以确保它是图像文件
    if not UT.get_file_name_with_suffix(params.path).lower().endswith(tuple(ST.IMAGE_SUFFIXS)):
        return fail("错误！只支持以下格式的图像：" + ",".join(ST.IMAGE_SUFFIXS))

    # 获取图片特征向量
    file_bytes = UT.get_bytes_from_path(params.path)
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口存储图片
    if np_embedding is not None and np_embedding.size > 0:
        datas = []
        if not params.key:
            key = UT.calculate_md5(file_bytes)
        data = MV.create_a_data(params.key, params.imgPath, np_embedding.flatten())
        datas.append(data)
        # 插入数据
        insert_res = MV.insert_data(MV.EB_TB_NAME, datas)
        if insert_res:
            return sucess(insert_res, '存储图片成功！')
    return fail('存储图片失败！')


"""
相似图片搜索-通过url
参数：
    url：   图片url链接
    limit:  返回的相似图片数量
"""
@app.post("/api/image/sim/search/url")
def img_search_by_url(params: SearchModel):
    # 检查文件扩展名以确保它是图像文件
    if not UT.get_file_name_with_suffix(params.url).lower().endswith(tuple(ST.IMAGE_SUFFIXS)):
        return fail("错误！只支持以下格式的图像：" + ",".join(ST.IMAGE_SUFFIXS))

    # 获取图片特征向量
    file_bytes = UT.get_bytes_from_url(params.url)
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口检索相似图片
    if not params.limit:
        limit = ST.IMAGE_SEARCH_LIMIT
    if np_embedding is not None and np_embedding.size > 0:
        search_res = MV.search_similar_vectors(MV.EB_TB_NAME, np_embedding.flatten(), params.limit)
        if search_res is not None:
            return sucess(search_res, '检索图片成功！')
    return fail('检索图片失败！')


"""
相似图片搜索-通过文件路径
参数：
    path：   图片文件路径（同一台机器的绝对路径）
    limit:  返回的相似图片数量
"""
@app.post("/api/image/sim/search/path")
def img_search_by_path(params: SearchModel):
    # 检查文件扩展名以确保它是图像文件
    if not UT.get_file_name_with_suffix(params.path).lower().endswith(tuple(ST.IMAGE_SUFFIXS)):
        return fail("错误！只支持以下格式的图像：" + ",".join(ST.IMAGE_SUFFIXS))

    # 获取图片特征向量
    file_bytes = UT.get_bytes_from_path(params.path)
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口检索相似图片
    if not params.limit:
        limit = ST.IMAGE_SEARCH_LIMIT
    if np_embedding is not None and np_embedding.size > 0:
        search_res = MV.search_similar_vectors(MV.EB_TB_NAME, np_embedding.flatten(), params.limit)
        if search_res is not None:
            return sucess(search_res, '检索图片成功！')
    return fail('检索图片失败！')


"""
相似图片搜索-通过url
参数：
    base64：   图片的base64数据
    limit:  返回的相似图片数量
"""
@app.post("/api/image/sim/search/base64")
def img_search_by_base64(params: SearchModel):

    # 检查是否包含前缀
    if params.base64 and params.base64.startswith("data:image"):
        # 去除前缀
        params.base64 = params.base64.split(",", 1)[1]

    # 解码Base64字符串并获取字节数组
    file_bytes = base64.b64decode(params.base64)
    # 获取图片特征向量
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口检索相似图片
    if not params.limit:
        limit = ST.IMAGE_SEARCH_LIMIT
    if np_embedding is not None and np_embedding.size > 0:
        search_res = MV.search_similar_vectors(MV.EB_TB_NAME, np_embedding.flatten(), params.limit)
        if search_res is not None:
            return sucess(search_res, '检索图片成功！')
    return fail('检索图片失败！')


"""
相似图片搜索-通过文件流
参数：
    file：   图片的文件流
    limit:  返回的相似图片数量
"""
@app.post("/api/image/sim/search/file")
async def img_search_by_file(file: UploadFile = File(...), limit: int = Form(None)):
    # 检查文件扩展名以确保它是图像文件
    if not file.filename.lower().endswith(tuple(ST.IMAGE_SUFFIXS)):
        return fail("错误！只支持以下格式的图像：" + ",".join(ST.IMAGE_SUFFIXS))

    # 获取图片特征向量
    file_bytes = await file.read()
    np_embedding = FT.get_img_embedding(file_bytes)

    # 调用接口检索相似图片
    if not limit:
        limit = ST.IMAGE_SEARCH_LIMIT
    if np_embedding is not None and np_embedding.size > 0:
        search_res = MV.search_similar_vectors(MV.EB_TB_NAME,np_embedding.flatten(),limit)
        if search_res is not None:
            return sucess(search_res, '检索图片成功！')
    return fail('检索图片失败！')


"""
删除图片-通过图片id
参数：
    id：   图数据库ID，多个用逗号分隔
"""
@app.post("/api/image/sim/del")
def img_search_del(params: OperateModel):
    # 检查文件扩展名以确保它是图像文件
    if not params.id:
        return fail("错误！主键不能为空")

    # 删除数据
    delete_count = MV.delete_batch(MV.EB_TB_NAME,UT.split_comma_separated_string(params.id))
    if delete_count>0:
        return sucess(delete_count,'删除图片成功！')
    return fail('删除图片失败！')


#********************************************图像处理 Api 清单**********************************************#
