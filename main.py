import getIDs
import xmlToCsv
import xmlDownloader

# Use get_perseus_work_info_trResults for authors that aren't collapsed


# Get the work information
work_info = getIDs.get_perseus_work_info()

# Save the work information to a CSV file
getIDs.save_work_info_to_csv(work_info)

getIDs.split_work_info_file('workInfo.csv', 'work_info_gr.csv', 'work_info_lat.csv')

xmlDownloader.fetch_text_frequencies("work_info_lat.csv", "latin", "E:/classicalTextFrequencies")
xmlDownloader.fetch_text_frequencies("work_info_gr.csv", "greek", "E:/classicalTextFrequencies")

xmlDownloader.delete_small_xml_files('E:/classicalTextFrequencies')
xmlDownloader.delete_empty_folders('E:/classicalTextFrequencies')

xmlToCsv.convert_directory_xml_to_csv("E:\classicalTextFrequencies")
