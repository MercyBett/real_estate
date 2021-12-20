from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import House
from .serializers import HouseSerializer


class ManageHousesView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions to get a house listing'},
                    status=status.HTTP_403_FORBIDDEN
                )
            slug = request.query_params.get('slug')
            if not slug:
                house = House.objects.order_by('-created_at').filter(
                    realtor=user.email
                )
                house = HouseSerializer(house, many=True)
                return Response(
                    {'Houses': house.data},
                    status=status.HTTP_200_OK
                )
            if not House.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'House not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            house = House.objects.get(realtor=user.email, slug=slug)
            house = HouseSerializer(house)
            return Response(
                {'house': house.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'something went wrong when trying to get house details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_values(self, data):
        title = data['title']
        slug = data['slug']
        if House.objects.filter(slug=slug).exists():
            return Response(
                {'error': 'House with this slug already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        county = data['county']
        location = data['location']
        description = data['description']
        price = data['price']
        try:
            price = int(price)
        except:
            return Response(
                {'error': 'price must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)
        except:
            return Response(
                {'error': 'bedrooms must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)
        except:
            return Response(
                {'error': 'bathrooms must be a decimal number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if bathrooms <= 0 or bathrooms >= 10:
            bathrooms = 1.0

        bathrooms = round(bathrooms, 1)
        home_type = data['home_type']
        if home_type == 'APARTMENT':
            home_type = 'Apartment'
        elif home_type == 'BUNGALOW':
            home_type = 'Bungalow'
        elif home_type == 'STUDIO':
            home_type = 'Studio'
        elif home_type == 'TOWNHOUSE':
            home_type = 'Townhouse'
        else:
            home_type = 'Maisonette'
        sale_type = data['sale_type']
        if sale_type == 'RENT':
            sale_type = 'For Rent'
        else:
            sale_type = 'For Sale'
        main_photo = data['main_photo']
        photo_2 = data['photo_2']
        photo_3 = data['photo_3']
        photo_4 = data['photo_4']
        is_published = data['is_published']
        if is_published == 'True':
            is_published = True
        else:
            is_published = False

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions to create a house listing'},
                    status=status.HTTP_403_FORBIDDEN
                )
            data = request.data

            House.objects.create(
                realtor=user.email,
                title=title,
                slug=slug,
                county=county,
                location=location,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                home_type=home_type,
                sale_type=sale_type,
                main_photo=main_photo,
                photo_2=photo_2,
                photo_3=photo_3,
                photo_4=photo_4,
                is_published=is_published
            )
            return Response(
                {'success': 'House created successfully'},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'something went wrong when retrieving houses'},
                status=status.HTTP_400_BAD_REQUEST
            )


class HouseDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = requets.query_params.get('slug')
            if not slug:
                return Response(
                    {'error': 'kindly provide slug'},
                    status=status.HTTP_400_BAD_REQUEST)
            if not House.objects.filter(slug=slug, is_published=True).exists():
                return Response(
                    {'error': 'Published house with this slug is nonexistent'},
                    status=status.HTTP_400_BAD_REQUEST)
            house = House.objects.get(slug=slug, is_published=True)
            house = HouseSerializer(house)
            return Response(
                {'house': house.data},
                status=status.HTTP_200_OK)
        except:
            return Response(
                {'error': 'something went wrong when retrieving house details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HousesView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, formats=None):
        try:
            if not House.objects.filter(is_published=True).exists():
                return Response(
                    {'error': 'No published houses found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            house = House.objects.order_by(
                '-created_at').filter(is_published=True)
            house = HouseSerializer(house)
            return Response(
                {'house': house.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'something went wrong when retrieving houses'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
