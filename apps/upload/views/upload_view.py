# 文件说明：处理 apps/upload/views/upload_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

import logging

import os

import uuid

from django.conf import settings

from PIL import Image

from PIL import ImageDraw

from PIL import ImageFont

from rest_framework.views import APIView

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)

logger = logging.getLogger(__name__)


class UploadView(APIView):
    """
    文件上传
    """

    def post(self, request):

        upload_type = request.data.get("type", "file")
        # 获取上传文件
        file = request.FILES.get("file")

        # 文件为空
        if not file:
            return ResponseError(msg="请选择文件")

        ext = os.path.splitext(file.name)[1]
        image_types = {"avatar", "id_card", "repair_image", "image"}
        image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

        if upload_type in image_types:
            if ext.lower() not in image_exts or not file.content_type.startswith("image/"):
                return ResponseError(msg="只能上传 jpg、png、gif、webp 图片")

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

        if upload_type == "id_card":

            try:
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
