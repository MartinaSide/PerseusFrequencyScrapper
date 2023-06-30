import csv
import xml.etree.ElementTree as ET
import os

def convert_xml_to_csv(xml_file, csv_file):
    if os.path.isfile(csv_file):
        print(f'Skipped: {csv_file} (File already exists)')
        return

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract data from XML and prepare rows
    rows = []
    for frequency in root.findall('.//frequency'):
        headword = frequency.find('lemma/headword').text
        short_definition = frequency.find('lemma/shortDefinition').text
        max_frequency = frequency.find('maxFrequency').text
        min_frequency = frequency.find('minFrequency').text
        weighted_frequency = frequency.find('weightedFrequency').text
        key_term_score = frequency.find('keyTermScore').text
        rows.append([headword, short_definition, max_frequency, min_frequency, weighted_frequency, key_term_score])

    # Write data to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['headword', 'shortDefinition', 'maxFrequency', 'minFrequency', 'weightedFrequency', 'keyTermScore'])
        writer.writerows(rows)

    print(f'CSV file "{csv_file}" created successfully.')


def convert_directory_xml_to_csv(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_file = os.path.join(root, file)
                csv_file = os.path.splitext(xml_file)[0] + '.csv'
                convert_xml_to_csv(xml_file, csv_file)

    print('Conversion completed for all XML files in the directory.')
