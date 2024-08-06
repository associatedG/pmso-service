from rest_framework import serializers
from utils.roles_utils import get_all_roles_names
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "display_name",
            "phone_number",
            "address",
            "role",
            "avatar",
            "created_at",
        ]

    def validate_role(self, value):
        if value not in get_all_roles_names():
            raise serializers.ValidationError("Invalid role name")
        return value
