from rest_framework import serializers

from api_service import models


class ProfilePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PictureModel
        fields = ['file']