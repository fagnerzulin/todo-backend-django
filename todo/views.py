from django.shortcuts import render
from django.contrib.auth import login

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer


from todo.serializers import TodoSerializer, RegisterSerializer, UserSerializer, ChangeTodoStatusSerializer
from todo.models import Todo

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView


def index(request):
    return render(request, 'index.html')


class TodoView (generics.GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        todo = Todo.objects.filter(user=user)
        todo = TodoSerializer(todo, many=True)

        return Response({'todos': todo.data})

    def post(self, request, *args, **kwargs):
        user = request.user
        values = request.data
        values['user'] = user.pk

        serializer = TodoSerializer(data=values)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()

        return Response({'todo': TodoSerializer(todo, context=self.get_serializer_context()).data})


class ItemTodoView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ChangeTodoStatusSerializer
    model = Todo
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = Todo.objects.filter(id=self.kwargs['pk'], user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if self.object:
            if serializer.is_valid():
                self.object.update(completed=serializer.data.get('completed'))
                return Response({
                    "success": "Todo has been successfully changed",
                })
        else:
            return Response({'error': 'todo not not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object:
            self.object.delete()
            return Response({
                "success": "Todo has been successfully deleted",
            })
        else:
            return Response({'error': 'todo not not found'}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return super(LoginView, self).post(request, format=None)
