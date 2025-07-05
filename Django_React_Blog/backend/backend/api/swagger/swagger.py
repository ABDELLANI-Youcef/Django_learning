# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
# from drf_spectacular.types import OpenApiTypes
# from api import serializers as api_serializer

# @extend_schema(
#   tags=['Dashboard'],
#     request=api_serializer.PostSerializerPost,
#     responses={
#         201: OpenApiTypes.OBJECT,
#         400: OpenApiTypes.OBJECT
#     },
#     examples=[
#         OpenApiExample(
#             'Example request',
#             value={
#                 "user_id": 1,
#                 "title": "Sample Post",
#                 "image": "string",  # or actual base64 image
#                 "description": "Post content",
#                 "slug": "sample-post-xy",  # optional
#                 "category_id": 1,
#                 "post_status": "Active"
#             },
#             request_only=True
#         ),
#         OpenApiExample(
#             'Success response',
#             value={"message": "Post was created successfully"},
#             response_only=True
#         )
#     ],
#     description='''
#     Creates a new blog post.
#     Required fields: user_id, title, category_id.
#     Slug will be auto-generated if not provided.
#     '''
# )