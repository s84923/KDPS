from django.core.management.base import BaseCommand
import requests
import os

API_KEY = os.getenv("API_KEY")

class Command(BaseCommand):
    help = 'Check the status of the Gemini API'

    def handle(self, *args, **kwargs):
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        try:
            response = requests.get("https://api.gemini.com", headers=headers)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("Gemini API is running with valid API key."))
            else:
                self.stdout.write(self.style.WARNING(f"Gemini API returned status code: {response.status_code}"))
        except requests.exceptions.RequestException as e: 
            self.stdout.write(self.style.ERROR(f"Could not connect to Gemini API: {e}"))
