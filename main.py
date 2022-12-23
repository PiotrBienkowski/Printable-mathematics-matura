import lib

def init():
    print("Last page:")
    last_page = int(input())
    print("File name:")
    file_name = input()

    lib.createDirectory("files_tmp")

    files_tmp = lib.pdfToPng(file_name, "files_tmp", last_page)

    to_delete = []
    to_print = []

    for i in files_tmp:
        tmp = lib.detectTask(i)
        if tmp != -1:
            to_print.append(lib.cropImage(i, tmp))
            to_delete.append(i)
        else:
            to_delete.append(i)

    page_size = lib.getSizeOfImage(to_delete[0])
    ret = lib.mergeImages(to_print, page_size)
    ret_pdf = lib.pdfMerger(ret)

    for i in ret:
        to_delete.append(i)

    for i in ret_pdf:
        to_delete.append(i)

    for i in to_print:
        to_delete.append(i)

    lib.removeFiles(to_delete)
    lib.deleteDirectory("files_tmp")
    lib.deleteDirectory("final")

init()