import os
import csv
from collections import Counter
import shutil


def delete_lines_with_duplicate_word(input_file):
    output_file = f"{input_file}.tmp"  # Temporary file to store filtered lines

    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row

        word_column_index = 0  # Assuming the word is in the first column
        lines_to_keep = []
        word_counts = Counter()

        # Iterate over each row in the CSV file
        for row in reader:
            word = row[word_column_index]
            word_counts[word] += 1

            # Keep the line if it's the first occurrence of the word
            if word_counts[word] == 1:
                lines_to_keep.append(row)

    # Write the filtered lines to the temporary file
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(lines_to_keep)

    # Replace the input file with the temporary file
    shutil.move(output_file, input_file)

    print(f"Lines with duplicate words deleted from the file: {input_file}")


def eliminate_words(input_dir, words_file):
    # Read the words to eliminate from the file
    with open(words_file, 'r', encoding='utf-8') as words_csv:
        words_reader = csv.reader(words_csv, delimiter=',')
        next(words_reader)  # Skip the header row
        words_to_eliminate = set([row[0] for row in words_reader])

    # Recursively iterate over the directory and process CSV files
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name == 'greek - wordsToEliminate.csv':
                continue

            if file_name.endswith('.csv') and not file_name.endswith('- cleaned.csv'):
                input_file = os.path.join(root, file_name)
                output_file = os.path.join(root, file_name.replace('.csv', ' - cleaned.csv'))

                with open(input_file, 'r', encoding='utf-8') as input_csv, \
                        open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
                    reader = csv.reader(input_csv, delimiter=',')
                    writer = csv.writer(output_csv, delimiter=',')
                    for row in reader:
                        if row[0] not in words_to_eliminate:
                            writer.writerow(row)
                delete_lines_with_duplicate_word(output_file)
                remove_columns(output_file)

                print(f'{file_name} cleaned and saved as {output_file}')


def eliminate_cleaned_files(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('- cleaned.csv'):
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f'Removed file: {file_path}')


def delete_non_cleaned_files(folder):
    # Recursively traverse the directory and process files
    for root, dirs, files in os.walk(folder):
        for file in files:
            # Check if the file doesn't end with '- cleaned.csv'
            if not file.endswith('- cleaned.csv'):
                file_path = os.path.join(root, file)
                # Remove the file
                os.remove(file_path)
                print(f'Deleted: {file_path}')


def remove_columns(csv_file):
    # Read the CSV file
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Create new rows with desired columns
        rows = [row[:1] + row[3:5] for row in reader]

    # Write the modified rows back to the CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f'Columns removed successfully from "{csv_file}".')
