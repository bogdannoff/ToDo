from django.urls import path, include, re_path
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'tasks', TasksModelViewSet, 'tasks')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token-auth', views.obtain_auth_token),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    # path('v1/tasks', ModelViewSet.as_view({'get': 'list',
    #                                        'post': 'create'})),
    # path('v1/tasks/<int:pk>/', ModelViewSet.as_view({'get': 'retrieve',
    #                                                  'put': 'update',
    #                                                  'delete': 'destroy'})),
]

# urlpatterns = [
#     path('v1/', include('rest_framework.urls')),
#     path('v1/tasks/', TasksListAPIView.as_view()),
#     path('v1/tasks/<int:pk>/', TasksRetrieveUpdateDestroyAPIView.as_view()),
#     path('v1/auth/', include('djoser.urls')),
#     re_path(r'^v1/auth/', include('djoser.urls.authtoken')),
#     path('v1/jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('v1/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
# ]