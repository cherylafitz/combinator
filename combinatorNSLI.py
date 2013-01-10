from pyPdf import PdfFileWriter, PdfFileReader
import pyPdf
import os

class Pdf(object):
    def __init__(self, refCode):
        self.refCode = refCode
        self.appPdf = None
        self.teacherPdf = None
        self.parentPdf = None
    def addAppPdf(self,filename):
        self.appPdf = filename
    def addTeacherPdf(self,filename):
        self.teacherPdf = filename
    def addParentPdf(self,filename):
        self.parentPdf = filename
    def getRefCode(self):
        return self.refCode
    def getAppPdf(self):
        return self.appPdf
    def getTeacherPdf(self):
        return self.teacherPdf
    def getParentPdf(self):
        return self.parentPdf
        
def getFiles():
    return [file for file in os.listdir('.')]

def printFiles():
    for file in getFiles():
        print file

def getRefCode(filename):
    return str(filename[:8])

def getUniqueRefCodes():
    refCodes = []
    for file in getFiles():
        if '.pdf' not in file:
            continue
        elif getRefCode(file) not in refCodes:
            refCodes.append(getRefCode(file))
    return refCodes

def createPDFObjects():
    Pdfs = []
    for refCode in getUniqueRefCodes():
        Pdfs.append(Pdf(refCode))
    return Pdfs

def findPdfObject(refCode, pdfList):
    for pdf in pdfList:
        if pdf.getRefCode() == refCode:
            return pdf
    return None
    
def combine(pdfList, files = getFiles()):
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
        elif 'Teacher' in file:
            pdf.addTeacherPdf(file)
        elif 'Parent' in file:
            pdf.addParentPdf(file)

def makeOutputPdf(pdf):
    output = PdfFileWriter()
    pieces = []
    if pdf.getAppPdf() != None:
        pieces.append(pdf.getAppPdf())
    if pdf.getParentPdf() != None:
        pieces.append(pdf.getParentPdf())
    if pdf.getTeacherPdf() != None:
        pieces.append(pdf.getTeacherPdf())
##    print pdf.getRefCode()
##    print inputs
    for piece in pieces:
        input = PdfFileReader(file(piece, "rb"))
        numPages = input.getNumPages()
        for page in range (numPages):
            output.addPage(input.getPage(page))
    outputName = "output/" + pdf.getRefCode() + "-Full.pdf"
    outputStream = file(outputName, "wb")
    output.write(outputStream)
    outputStream.close()
        

pdfList = createPDFObjects()
combine(pdfList)




def go():
    for pdf in pdfList:
        makeOutputPdf(pdf)
