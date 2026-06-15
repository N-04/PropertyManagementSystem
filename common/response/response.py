# 文件说明：封装统一接口响应格式。

# 导入 DRF Response
from rest_framework.response import Response


# 成功响应
class ResponseSuccess(Response):

    def __init__(self, data=None, msg="success", code=200, status=200):

        result = {"code": code, "msg": msg, "data": data}

        super().__init__(data=result, status=status)


# 失败响应
class ResponseError(Response):

    def __init__(self, msg="error", code=500, status=200, data=None):

        result = {"code": code, "msg": msg, "data": data}

        super().__init__(data=result, status=status)
