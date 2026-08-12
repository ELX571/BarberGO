from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.jwt_utils import blocklisted, generate_token, verify_token
from accounts.authtications import JwtAuthentication
from accounts.serializers import (
    UserSerializer,
    RegistrationSerializer,
    LoginSerializer,
    RefreshSerializer,
    ForgetPasswordRequestSerializer,

)
from accounts.models import BlocklistedToken, Account, VerificationCode
from accounts.tasks import welcome_email, verification_code


class AuthApiViewSet(viewsets.GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False, url_path='register', serializer_class=RegistrationSerializer)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = generate_token(user)
        if user.email:
            welcome_email.delay(user.email, user.first_name, user.last_name)
        return Response({
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'token_type': 'bearer',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path='login', serializer_class=LoginSerializer)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = generate_token(user)
        return Response({
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'token_type': 'bearer',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='refresh', serializer_class=RefreshSerializer)
    def refresh(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['refresh_token']
        if blocklisted(token):
            return Response({
                'error': 'Token is blocklisted',
            }, status=status.HTTP_401_UNAUTHORIZED)

        payload, error = verify_token(token)

        if error:
            return Response({
                'error': error,
            }, status=status.HTTP_401_UNAUTHORIZED)
        if payload.get('type') != 'refresh':
            return Response({
                'error': 'Notogri token turi',
            }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = Account.objects.get(pk=payload['user_id'])
        except Account.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_404_NOT_FOUND)
        tokens = generate_token(user)
        return Response({
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
        }, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='logout',
        authentication_classes=[JwtAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']
        access_token = request.auth

        payload, error = verify_token(refresh_token)
        if error:
            return Response({
                'error': error,
            }, status=status.HTTP_401_UNAUTHORIZED)
        if payload.get('type') != 'refresh':
            return Response({
                'error': 'Notogri token turi',
            }, status=status.HTTP_401_UNAUTHORIZED)
        if payload.get('user_id') != request.user.id:
            return Response({
                'error': 'Refresh token does not belong to this user',
            }, status=status.HTTP_401_UNAUTHORIZED)

        if access_token:
            BlocklistedToken.objects.get_or_create(token=access_token)
        BlocklistedToken.objects.get_or_create(token=refresh_token)
        return Response({
            'message': 'Successfully logged out',
        }, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='second_register',
        authentication_classes=[JwtAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def second_register(self, request):
        user = request.user
        
        if 'phone' in request.data:
            user.phone_number = request.data['phone']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            
        user.save()
        return Response({'detail': "Profil muvaffaqiyatli saqlandi!"}, status=status.HTTP_200_OK)

class VerificationCodeViewSet(viewsets.GenericViewSet):
    @action(
        methods=['post'],
        detail=False,
        url_path='verify_code',
        serializer_class=ForgetPasswordRequestSerializer,
    )
    def verify_code(self, request):
        serializer = ForgetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        verification = VerificationCode.objects.create(user=user)
        verification_code.delay(
            verification.code,
            user.username,
            user.email,
        )

        return Response(
            {'success': 'code yaratildi va jonatildi'},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['post'],
        detail=False,
        url_path='restore_password',
    )
    def restore_password(self, request):
        code = request.data['code']
        new_password= request.data['password']
        re_password= request.data['re_password']

        if new_password != re_password:
            return Response({'error':'Parollar mos emas'})

        try:
            code_obj = VerificationCode.objects.get(code=code)
        except VerificationCode.DoesNotExist:
            return Response(
                {'error': 'Code notogri tekshirib qaytadan kiriting'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not code_obj.is_valid():
            return Response(
                {'message': 'Codeni mudati otgan qaytadan sorang'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = code_obj.user
        user.set_password(new_password)
        user.save()
        code_obj.delete()

        return Response(
            {'success': 'Parol muvofaqiyatli tasdiqlandi'},
            status=status.HTTP_200_OK,
        )
