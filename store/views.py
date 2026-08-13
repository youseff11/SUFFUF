from django.shortcuts import render, get_object_or_404
from .models import CompanyInfo, Service, Project, Client, Stat, SafetyPoint, SuffufMeaning


def home(request):
    context = {
        'company': CompanyInfo.objects.first(),
        'services': Service.objects.all(),
        'featured_projects': Project.objects.filter(is_featured=True).prefetch_related('images').select_related('service')[:6],
        'clients': Client.objects.all(),
        'stats': Stat.objects.all(),
        'meanings': SuffufMeaning.objects.all(),
    }
    return render(request, 'home.html', context)


def about(request):
    context = {
        'company': CompanyInfo.objects.first(),
        'safety_points': SafetyPoint.objects.all(),
        'meanings': SuffufMeaning.objects.all(),
        'stats': Stat.objects.all(),
    }
    return render(request, 'about.html', context)


def services(request):
    context = {
        'company': CompanyInfo.objects.first(),
        'services': Service.objects.prefetch_related('projects__images').all(),
    }
    return render(request, 'services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    context = {
        'company': CompanyInfo.objects.first(),
        'service': service,
        'projects': service.projects.prefetch_related('images').all(),
    }
    return render(request, 'service_detail.html', context)


def projects(request):
    service_filter = request.GET.get('service', '')
    all_projects = Project.objects.select_related('service').prefetch_related('images').all()
    if service_filter:
        all_projects = all_projects.filter(service__slug=service_filter)
    context = {
        'company': CompanyInfo.objects.first(),
        'projects': all_projects,
        'services': Service.objects.all(),
        'current_filter': service_filter,
    }
    return render(request, 'projects.html', context)


def contact(request):
    context = {
        'company': CompanyInfo.objects.first(),
    }
    return render(request, 'contact.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project.objects.select_related('service').prefetch_related('images'), pk=pk)
    related_projects = Project.objects.filter(service=project.service).exclude(pk=project.pk)[:3]
    
    context = {
        'company': CompanyInfo.objects.first(),
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)