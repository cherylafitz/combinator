# -*- coding: utf-8 -*-

from pyPdf import PdfFileReader, PdfFileWriter
import re
import os

# Classes

class Configuration(object):
    """
    Hold logic for assembling documents and directing output
    """

    def __init__(self, config_directory = "./config"):
        """
        _input_directory: Directory of PDFs to handle
        _documents_to_ignore: information about documents to ignore
        _recommendation_application_associations: rec -> app association dict
        _application_filenames: app -> filename dict
        _document_order: List of strings to be found in filenames, in order for output
        """
        self._config_directory = config_directory
        self._input_directory = "./input"
        self._documents_to_ignore = self._load_documents_to_ignore()
        self._recommendation_application_associations = self._load_recommendation_application_associations()
        self._application_filenames = self._load_application_filenames()
        self._document_order = self._load_document_order()

    def _load_documents_to_ignore(self):
        """
        Looks for this file: documents_to_ignore.txt
        if it is found, loads documents_to_ignore based on that file
        if it's not found, returns a sensible default
        """
        config_document = "".join([self._config_directory, "/documents_to_ignore.txt"])
        output_list = parse_config_file_into_list(config_document)
        return output_list

    def _load_recommendation_application_associations(self):
        """
        Looks for this file: recommendation_application_associations.txt
        if it is found, loads recommendation_application_associations based on that file
        if it's not found, returns a sensible default
        """
        config_document = "".join([self._config_directory, "/recommendation_application_associations.txt"])
        output_dict = parse_config_file_into_dictionary(config_document)
        return output_dict

    def _load_application_filenames(self):
        """
        Looks for this file: application_filenames.txt
        if it is found, loads application_filenames based on that file
        if it's not found, returns a sensible default
        """
        config_document = "".join([self._config_directory, "/application_filenames.txt"])
        output_list = parse_config_file_into_dictionary(config_document)
        return output_list

    def _load_document_order(self):
        """
        Looks for this file: document_order.txt
        if it is found, loads document_order based on that file
        if it's not found, returns a sensible default
        """
        config_document = "".join([self._config_directory, "/document_order.txt"])
        output_list = parse_config_file_into_list(config_document)
        return output_list

    def get_input_directory(self):
        if self._input_directory is not None:
            return self._input_directory

    def get_documents_to_ignore(self):
        if self._documents_to_ignore is not []:
            return self._documents_to_ignore

    def get_recommendation_application_associations(self):
        if self._recommendation_application_associations is not {}:
            return self._recommendation_application_associations

    def get_application_filenames(self):
        if self._application_filenames is not {}:
            return self._application_filenames

    def get_document_order(self):
        if self._document_order is not []:
            return self._document_order

class Document(object):
    """
    Represents final or output document, contains some number of filenames. Initialize with an applicant reference code and an output filename
    """

    def __init__(self,applicant_reference_code, output_filename):
        """
        initialize internal variables:

        _filenames: list of filenames to be combined
        _applicant_reference_code: string; the applicant's reference code
        _output_filename: the filename that should be used for the final output
        """
        self._filenames = []
        self._applicant_reference_code = applicant_reference_code
        self._output_filename = output_filename

    def contains_encrypted_pdfs(self):
        """
        Returns True if there are encrypted PDFs in self._filenames, False otherwise
        """
        for filename in self._filenames:
            if is_encrypted(filename) == True:
                return True
        else:
            return False

    def find_encrypted_pdfs(self):
        """
        Returns list of all encrypted PDFs in Document, empty list if there are none
        """
        output_list = []
        for filename in self._filenames:
            if is_encrypted(filename) == True:
                output_list.append(filename)
        return output_list

    def sort_filenames(self, configuration):
        """
        Puts self._filenames into the correct order for printing, based on logic in configuration_object
        """
        nested_list = []
        filenames_to_sort = self._filenames[:]
        document_order = configuration.get_document_order()
        for pattern in document_order:
            tier_list = find_matching_filenames(filenames_to_sort, pattern)
            for filename in tier_list:
                filenames_to_sort.remove(filename)
            if tier_list != []:
                nested_list.append(tier_list)
        if filenames_to_sort:
            filenames_to_sort.sort()
            nested_list.append(filenames_to_sort)
        flattened_list = flatten_list(nested_list)
        if len(flattened_list) != len(self._filenames):
            raise Exception
        self._filenames = flattened_list
        return True

    def add_filename(self, filename):
        self._filenames.append(filename)
        return True

    def get_filenames(self):
        if self._filenames is not []:
            # self.sort_filenames()
            return self._filenames
        else:
            raise NoFilenamesException

    def get_applicant_reference_code(self):
        if self._applicant_reference_code is not None:
            return self._applicant_reference_code
        else:
            raise UnknownReferenceCodeException

    def get_output_filename(self):
        if self._output_filename is not None:
            return self._output_filename
        else:
            raise UnknownOutputFilenameException

