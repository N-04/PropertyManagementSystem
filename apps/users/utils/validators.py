import re
from datetime import datetime

from rest_framework import serializers

# 手机号规则：11 位，第一位为 1，第二位为 3-9。
PHONE_RE = re.compile(r"^1[3-9]\d{9}$")

# 身份证基础格式：地址码 6 位 + 出生日期 8 位 + 顺序码 3 位 + 校验位。
ID_CARD_RE = re.compile(
    r"^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])"
    r"(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$"
)


def validate_phone_format(phone):
    """校验中国大陆手机号基础格式。"""

    if not phone:
        raise serializers.ValidationError("手机号不能为空")

    if not PHONE_RE.match(phone):
        raise serializers.ValidationError("手机号格式不正确")

    return phone


def validate_password_strength(password):
    """
    校验密码强度。

    当前规则对应结构图要求：8-20 位，不能纯数字，不能纯字母，
    允许特殊字符，但不允许空白字符。
    """

    if not 8 <= len(password) <= 20:
        raise serializers.ValidationError("密码长度必须为8-20位")

    if password.isdigit():
        raise serializers.ValidationError("密码不能为纯数字")

    if password.isalpha():
        raise serializers.ValidationError("密码不能为纯字母")

    if re.search(r"\s", password):
        raise serializers.ValidationError("密码不能包含空白字符")

    return password


def validate_id_card(id_card):
    """
    校验 18 位身份证号。

    校验内容包括：基础格式、出生日期是否合法、校验位算法。
    """

    if not id_card:
        raise serializers.ValidationError("身份证号不能为空")

    if not ID_CARD_RE.match(id_card):
        raise serializers.ValidationError("身份证号格式不正确")

    birthday_text = id_card[6:14]

    # 身份证第 7-14 位是出生日期，必须是真实存在的日期。
    try:
        birthday = datetime.strptime(birthday_text, "%Y%m%d").date()
    except ValueError as exc:
        raise serializers.ValidationError("身份证出生日期不合法") from exc

    if birthday > datetime.now().date():
        raise serializers.ValidationError("身份证出生日期不能晚于今天")

    # 身份证第 18 位校验码算法：前 17 位乘权重后取模，再映射到校验码表。
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = "10X98765432"
    total = sum(int(id_card[index]) * weights[index] for index in range(17))
    expected = check_map[total % 11]

    if id_card[-1].upper() != expected:
        raise serializers.ValidationError("身份证校验位不正确")

    return id_card.upper()


def mask_id_card(id_card):
    """身份证脱敏展示，只保留前 6 位和后 4 位。"""

    if not id_card:
        return ""

    return f"{id_card[:6]}********{id_card[-4:]}"
