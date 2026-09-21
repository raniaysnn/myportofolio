from django.forms import DateTimeInput, ModelForm, TextInput, Textarea, URLInput

from main.models import Project, Experience

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "category": "Jenis Proyek",
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
        }

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