import pytesseract
import os
import glob
from pdf2image import convert_from_path



def tesseractOCR_pdf(pdf):

    filePath = pdf
    
    pages = convert_from_path(filePath, 500,
                              poppler_path = r"C:\Users\rahulr6\Downloads\poppler\Release-23.08.0-0\poppler-23.08.0\Library\bin", 
                              )

    # Counter to store images of each page of PDF to image 
    image_counter = 1

    # Iterate through all the pages stored above 
    for page in pages:
        # Declaring filename for each page of PDF as JPG 
        # For each page, filename will be: 
        # PDF page 1 -> page_1.jpg 
        # PDF page 2 -> page_2.jpg 
        # PDF page 3 -> page_3.jpg 
        # .... 
        # PDF page n -> page_n.jpg 

        filename = "page_"+str(image_counter)+".jpg"
        
        # Save the image of the page in system 
        page.save(filename, 'JPEG') 
        # Increment the counter to update filename 
        image_counter = image_counter + 1

    # Variable to get count of total number of pages 
    filelimit = image_counter-1


    # Create an empty string for stroing purposes
    text = ""
    # Iterate from 1 to total number of pages 
    for i in range(1, filelimit + 1): 
        # Set filename to recognize text from 
        # Again, these files will be: 
        # page_1.jpg 
        # page_2.jpg 
        # .... 
        # page_n.jpg 
        filename = "page_"+str(i)+".jpg"

        # Recognize the text as string in image using pytesserct 
        text += str(((pytesseract.image_to_string(Image.open(filename))))) 

        text = text.replace('-\n', '')     

    
    #Delete all the jpg files that created from above
    for i in glob.glob("*.jpg"):
        os.remove(i)
        
    return text

def tesseractOCR_img(img):

    filePath = img
    
    text = str(pytesseract.image_to_string(filePath,lang='eng',config='--psm 6'))
    
    text = text.replace('-\n', '')
    
    return text

def Tesseract_ALL(docDir, txtDir):
    if docDir == "": docDir = os.getcwd() + "\\" #if no docDir passed in 
        
    for doc in os.listdir(docDir): #iterate through docs in doc directory
        try:
            fileExtension = doc.split(".")[-1]
            
            if fileExtension == "pdf":
                pdfFilename = docDir + doc 
                text = tesseractOCR_pdf(pdfFilename) #get string of text content of pdf
                textFilename = txtDir + doc + ".txt"
                textFile = open(textFilename, "w") #make text file
                textFile.write(text) #write text to text file
            else:   
#             elif (fileExtension == "tif") | (fileExtension == "tiff") | (fileExtension == "jpg"):
                imgFilename = docDir + doc 
                text = tesseractOCR_img(imgFilename) #get string of text content of img
                textFilename = txtDir + doc + ".txt"
                textFile = open(textFilename, "w") #make text file
                textFile.write(text) #write text to text file
        except Exception as e:
            print("Error in file: "+ str(doc))
            print(e)
            
    for filename in os.listdir(txtDir):
        fileExtension = filename.split(".")[-2]
        if fileExtension == "pdf":
            os.rename(txtDir + filename, txtDir + filename.replace('.pdf', ''))
        elif fileExtension == "tif":
            os.rename(txtDir + filename, txtDir + filename.replace('.tif', ''))
        elif fileExtension == "tiff":
            os.rename(txtDir + filename, txtDir + filename.replace('.tiff', ''))
        elif fileExtension == "jpg":
            os.rename(txtDir + filename, txtDir + filename.replace('.jpg', ''))

#Below are the code to run the functions
#Specific telling the function where the documents located and where you want the txt files to be at
docDir = r"documentSearch\data"
txtDir = r"documentSearch\text_data"

Tesseract_ALL(docDir, txtDir)