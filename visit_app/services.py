from django.core.cache import cache

from .models import Visit


def log_to_cache(data):
    log_id = f"log_{data['date'].timestamp()}"
    cache.set(log_id, data, timeout=60 * 60)


def save_log():
    keys = cache.keys("log_*")
    for key in keys:
        try:
            data = cache.get(key)
            if data:
                Visit.objects.create(**data)
                cache.delete(key)
        except Exception as e:
            print(e)



