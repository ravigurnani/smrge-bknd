from email.policy import default
from rest_framework import serializers

from .models import Interest, UserProfile

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        depth = 2
        exclude = ("saved_profiles", "token")
