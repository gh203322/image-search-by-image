# -*- coding: UTF-8 -*-

import uvicorn
import api
import init
import setting as ST
import utils as UT
import feature as FT

app = api.app

# 主入口
if __name__ == '__main__':
    # 初始化图库和导入增量图片
    init.run()
    uvicorn.run("main:app", host="0.0.0.0", port=ST.API_PORT, reload=True)