import os
from django.db import models
from django_resized import ResizedImageField


class CompanyInfo(models.Model):
    name = models.CharField(max_length=200)
    slogan = models.CharField(max_length=300)
    backstory = models.TextField()
    what_we_do = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    safety_statement = models.TextField()
    quality_policy = models.TextField()
    founded_year = models.IntegerField(default=2017)
    years_experience = models.IntegerField(default=6)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Company Info"

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Emoji fallback icon")
    image_url = models.URLField(max_length=500, blank=True, help_text="External image URL for the service card")
    image = ResizedImageField(
        force_format='WEBP', 
        quality=80, 
        upload_to='services/', 
        blank=True, 
        null=True, 
        help_text="Uploaded image (Auto-converted to WEBP)"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None


class Project(models.Model):
    title = models.CharField(max_length=300)
    client_name = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField()
    description_ar = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    cover_image = ResizedImageField(
        force_format='WEBP', 
        quality=80, 
        upload_to='projects/covers/', 
        blank=True, 
        null=True, 
        help_text="Main cover image (Auto-converted to WEBP)"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def first_image(self):
        if self.cover_image:
            return self.cover_image
        img = self.images.first()
        return img.image if img else None


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(
        force_format='WEBP', 
        quality=80, 
        upload_to='projects/gallery/'
    )
    caption = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} — Image {self.order}"


class Client(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Stat(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.value}"


class SafetyPoint(models.Model):
    text = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:80]


class SuffufMeaning(models.Model):
    letter = models.CharField(max_length=1)
    word = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.letter} - {self.word}"