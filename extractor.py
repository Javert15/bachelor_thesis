from bs4 import BeautifulSoup
import pandas as pd
import requests



input_excel_file = pd.read_excel("C:/Users/43677/Downloads/merged_publications/merged.xlsx")
output_excel_file = pd.DataFrame() 


for index,row in input_excel_file.iterrows():
    
# test on the first 5 rows, instead of upper for
#for index in range(5): 
    
    #if index >= 3000:
    #print(input_excel_file.iloc[index,2])
    position = input_excel_file.iloc[index,0]
    URL = input_excel_file.iloc[index,2]
   
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(id="cite-RIS")
    
    
    tags = results.find_all("p")
    new_entry = [position, URL]
    
    for tag in tags:
        tag_text = tag.text.strip()
        tag_output = tag_text[0:2]+":"+tag_text[6:]
        new_entry.append(tag_output)
        #print(tag_output)
        
    print(new_entry)
    
    df = pd.DataFrame(new_entry).T
    output_excel_file = output_excel_file._append(df)
    
    
    if index % 300 == 0:
        output_excel_file.to_excel("C:/Users/43677/Downloads/merged_publications/output"+str(index)+".xlsx", index=False)

# Write the DataFrame to an Excel file
output_excel_file.to_excel("C:/Users/43677/Downloads/merged_publications/output.xlsx", index=False)
print("finished")
    