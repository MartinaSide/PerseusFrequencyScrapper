import getIDs
import xmlToCsv
import xmlDownloader
import removeUselessData
import csvAnalysis
import winsound
import os


def run_all(work_directory, delete_files=False):
    # STEP 1: DOWNLOAD THE LIST OF WORKS WITH THE IDs FROM THE WEBSITE AND SAVE THE RESULT

    work_info = getIDs.get_perseus_work_info()

    getIDs.save_work_info_to_csv(work_info)

    getIDs.split_work_info_file('workInfo.csv', 'work_info_gr.csv', 'work_info_lat.csv')

    # delete the useless file that contains the list of IDs not split
    os.remove('workInfo.csv')

    work_directory = os.path.join(work_directory, "classicalTextFrequencies")

    xmlDownloader.delete_small_xml_files(work_directory)

    # create all .csv files
    xmlDownloader.fetch_text_frequencies("work_info_lat.csv", "latin", work_directory)
    xmlDownloader.fetch_text_frequencies("work_info_gr.csv", "greek", work_directory)
    xmlDownloader.delete_small_xml_files(work_directory)
    xmlDownloader.delete_empty_folders(work_directory)

    # delete the id for Greek and Latin
    if delete_files:
        os.remove("work_info_lat.csv")
        os.remove("work_info_gr.csv")

    # STEP 2: CREATE THE .CSV FILES

    xmlToCsv.convert_directory_xml_to_csv(work_directory)

    work_directory_gr = os.path.join(work_directory, "greek")
    work_directory_lat = os.path.join(work_directory, "latin")

    removeUselessData.eliminate_words(work_directory_gr, "gr - wordsToEliminate.csv")

    output_directory_gr = os.path.join(work_directory, "greek output")
    output_directory_lat = os.path.join(work_directory, "latin output")
    os.makedirs(output_directory_gr, exist_ok=True)
    os.makedirs(output_directory_lat, exist_ok=True)

    output_directory_gr_auth = os.path.join(output_directory_gr, "By Author")
    output_directory_gr_filt = os.path.join(output_directory_gr, "All Works - Filtered")
    output_directory_gr_pure = os.path.join(output_directory_gr, "All Works - pure")
    output_directory_lat_pure = os.path.join(output_directory_lat, "All works")

    try:
        os.makedirs(output_directory_gr_auth, exist_ok=True)
    except:
        pass

    try:
        os.makedirs(output_directory_gr_filt, exist_ok=True)
    except:
        pass

    try:
        os.makedirs(output_directory_gr_pure, exist_ok=True)
    except:
        pass

    try:
        os.makedirs(output_directory_lat_pure, exist_ok=True)
    except:
        pass

    csvAnalysis.merge_all_by_author(work_directory_gr, output_directory_gr_auth)
    csvAnalysis.delete_files_with_pattern(work_directory_gr)

    winsound.Beep(800, 1000)

    csvAnalysis.merge_csv_files(work_directory_gr, os.path.join(output_directory_gr_filt, "- all freq.csv"))
    csvAnalysis.delete_files_with_pattern(work_directory_gr, "- cleaned.csv")

    winsound.Beep(800, 1000)

    removeUselessData.clean_columns_but_keep_all_data(work_directory_gr)
    csvAnalysis.merge_all_csv_files(work_directory_gr, os.path.join(output_directory_gr_pure, "- all freq.csv"))

    winsound.Beep(800, 1000)

    removeUselessData.clean_columns_but_keep_all_data(work_directory_lat)
    csvAnalysis.merge_all_csv_files(work_directory_lat, os.path.join(output_directory_lat_pure, "- all freq.csv"))

    winsound.Beep(800, 1000)

    if delete_files:
        os.remove(work_directory_gr)
        os.remove(work_directory_lat)

    create_Dataset(output_directory_gr_auth)
    create_Dataset(output_directory_gr_filt)
    create_Dataset(output_directory_gr_pure)

    winsound.Beep(800, 1000)


def create_Dataset(directory):
    csvAnalysis.add_progressive_numbering(os.path.join(directory, "- all freq.csv"),
                                          os.path.join(directory, "- dictionary.csv"),
                                          os.path.join(directory, "- all freq no dict.csv"))

    csvAnalysis.calculate_percentages(os.path.join(directory, "- all freq no dict.csv"),
                                      os.path.join(directory, "- all perc.csv"))

    csvAnalysis.calculate_similarity_matrix(os.path.join(directory, "- all perc.csv"),
                                            os.path.join(directory, "- similarity matrix.csv"))


# USE RUN ALL
