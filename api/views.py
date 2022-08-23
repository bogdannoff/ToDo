from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets, mixins, filters
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.permissions import IsOwner, IsAdminOrReadOnly
from api.serializers import TasksSerializer
from api.throttles import CustomUserRateThrottle
from mainapp.models import Tasks, Projects


class MyPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class TasksModelViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication, JWTAuthentication]
    filter_backends = [IsOwnerFilterBackend]
    pagination_class = MyPagination

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAdminUser],
            url_path='showproject',
            url_name='show-project')
    def project(self, request):
        projects = Projects.objects.all()
        return Response([c.title for c in projects])

    @action(methods=['get'], detail=True)
    def projects(self, request, pk):
        task = Tasks.objects.get(pk=pk)
        return Response({'project': task.project_id})


# class TasksModelViewSet(
#                   mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#
#      queryset = Tasks.objects.all()
#      serializer_class = TasksSerializer
#
#      def get_queryset(self):
#          pk = self.kwargs.get('pk')
#          if pk:
#              return Tasks.objects.filter(pk=pk)
#          else:
#              return Tasks.objects.all()[:5]
#
#      @action(methods=['get'], detail=False)
#      def projects(self, request):
#          projects = Projects.objects.all()
#          return Response([c.title for c in projects])
#
#      @action(methods=['get'], detail=True)
#      def projects(self, request, pk):
#          task = Tasks.objects.get(pk=pk)
#          return Response({'project': task.project_id})



# class TasksListAPIView(generics.ListCreateAPIView):
#     queryset = Tasks.objects.all()
#     serializer_class = TasksSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = [TokenAuthentication, SessionAuthentication, JWTAuthentication]
#     pagination_class = MyPagination
#
#
# class TasksRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tasks.objects.all()
#     serializer_class = TasksSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = [TokenAuthentication, SessionAuthentication, JWTAuthentication]

# class TasksAPIView(APIView):
#
#     def get(self, request):
#         q = Tasks.objects.all()
#         return Response({'tasks': TasksSerializer(q, many=True).data})
#
#     def post(self, request):
#         serializer = TasksSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'task': serializer.data})
#
#     def put(self,request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'pk is required'})
#         try:
#             instance = Tasks.objects.get(pk=pk)
#         except:
#             return Response({'error': 'Object does not exist'})
#         serializer = TasksSerializer(instance=instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'task': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'pk is required'})
#         try:
#             result = Tasks.objects.get(pk=pk).delete()
#         except:
#             return Response({'error': 'Object does not exist'})
#         print(result[1])
#         return Response(result[1])

# class TasksAPIView(generics.ListAPIView):
#     queryset = Tasks.objects.all()
#     serializer_class = TasksSerializer

