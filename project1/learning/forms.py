from django import forms
from .models import Lesson
from django.utils.text import slugify


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'short_description',
            'html_content',
            'scorm_package',
            'cover_image',
            'video_url',
            'resource_file',
            'eco_points',
            'is_published'
        ]
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'html_content': forms.Textarea(attrs={'rows': 8, 'class': 'form-control monospace'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Engaging lesson title'})
        self.fields['eco_points'].widget.attrs.update({'class': 'form-control', 'min': '0'})
        self.fields['scorm_package'].widget.attrs.update({'class': 'form-control'})
        if 'cover_image' in self.fields:
            self.fields['cover_image'].widget.attrs.update({'class': 'form-control'})
        if 'video_url' in self.fields:
            self.fields['video_url'].widget.attrs.update({'class': 'form-control', 'placeholder': 'https://youtu.be/... or full URL'})
        if 'resource_file' in self.fields:
            self.fields['resource_file'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            base = slugify(instance.title)
            slug = base
            from .models import Lesson
            counter = 2
            while Lesson.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            instance.slug = slug
        if commit:
            instance.save()
        return instance

    def clean_video_url(self):
        url = self.cleaned_data.get('video_url')
        if not url:
            return url
        # Basic YouTube normalization
        import re
        yt_patterns = [
            r'https?://youtu\.be/(?P<id>[A-Za-z0-9_-]{11})',
            r'https?://(www\.)?youtube\.com/watch\?v=(?P<id>[A-Za-z0-9_-]{11})',
            r'https?://(www\.)?youtube\.com/embed/(?P<id>[A-Za-z0-9_-]{11})'
        ]
        for pat in yt_patterns:
            m = re.match(pat, url)
            if m:
                vid = m.group('id')
                return f'https://www.youtube.com/embed/{vid}'
        return url
