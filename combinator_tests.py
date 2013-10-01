from combinator import Configuration, Document, should_be_ignored
import unittest

class Configuration_Tests(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration("./test_config")
    def test_get_input_directory(self):
        assert self.configuration.get_input_directory() == "./input"
    def test_get_documents_to_ignore(self):
        assert self.configuration.get_documents_to_ignore() == ["UpADocumentToIgnore",
        "AndAnotherOne"]
    def test_get_recommendation_application_associations(self):
        assert self.configuration.get_recommendation_application_associations() == {"AJDK5462":"SJDK2136",
        "SLE82654":"SCIE9643",
        "ALDJ2136":"POEU2146",
        "CJEU3216":"PSOF3215",
        "SLDK2643":"AODJ5468"}
    def test_get_application_filenames(self):
        assert self.configuration.get_application_filenames() == {"AJDK5462":"Some_Application_John_Smith_AJDK5462",
        "SLE82654":"Some_Application_Jim_John_SLE82654",
        "ALDJ2136":"Some_Application_Elon_Musk_ALDJ2136",
        "CJEU3216":"Some_Application_Old_Man_Winter_CJEU3216",
        "SLDK2643":"Some_Application_The_Friend_SLDK2643"}
    def test_get_document_order(self):
        assert self.configuration.get_document_order() == ["Application",
        "Up Resume",
        "UpPassport",
        "Recommendation"]

class Document_Tests(unittest.TestCase):
    def setUp(self):
        self.document = Document("ABCD2356","Some_Application_Neal_Knight_ABCD2356.pdf")
        self.configuration = Configuration("./test_config")
    def test_contains_encrypted_pdfs(self):
        assert self.document.contains_encrypted_pdfs() == False
    def test_find_encrypted_pdfs(self):
        assert self.document.find_encrypted_pdfs() == []
    def test_get_filenames(self):
        assert self.document.get_filenames() == []
    def test_add_filename(self):
        assert self.document.get_filenames() == []
        self.document.add_filename("here_is_a_file.txt")
        self.document.add_filename("here's_another_one.pdf")
        assert len(self.document.get_filenames()) == 2
        assert "here_is_a_file.txt" in self.document.get_filenames()
    def test_sort_filenames(self):
        self.document.add_filename("here_is_a_file.txt")
        self.document.add_filename("here's_another_one.pdf")
        self.document.add_filename("Application_45632.friend")
        self.document.add_filename("some_Recommendation.ext")
        assert self.document.get_filenames() == ["here_is_a_file.txt",
        "here's_another_one.pdf",
        "Application_45632.friend",
        "some_Recommendation.ext"]
        self.document.sort_filenames(self.configuration)
        assert self.document.get_filenames() == ["Application_45632.friend",
        "some_Recommendation.ext",
        "here's_another_one.pdf",
        "here_is_a_file.txt"]
    def test_get_applicant_reference_code(self):
        assert self.document.get_applicant_reference_code() == "ABCD2356"
    def test_get_output_filename(self):
        assert self.document.get_output_filename() == "Some_Application_Neal_Knight_ABCD2356.pdf"

class Should_Be_Ignored_Tests(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration("./test_config")
    def test_should_be_ignored(self):
        assert should_be_ignored("something_UpADocumentToIgnore_something",self.configuration) == True

if __name__ == "__main__":
    unittest.main()
