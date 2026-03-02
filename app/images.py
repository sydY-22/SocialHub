from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

# initialize the imagekit
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    base_url=os.getenv("IMAGEKIT_URL"),
)

# define imagekit upload options
upload_options = {
    "file_name": "my_file.jpg", "use_unique_file_name": True, "tags": ["tag1""tag2"], "folder": "my_folder",
    "is_private_file": False, "response_fields": "tags,customCoordinates"
}

# define upload response
# response = imagekit.files.upload(
#     file=open("E:/Uploads/bean.jpg", "rb"),
#     file_name="bean.jpg",
#     folder="/Uploads/",
#     public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
#     use_unique_file_name=True
#
# )


def upload_image(file_path, file_name):
    with open(file_path, "rb") as f:
        response = imagekit.files.upload(
            file=f,
            file_name=file_name
        )
    return response


# Upload from bytes (web forms)
# image_data = imagekit.request.files['image'].read()
# response = imagekit.files.upload(
#     file=image_data,
#     file_name="upload.jpg",
#     public_key=os.getenv("IMAGEKIT_PUBLIC_KEY")
# )
#
# with open("video.mp4", "rb") as f:
#     response = imagekit.files.upload(file=f, file_name="video.mp4", public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"))

