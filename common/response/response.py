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

    def __init__(self, msg="error", code=400, status=None, data=None):
        """失败响应默认使用真实 HTTP 状态码，避免业务失败被监控识别成 200。"""

        if status is None:
            status = {
                400: 400,
                401: 401,
                403: 403,
                404: 404,
                409: 409,
                429: 429,
            }.get(code, 400)

        result = {"code": code, "msg": msg, "data": data}

        super().__init__(data=result, status=status)
