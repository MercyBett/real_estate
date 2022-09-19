from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import House
from .serializers import HouseSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery


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

        county = data['county']
        location = data['location']
        description = data['description']
        price = data['price']
        try:
            price = int(price)
        except:
            return -1
        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)
        except:
            return -2
        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)
        except:
            return -3
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

        data = {

            'title': title,
            'slug': slug,
            'county': county,
            'location ': location,
            'description': description,
            'price ': price,
            'bedrooms ': bedrooms,
            'bathrooms ': bathrooms,
            'home_type ': home_type,
            'sale_type ': sale_type,
            'main_photo': main_photo,
            'photo_2 ': photo_2,
            'photo_3': photo_3,
            'photo_4': photo_4,
            'is_published': is_published

        }
        return data

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions to create a house listing'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data
            data = self.get_values(data)

            if data == -1:
                return Response(
                    {'error': 'price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -2:
                return Response(
                    {'error': 'bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -3:
                return Response(
                    {'error': 'bathrooms must be a decimal number'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            county = data['county']
            location = data['location']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            home_type = data['home_type']
            sale_type = data['sale_type']
            main_photo = data['main_photo']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            photo_4 = data['photo_4']
            is_published = data['is_published']
            if House.objects.filter(slug=slug).exists():
                return Response(
                    {'error': 'House with this slug already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
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

    def put(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error': 'User does not have permission to update house details'},
                                status=status.HTTP_403_FORBIDDEN)

            data = request.data
            data = self.get_values(data)

            if data == -1:
                return Response(
                    {'error': 'price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -2:
                return Response(
                    {'error': 'bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -3:
                return Response(
                    {'error': 'bathrooms must be a decimal number'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            county = data['county']
            location = data['location']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms']
            home_type = data['home_type']
            sale_type = data['sale_type']
            main_photo = data['main_photo']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            photo_4 = data['photo_4']
            is_published = data['is_published']

            if not House.objects.filter(realtor=user.email, slug=slug).update():
                return Response({'error': 'House does not exist'}, status=status.HTTP_404_NOT_FOUND)

            House.objects.filter(realtor=user.email, slug=slug).update(
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
                {'success': 'House updated successfully'},
                status=status.HTTP_200_OK
            )
        except:
            return Response({'error': 'something went wrong when trying to update house details'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response(
                    {'error': 'user does not have necessary permissions to create a house listing'},
                    status=status.HTTP_403_FORBIDDEN
                )
            data = request.data
            slug = data['slug']
            is_published = data['is_published']
            if is_published == 'True':
                is_published = True
            else:
                is_published = False

            if not House.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'error': 'House does not exist'}, status=status.HTTP_404_NOT_FOUND)
            House.objects.filter(realtor=user.email, slug=slug).update(
                is_published=is_published
            )
            return Response({'success': 'House published status updated successfully '}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'something went wrong when trying to update house details'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error': 'User does not have permission to delete this house'},
                                status=status.HTTP_403_FORBIDDEN)
            data = request.data
            slug = data['slug']
            if not House.objects.filter(realtor=user.email, slug=slug).exists():
                return Response({'error': 'The House you are trying to delete does not exist'}, status=status.HTTP_404_NOT_FOUND)
            House.objects.filter(realtor=user.email, slug=slug).delete()
            if not House.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Failed to delete the House'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'something went wrong when trying to delete the house'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HouseDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')
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


class SearchHouseView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, form=None):
      try:
        county = request.query_params.get('county')
        location = request.query_params.get('location')
        description = request.query_params.get('description')
        max_price = request.query_params.get('max_price')
        try:
          price = int(price)
        except Exception:
          return Response(
              {'error': 'price must be an integer'},
              status=status.HTTP_400_BAD_REQUEST
          )
        bedrooms = request.query_params.get('bedrooms')
        try:
          bedrooms = int(bedrooms)
        except Exception:
          return Response(
              {'error': 'bedrooms must be an integer'},
              status=status.HTTP_400_BAD_REQUEST
          )
        bathrooms = request.query_params.get('bathrooms')
        try:
          bathrooms = float(bathrooms)
        except Exception:
          return Response(
              {'error': 'bathrooms must be a decimal value'},
              status=status.HTTP_400_BAD_REQUEST
          )
        if bathrooms <= 0 or bathrooms >= 10:
            bathrooms = 1.0

        bathrooms = round(bathrooms, 1)
        home_type = request.query_params.get('home_type')
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
        sale_type = request.query_params.get('sale_type')
        sale_type = 'For Rent' if sale_type == 'RENT' else 'For Sale'
        search = request.query_params.get('search')
        if not search:
            return Response({'error': 'Missing search criteria'}, status=status.HTTP_400_BAD_REQUEST)

        vector = SearchVector('title', 'location')
        query = SearchQuery(search)

        if not House.objects.annotate(search=vector
                                      ).filter(
            search=query,
            county=county,
            location=location,
            price__lte=max_price,
            bedrooms__gte=bedrooms,
            bathrooms__gte=bathrooms,
            home_type=home_type,
            sale_type=sale_type
        ).exists():
            return Response({'error': 'No house with this search criteria'}, status=status.HTTP_404_NOT_FOUND)

        houses = House.objects.annotate(search=vector
                                        ).filter(
            search=query,
            county=county,
            location=location,
            price__lte=max_price,
            bedrooms__gte=bedrooms,
            bathrooms__gte=bathrooms,
            home_type=home_type,
            sale_type=sale_type)
        houses = HouseSerializer(houses, many=True)
        return Response({'houses': houses.data}, status=status.HTTP_200_OK)

      except Exception:
        return Response({'error': 'something went wrong with the house search'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
