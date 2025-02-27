from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet, AttendanceViewSet, LoginView

router = DefaultRouter()
router.register(r'notices', NoticeViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('notices/<int:pk>/toggle-visibility/', NoticeViewSet.as_view({'post': 'toggle_visibility'}), name='toggle-visibility'),
]
