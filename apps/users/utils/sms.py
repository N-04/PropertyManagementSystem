# 文件说明：封装 apps/users/utils/sms.py 中跨接口复用的工具函数。

import random

from django.core.cache import cache

# 短信验证码有效期：5 分钟；重复发送冷却：60 秒。
SMS_TTL = 300
SMS_COOLDOWN = 60

# 允许发送验证码的业务场景，防止前端随意传 purpose。
SMS_PURPOSES = {"register", "reset_password", "login"}


def _sms_cache_key(purpose, phone):
    """短信验证码缓存 key，按业务场景和手机号隔离。"""

    return f"auth:sms:{purpose}:{phone}"


def _cooldown_cache_key(purpose, phone):
    """短信发送冷却缓存 key。"""

    return f"auth:sms-cooldown:{purpose}:{phone}"


def create_sms_code(phone, purpose):
    """
    生成并缓存短信验证码。

    当前项目还没有真实短信服务，所以这里只负责生成和缓存验证码；
    视图层在 DEBUG 模式下会把验证码返回给前端用于本地调试。
    """

    cooldown_key = _cooldown_cache_key(purpose, phone)

    if cache.get(cooldown_key):
        return None

    code = f"{random.randint(0, 999999):06d}"
    cache.set(_sms_cache_key(purpose, phone), code, SMS_TTL)
    cache.set(cooldown_key, True, SMS_COOLDOWN)

    return code


def validate_sms_code(phone, purpose, code):
    """
    校验短信验证码。

    校验成功后删除缓存，保证验证码只能使用一次。
    """

    if not phone or not purpose or not code:
        return False

    cache_key = _sms_cache_key(purpose, phone)
    cached_code = cache.get(cache_key)

    if not cached_code:
        return False

    if str(cached_code) != str(code):
        return False

    cache.delete(cache_key)
    return True
