from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data

            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            password2 = data['password2']
            is_realtor = data['is_realtor']

            if password == password2:
                if len(password) >= 8:
                    if not User.ojects.filter(email=email).exists():
                        if is_realtor:
                            User.objects.create_realtor(
                                email=email, name=name, password=password)
                            return Response(
                                {'success': 'Realtor account created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        else:
                            User.objects.create_user(
                                email=email, name=name, password=password)
                            return Response(
                                {'success': 'User created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                    else:
                        return Response(
                            {'error': 'User with this email already exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error': 'Password has to be at least 8 characters long'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Passwords do not match'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if is_realtor == 'True':
                is_realtor = True
            else:
                is_realtor = False

        except:
            return Response(
                {'error': 'Something went wrong when registering the user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
