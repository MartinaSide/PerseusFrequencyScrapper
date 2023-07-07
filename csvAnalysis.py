import os
import pandas as pd
import numpy as np
import csv


def merge_csv_files(csv_directory, output_file):
    # Initialize variables to store data and headers
    data_list = []
    headers = ["headword", "shortDefinition"]

    # Traverse the specified directory and its subdirectories
    for root, dirs, files in os.walk(csv_directory):
        for file in files:
            # Check if the file ends with "- cleaned.csv"
            if file.endswith("- cleaned.csv"):
                # Build the full file path
                file_path = os.path.join(root, file)

                # Read the current CSV file as a DataFrame
                current_data = pd.read_csv(file_path)

                # Extract author and title from the file name
                file_parts = os.path.splitext(os.path.basename(file))[0].split(" - ")
                author_title = "-".join(file_parts[:2])

                # Add a new column for author and title
                current_data["Author_Title"] = author_title

                # Append the current DataFrame to the list
                data_list.append(current_data)

                # Add author and title to the headers
                headers.append(author_title)

    # Check if any cleaned CSV files were found
    if not data_list:
        print("No cleaned CSV files found in the specified directory.")
        return

    # Concatenate all DataFrames into a single DataFrame
    merged_data = pd.concat(data_list, ignore_index=True)

    # Create an empty DataFrame with the headers
    data = pd.DataFrame(columns=headers)
    data.to_csv(output_file, index=False)

    # Iterate over each row in the merged data
    for _, row in merged_data.iterrows():
        col_to_modify = row[3]
        if col_to_modify in headers:
            col_index = headers.index(col_to_modify)

            # Create a new row with zeros for all columns
            row_data = [0] * len(headers)
            row_data[0] = row[0]  # Copy headword
            row_data[1] = row[1]  # Copy shortDefinition
            row_data[col_index] = row[2]  # Set the value of the matching column

            # Append the row to the output CSV file
            with open(output_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(row_data)

    # Read the temporary output file into a DataFrame
    temp_data = pd.read_csv(output_file)

    # Group the data by headword and shortDefinition, and sum the values
    temp_data = temp_data.groupby(headers[:2]).sum().reset_index()

    # Drop duplicate rows based on the headword column
    temp_data.drop_duplicates(subset=headers[0], keep="first", inplace=True)

    # Write the final merged data to the output file
    temp_data.to_csv(output_file, index=False)

    print("CSV files merged successfully.")


def calculate_percentages(input_file, output_file):
    data = pd.read_csv(input_file)
    percent_data = data.copy()
    numeric_cols = percent_data.columns

    for col in numeric_cols:
        print(col)
        percent_data[col] = (percent_data[col] / percent_data[col].sum()) * 100
        percent_data[col] = percent_data[col].apply(lambda x: f"{x:.4f}")

    percent_data.to_csv(output_file, index=False)

    print("Percentages calculated and written to file.")


def add_progressive_numbering(input_file, output_file_dict, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as input_csv, \
            open(output_file_dict, 'w', newline='', encoding='utf-8') as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)

        # Write header row to the output file
        header = next(reader)
        writer.writerow(header[:2] + ['Number'])

        # Write data rows with progressive numbering
        for i, row in enumerate(reader, start=1):
            writer.writerow(row[:2] + [i])

    print(f"Progressive numbering added to '{output_file_dict}'.")

    # Remove the first two columns from the input file
    with open(input_file, 'r', newline='', encoding='utf-8') as input_csv, \
            open(output_file, "w", newline='', encoding="utf-8") as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)
        # next(reader)  # Skip the header row
        for row in reader:
            writer.writerow(row[2:])

    print(f"First two columns removed from '{output_file}'.")


def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    similarity = 0
    if norm_product != 0:
        similarity = dot_product / norm_product
    return similarity


def calculate_similarity_matrix(input_file, output_file):
    # Read the input data into a DataFrame
    data = pd.read_csv(input_file)

    # Write the first row of data to the output file
    first_row = data.columns.values
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)

    # Compute the similarity matrix between each pair of columns
    similarity_matrix = np.zeros((data.shape[1], data.shape[1]))
    for i in range(0, data.shape[1]):
        for j in range(i, data.shape[1]):
            similarity_value = cosine_similarity(data.iloc[:, i].values, data.iloc[:, j].values)
            similarity_matrix[i, j] = similarity_value
            similarity_matrix[j, i] = similarity_value

    # Append the similarity matrix to the output file
    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(similarity_matrix)
