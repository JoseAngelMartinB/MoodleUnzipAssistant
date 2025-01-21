# MoodleUnzipAssistant

![Version](https://img.shields.io/badge/version-1.2.0-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)

![Last commit](https://img.shields.io/github/last-commit/JoseAngelMartinB/MoodleUnzipAssistant)
![Issues](https://img.shields.io/github/issues/JoseAngelMartinB/MoodleUnzipAssistant)
![Forks](https://img.shields.io/github/forks/JoseAngelMartinB/MoodleUnzipAssistant?style=social)
![Stars](https://img.shields.io/github/stars/JoseAngelMartinB/MoodleUnzipAssistant?style=social)

Python code for extracting and organizing student submissions from Moodle. It streamlines the process of decompressing the submissions, while intelligently categorizing them by class groups. All the student submissions must be a compressed ZIP file, otherwise they will be ignored.

## Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/JoseAngelMartinB/MoodleUnzipAssistant.git
   ```

2. Navigate to the repository directory:

   ```shell
   cd MoodleUnzipAssistant
   ```

3. Customize the parameters in the `MoodleUnzipAssistant.py` file according to your needs:

    ```shell
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
   students_file = "alumnos.csv"
   csv_group_column = "Group"
   csv_name_column = "Name"
   csv_surname_column = "Surname"
   
   # CSV separator
   csv_separator = ';'
   
   # Would you like to store the submissions depending on the group of the student?
   store_in_groups = True
   
   # Path to the log file that will be generated
   log_file = "log.txt"
   
   # Decompression mode: raw, sub-folders, remove-folders
   #   - raw: decompress everything as it is, without modifying anything
   #   - sub-folders: the subfolders of the zip files are joined to the file name
   #                  and copied to the parent directory
   #   - remove-folders: all subfolders are removed and everything is moved to the
   #                     parent directory
   decompresion_mode = "sub-folders"
   
   # Prevent the creation of a directory with the name of the zip file (only in raw
   # and sub-folders)
   prevent_parent_directory = True
    ```

4. Run the script:

   ```shell
   python MoodleUnzipAssistant.py
   ```

5. Check the generated log file for the results and any potential errors:

   ```shell
   cat log.txt
   ```


## Requirements

- Python 3.6 or higher
- Pandas


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Author

- José Ángel Martín Baos ([@JoseAngelMartinB](https://github.com/JoseAngelMartinB))
