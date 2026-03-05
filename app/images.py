from dotenv import load_dotenv
from imagekitio import ImageKit
import os
from pathlib import Path

load_dotenv()

# initialize the imagekit
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY")
    # base_url=os.getenv("IMAGEKIT_URL"),
)

# define imagekit upload options
upload_options = {
    "file_name": "my_file.jpg", "use_unique_file_name": True, "tags": ["tag1""tag2"], "folder": "my_folder",
    "is_private_file": False, "response_fields": "tags,customCoordinates"
}


def upload_image(file, file_name):
    response = imagekit.files.upload(
        file=file,  # file object from FastAPI
        file_name=file_name,
        folder="/Uploads",
        use_unique_file_name=True,
        public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),
        tags=["backend-upload"]
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

