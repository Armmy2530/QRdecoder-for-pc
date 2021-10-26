from PIL import ImageGrab
from pyzbar import pyzbar
import pyperclip
import cv2
import os
import time

pev_barcodeData = ""
printed = False
num_qr=1
img_path = 'image\image_1.png'
img_folder = 'E:\\Documents\\All of code\\In class\\test\\image'
config_path = 'E:\\Documents\\All of code\\In class\\test\\myconfig.txt'
result_path = 'E:\\Documents\\All of code\\In class\\test\\result.txt'

def recalldata():
    f = open(config_path, 'r+')
    while True:
        s = f.readline()
        if s == '': # check file end
            break
        # spliting line to key and value
        d = s.rstrip().split(':')
        num_qr = int(d[1])
        print(f'numqr: {num_qr}')
    f.close()
    return num_qr

def savedata(save_path,inside_text,mode):
    f = open(save_path, mode)
    f.write(inside_text)
    f.close()

check_img_folder = os.path.isdir(img_folder)
if not check_img_folder:
    os.makedirs(img_folder)
    print('created folder : ', img_folder)
    savedata(config_path,f"numqr : 0",'x')
    savedata(result_path,f"",'x')

num_qr=recalldata()+1
while True:
    try:
        im = ImageGrab.grabclipboard()
        im.save(img_path)
        printed = False
        img = cv2.imread(img_path)
        barcodes = pyzbar.decode(img)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 0), 2)
            print("[INFO] found {} : {}".format(barcodeType, barcodeData))
            print(f'pev_barcode:{pev_barcodeData}  Current_Data:{barcodeData}')
            if not pev_barcodeData==barcodeData:
                file_name = 'result_'+str(num_qr)+'.png'
                cv2.imwrite(os.path.join(img_folder , file_name), img)
                pev_barcodeData=barcodeData
                pyperclip.copy(barcodeData)
                savedata(config_path,f"numqr : {num_qr}",'w')
                savedata(result_path,f"{num_qr} : {barcodeData}\n",'a')
                print(f'numqr : {num_qr}')
                num_qr=num_qr+1
            elif pev_barcodeData==barcodeData:
                pyperclip.copy(pev_barcodeData)
    except:
        if not printed:
            print("""
            another programe using clipboard or current clipboard is not image
            """)
        printed = True
    
    time.sleep(0.1)



