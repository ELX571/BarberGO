from rest_framework import serializers

from accounts.models import Account, VerificationCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'password',

        )


class RegistrationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)
    class Meta:
        model = Account
        fields = (
            'id',
            'avatar',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'password',
            're_password',
        )

    def validate(self, data):
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError('Passwords must be match.')
        return data

    def create(self, validated_data):
        validated_data.pop('re_password')
        password = validated_data.pop('password')
        user=Account.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = Account.objects.get(username=data['username'])
        except Account.DoesNotExist:
            raise serializers.ValidationError('Username or password is incorrect.')

        if not user.check_password(data['password']):
            raise serializers.ValidationError('Username or password is incorrect.')
        data['user'] = user
        return data


class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)


class ForgetPasswordRequestSerializer(serializers.Serializer):
    username = serializers.CharField()


class VerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationCode
        fields = (
            'user',
            'code',
            'expired_at',
        )



