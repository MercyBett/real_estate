from .models import House

def remove_realtor_data(realtor_mail):
  if House.objects.filter(realtor=realtor_mail).exists():
    House.objects.filter(realtor=realtor_mail).delete()