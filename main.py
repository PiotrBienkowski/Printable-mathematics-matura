import lib

last_page = 54

files_tmp = lib.pdfToPng("files_cke/Matematyka - zbior zadan na poziomie rozszerzonym.pdf", "files_tmp", last_page)

# files_tmp = ['files_tmp/page_0.png', 'files_tmp/page_1.png', 'files_tmp/page_2.png', 'files_tmp/page_3.png', 'files_tmp/page_4.png', 'files_tmp/page_5.png', 'files_tmp/page_6.png', 'files_tmp/page_7.png', 'files_tmp/page_8.png', 'files_tmp/page_9.png', 'files_tmp/page_10.png', 'files_tmp/page_11.png', 'files_tmp/page_12.png', 'files_tmp/page_13.png', 'files_tmp/page_14.png', 'files_tmp/page_15.png', 'files_tmp/page_16.png', 'files_tmp/page_17.png', 'files_tmp/page_18.png', 'files_tmp/page_19.png', 'files_tmp/page_20.png', 'files_tmp/page_21.png', 'files_tmp/page_22.png', 'files_tmp/page_23.png', 'files_tmp/page_24.png', 'files_tmp/page_25.png', 'files_tmp/page_26.png', 'files_tmp/page_27.png', 'files_tmp/page_28.png', 'files_tmp/page_29.png', 'files_tmp/page_30.png', 'files_tmp/page_31.png', 'files_tmp/page_32.png', 'files_tmp/page_33.png', 'files_tmp/page_34.png', 'files_tmp/page_35.png', 'files_tmp/page_36.png', 'files_tmp/page_37.png', 'files_tmp/page_38.png', 'files_tmp/page_39.png', 'files_tmp/page_40.png', 'files_tmp/page_41.png', 'files_tmp/page_42.png', 'files_tmp/page_43.png', 'files_tmp/page_44.png', 'files_tmp/page_45.png', 'files_tmp/page_46.png', 'files_tmp/page_47.png', 'files_tmp/page_48.png', 'files_tmp/page_49.png', 'files_tmp/page_50.png', 'files_tmp/page_51.png', 'files_tmp/page_52.png', 'files_tmp/page_53.png']

to_delete = []

tmp_show = []


print(files_tmp)

for i in files_tmp:
    tmp = lib.detectTask(i)
    if tmp != -1:
        lib.cropImage(i, tmp)
        # tmp_show.append(i)
    else:
        to_delete.append(i)

# # for i in to_delete:
# #     files_tmp.remove(i)
# # lib.removeFiles(to_delete)


# lib.showImages(tmp_show)

