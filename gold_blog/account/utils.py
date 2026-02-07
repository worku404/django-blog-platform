import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def generate_otp():
    code = f'{secrets.randbelow(1000000):06d}'
    return code

def otp_expire(minutes=15):
    return timezone.now() + timedelta(minutes=minutes)

def otp_cooldown_remaining(last_seen_at, seconds=60):
    if not last_seen_at:
        return 0
    remaining = (last_seen_at + timedelta(seconds=seconds) - timezone.now()).total_seconds()
    return max(0, int(remaining))