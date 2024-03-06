from django.test import RequestFactory, TestCase
from django.urls import reverse

from ecgs.views import get_predict


class ECGDetectionTest(TestCase):
    """
    Интеграция с сервисом детекции.
    """
    def setUp(self):
        self.ecg_name = "scan1.jpg"

    def test_get_predict(self):
        url = reverse("predict", kwargs={"filename": self.ecg_name, })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
