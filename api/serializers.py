import io

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from api.validators import DateGreaterEqualToday
from mainapp.models import Tasks, Projects


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title']

class TasksSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # project = serializers.StringRelatedField(read_only=True)
    # project = ProjectSerializer()

    class Meta:
        model = Tasks
        fields = ('title', 'description', 'target_date', 'complete', 'project', 'user')
        extra_kwargs = {
            'complete': {'read_only': True},
            'target_date': {'validators': [DateGreaterEqualToday()]}
        }

# class TasksSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(allow_blank=True)
#     target_date = serializers.DateTimeField(required=False)
#     complete = serializers.BooleanField(default=False)
#     project_id = serializers.IntegerField(allow_null=True)
#
#     def create(self, validated_data):
#         return Tasks.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.target_date = validated_data.get('target_date', instance.target_date)
#         instance.complete = validated_data.get('complete', instance.complete)
#         instance.project_id = validated_data.get('project_id', instance.project_id)
#         instance.save()
#         return instance

