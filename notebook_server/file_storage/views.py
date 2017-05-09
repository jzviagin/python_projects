from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import UserOrig, Picture
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from file_storage.serializers import UserSerializer
from file_storage.serializers import PictureSerializer
from file_storage.permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from file_storage.permissions import IsAuthenticatedOrCreate
from file_storage.permissions import IsOwner
from social.apps.django_app.utils import load_strategy
from social.apps.django_app.utils import load_backend
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.exceptions import AuthAlreadyAssociated
from django.contrib.auth import login
from rest_framework.parsers import FileUploadParser
from file_storage.models import Picture
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files import File
import sys
import os, glob
from django.core.files.base import ContentFile

from social.apps.django_app.utils import psa


#class JSONResponse(HttpResponse):

#    def __init__(self, data, **kwargs):
#        content = JSONRenderer().render(data)
#        kwargs['content_type'] = 'application/json'
#        super(JSONResponse, self).__init__(content, **kwargs)


class UserListOld(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        users = UserOrig.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListOls2(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = UserOrig.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetailOld2(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = UserOrig.objects.all()
    lookup_field = 'email'
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserDetailOld(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return UserOrig.objects.get(email=pk)
        except UserOrig.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListOld3(generics.ListCreateAPIView):
    queryset = UserOrig.objects.all()
    serializer_class = UserSerializer


class UserDetailOld3(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserOrig.objects.all()
    lookup_field = 'email'
    serializer_class = UserSerializer




@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        users = UserOrig.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'data': serializer.data, 'format': format})

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = UserOrig.objects.get(email=pk)
    except UserOrig.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PictureList(generics.ListAPIView):
    #permission_classes = IsOwnerOrAdmin


    def get_queryset(self):
        #renderer_classes = (JSONRenderer,)
        """
        Filter objects so a user only sees his own stuff.
        If user is admin, let him see all.
        """

        #serializer = self.get_serializer(data=request.data)
        #serializer.is_valid(raise_exception=True)

##        provider = self.request.authenticators['provider']

        # If this request was made with an authenticated user, try to associate this social
        # account with it
        #authed_user = request.user if not request.user.is_anonymous() else None

        # `strategy` is a python-social-auth concept referencing the Python framework to
        # be used (Django, Flask, etc.). By passing `request` to `load_strategy`, PSA
        # knows to use the Django strategy
        ##strategy = load_strategy(self.request)
        # Now we get the backend that corresponds to our user's social auth provider
        # e.g., Facebook, Twitter, etc.
       ## backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)

      ##  if isinstance(backend, BaseOAuth1):
            # Twitter, for example, uses OAuth1 and requires that you also pass
            # an `oauth_token_secret` with your authentication request
       ##     token = {
        #        'oauth_token': self.request.authenticators['access_token'],
        #        'oauth_token_secret': self.request['access_token_secret'],
        #    }
        #elif isinstance(backend, BaseOAuth2):
            # We're using oauth's implicit grant type (usually used for web and mobile
            # applications), so all we have to pass here is an access_token
         #   token = self.request.authenticators['access_token']

        #try:
            # if `authed_user` is None, python-social-auth will make a new user,
            # else this social account will be associated with the user you pass in
          #  user = backend.do_auth(token)
        #except AuthAlreadyAssociated:
            # You can't associate a social account with more than user
         #   return Response({"errors": "That social media account is already in use"},
          #                  status=status.HTTP_400_BAD_REQUEST)

        #if user and user.is_active:
         #   return Picture.objects.filter(user)
            # if the access token was set to an empty string, then save the access token
            # from the request
            #auth_created = user.social_auth.get(provider=provider)
            #if not auth_created.extra_data['access_token']:
                # Facebook for example will return the access_token in its response to you.
                # This access_token is then saved for your future use. However, others
                # e.g., Instagram do not respond with the access_token that you just
                # provided. We save it here so it can be used to make subsequent calls.
                #auth_created.extra_data['access_token'] = token
                #auth_created.save()

            # Set instance since we are not calling `serializer.save()`
            #serializer.instance = user
            #headers = self.get_success_headers(serializer.data)
            #return Response(serializer.data, status=status.HTTP_201_CREATED,
             #               headers=headers)
        #else:
            #return Response({"errors": "Error with social authentication"},
            #                status=status.HTTP_400_BAD_REQUEST)
        if self.request.user.is_staff:
            return Picture.objects.all()
        else:
           # return Picture.objects.all()
            return Picture.objects.filter(owner=self.request.user)
    serializer_class = PictureSerializer




class SocialSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # This permission is nothing special, see part 2 of this series to see its entirety
    permission_classes = (IsAuthenticatedOrCreate,)

    def create(self, request, *args, **kwargs):
        """
        Override `create` instead of `perform_create` to access request
        request is necessary for `load_strategy`
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = request.data['provider']

        # If this request was made with an authenticated user, try to associate this social
        # account with it
        #authed_user = request.user if not request.user.is_anonymous() else None
        authed_user = None

        # `strategy` is a python-social-auth concept referencing the Python framework to
        # be used (Django, Flask, etc.). By passing `request` to `load_strategy`, PSA
        # knows to use the Django strategy
        strategy = load_strategy(request)
        # Now we get the backend that corresponds to our user's social auth provider
        # e.g., Facebook, Twitter, etc.
        backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)

        if isinstance(backend, BaseOAuth1):
            # Twitter, for example, uses OAuth1 and requires that you also pass
            # an `oauth_token_secret` with your authentication request
            token = {
                'oauth_token': request.data['access_token'],
                'oauth_token_secret': request.data['access_token_secret'],
            }
        elif isinstance(backend, BaseOAuth2):
            # We're using oauth's implicit grant type (usually used for web and mobile
            # applications), so all we have to pass here is an access_token
            token = request.data['access_token']

        try:
            # if `authed_user` is None, python-social-auth will make a new user,
            # else this social account will be associated with the user you pass in
            user = backend.do_auth(token, user=authed_user)
        except AuthAlreadyAssociated:
            # You can't associate a social account with more than user
            return Response({"errors": "That social media account is already in use"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            # if the access token was set to an empty string, then save the access token
            # from the request
            auth_created = user.social_auth.get(provider=provider)
            if not auth_created.extra_data['access_token']:
                # Facebook for example will return the access_token in its response to you.
                # This access_token is then saved for your future use. However, others
                # e.g., Instagram do not respond with the access_token that you just
                # provided. We save it here so it can be used to make subsequent calls.
                auth_created.extra_data['access_token'] = token
                auth_created.save()

            # Set instance since we are not calling `serializer.save()`
            serializer.instance = user
            headers = self.get_success_headers(serializer.data)
#            return login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response({"errors": "Error with social authentication"},
                            status=status.HTTP_400_BAD_REQUEST)




# Define an URL entry to point to this view, call it passing the
# access_token parameter like ?access_token=<token>. The URL entry must
# contain the backend, like this:
#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$',
#       'register_by_access_token')

@psa('social:complete')
def register_by_access_token(request):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    token = request.POST.get('access_token')
    user = request.backend.do_auth(request.POST.get('access_token'))
    if user:
        login(request, user)
        return 'OK'
    else:
        return 'ERROR'


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.FILES['file']
        picture = Picture.objects.create()
        picture.file_name = file_obj
        #picture.owner = request.
        # do some stuff with uploaded file
        return Response(status=204)

@api_view(['PUT'])
def upload_picture(request):
    if request.method == 'PUT':
        user = request.user
        username = user.username
        file_obj = request.FILES['file']
        picture = Picture()
        picture.owner = user
        picture.file_name = file_obj.name
        picture.save()
        default_storage.save(os.path.join( username + '/' , picture.file_name), ContentFile(file_obj.read()))
        serializer = PictureSerializer(picture)
        return Response(serializer.data)

@api_view(['GET'])
def download_picture(request, filename):
    if request.method == 'GET':
        user = request.user
        username = user.username
        path = os.path.join(username + '/' , filename)
        if os.path.exists(path):
            with open(path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
                return response
        else:
            raise Http404





