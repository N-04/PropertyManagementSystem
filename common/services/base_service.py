# 文件说明：封装 common/services/base_service.py 对应业务的可复用服务逻辑。

class BaseService:

    @staticmethod
    def get_object(model, pk):

        try:
            return model.objects.get(pk=pk)

        except model.DoesNotExist:
            return None