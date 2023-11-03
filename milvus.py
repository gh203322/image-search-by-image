# -*- coding: UTF-8 -*-

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

import setting as ST


# 图片向量库名称(表名)
EB_TB_NAME = 'images'
# 图片向量库维度
EB_DB_DIM = 2048 #Milvus 支持的最大向量维度是32768，一般情况为了检索性能建议在1024-2048

# 全局 Milvus 连接对象
connections.connect("default", host=ST.MILVUS_HOST, port=ST.MILVUS_PORT)

"""
创建表
参数：
    collection_name：   表名称
    dim:                向量维度
"""
def create_milvus_collection(table_name, dim):
    try:
        # 检查表是否已经存在
        if not utility.has_collection(collection_name=table_name):
            # 定义字段
            fields = [
                FieldSchema(name='id', dtype=DataType.INT64, descrition='index id', max_length=500, is_primary=True,
                            auto_id=True),
                FieldSchema(name='key', dtype=DataType.VARCHAR, descrition='external system primary key',
                            max_length=64),
                FieldSchema(name='filepath', dtype=DataType.VARCHAR, description='image file path and file name',
                            max_length=512),
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, descrition='image embedding vectors',
                            dim=dim),
            ]

            # 创建表结构
            schema = CollectionSchema(fields=fields, description="image search vector library")
            collection = Collection(name=table_name, schema=schema, using='default', shards_num=2)
            # 给embedding字段创建索引
            index_params = {
                'metric_type': 'L2',
                'index_type': "IVF_FLAT",
                'params': {"nlist": 1024}  # nlist参数可以根据官方4×sqrt(n)计算，n为数据条数，根据实际的数量级来调整
            }
            collection.create_index(field_name="embedding", index_params=index_params)
            # 验证表是否创建成功
            if utility.has_collection(collection_name=table_name):
                print(f"Table '{table_name}' created successfully!")
        else:
            print(f"Table '{table_name}' already exists. Skipping creation.")
        # 关闭连接
        connections.disconnect("default")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


"""
插入数据
参数：
    table_name：   表名称
    data:          数据集合，格式[{'key':,'filepath':,'embedding':}]
"""
def insert_data(table_name, data):
    try:
        # 获取表
        collection = Collection(table_name)

        # 插入数据
        entities = []
        for item in data:
            entity = {
                'key': item['key'],
                'filepath': item['filepath'],
                'embedding': item['embedding']
            }
            entities.append(entity)

        mr = collection.insert(entities)

        # 验证数据是否插入成功
        count = mr.insert_count
        print(f"{count} rows inserted into '{table_name}'")
        if count > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")


"""
搜索数据
参数：
    table_name：   表名称
    dim:           目标向量
    limit:         前n条相似的向量
"""
def search_similar_vectors(table_name, query_vector, limit):
    try:
        # 获取表
        collection = Collection(table_name)
        collection.load()

        search_params = {"metric_type": "L2", "params": {"nprobe": 16}} # nprobe 聚类中心的数量，可根据实际大小调整
        # 在数据库中搜索
        results = collection.search(
            data=[query_vector],
            anns_field='embedding',
            param=search_params,
            output_fields=['id','key','filepath'],
            limit=limit,
            expr=None,
            consistency_level="Strong"
        )
        collection.release()
        res_datas = []
        for item in results[0]:
            res_datas.append(item.entity.to_dict().get('entity'))
        return res_datas
    except Exception as e:
        print(f"An error occurred: {str(e)}")


"""
删除数据（单条）
参数：
    table_name：   表名称
    id:            主键
"""
def delete(table_name, id):
    try:
        exp = 'id = '+id
        # 获取表
        collection = Collection(table_name)
        mr = collection.delete(exp)
        return mr.delete_count
    except Exception as e:
        print(f"An error occurred: {str(e)}")


"""
删除数据（多条）
参数：
    table_name：   表名称
    id:            主键
"""
def delete_by_id_batch(table_name, ids):
    try:
        exp = 'id in ['+','.join(ids)+']'
        # 获取表
        collection = Collection(table_name)
        mr = collection.delete(exp)
        return mr.delete_count
    except Exception as e:
        print(f"An error occurred: {str(e)}")


"""
删除数据（多条）
参数：
    table_name：   表名称
    key:            外部系统唯一标识
"""
def delete_by_key_batch(table_name, keys):
    try:
        exp = 'key in ['+','.join(keys)+']'
        # 获取表
        collection = Collection(table_name)
        mr = collection.delete(exp)
        return mr.delete_count
    except Exception as e:
        print(f"An error occurred: {str(e)}")


"""
构造单条插入数据
参数：
    key：          外部系统主键，可用于外部系统传入
    filepath:      图片路径
    embedding:     图片向量
"""
def create_a_data(key, filepath, embedding):
    try:
        data = {
            'key': key,
            'filepath': filepath,
            'embedding': embedding
        }
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
