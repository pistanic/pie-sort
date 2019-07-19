#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Nicholas Forest                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################

# Document Managment module.
import tempfile
from datetime import datetime
from os import listdir, remove, rename, makedirs
from os.path import isfile, join, splitext, basename
from shutil import rmtree
from pdf2image import convert_from_path
import pandas as pd
from dateutil.parser import parse

# INPUT: excel_path - Path to patient database excel file
# OUTPUT: df - Patient dataframe in correct format for validation
# DESCRIPTION: This function imports the patient database and returns a formatted dataframe
def init_validation_df(excel_path):
    patient_df = pd.read_excel(excel_path) # need to reformat 'PatientName' and 'DOB' columns

    # Transform patient name into "Last_Name", "Middle_Name" and "First_Name" columns in title case
    name_patient_df = patient_df['PatientName'].str.split(",", n = 1, expand = True)
    patient_df['Last_Name'] = name_patient_df[0]
    patient_df['Last_Name'] = patient_df['Last_Name'].str.title()
    patient_df['First_Middle'] = name_patient_df[1]
    patient_df.drop(columns=['PatientName'], inplace=True)
    name_patient_df = patient_df['First_Middle'].str.split(" ", expand = True)
    patient_df['First_Name'] = name_patient_df[1]
    patient_df['Middle_Name'] = name_patient_df[2]
    patient_df.drop(columns=['First_Middle'], inplace=True)
    patient_df['First_Name'] = patient_df['First_Name'].str.title() # convert to title case
    patient_df['Middle_Name'] = patient_df['Middle_Name'].str.title()
    patient_df['First_Name'] = patient_df['First_Name'].str.strip() # strip leading and trailing spaces
    patient_df['Middle_Name'] = patient_df['Middle_Name'].str.strip()

    # Transform date of birth into 'DOB-YYYY', 'DOB-MM', 'DOB-DD'  columns in correct format
    dates_df = pd.DataFrame(columns=['DOB-YYYY', 'DOB-MM', 'DOB-DD'])

    dates_ls = patient_df['DOB'].tolist()

    # Convert unformatted dates to ISO 8601 format (YYYY-MM-DD) using EAFP practice (easier to ask forgiveness than permission)
    for date in dates_ls:
        try:
            obj = parse(date.__str__())
            new_date_df = pd.DataFrame({'DOB-YYYY': [str(obj.strftime('%Y'))],
                                        'DOB-MM': [str(obj.strftime('%m'))],
                                        'DOB-DD': [str(obj.strftime('%d'))]})
            dates_df = dates_df.append(new_date_df, ignore_index=True)

        except ValueError:
            print("init_validation_df debug - '" + date.__str__() + "' is not in a readable date format")

    patient_df.join(dates_df)
    patient_df.drop(columns=['DOB'], inplace=True)

    patient_df = patient_df.applymap(str) # converts data to string format

    return patient_df



# INPUT: List of dirs to create
def init_folders(dir_list):
    for dir_ in dir_list:
        try:
            makedirs(dir_)
        except:
            print('file directory already exists')

# INPUT: Path to files
# OUTPUT: List of files in path
def get_file_list(path):
    fileList = [f for f in listdir(path) if isfile(join(path,f))]
    return fileList

# INPUT: Path to image folder
# OUTPUT: list of images in folder
def get_image_name(path):
    return get_file_list(path)

# INPUT: Path to be removed
def delete_dir(path):
    rmtree(path)

# INPUT: Path to to removed
def delete_file(path):
    remove(path)

# INPUT: pdf_path - path to PDF
#        jpg_path - path to store .jpg
# OUTPUT: base_filename - <file_name>.jpg
# DESCRIPTION: This function converts a PDF to JPG image format.
def pdf2jpg(pdf_path, jpg_path):
    #PDF to JPG
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(pdf_path, dpi=200, output_folder=path) #PDF to PIL image output

    base_filename = splitext(basename(pdf_path))[0]

    try:
        makedirs(join(jpg_path, base_filename))
    except:
        print('file directory already exists')

    for i, page in enumerate(images_from_path):
        page.save(join(jpg_path,base_filename,base_filename +'_page'+str(i+1)+'.jpg'), 'JPEG')

    print('pdf2jpg debug - base_filename: ',base_filename)

    return base_filename

# INPUT file_name: name of file
#       sort_path: path file was sorted to
# DESCRIPTION: Log the location a file was sorted to.
# log file is placed in top dir of program execution
def log(file_name, sort_path):
    log_path = 'log/'+str(datetime.now().date())+'/'
    try:
        makedirs(log_path)
    except:
        print('log dir already exists')

    log_file = log_path+'Verification-log.txt'
    file = open(log_file, 'w')
    file.write(file_name + ' sorted to: '+ sort_path+'\n')
    file.close

# INPUT source_path: path to file
#       dist_path: destination path for file
def sort(source_path, dist_path):
    base_filename = basename(source_path)
    dist_dir = dist_path.replace(base_filename,'') #strip filename
    try:
        makedirs(dist_dir)
    except:
        print('Patient dir already exists')
    log(base_filename, dist_path)
    rename(source_path, dist_path)


# DEBUG FUNCTION:
# This function is used to unsort documents.
def un_sort(source_path, dist_path):
    print('DEBUG! - PDF HAS BEEN RETURNED TO ORG LOCATION')
    rename(source_path, dist_path)
