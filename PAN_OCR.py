# For this PAN-OCR project, I have used 2 different OCRs
# tesseract for extracting the PAN card no. and easyocr for extracting the DOBs
# This done because both tend to misrecognise each others thing, that is
# tesseract mis-recognised DOBs and easyocr mis-recognised PAN card no.

# importing required modules
from PIL import Image,ImageEnhance,ImageOps
import pytesseract as tes
import os
import datetime
import easyocr as eas


# Increasing contrast of all the images and then saving them
# This is done so as to increase the accuracy of the ocr engine

path='findmind//original' #directory of original images

i=1
for f in os.listdir(path):
    im_path=os.path.join(path,f)
    im=Image.open(im_path)
    im=ImageOps.grayscale(im)
    enhancer=ImageEnhance.Contrast(im)
    im=enhancer.enhance(3)
    im.save('findmind//img//'+str(i)+'.png')
    i+=1


path2='findmind//img' #directory of high-contrast images

tes_data=[] #for storing tesseract ocr text
eas_data=[] #for storing easyocr text


# iterating over the "high contrast" image directory
# then extracting and storing text using both OCRs
for f in os.listdir(path2):
    im_path=os.path.join(path2,f)
    im=Image.open(im_path)

    #extracting text using tesseract
    text1=tes.image_to_string(im,'eng')
    tes_data.append(text1.split())
    
    #extractinf text using easyocr
    reader=eas.Reader(['en'],False)
    text2=reader.readtext(im_path)
    eas_data.append(text2)

# function to detect PAN no.
def find_pan(str):

    if len(str)==10:

        alpha=False
        num=False

        for i in str:
            if i.isdigit():
                num=True
            if i.isalpha():
                alpha=True

        return alpha and num

# function to detect DOB
def find_dob(date_text):
    try:
        date=datetime.datetime.strptime(date_text, '%d/%m/%Y').date()
        return date.strftime('%d-%m-%Y') #changing date format to dd/mm/yyyy
    except:
        pass

pan_no=[] #for storing PAN numbers
dob=[] #for storing DOBs

# extracting and storing PAN no.
for data in tes_data:
    for details in data:
        if find_pan(details):
            pan_no.append(details)

# extracting and storing DOB
for data in eas_data:
    for details in data:
        if find_dob(details[1]) is not None:
            dob.append(details[1])

# printing the extracted DOB and PAN no.
for i in range(3):
    print('PAN No. :',pan_no[i])
    print('DOB :',dob[i])
    print()
