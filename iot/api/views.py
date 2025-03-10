from django.db.models import Q
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SensorReading
from .serializers import SensorReadingSerializer


class SensorReadingUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = SensorReadingSerializer

    def post(self, request):
        serializer = SensorReadingSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"Successfully saved {len(serializer.data)} readings"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorReadingListView(generics.ListAPIView):
    serializer_class = SensorReadingSerializer

    def get_queryset(self):
        sensor_ids = self.request.query_params.getlist("sensor_id")
        reading_ids = self.request.query_params.getlist("id")
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        limit = int(self.request.query_params.get("limit", 500))

        query = Q()

        if reading_ids:
            query |= Q(id__in=reading_ids)

        if sensor_ids:
            query &= Q(sensor_id__in=sensor_ids)

        if start_time:
            query &= Q(timestamp__gte=start_time)

        if end_time:
            query &= Q(timestamp__lte=end_time)

        readings = SensorReading.objects.filter(query)[:limit]

        serializer = SensorReadingSerializer(readings, many=True)
        return Response(serializer.data)
