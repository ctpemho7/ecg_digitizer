from rest_framework import serializers

from users.models import UserModel, PatientToDocktor


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'status', 'password']


class PatientToDocktorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientToDocktor
        fields = ['doctor', 'patient']
