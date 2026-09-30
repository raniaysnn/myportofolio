from django.core.exceptions import ValidationError
from django.forms import DateTimeInput, ModelForm, TextInput, Textarea, URLInput
from django.utils.html import strip_tags

from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "project_image_url"
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "category": "Jenis Proyek",
             "project_image_url": "URL Gambar",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Lomba, Tugas Proyek, Proyek Mandiri",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://... (opsional)"
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_category(self):
        return strip_tags(self.cleaned_data["category"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Posisi atau Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Gambar",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Teaching Assistant",
                "maxlength": 255,
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan pengalamanmu",
                "rows": 4,
            }),
            "thumbnail": URLInput(attrs={
                "placeholder": "https://contoh.com/gambar.jpg",
            }),
            "ended_at": DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }