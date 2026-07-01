# 文件说明：封装统一接口响应格式。

# 导入 DRF Response
from rest_framework.response import Response


# 成功响应分块：业务接口成功时统一返回 code/msg/data。
class ResponseSuccess(Response):
    """项目统一成功响应，默认 HTTP 状态码和业务 code 都是 200。"""

    def __init__(self, data=None, msg="success", code=200, status=200):

        # 前端统一从 data 字段读取业务数据，避免每个页面适配不同结构。
        result = {"code": code, "msg": msg, "data": data}

        super().__init__(data=result, status=status)


# 失败响应分块：业务错误同时暴露 HTTP 状态码和业务 code。
class ResponseError(Response):

    def __init__(self, msg="error", code=400, status=None, data=None):
        """失败响应默认使用真实 HTTP 状态码，避免业务失败被监控识别成 200。"""

        if status is None:
            # 未显式传 status 时，按常见业务 code 映射真实 HTTP 状态码。
            status = {
                400: 400,
                401: 401,
                403: 403,
                404: 404,
                409: 409,
                422: 422,
                429: 429,
                500: 500,
                503: 503,
            }.get(code, 400)

        # data 允许携带字段级错误或额外排查信息，默认保持空。
        result = {"code": code, "msg": msg, "data": data}

        super().__init__(data=result, status=status)
