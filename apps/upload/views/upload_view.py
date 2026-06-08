import os

import uuid

from PIL import Image

from PIL import ImageDraw

from PIL import ImageFont

from rest_framework.views import APIView

from common.response.response import (
    ResponseSuccess,
    ResponseError,
)


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

        # 保存目录

        ext = os.path.splitext(file.name)[1]

        filename = f"{uuid.uuid4().hex}{ext}"

        save_path = os.path.join(
            "media",
            "upload",
            filename,
        )

        # 身份证才加水印

        if upload_type == "id_card":

            try:
                from PIL import Image
                from PIL import ImageDraw
                from PIL import ImageFont

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
                print("水印失败：", e)

        # 写入文件
        with open(save_path, "wb+") as f:

            for chunk in file.chunks():
                f.write(chunk)

        return ResponseSuccess(data={"url": f"/media/upload/{filename}"})
