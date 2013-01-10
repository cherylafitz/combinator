from pyPdf import PdfFileWriter, PdfFileReader
import pyPdf
import os

try:
    os.mkdir "output/"
except:
    print "did not create output dir"


class Pdf(object):
    '''
    Object to associate the various documents of a given application
    Perhaps I should rename this.
    '''
    def __init__(self, refCode):
        self.refCode = refCode
        self.appPdf = None
        self.recPdfs = []
        self.uploads = []

    def addAppPdf(self,filename):
        self.appPdf = filename
    def addRecPdf(self,filename):
        self.recPdfs.append(filename)
    def addUpload(self,filename):
        self.uploads.append(filename)
    def getRefCode(self):
        return self.refCode
    def getAppPdf(self):
        return self.appPdf
    def getRecPdfs(self):
        return self.recPdfs
    def getUploads(self):
        return self.uploads
        
def getFiles():
    '''
    get all files in directory
    '''
    return [file for file in os.listdir('.')]

def printFiles():
    '''
    print all files in directory
    '''
    for file in getFiles():
        print file

def getRefCode(filename):
    '''
    Extracts the first 8 characters of a filename, on the assumption that they are a reference code
    '''
    return str(filename[:8])

def getUniqueRefCodes():
    '''
    Gets Unique Reference Codes for documents in given directory
    '''
    refCodes = []
    for file in getFiles():
        if '.pdf' not in file:
            continue
        elif getRefCode(file) not in refCodes:
            refCodes.append(getRefCode(file))
    return refCodes

def createPDFObjects():
    '''
    Creates pdf objects
    '''
    Pdfs = []
    for refCode in getUniqueRefCodes():
        Pdfs.append(Pdf(refCode))
    return Pdfs

def findPdfObject(refCode, pdfList):
    '''
    refCode: string
    pdfList: list of Pdf objects

    if a matching reference code is found in pdfList, returns that pdf object
    otherwise, returns None
    '''
    for pdf in pdfList:
        if pdf.getRefCode() == refCode:
            return pdf
    return None
    
def combine(pdfList, files = getFiles()):
    '''
    Combines files found in a folder into Pdf objects, based on strings found in their filenames
    '''
    for file in files:
##        if ".pdf" not in file:
##            break
##        if 'App' in file:
##            print file, 'app'
##        elif 'Teacher' in file:
##            print file, 'teacher'
##        elif 'Parent' in file:
##            print file, 'parent'
##        else:
##            print "PROBLEM", file
        refCode = getRefCode(file)
        pdf = findPdfObject(refCode,pdfList)
        if 'App' in file:
            pdf.addAppPdf(file)
        elif 'rec' in file:
            pdf.addRecPdf(file)
        else:
            if ".pdf" in file or ".PDF" in file:
                pdf.addUpload(file)


        
def getPdfs():
    '''
    returns all pdf files found in a given directory
    '''
    Pdf = []
    for file in getFiles():
        if '.pdf' in file:
            Pdf.append(file)
    return Pdf


def makeOutputPdf(pdf):
    '''
    Takes a Pdf object, combines all its constituent parts into a pdf document in /output directory
    '''
    output = PdfFileWriter()
    pieces = []
    if pdf.getAppPdf() != None:
        pieces.append(pdf.getAppPdf())
    for rec in pdf.getRecPdfs():
        pieces.append(rec)
    for rec in pdf.getUploads():
        pieces.append(rec)
    for piece in pieces:
        if isPdfEncrypted(piece) == True:
            raise Exception(piece)
    for piece in pieces:
        if isPdfEncrypted(piece) == False:
            input = PdfFileReader(file(piece, "rb"))
            numPages = input.getNumPages()
            for page in range (numPages):
                output.addPage(input.getPage(page))
        else:
            print "skipping", piece
        outputName = "output/" + pdf.getRefCode() + "-Full.pdf"
        outputStream = file(outputName, "wb")
        output.write(outputStream)
        outputStream.close()

def isPdfEncrypted(filename):
    '''
    First-pass attempt to see if a given pdf will give the makeOutputPdf function trouble.
    Returns True if PDFFileReader object gives an exception when trying to get the number of pages
    '''
    input = PdfFileReader(file(filename, "rb"))
    try:
        numPages = input.getNumPages()
    except:
        #print filename
        return True
    return False
        
def listProblemPdfs():
    '''
    Lists all the Pdfs that will give PdfFileReader object trouble
    '''
    for pdf in getFiles():
        try:
            isPdfEncrypted(pdf)
        except:
            print pdf

def listPdfs(list):
    for pdf in list:
        print pdf.getRefCode()
        print pdf.getAppPdf()
        print pdf.getRecPdfs()
        print pdf.getUploads()
        print "###"




def go():
    for pdf in pdfList:
        try:
            makeOutputPdf(pdf)
        except:
            print pdf.getRefCode(), "not created"

### Setup

pdfList = createPDFObjects()
combine(pdfList)


####

### Nonsense and half-formed ideas graveyard


# def outputter(pieces):
#     print pieces
#     output = PdfFileWriter()
#     for piece in pieces:
#         input = PdfFileReader(file(piece, "rb"))
#         try:
#             numPages = input.getNumPages()
#         except:
#             print piece
# ##        for page in range (numPages):
# ##            output.addPage(input.getPage(page))
# ##    outputName = "output/" + pieces[1]
# ##    outputStream = file(outputName, "wb")
# ##    output.write(outputStream)
# ##    outputStream.close()

##def makeOutputPdf2():
##    index = 0
##    pdfs = getPdfs()
##    while index < len(pdfs):
##        pieces = []
##        pieces.append(pdfs[index])
##        pieces.append(pdfs[index + 1])
##        print pieces
##        print '###'
##        outputter(pieces)
##        index += 2