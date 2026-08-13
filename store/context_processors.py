from .models import Service

def footer_services(request):
    return {'services_footer': Service.objects.all()[:6]}
