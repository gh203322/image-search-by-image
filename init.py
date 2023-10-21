# -*- coding: UTF-8 -*-

import os
import shutil

import setting as ST
import utils as UT
import milvus as MV
import feature as FT


"""
方法：初始化默认目录里面的图片，如果存在则导入向量数据库
参数：
"""
def run():
    # 创建向量数据库
    MV.create_milvus_collection(MV.EB_TB_NAME, MV.EB_DB_DIM)
    # 如果初始化目录有图片则初始化图片
    if ST.IMAGE_INC_PATH:
        incImages= UT.get_files_by_suffix(ST.IMAGE_INC_PATH, ST.IMAGE_SUFFIXS)
        if not incImages:
            try:
                # 构造插入数据集
                datas = []
                for imgPath in incImages:
                    # 初始化的文件使用md5作为key
                    md5 = UT.calculate_md5(imgPath)
                    embedding = FT.get_img_embedding(imgPath)
                    if not embedding:
                        # 降维（因为milvus的向量维度有一个最大值，所以需要将图向量的维度降低到这个极限值之下）
                        # embedding = FT.de_embedding(embedding,1024)
                        data = MV.create_a_data(md5,imgPath,embedding)
                        datas.append(data)
                # 插入数据
                insert_res = MV.insert_data(MV.EB_TB_NAME,datas)
                if insert_res:
                    for imgPath in incImages:
                        # 移动文件
                        try:
                            shutil.move(imgPath, ST.IMAGE_POOL_PATH)
                        except Exception as e:
                            print(f"An error occurred: {str(e)}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")