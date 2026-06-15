# 文件说明：封装 apps/users/utils/captcha.py 中跨接口复用的工具函数。

import base64
import random
import string
import uuid

from django.core.cache import cache

# 图形验证码有效期：5 分钟。
CAPTCHA_TTL = 300
CAPTCHA_PREFIX = "auth:captcha"


def _captcha_cache_key(captcha_key):
    """统一生成缓存 key，避免和其他缓存数据冲突。"""

    return f"{CAPTCHA_PREFIX}:{captcha_key}"


def generate_captcha_code(length=4):
    """生成字母数字组合验证码。"""

    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def build_captcha_svg(code):
    """
    生成验证码 SVG，并转成 data URL。

    这样前端可以直接把 captcha_image 放到 img.src，不需要额外静态文件。
    """

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="120" height="42" viewBox="0 0 120 42">
  <rect width="120" height="42" rx="6" fill="#f4f7fb"/>
  <path d="M8 31 C25 5, 48 40, 65 13 S98 31, 112 9" fill="none" stroke="#b7c2d0" stroke-width="2"/>
  <text x="60" y="28" text-anchor="middle" font-family="Arial, sans-serif" font-size="22"
        font-weight="700" letter-spacing="4" fill="#1f2937">{code}</text>
  <circle cx="18" cy="12" r="2" fill="#94a3b8"/>
  <circle cx="101" cy="29" r="2" fill="#94a3b8"/>
</svg>
""".strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def create_captcha():
    """
    创建一组验证码。

    返回给前端的是 captcha_key 和图片；真实答案只保存在后端缓存里。
    """

    captcha_key = uuid.uuid4().hex
    code = generate_captcha_code()
    cache.set(_captcha_cache_key(captcha_key), code.lower(), CAPTCHA_TTL)

    return {
        "captcha_key": captcha_key,
        "captcha_image": build_captcha_svg(code),
        "expire_seconds": CAPTCHA_TTL,
    }


def validate_captcha(captcha_key, captcha_code):
    """
    校验图形验证码。

    验证码使用一次后立即删除，防止同一个验证码被重复提交。
    """

    if not captcha_key or not captcha_code:
        return False

    cache_key = _captcha_cache_key(captcha_key)
    cached_code = cache.get(cache_key)

    if not cached_code:
        return False

    cache.delete(cache_key)
    return cached_code == captcha_code.lower()
