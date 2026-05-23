# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TrafficData
from .serializers import TrafficDataSerializer
from .algorithms import calculate_signal

from .permissions import (
    IsAdmin,
    IsOperator,
    IsViewer,
    IsAdminOrOperator
)


# ---------------- CREATE ----------------
class TrafficDataView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOperator]

    def post(self, request):

        road_name = request.data.get("road_name")
        vehicle_count = request.data.get("vehicle_count")
        emergency_vehicle = request.data.get("emergency_vehicle", False)

        # ---- VALIDATION ----
        if not road_name:
            return Response({"error": "road_name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if vehicle_count is None:
            return Response({"error": "vehicle_count is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicle_count = int(vehicle_count)
        except:
            return Response({"error": "vehicle_count must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        # ---- BOOLEAN HANDLING ----
        if not isinstance(emergency_vehicle, bool):
            emergency_vehicle = str(emergency_vehicle).lower() in ["true", "1", "yes"]

        # ---- ALGORITHM ----
        result = calculate_signal(vehicle_count, emergency_vehicle)

        # ---- SAVE ----
        traffic = TrafficData.objects.create(
            road_name=road_name,
            vehicle_count=vehicle_count,
            emergency_vehicle=emergency_vehicle,
            signal_status=result["signal"],
            traffic_level=result["traffic_level"],
            green_time=result["green_time"]
        )

        serializer = TrafficDataSerializer(traffic)

        return Response({
            "message": "Traffic data stored successfully",
            "data": serializer.data,
            "traffic_analysis": result
        }, status=status.HTTP_201_CREATED)


# ---------------- READ ----------------
class TrafficDataListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = TrafficData.objects.all().order_by('-created_at')
        serializer = TrafficDataSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------- UPDATE ----------------
class TrafficDataUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOperator]

    def put(self, request, pk):

        try:
            traffic = TrafficData.objects.get(id=pk)
        except TrafficData.DoesNotExist:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

        # ---- SAFE UPDATES ----
        if request.data.get("road_name") is not None:
            traffic.road_name = request.data.get("road_name")

        if request.data.get("vehicle_count") is not None:
            try:
                traffic.vehicle_count = int(request.data.get("vehicle_count"))
            except:
                return Response({"error": "vehicle_count must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("emergency_vehicle") is not None:
            ev = request.data.get("emergency_vehicle")
            if isinstance(ev, bool):
                traffic.emergency_vehicle = ev
            else:
                traffic.emergency_vehicle = str(ev).lower() in ["true", "1", "yes"]

        traffic.save()

        serializer = TrafficDataSerializer(traffic)

        return Response({
            "message": "Data updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# ---------------- DELETE ----------------
class TrafficDataDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk):

        try:
            traffic = TrafficData.objects.get(id=pk)
        except TrafficData.DoesNotExist:
            return Response({"error": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

        traffic.delete()

        return Response({
            "message": "Data deleted successfully"
        }, status=status.HTTP_200_OK)


# ---------------- OVERRIDE ----------------
class ManualOverrideView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):

        signal = request.data.get("signal_status")

        # ---- VALIDATION ----
        if not signal:
            return Response(
                {"error": "signal_status is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        signal = signal.upper()

        if signal not in ["RED", "YELLOW", "GREEN"]:
            return Response(
                {"error": "Invalid signal value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ---- UPDATE LATEST RECORD ----
        try:
            latest = TrafficData.objects.latest('created_at')
        except TrafficData.DoesNotExist:
            return Response(
                {"error": "No traffic data found to override"},
                status=status.HTTP_404_NOT_FOUND
            )

        latest.signal_status = signal
        latest.save()


        return Response({
            "message": "Signal overridden manually",
            "new_signal": signal,
            "updated_id": latest.id
        }, status=status.HTTP_200_OK)