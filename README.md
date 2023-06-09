# MoodleUnzipAssistant

![Version](https://img.shields.io/badge/version-1.0.0-blue)
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
    # Configure parameters
    input_dir = "MoodleFiles"
    output_dir = "output"
    error_dir = "Errors"
    students_file = "students.csv"
    csv_separator = ';'
    store_in_groups = True
    log_file = "log.txt"
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
