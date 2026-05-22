class BaseService:

    @staticmethod
    def get_object(model, pk):

        try:
            return model.objects.get(pk=pk)

        except model.DoesNotExist:
            return None