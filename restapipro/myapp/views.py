from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404, render

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import QuestionSerializer, UserSerializer, RegisterSerializer

from rest_framework.decorators import api_view
from .models import Questions

from rest_framework import serializers
from rest_framework import status


# Class To Register User
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": AuthToken.objects.create(user)[1],
            "status": "Account successfully created",
            "status_code": 201,
            "json_data": {
                "user_id": UserSerializer(user, context=self.get_serializer_context()).data,
                "account_state": "ACTIVE"
            },
        })


# Class To Login the User
class LoginAPI(KnoxLoginView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        temp_list = super(LoginAPI, self).post(request, format=None)
        temp_list.data["status"] = "Login to your Account SuccessFully"
        return Response({"data": temp_list.data})
        # return super(LoginAPI, self).post(request, format=None)


# Method to Create Question
@api_view(['POST'])
def add_question(request):
    ques = QuestionSerializer(data=request.data)

    # validating for already existing data
    if Questions.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if ques.is_valid():
        ques.save()
        return Response(ques.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Method to Get All Question With Particular Tags and Text
@api_view(['GET'])
def getByTagsText(request, tags, text):
    item = Questions.objects.all()
    listAns = []
    for i in item:
        if (tags in i.tags) or (text in i.tags):
            listAns.append(i)

    if listAns:
        data = QuestionSerializer(instance=listAns, many=True)
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Method to Get All Question
@api_view(['GET'])
def getAll(request):

    # checking for the parameters from the URL
    ques = Questions.objects.all()
    data = QuestionSerializer(instance=ques, many=True)
    # print(data)
    # if there is something in items else raise error
    if ques:
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Method to Get All Question With ID
@api_view(['GET'])
def getId(request, pk):
    # checking for the parameters from the URL
    item = Questions.objects.get(pk=pk)
    data = QuestionSerializer(instance=item)

    # if there is something in items else raise error
    if item:
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Method to Update a Question With ID
@api_view(['PUT'])
def update_items(request, pk):
    item = Questions.objects.get(pk=pk)
    data = QuestionSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Method to Delete a Question With ID
@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Questions, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


# Method to Block the User
@api_view(['POST'])
def logout_request(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    if user:
        logout(request)
        temp_list = {}
        temp_list["status"] = "Logout to your Account SuccessFully"
        return Response({"data": temp_list["status"]})
    return Response({"data": "User Does Not Exists"})


################### FRONTEND ###################

def home(req):
    return render(req, 'index.html', {})
