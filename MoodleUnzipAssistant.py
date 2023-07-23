#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MoodleUnzipAssistant.py

Description: Python code for extracting and organizing student submissions from 
Moodle. It streamlines the process of decompressing the submissions, while 
intelligently categorizing them by class groups. All the student submissions
must be a compressed ZIP file, otherwise they will be ignored.

Version: 1.0.0 (June 2023)
License: MIT License
Author: José Ángel Martín Baos
"""

################################# PARAMETERS ##################################
# Path to the directory containing the submissions as downloaded from Moodle
input_dir = "MoodleFiles"

# Path to the directory where the decompressed submissions will be stored
output_dir = "output"

# Path to the directory where the submissions that could not be decompressed
# will be stored
error_dir = "Errors"

# Path to the file containing the list of students and their groups. This file
# should be a CSV file with the following columns:
#   - Group: Group of the student (only if store_in_groups is True, otherwise
#            this column will be ignored)
#   - Name: Name of the student
#   - Surname: Surname/s of the student
students_file = "students.csv"

# CSV separator
csv_separator = ';'

# Would you like to store the submissions depending on the group of the student?
store_in_groups = True

# Path to the log file that will be generated
log_file = "log.txt"
###############################################################################

# Import required libraries
import os
import zipfile
import re
import shutil
import unidecode
import pandas as pd

# Progress bar
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1,
                        length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar.
    """
    percent = ("{0:." + str(decimals) + "f}").format(
                100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Initialize log
log = {"extracted": {},
       "errors": {},
       "other_errors": {}
       }

# Create or clean output directories
if not os.path.exists(output_dir+'/'):
    os.makedirs(output_dir+'/')
else:
    shutil.rmtree(output_dir+'/')
    os.makedirs(output_dir+'/')
if not os.path.exists(error_dir+'/'):
    os.makedirs(error_dir+'/')
else:
    shutil.rmtree(error_dir+'/')
    os.makedirs(error_dir+'/')

# Read list of students and their groups
if store_in_groups:
    students = pd.read_csv(students_file, sep=csv_separator)
    students.replace('\s+', '_', regex=True, inplace=True)
    students['FullName'] = (students['Name'].apply(unidecode.unidecode) +
        '_' + students['Surname'].apply(unidecode.unidecode)) 
    students['FullName'] = students['FullName'].str.upper()                     

# Process each student and try to decompress their submissions
i = 0
for dir_student in os.scandir(input_dir):
    i += 1
    if dir_student.name.startswith('.'): # Ignore hidden files
        continue

    if dir_student.is_dir(): # Only process directories
        # Infer the name of the student from the name of the directory
        student_name = re.sub(r'_[0-9]+_assignsubmission_file_$', '', 
                              dir_student.name)
        student_name = unidecode.unidecode(student_name).replace(' ', '_')
        student_name = student_name.upper()
        # Print a progress bar
        printProgressBar(i, len(os.listdir(input_dir)), prefix = 'Progress:', 
                         suffix = 'Complete', length = 50)

        # Find the group of the student (if store_in_groups is True)
        if store_in_groups:
            group_search = students.loc[students['FullName'] == student_name].Group
            if not group_search.empty:
                group = group_search.iloc[0]
            else:
                group = "WithoutGroup"
        else:
            group = ""

        try:
            # Unzip all the files submitted by the student
            for student_submission in os.scandir(dir_student.path):
                with zipfile.ZipFile(student_submission.path, 'r') as zip_ref:
                    zip_ref.extractall('aux_files/'+student_name)

            # Copy the unzipped files to the output directory
            if not os.path.exists(output_dir+'/'+group+'/'+student_name+'/'):
                os.makedirs(output_dir+'/'+group+'/'+student_name+'/')
            for root, dirs, files in os.walk('aux_files/'+student_name+'/'):
                for file in files:
                    shutil.copy2(os.path.join(root,file), output_dir+'/'+group+'/'+student_name+'/'+file)

            log['extracted'][dir_student.name] = "Ok"
        except Exception as e:
            log['errors'][dir_student.name] = str(e)

            # Copy the erroneous submission to the error directory
            shutil.copytree(dir_student.path, error_dir+'/'+group+'/'+student_name+'/')

    else: # If it is not a directory, copy it to the error directory
        log['other_errors'][dir_student.name] = "This submission is not a directory"
        # Copiar archivos
        student_name = re.sub(r'_[0-9]+_assignsubmission_file_$', '', dir_student.name)
        student_name = unidecode.unidecode(student_name).replace(' ', '_')
        if not os.path.exists(error_dir+'/'+student_name+'/'):
            os.makedirs(error_dir+'/'+student_name+'/')
        shutil.copy2(dir_student.path, error_dir+'/'+student_name+'/')

# Delete auxiliar files
if os.path.exists('aux_files/') and os.path.isdir('aux_files/'):
    shutil.rmtree('aux_files/')

# Write log to file
output_str = ""
with open(log_file, 'w') as file:
    output_str += "\n CORRECTLY DECOMPRESSED:\n"
    for alu in log['extracted'].keys():
        output_str += "  + "+alu + ': ' + log['extracted'][alu] + "\n"

    output_str += "\n ERROR WHILE DECOMPRESSING:\n"
    for alu in log['errors'].keys():
        output_str += "  + "+alu + ': ' + log['errors'][alu] + "\n"

    output_str += "\n OTHER ERRORS:\n"
    for alu in log['other_errors'].keys():
        output_str += "  + "+alu + ': ' + log['other_errors'][alu] + "\n"

    output_str += "\n\n TOTAL SUBMISSIONS: " + str(len(log['extracted']) + 
                                                   len(log['errors']) + 
                                                   len(log['other_errors'])) 
    output_str += "\n CORRECTLY DECOMPRESSED: " + str(len(log['extracted'])) +\
                  "\n ERROR WHILE DECOMPRESSING: " + str(len(log['errors'])) +\
                  "\n OTHER ERRORS: " + str(len(log['other_errors'])) +\
                  "\n The results are stored in the following directories:\n" +\
                  "  - Correctly decompressed: " + output_dir + "\n" +\
                  "  - Error while decompressing: " + error_dir + "\n" +\
                  "  - Other errors: " + error_dir + "\n"
    file.write(output_str)


print('\n'+'-'*50)
print('TOTAL SUBMISSIONS: ' + str(len(log['extracted']) +
                                  len(log['errors']) +
                                  len(log['other_errors'])))
print('CORRECTLY DECOMPRESSED: ' + str(len(log['extracted'])))
print('ERROR WHILE DECOMPRESSING: ' + str(len(log['errors'])) + ":")
for alu in log['errors'].keys():
    print("  - "+alu + ': ' + log['errors'][alu])

print('OTHER ERRORS: ' + str(len(log['other_errors'])) + ":")
for alu in log['other_errors'].keys():
    print("  - "+alu + ': ' + log['other_errors'][alu])

print('--Please solve the previous errors manually--')
