combinator.py
=============

1) Set up configuration files:

application_filenames.txt:

Tab-delimited list of application reference codes and output filenames. These will be used for the output filenames of the combined documents. Example:

AJDK5462	Some_Application_John_Smith_AJDK5462  
SLE82654	Some_Application_Jim_John_SLE82654  
ALDJ2136	Some_Application_Elon_Musk_ALDJ2136  

document_order.txt:

List of document identifiers in a given order. Matching documents will be sorted according to this order, nonmatching documents will be sorted, alphabetically, to the end. Example:

Application
UpResume
UpPassport
Recommendation

documents_to_ignore.txt:

List of document identifiers that can be ignored. This list will be matched against input document filenames; any matching filenames will be ignored. Example:

UpADocumentToIgnore
AndAnotherOne

recommendation_application_associations.txt:

Tab-delimited list of reference codes. First column is recommendation reference codes, second column is application reference codes. Example:

AJDK5462	SJDK2136
SLE82654	SCIE9643
ALDJ2136	POEU2146

2) Input documents, as PDF, into combinator/input

3) command line: python combinator.py
