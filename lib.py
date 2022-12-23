from pdf2image import convert_from_path
import os
import PIL
import random
from PyPDF2 import PdfMerger
import img2pdf

margin = 70
dist = 20

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
        for i in range(int(tmp_width * 0.7)):
            if tmp == (-1, -1, -1):
                tmp = rgb_im.getpixel((mid + i, h))
            else:
                if tmp != rgb_im.getpixel((mid + i, h)):
                    error = True
        if not error and tmp != (255, 255, 255) and tmp != COLOR and tmp != (0, 0, 0):
            BOTTOM = h - 1
            break
    if BOTTOM == -1:
        return -1

    return (LEFT, TOP, RIGHT, BOTTOM)

def cropImage(file_name, coordinates):
    im = PIL.Image.open(file_name)
    im1 = im.crop(coordinates)
    tmp = file_name[:len(file_name) - 4] + "_" + str(random.randint(1000, 9999)) + ".png"
    im1.save(tmp)
    return tmp

def showImages(files):
    for i in files:
        im = PIL.Image.open(i)
        im.show()

def getSizeOfImage(filename):
    im = PIL.Image.open(filename)
    image_width, image_height = im.size
    return (image_width, image_height)

def mergeImages(files, page_size):
    createDirectory("final")
    cnt = len(files)
    page_counter = 0
    space = False
    file_page = ""
    last = 0
    ret = []
    while cnt > 0:
        img = PIL.Image.new('RGB', (page_size[0], page_size[1]), color = 'white')
        file_page = 'final/final_page' + str(page_counter) + '.png'
        img.save(file_page)
        page_counter += 1
        last_idx = margin
        while last < len(files) and last_idx + PIL.Image.open(files[last]).size[1] <= page_size[1] - margin:
            tmp_img = PIL.Image.open(file_page)
            tmp_img_2 = PIL.Image.open(files[last])
            tmp_img.paste(tmp_img_2, (page_size[0] // 2 - PIL.Image.open(files[last]).size[0] // 2, last_idx))
            tmp_img.save(file_page)
            last_idx += PIL.Image.open(files[last]).size[1]
            last_idx += dist
            last += 1
            cnt -= 1
        ret.append(file_page)
    
    return ret

def pdfMerger(files):
    pdfs = []
  
    cnt = 0
    for i in files:
        image = PIL.Image.open(i)
        pdf_bytes = img2pdf.convert(image.filename)
        tmp = "final/page_" + str(cnt) + ".pdf"
        pdfs.append(tmp)
        file = open(tmp, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        cnt += 1
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("tasks_merged.pdf")
    merger.close()
    return pdfs

def createDirectory(name):
    os.mkdir(name)

def deleteDirectory(name):
    os.rmdir(name)