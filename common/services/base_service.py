# 文件说明：封装 common/services/base_service.py 对应业务的可复用服务逻辑。

class BaseService:
    """公共服务基类，封装跨模块通用的数据访问小工具。"""

    @staticmethod
    def get_object(model, pk):
        """按主键安全查询对象，未找到时返回 None 交给视图层统一响应。"""

        try:
            return model.objects.get(pk=pk)

        except model.DoesNotExist:
            return None
