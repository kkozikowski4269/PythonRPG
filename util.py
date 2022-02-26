def get_image(file_name):
    file = open(file_name, "r")
    image = file.read()
    file.close()
    return image

