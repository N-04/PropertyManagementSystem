# 文件说明：负责 apps/upload/serializers/upload_serializer.py 对应接口的数据序列化、反序列化和参数校验。

# 上传接口直接读取 multipart 文件流，目前不需要专用 Serializer。
# 文件类型、扩展名和图片水印等校验集中放在 UploadView 中处理。
