from django.utils import timezone

def timestamp(request):
    return {
        'timestamp': int(timezone.now().timestamp())
    }