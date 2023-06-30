import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import re


def get_perseus_work_info_trResults():
    """
    Scrapes Perseus Digital Library to retrieve work information from the table rows with class "trResults".

    Returns:
        A list of tuples containing the extracted work information.

    Each tuple in the list represents a work and contains the following information:
    - Language of the work (Greek, Latin, or English)
    - Author of the work
    - Title of the work
    - Work ID

    Note:
    - The method targets the Perseus Digital Library website for Greco-Roman works.
    - It extracts the link, language, author, and title from the table rows with class "trResults".
    - The language is determined by searching for keywords (Greek, Latin, or English) in the next line after the link.
    - The extracted work information is returned as a list of tuples.
    """

    url = 'http://www.perseus.tufts.edu/hopper/collection%3Fcollection%3DPerseus:collection:Greco-Roman'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    work_info = []

    # Find all the table rows with class "trResults"
    rows = soup.find_all('tr', class_='trResults')

    for row in rows:
        # Extract the link, language, author, and title from the row if available
        link = row.find('a', class_='aResultsHeader')
        if link:
            href = link.get('href')
            work_id = urllib.parse.unquote(href.split('doc=')[1])
            author_elem = row.find('td', class_='tdAuthor')
            if author_elem:
                author = author_elem.text.strip().split('\n')[0]
                title = link.text.strip()

                # Find the next line after the link to determine the language
                language_elem = link.find_next_sibling(string=True)
                if language_elem:
                    language = re.search(r'(Greek|Latin|English)', language_elem)
                    language = language.group() if language else ''
                else:
                    language = ''

                work_info.append((language, author, title, work_id))

    return work_info


def save_work_info_to_csv(work_info):
    """
    Saves the work information to a CSV file named 'workInfo.csv'.

    Args:
        work_info: A list of tuples containing the work information.

    The method writes the work information to a CSV file with the following columns:
    - Language
    - Author
    - Title
    - Work ID

    Note:
    - The CSV file is created with the 'utf-8' encoding.
    - The method assumes that the work_info list is in the correct format.
    - The CSV file is saved as 'workInfo.csv' in the current directory.
    - The method prints a message after successfully saving the work information to the file.
    """

    with open('workInfo.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Language', 'Author', 'Title', 'Work ID'])
        for info in work_info:
            writer.writerow(info)

    print("Work information saved to workInfo.csv file.")


def get_perseus_work_info_trHiddenResults():
    """
    Retrieves work information from the Perseus website for table rows with class "trHiddenResults".

    Returns:
        A list of tuples containing the work information in the format (language, author, title, work_id).

    This method specifically targets <tr> tags with class="trHiddenResults" on the Perseus website.
    It retrieves the link, language, author, and title from each row and extracts the necessary information.

    Note:
    - The method uses regular expressions and BeautifulSoup for parsing and extracting information.
    - The work information is returned as a list of tuples.
    """

    url = 'http://www.perseus.tufts.edu/hopper/collection%3Fcollection%3DPerseus:collection:Greco-Roman'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    work_info = []

    # Find all the table rows with class "trHiddenResults"
    rows = soup.find_all('tr', class_='trHiddenResults')

    for row in rows:
        # Extract the link, language, author, and title from the row if available
        link = row.find('a', class_='aResultsHeader')
        if link:
            href = link.get('href')
            work_id = urllib.parse.unquote(href.split('doc=')[1])

            # Extract the author from the 'id' attribute of the row
            author_match = re.search(r'id="([^"]+)"', str(row))
            author = author_match.group(1) if author_match else ''

            # Remove numbers and commas followed by a number from the author string
            author = re.sub(r'\b\d+\b|,\d+', '', author)

            title = link.text.strip()

            # Find the next line after the link to determine the language
            language_elem = link.find_next_sibling(string=True)
            if language_elem:
                language_match = re.search(r'(Greek|Latin|English)', language_elem)
                language = language_match.group() if language_match else ''
            else:
                language = ''

            work_info.append((language, author, title, work_id))

    return work_info


def get_perseus_work_info():
    """
    Retrieves work information from the Perseus website for both table rows with class "trResults" and "trHiddenResults"

    Returns:
        A list of tuples containing the work information in the format (language, author, title, work_id).

    This method combines the work information retrieved from both table row classes "trResults" and "trHiddenResults"
    on the Perseus website and returns the merged result.

    Note:
    - The method calls the helper methods get_perseus_work_info_trResults() and get_perseus_work_info_trHiddenResults().
    - The work information is returned as a list of tuples.
    """

    temp_work_info = get_perseus_work_info_trResults()
    temp_work_info += get_perseus_work_info_trHiddenResults()
    return temp_work_info


def split_work_info_file(input_file, output_file_gr, output_file_lat):
    """
    Splits the work info file into separate files based on the language (Greek and Latin).

    Args:
        input_file (str): Path to the input work info file.
        output_file_gr (str): Path to the output file for Greek works.
        output_file_lat (str): Path to the output file for Latin works.

    This method reads the input work info file and splits the rows into separate files based on the language column.
    Greek works are saved in the output_file_gr, and Latin works are saved in the output_file_lat.

    Note:
    - The input file is assumed to have a header row.
    - The language column is expected to be in the first position (index 0) in each row.
    """

    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip the header row

        with open(output_file_gr, 'w', newline='', encoding='utf-8') as csvfile_gr, \
                open(output_file_lat, 'w', newline='', encoding='utf-8') as csvfile_lat:
            writer_gr = csv.writer(csvfile_gr, delimiter=',')
            writer_lat = csv.writer(csvfile_lat, delimiter=',')
            writer_gr.writerow(['Work ID', 'Language', 'Author', 'Title'])
            writer_lat.writerow(['Work ID', 'Language', 'Author', 'Title'])

            for row in reader:
                language = row[0]
                if language == 'Greek':
                    writer_gr.writerow(row)
                elif language == 'Latin':
                    writer_lat.writerow(row)
