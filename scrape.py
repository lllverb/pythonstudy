from google_images_download import google_images_download
import os
import rename
import cutting
import judge


def fetch_image(params):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": params["search_keywords"],
        "limit": params["limit"],
        "format": params["image_format"],
        "chromedriver": "chromedriver",
        "--related_images": True,
        "output_directory": params["output_directory"],
        "no_directory": True,
    }
    response.download(arguments)


def input_argument():
    params = {}

    search_keywords = input("search keywords:")
    while not search_keywords:
        search_keywords = input("search keywords: ")

    print("0:'jpg',1:'gif',2:'png',3:'bmp',4:'svg',5:'webp',6:'ico',7:'raw'")
    image_format = ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]
    image_format_number = input("Please select image format number(0~7): ")
    while not image_format_number.isdigit() or int(image_format_number) > 7:
        image_format_number = input("Please select image format number(0~7): ")

    limit = input("How much do you want a image?: ")
    while not limit.isdigit():
        limit = input("How much do you want a image?: ")

    output_directory = input("Where are you saving download image?")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    params["search_keywords"] = search_keywords
    params["image_format"] = image_format[int(image_format_number)]
    params["limit"] = limit
    params["output_directory"] = output_directory

    return params


def scrape():
    params = input_argument()
    fetch_image(params)
    name = params["output_directory"]
    image_format = "." + params["image_format"]
    limit = int(params["limit"])
    return name, image_format, limit


if __name__ == "__main__":
    name, image_format, limit = scrape()
    rename.rename(name, image_format)
    cutting.cutting(name, image_format, limit)
    # judge.judge(name)
