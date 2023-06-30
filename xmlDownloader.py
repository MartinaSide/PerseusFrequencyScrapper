import csv
import requests
import os


def fetch_text_frequencies(csv_file, lang, folder):
    base_url = 'https://www.perseus.tufts.edu/hopper/vocablist'

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip the header row

        for row in reader:
            works = row[3]
            author = row[1]
            title = row[2]

            # Create the directory path for saving the XML file
            directory = f'{folder}/{lang}/{author}'
            os.makedirs(directory, exist_ok=True)

            # Construct the query parameters
            params = {
                'works': works,
                'sort': 'weighted_freq',
                'filt': '100',
                'filt_custom': '',
                'output': 'xml',
                'lang': lang
            }

            # Define the file name
            file_name = f'{author} - {title} - Pure freq.xml'
            file_path = os.path.join(directory, file_name)

            if os.path.isfile(file_path):
                print(f'Skipped: {file_name} (File already exists)')
            else:
                response = requests.get(base_url, params=params)
                xml_data = response.text

                # Save the XML file
                with open(file_path, 'w', encoding='utf-8') as xml_file:
                    xml_file.write(xml_data)

                print(f'Saved: {file_name}')


def delete_small_xml_files(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) < 10 * 1024:  # Check if file size is smaller than 2 KB
                    os.remove(file_path)
                    print(f'Deleted: {file_path}')


def delete_empty_folders(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if the folder is empty
                os.rmdir(dir_path)
                print(f'Deleted empty folder: {dir_path}')
