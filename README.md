# pie-sort
Source code for pie-sort a pdf information extraction and sorting tool for Medical Offices.

# Motivation
Document management is a growing issue in the health care industry.
Systems to manage this information are changing faster than they can be uniformly implemented.
Patient information communicated between offices, must be sorted to each patient in each office database.
This procedure is not standardized and requires valuable clinic resources.

Pie-sort's aim is to automate the process of merging scanned documents into medical office databases.
This accomplished by using OCR and NLP libraries to extract names, PHNs (Personal Health Numbers) and
DOB (Date of Birth) from scanned documents and match them to current patient databases.

# Technologies
Project is created with:
* Python 3.7
* Tesseract - OCR (pytesseract 0.2.6)
* NLTK (3.4.3)
* spaCey (2.1.4)

# How it works
1. To run this program locally install by cloning basic pipeline repository
    ```shell
    git clone -b basic https://github.com/pistanic/pie-sort.git
    ```
1. Create MISC folder in project directory with "tmp" and "PDF" folders inside.
1. Move PDF documents to be sorted will be stored in the "PDF Folder."
1. Install required dependencies.
1. When run the pipeline will test possible PHNs and names against the test
patient database defined in "searchHelp" module and output validated patients to the terminal.

# Project Status
 The basic pipeline is a simple verification algorithm, which uses the
 Hello World pipeline with the addition of image preprocessing and a
 PHN verification. This pipeline provides a level of
 pipeline accuracy and success that will be improved upon in the future pipelines.

# Authors
**Nicholas Forest** - [Pistanic](https://github.com/pistanic)
**Jakob Mawdsley** - [JollyJellyBean](https://github.com/JollyJellyBean)
**David Cheng** - [ChengDave](https://github.com/ChengDave)
**Siddharth Verma** - [SidVerma27](https://github.com/sidverma27)

# License
This program is released under the GPLV3 license
