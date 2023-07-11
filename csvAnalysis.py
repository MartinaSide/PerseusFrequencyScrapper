import os
import shutil

import pandas as pd
import numpy as np
import csv


def merge_csv_files(csv_directory: object, output_file: object, pattern: object = "- cleaned.csv") -> object:
    # Initialize variables to store data and headers
    data_list = []
    headers = ["headword", "shortDefinition"]

    # Traverse the specified directory and its subdirectories
    for root, dirs, files in os.walk(csv_directory):
        for file in files:
            # Check if the file ends with "- cleaned.csv"
            if file.endswith(pattern):
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


def merge_all_csv_files(csv_directory, output_file, pattern=".csv"):
    # Initialize variables to store data and headers
    data_list = []
    headers = ["headword", "shortDefinition"]

    # Traverse the specified directory and its subdirectories
    for root, dirs, files in os.walk(csv_directory):
        for file in files:
            # Check if the file ends with "- cleaned.csv"
            if file.endswith(pattern):
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


def delete_files_with_pattern(dir, pattern="- freq author"):
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if pattern in filename:
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        for folder in dirs:
            if pattern in folder:
                folder_path = os.path.join(root, folder)
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")


def merge_csv_files_by_author(folder_path, output_file, pattern="- cleaned.csv"):
    # Initialize variables to store data and headers
    data_list = []
    headers = ["headword", "shortDefinition"]

    # Traverse the specified folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(pattern):
            file_path = os.path.join(folder_path, file_name)

            # Read the current CSV file as a DataFrame
            current_data = pd.read_csv(file_path)

            # Extract the author from the folder name
            author = os.path.basename(folder_path)

            # Add a new column for author
            current_data["author"] = author

            # Append the current DataFrame to the list
            data_list.append(current_data)

            # Add author to the headers
            headers.append(author)

    # Check if any CSV files were found
    if not data_list:
        print("No CSV files found in the specified folder.")
        return

    # Concatenate all DataFrames into a single DataFrame
    merged_data = pd.concat(data_list, ignore_index=True)

    # Create an empty DataFrame with the headers
    data = pd.DataFrame(columns=headers)
    data.to_csv(output_file, index=False)

    # Iterate over each row in the merged data
    for _, row in merged_data.iterrows():
        col_to_modify = row[3]  # Assuming the data starts from the fourth column
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

    # Sum the values for numeric columns after the second one (author column)
    numeric_cols = temp_data.columns[2:].tolist()
    temp_data[numeric_cols] = temp_data[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Group by "author" column and sum the numeric columns
    temp_data[2] = temp_data.iloc[1:, 2:].sum()

    # Write the final merged and summed data to the output file
    temp_data.iloc[:, 0:3].to_csv(output_file, index=False)

    print("CSV files merged and columns summed successfully.")


def merge_all_by_author(folder_path, out_loc, pattern="- cleaned.csv", reverse=False):
    os.makedirs(out_loc, exist_ok=True)
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            file_name = dir + " - freq author" + ".csv"
            dir_loc = os.path.join(root, dir)
            file_loc = os.path.join(out_loc, file_name)
            print(file_name)
            merge_csv_files_by_author(dir_loc, file_loc)
    merge_authors(out_loc,
                  os.path.join(out_loc, "- all freq.csv"),
                  pattern=" - freq author.csv")


def merge_authors(csv_directory, output_file, pattern="- cleaned.csv"):
    # Find files that match the pattern in the specified directory
    files = [file for file in os.listdir(csv_directory) if file.endswith(pattern)]

    # Check if any cleaned CSV files were found
    if not files:
        print("No cleaned CSV files found in the specified directory.")
        return

    # Initialize variables to store data and headers
    data_list = []
    headers = ["headword", "shortDefinition"]

    # Read and process each file
    for i, file in enumerate(files):
        # Build the full file path
        file_path = os.path.join(csv_directory, file)

        # Read the current CSV file as a DataFrame
        current_data = pd.read_csv(file_path)

        # Extract the column name for the current file
        column_name = os.path.splitext(file)[0]

        # Create a new column for the current file
        current_data[column_name] = current_data.iloc[:, 2]

        # Fill empty positions with zeros
        current_data[column_name].fillna(0, inplace=True)

        # Append the current DataFrame to the list
        data_list.append(current_data)

        # Add the current column name to the headers
        headers.append(column_name)

    # Concatenate all DataFrames into a single DataFrame
    merged_data = pd.concat(data_list, ignore_index=True)

    # Remove columns whose first row contains "freq author"
    merged_data = merged_data.loc[:, ~merged_data.columns.str.contains("freq author")]

    # Group the data by headword and shortDefinition, and sum the values
    merged_data = merged_data.groupby(headers[:2]).sum().reset_index()

    # Write the merged data to the output file
    merged_data.to_csv(output_file, index=False)

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

    get_headers(output_file)
    remove_first_row(output_file)


def prepend_vector_to_csv(input_file, output_file):
    # Read the existing CSV file
    with open(input_file, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Extract the first row of data
    first_row = data[0]

    # Prepend the vector with 0 as the first element
    vector = [str(0)] + first_row

    # Insert the vector as the first column in the data
    for row in data:
        row.insert(0, vector[data.index(row)])

    # Write the data to the output CSV file
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("Vector prepended to the CSV file successfully.")


def get_headers(input_file):
    with open(input_file, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    first_row = data[0]

    dir_name = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    output_name = os.path.splitext(base_name)[0] + " - headers.csv"
    output_path = os.path.join(dir_name, output_name)

    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)


def remove_first_row(csv_file):
    with open(csv_file, 'r') as file:
        rows = list(csv.reader(file))

    if len(rows) > 1:
        rows = rows[1:]

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
