import pandas as pd
import glob

    
      
directory = "C:/Users/43677/Downloads/researchers"
output_file = "C:/Users/43677/Downloads/merged_researchers/merged_researchers.xlsx"

# Get a list of XLS files in the directory
filenames = glob.glob(directory + "\*.xls")
print('File names:', filenames)

#create list with excel files
excel_list = []
      
for file in filenames:
    excel_list.append(pd.read_excel(file))

# create a new dataframe to store the merged excel file
excel_merged = pd.DataFrame()
 
for excel_file in excel_list:
    excel_merged = excel_merged._append(
      excel_file, ignore_index=True)


# exports the dataframe into excel file with specified name
excel_merged.to_excel(output_file, index=False)  