from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CompanyInfo, Service, Project, ProjectImage,
    Client, Stat, SafetyPoint, SuffufMeaning,
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'founded_year']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'order']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'icon', 'order')
        }),
        ('Service Image', {
            'fields': ('image', 'image_url', 'image_preview_large'),
            'description': 'Upload a local image OR paste an external URL. Local image takes priority.',
        }),
    )
    readonly_fields = ['image_preview_large']

    def image_preview(self, obj):
        src = obj.display_image
        if src:
            return format_html(
                '<img src="{}" style="height:40px; width:70px; object-fit:cover; '
                'border-radius:4px; border:1px solid #ddd;" />',
                src,
            )
        return format_html('<span style="font-size:1.4rem;">{}</span>', obj.icon)
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        src = obj.display_image
        if src:
            return format_html(
                '<img src="{}" style="max-height:200px; border-radius:8px; '
                'border:1px solid #ddd;" />',
                src,
            )
        return format_html('<span style="color:#aaa;">No image set — emoji "{}" will be used as fallback</span>', obj.icon)
    image_preview_large.short_description = 'Preview'


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'thumbnail_preview', 'caption', 'order']
    readonly_fields = ['thumbnail_preview']
    ordering = ['order']

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px; width:120px; object-fit:cover; '
                'border-radius:6px; border:1px solid #ddd;" />',
                obj.image.url,
            )
        return format_html(
            '<span style="color:#aaa; font-size:12px;">No image yet</span>'
        )
    thumbnail_preview.short_description = 'Preview'


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class ProjectAdminForm(forms.ModelForm):
    bulk_images = MultipleFileField(
        required=False,
        label="رفع صور متعددة دفعة واحدة",
        help_text="يمكنك تحديد عدة صور معاً من جهازك باختيارها دفعة واحدة ليتم إضافتها تلقائياً لمعرض الصور."
    )

    class Meta:
        model = Project
        fields = '__all__'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ['title', 'client_name', 'service', 'is_featured', 'cover_preview', 'image_count']
    list_filter = ['service', 'is_featured', 'client_name']
    search_fields = ['title', 'client_name', 'description', 'description_ar']
    list_editable = ['is_featured']
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'client_name', 'service', 'description', 'description_ar', 'location')
        }),
        ('Display', {
            'fields': ('cover_image', 'cover_image_preview', 'is_featured', 'order'),
        }),
        ('رفع صور المعرض بالدفعة (Multiple Upload)', {
            'fields': ('bulk_images',),
        }),
    )
    readonly_fields = ['cover_image_preview']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        images = request.FILES.getlist('bulk_images')
        current_order = obj.images.count()
        for img in images:
            current_order += 1
            ProjectImage.objects.create(
                project=obj,
                image=img,
                order=current_order
            )

    def cover_preview(self, obj):
        img = obj.first_image
        if img:
            return format_html(
                '<img src="{}" style="height:45px; width:70px; object-fit:cover; '
                'border-radius:4px; border:1px solid #ddd;" />',
                img.url,
            )
        return format_html(
            '<span style="color:#ccc; font-size:18px;">📷</span>'
        )
    cover_preview.short_description = 'Cover'

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height:200px; border-radius:8px; '
                'border:1px solid #ddd;" />',
                obj.cover_image.url,
            )
        return format_html(
            '<span style="color:#aaa;">No cover image uploaded</span>'
        )
    cover_image_preview.short_description = 'Cover Preview'

    def image_count(self, obj):
        count = obj.images.count()
        if count == 0:
            return format_html('<span style="color:#ccc;">0</span>')
        return format_html(
            '<span style="background:#0f3d5c; color:#fff; padding:2px 10px; '
            'border-radius:12px; font-size:12px;">{}</span>',
            count,
        )
    image_count.short_description = 'Gallery'


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'thumbnail_preview', 'caption', 'order']
    list_filter = ['project__service', 'project']
    search_fields = ['project__title', 'caption']

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; width:80px; object-fit:cover; '
                'border-radius:4px; border:1px solid #ddd;" />',
                obj.image.url,
            )
        return '—'
    thumbnail_preview.short_description = 'Preview'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value']


@admin.register(SafetyPoint)
class SafetyPointAdmin(admin.ModelAdmin):
    list_display = ['text', 'order']


@admin.register(SuffufMeaning)
class SuffufMeaningAdmin(admin.ModelAdmin):
    list_display = ['letter', 'word', 'order']