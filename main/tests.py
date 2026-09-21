from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

class ExperienceDataDeliveryTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Lab",
            description="Membantu kegiatan praktikum.",
            category="organization",
        )

    def test_experience_json_returns_data(self):
        response = self.client.get(reverse("main:get_experiences_json"))
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]["fields"]["title"], "Asisten Lab")

    def test_create_experience(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Panitia Acara",
                "description": "Mengatur acara kampus.",
                "category": "organization",
                "thumbnail": "",
                "ended_at": "",
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(title="Panitia Acara").exists()
        )

    def test_update_experience(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Asisten Laboratorium",
                "description": "Membantu kegiatan praktikum.",
                "category": "organization",
                "thumbnail": "",
                "ended_at": "",
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Laboratorium")

    def test_delete_experience(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(
            Experience.objects.filter(id=self.experience.id).exists()
        )