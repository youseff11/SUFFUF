from django.core.management.base import BaseCommand
from store.models import Project, ProjectImage

class Command(BaseCommand):
    help = 'Convert all existing JPG/PNG project images to WebP format'

    def handle(self, *args, **options):
        self.stdout.write("جاري بدء ضغط وتحويل الصور القديمة...")
        
        # 1. تحويل صور الأغلفة (Cover Images)
        covers = Project.objects.exclude(cover_image='')
        cover_count = 0
        for project in covers:
            if project.cover_image and not project.cover_image.name.endswith('.webp'):
                self.stdout.write(f"تحويل غلاف المشروع: {project.title}")
                project.save() # دالة save المعدلة ستتولى التحويل تلقائياً
                cover_count += 1

        # 2. تحويل صور المعارض (Gallery Images)
        gallery_images = ProjectImage.objects.exclude(image='')
        gallery_count = 0
        for img_obj in gallery_images:
            if img_obj.image and not img_obj.image.name.endswith('.webp'):
                self.stdout.write(f"تحويل صورة المعرض للمشروع: {img_obj.project.title}")
                img_obj.save() # دالة save المعدلة ستتولى التحويل تلقائياً
                gallery_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"تم بنجاح! تم تحويل {cover_count} صورة غلاف و {gallery_count} صورة معرض إلى صيغة WebP."
            )
        )