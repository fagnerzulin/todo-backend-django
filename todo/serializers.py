from rest_framework import serializers
from todo.models import Todo
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed', 'user')

    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        completed = validated_data['completed']
        user = validated_data['user']

        todo = Todo.objects.create(title=title, description=description, completed=completed, user=user)
        return todo

    def update(self, instance, validated_data):

        instance.completed = validated_data.get(
            'completed', instance.completed)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],)

        return user
