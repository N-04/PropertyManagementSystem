# 文件说明：处理 apps/upload/views/upload_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

import logging
import os
import uuid

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.response.response import (
    ResponseError,
    ResponseSuccess,
)

logger = logging.getLogger(__name__)

Image.MAX_IMAGE_PIXELS = 20_000_000

ALLOWED_UPLOAD_TYPES = {
    "avatar",
    "id_card",
    "repair_image",
    "image",
    "file",
}
IMAGE_TYPES = {"avatar", "id_card", "repair_image", "image"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
DOCUMENT_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/zip",
    "text/csv",
    "text/plain",
}


def _safe_remove(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        return


def _validate_image_file(path):
    """解析图片结构并限制异常大图，避免伪装文件和解压炸弹。"""

    try:
        with Image.open(path) as image:
            image.verify()
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError):
        return False

    return True


class UploadView(APIView):
    """
    文件上传
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """保存上传文件，并按业务类型执行基础安全校验和后处理。"""

        upload_type = request.data.get("type", "file")
        # 获取上传文件
        file = request.FILES.get("file")

        # 文件为空
        if not file:
            return ResponseError(msg="请选择文件")

        if upload_type not in ALLOWED_UPLOAD_TYPES:
            return ResponseError(msg="不支持的上传类型")

        ext = os.path.splitext(file.name)[1].lower()
        allowed_file_exts = set(settings.UPLOAD_ALLOWED_FILE_EXTS)

        if file.size > settings.UPLOAD_MAX_SIZE:
            return ResponseError(msg="文件大小不能超过10MB")

        if upload_type in IMAGE_TYPES:
            # 图片业务需要同时校验扩展名和 content_type，降低伪装文件风险。
            if ext not in IMAGE_EXTS or not file.content_type.startswith("image/"):
                return ResponseError(msg="只能上传 jpg、png、gif、webp 图片")
        else:
            # 普通文件也必须命中文件白名单，避免脚本、可执行文件等被上传。
            if ext not in allowed_file_exts:
                return ResponseError(msg="不支持的文件类型")

            if file.content_type and file.content_type not in DOCUMENT_CONTENT_TYPES:
                return ResponseError(msg="文件类型校验失败")

        # 使用 UUID 文件名避免暴露原始文件名，也降低重名覆盖风险。
        filename = f"{uuid.uuid4().hex}{ext}"

        save_dir = os.path.join(
            settings.MEDIA_ROOT,
            "upload",
        )
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, filename)

        # 先写入文件，再按上传类型做后处理。
        with open(save_path, "wb+") as f:

            for chunk in file.chunks():
                f.write(chunk)

        if upload_type in IMAGE_TYPES:
            if not _validate_image_file(save_path):
                _safe_remove(save_path)
                return ResponseError(msg="图片内容校验失败")

        if upload_type == "id_card":

            try:
                # 身份证图片加水印，降低敏感图片被二次传播的风险。
                image = Image.open(save_path)

                if image.mode != "RGBA":
                    image = image.convert("RGBA")

                watermark = Image.new(
                    "RGBA",
                    image.size,
                    (255, 255, 255, 0),
                )

                draw = ImageDraw.Draw(watermark)

                width, height = image.size

                text = "物业管理系统\n仅用于业主认证\n禁止传播"

                font = ImageFont.load_default()

                draw.text(
                    (width // 4, height // 3),
                    text,
                    fill=(255, 0, 0, 80),
                    font=font,
                )

                watermark = watermark.rotate(
                    45,
                    expand=False,
                )

                result = Image.alpha_composite(
                    image,
                    watermark,
                )

                result.save(save_path)

            except Exception as e:
                logger.warning("水印失败：%s", e)

        return ResponseSuccess(data={"url": f"{settings.MEDIA_URL}upload/{filename}"})
