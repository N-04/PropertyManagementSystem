from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.repairs.models import Repair
from rest_framework.response import Response
from apps.repairs.serializers import RepairSerializer
from common.response.response import success_response

class RepairCreateView(APIView):

    def post(self, request):

        data = request.data.copy()

        data['user'] = request.user.id

        serializer = RepairSerializer(data=data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)

class RepairListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        repairs = Repair.objects.filter(
            user = request.user
        ).order_by('-id')

        serializer = RepairSerializer(
            repairs,
            many = True
        )

        return success_response(
            data = serializer.data
        )

class RepairStatusView(APIView):

    def put(self, request, pk):

        repair = Repair.objects.get(id=pk)

        repair.status = request.data.get('status')

        repair.save()

        return Response({
            'msg': '修改成功'
        })