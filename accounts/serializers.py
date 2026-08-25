from rest_framework import serializers

from accounts.models import Account, VerificationCode


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

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
            'avatar',
        )

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            try:
                url = obj.avatar.url
                if url.startswith('/media/media/'):
                    url = url.replace('/media/media/', '/media/', 1)
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
            except ValueError:
                pass
        
        default_url = '/media/avatars/default.jpg'
        if request is not None:
            return request.build_absolute_uri(default_url)
        return default_url


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



