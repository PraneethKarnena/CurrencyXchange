from rest_framework import serializers

from api_service import models


class ProfilePictureSerializer(serializers.ModelSerializer):

    file_url = serializers.ReadOnlyField(source='file.url')

    class Meta:
        model = models.PictureModel
        fields = ['file', 'file_url']


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WalletModel
        fields = ['money']