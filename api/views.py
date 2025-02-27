from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Notice, Attendance
from .serializers import NoticeSerializer, AttendanceSerializer, UserSerializer
from rest_framework.authtoken.models import Token


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Notice ViewSet with Delete and Visibility Toggle
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer

    def create(self, request, *args, **kwargs):
        """ Limit max visible notices to 4 """
        if request.data.get('visible'):
            visible_notices = Notice.objects.filter(visible=True).count()
            if visible_notices >= 4:
                return Response({"error": "Only 4 notices can be visible at a time."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """ Enforce max 4 visible notices when updating """
        instance = self.get_object()
        if request.data.get('visible') and not instance.visible:
            visible_notices = Notice.objects.filter(visible=True).count()
            if visible_notices >= 4:
                return Response({"error": "Only 4 notices can be visible at a time."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Delete a notice """
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Notice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def toggle_visibility(self, request, pk=None):
        """ Show/Hide a notice """
        instance = self.get_object()
        instance.visible = not instance.visible
        instance.save()
        return Response({"message": f"Notice visibility set to {instance.visible}"}, status=status.HTTP_200_OK)

# Attendance ViewSet with Delete
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by('-uploaded_at')
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        """ Handle Excel file upload and process data """
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'file': file})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """ Delete attendance record """
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Attendance record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
