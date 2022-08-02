from django.apps import AppConfig




class BossraidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bossraid'

    def ready(self):
        """
        장고 서버 시작 시, bossraids 및 상태 데이터
        Redis에 caching
        """
        import requests, os, json

        from django.core.cache import cache
        from dotenv import load_dotenv
        from bossraid.utils.utils import RAIDS_STATUS

        load_dotenv()
        static_data = requests.get(os.environ['STATIC_DATA_URL']).json()
        cache.get_or_set('bossRaids', static_data)
        cache.get_or_set('status', RAIDS_STATUS)