class Combinator(object):
    """
    Uses the combinate() method on Document objects to produce PDFs
    """

    def __init__(self):
        """
        initialize internal variables:

        _output_directory: string; path to directory for output
        """
        self._output_directory = "./output"

    def combine(self, document):
        """
        Takes document object, combines the constituent filenames and outputs to self._output_directory
        """
        output = PdfFileWriter()
        filenames = document.get_filenames()
        for filename in filenames:
            input_file = PdfFileReader(file(filename, "rb"))
            numPages = input_file.getNumPages()
            for page in range (numPages):
                output.addPage(input_file.getPage(page))
        output_filename = "".join([self._output_directory, "/", document.get_output_filename()])
        output_stream = file(output_filename, "wb")
        output.write(output_stream)
        output_stream.close()
        return True
    
    def set_output_directory(self, output_directory):
        self._output_directory = output_directory
        return True

# Functions

def is_encrypted(filename):
    '''
    First-pass attempt to see if a given pdf will give the makeOutputPdf function trouble.
    Returns True if PDFFileReader object gives an exception when trying to get the number of pages
    '''
    input = PdfFileReader(file(filename, "rb"))
    try:
        numPages = input.getNumPages()
    except:
        return True
    return False

def create_document_objects(configuration):
    """
    based on configuration object, initializes document objects, returns as a list
    """
    output_list = []
    filename_dict = configuration.get_application_filenames()
    for input_filename in filename_dict.keys():
        output_filename = filename_dict[input_filename]
        applicant_reference_code = extractReferenceCode(input_filename)
        document = Document(applicant_reference_code,output_filename)
        output_list.append(document)
    return output_list

def find_document(filename, documents, configuration):
    """
    given a filename as a string, figures out which document object it should be associated with, returns that document object
    """
    document_reference_code = extractReferenceCode(filename)
    target_reference_code = None
    if document_reference_code in configuration.get_application_filenames().keys():
        # Belongs to application
        target_reference_code = document_reference_code
    elif document_reference_code in configuration.get_recommendation_application_associations().keys():
        target_reference_code = configuration.get_recommendation_application_associations()[document_reference_code]
    for document in documents:
        if target_reference_code == document.get_applicant_reference_code():
            return document

def find_all_encrypted_pdfs(documents):
    """
    given a list of document objects, finds all the encrypted pdfs in each one and returns a list
    """
    nested_list = []
    for document in documents:
        encrypted_documents = document.find_encrypted_pdfs()
        if encrypted_documents != []:
            nested_list.append(encrypted_documents)
    flattened_list = flatten_list(nested_list)
    flattened_list.sort()
    return flattened_list

def parse_config_file_into_dictionary(filename):
    """
    assumes tab-delimited file
    """
    output_dict = {}
    input_file = open(filename, "rb")
    for line in input_file:
        items = line.split("\t")
        if len(items) != 2:
            raise Exception
        else:
            output_dict[items[0].strip()] = items[1].strip()
    return output_dict

def parse_config_file_into_list(filename):
    output_list = []
    input_file = open(filename, "rb")
    for line in input_file:
        output_list.append(line.strip())
    return output_list

def extractReferenceCode(filename):
    '''
    takes filename as string
    returns reference code as string in format AAAA1111
    '''
    regex = re.compile('[A-Z]{4}[\d]{4}')
    result = regex.findall(filename)
    if len(result) != 1:
        print filename
        print result
        print len(result)
        raise Exception
    if len(result[0]) != 8:
        raise Exception
    return result[0]

def find_matching_filenames(filename_list, text_to_match):
    """
    find all filenames that match that pattern, returns them as a list
    """
    output_list = []
    for filename in filename_list:
        if text_to_match in filename:
            output_list.append(filename)
    return output_list

def flatten_list(input_list):
    """
    flattens a tiered list of lists into one list
    """
    # http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    if type(input_list) != list:
        raise Exception
    else:
        return [item for sublist in input_list for item in sublist]

# Exceptions

class NotImplementedException(Exception):
    def __init__(self):
        pass

class NoFilenamesException(Exception):
    def __init__(self):
        pass

class UnknownReferenceCodeException(Exception):
    def __init__(self):
        pass

class UnknownOutputFilenameException(Exception):
    def __init__(self):
        pass
# Main

def main():
    try:
        os.mkdir("output")
    except WindowsError:
        pass
    configuration = Configuration()
    combinator = Combinator()
    documents = create_document_objects(configuration)
    for filename in os.listdir(configuration.get_input_directory()):
        # configuration.get_input_directory()
        document = find_document(filename, documents, configuration)
        document.add_filename("".join([configuration.get_input_directory(),"/", filename]))
    for document in documents:
        document.sort_filenames(configuration)
    encrypted_pdfs = find_all_encrypted_pdfs(documents)
    if len(encrypted_pdfs) == 0:
        for document in documents:
            combinator.combine(document)
    else:
        print("encrypted pdfs found:")
        for filename in encrypted_pdfs:
            print filename
