import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models


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
    image = models.ImageField(upload_to='services/', blank=True, null=True, help_text="Local uploaded image (takes priority over URL)")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        """Return local image URL, external URL, or None."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None


def convert_to_webp(image_field, quality=80):
    """دالة مساعدة لضغط وتحويل أي صورة إلى صيغة WebP"""
    if not image_field:
        return

    # فتح الصورة باستخدام Pillow
    img = Image.open(image_field)
    
    # تحويل نمط الألوان إلى RGB إذا كانت RGBA لضمان التوافق مع WebP
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    output = BytesIO()
    # حفظ الصورة بصيغة WEBP مع ضبط الجودة (افتراضياً 80%)
    img.save(output, format='WEBP', quality=quality, optimize=True)
    output.seek(0)

    # تغيير امتداد الملف إلى .webp
    filename = os.path.splitext(image_field.name)[0] + '.webp'
    
    # حفظ الملف الجديد في الحقل دون إعادة استدعاء save() لمنع Infinite Loop
    image_field.save(filename, ContentFile(output.read()), save=False)


class Project(models.Model):
    title = models.CharField(max_length=300)
    client_name = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField()
    description_ar = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True, help_text="Main cover image for the project card")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # تحويل غلاف المشروع (Cover) إلى WebP إذا تم رفعه/تعديله
        if self.cover_image and not self.cover_image.name.endswith('.webp'):
            convert_to_webp(self.cover_image)
        super().save(*args, **kwargs)

    @property
    def first_image(self):
        """Return cover_image or the first gallery image as fallback."""
        if self.cover_image:
            return self.cover_image
        img = self.images.first()
        return img.image if img else None


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} — Image {self.order}"

    def save(self, *args, **kwargs):
        # تحويل صورة المعرض إلى WebP تلقائياً عند الحفظ
        if self.image and not self.image.name.endswith('.webp'):
            convert_to_webp(self.image)
        super().save(*args, **kwargs)


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