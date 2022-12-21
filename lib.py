from pdf2image import convert_from_path
import os
import PIL

def pdfToPng(pdf_name, folder = "", pages_limit = -1):
    files_list = []

    if len(pdf_name) < 4 or pdf_name[len(pdf_name) - 4:len(pdf_name)] != ".pdf":
        pdf_name += ".pdf"
    if folder[len(folder) - 1] != '/':
        folder += '/'

    images = convert_from_path(pdf_name)
    if pages_limit == -1:
        pages_limit = len(images)

    for i in range(len(images)):
        if i >= pages_limit:
            break
        tmp = folder + 'page_' + str(i) + '.png'
        images[i].save(tmp, 'PNG')
        files_list.append(tmp)
    return files_list

def removeFiles(files_list):
    for i in files_list:
        if os.path.exists(i):
            os.remove(i)

def detectTask(file_name):
    im = PIL.Image.open(file_name)
    image_width, image_height = im.size
    mid = image_width // 2
    rgb_im = im.convert('RGB')

    TOP = -1
    COLOR = (-1, -1, -1)
    for h in range(image_height - 3):
        tmp = (-1, -1, -1)
        error = False
        for k in range(4):
            for i in range(50):
                if tmp == (-1, -1, -1):
                    tmp = rgb_im.getpixel((mid + i, h))
                else:
                    if tmp != rgb_im.getpixel((mid + i, h)):
                        error = True
        if not error and tmp != (255, 255, 255):
            TOP = h
            COLOR = tmp
            break
        
    if TOP == -1:
        return -1
    
    i = 1
    while rgb_im.getpixel((mid - i, TOP)) == COLOR or rgb_im.getpixel((mid - i, TOP)) == (112, 48, 160):
        i += 1
    LEFT = mid - i


    i = 1
    while rgb_im.getpixel((mid - i, TOP)) == COLOR:
        i -= 1
    RIGHT = mid - i

    BOTTOM = -1
    for h in range(TOP, image_height - 3):
        tmp_width = int((RIGHT - LEFT) * 0.7)
        tmp = (-1, -1, -1)
        error = False
        for i in range(tmp_width // 2):
            if tmp == (-1, -1, -1):
                tmp = rgb_im.getpixel((mid + i, h))
            else:
                if tmp != rgb_im.getpixel((mid + i, h)):
                    error = True
        if not error and tmp != (255, 255, 255) and tmp != COLOR:
            BOTTOM = h - 1
            break
    if BOTTOM == -1:
        return -1

    return (LEFT, TOP, RIGHT, BOTTOM)

def cropImage(file_name, coordinates):
    im = PIL.Image.open(file_name)
    im1 = im.crop(coordinates)
    im1.save(file_name)

def showImages(files):
    for i in files:
        im = PIL.Image.open(i)
        im.show()