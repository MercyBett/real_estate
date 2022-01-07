from django.db import models
from django.db.models.fields import SlugField

# Create your models here


class House(models.Model):
    class HomeType(models.TextChoices):
        APARTMENT = 'Apartment'
        BUNGALOW = 'Bungalow'
        STUDIO = 'Studio'
        TOWNHOUSE = 'Townhouse'
        MAISONETTE = 'Maisonette'

    class SaleType(models.TextChoices):
        RENT = 'For Rent'
        BUY = 'For Sale'

    realtor = models.EmailField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    county = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    home_type = models.CharField(max_length=50,
                                 choices=HomeType.choices, default=HomeType.APARTMENT)
    sale_type = models.CharField(
        max_length=10, choices=SaleType.choices, default=SaleType.BUY)
    main_photo = models.ImageField(upload_to='houses/')
    photo_2 = models.ImageField(upload_to='houses/')
    photo_3 = models.ImageField(upload_to='houses/')
    photo_4 = models.ImageField(upload_to='houses/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def delete(self):
        self.main_photo.storage.delete(self.main_photo.name)
        self.photo_2.storage.delete(self.photo_2.name)
        self.photo_3.storage.delete(self.photo_3.name)
        self.photo_4.storage.delete(self.photo_4.name)
        super().delete()

    def __str__(self):
        return self.title
