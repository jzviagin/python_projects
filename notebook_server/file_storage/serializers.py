from rest_framework import serializers
from file_storage.models import UserOrig, Picture
from django.contrib.auth.models import User



#class UserSerializer(serializers.ModelSerializer):
#    pictures = serializers.PrimaryKeyRelatedField(many=True, queryset=Picture.objects.all())

#    class Meta:
#        model = UserOrig
#        fields = ('email', 'files_directory', 'pictures')


class UserSerializerOld(serializers.ModelSerializer):
    pictures = serializers.PrimaryKeyRelatedField(many=True, queryset=Picture.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'pictures', 'email')


class UserSerializer(serializers.ModelSerializer):
#    pictures = serializers.PrimaryKeyRelatedField(many=True, queryset=Picture.objects.all())

    class Meta:
        model = User
        fields = ()


class PictureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Picture
        fields = ('owner', 'file_name')






