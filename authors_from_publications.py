import pandas as pd

publications_RIS_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_publications/merged_publications_RIS.xlsx")
authors_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_researchers/researchers_without_titles.xlsx")


#initiate pd Dataframes to handle the data and for later export into excel files
#publications_RIS_excel_file = publications_RIS_excel_file.head(50)
pubs_and_auths_excel_file = pd.DataFrame() 
multiple_auths_excel_file = pd.DataFrame()
collabs_excel_file = pd.DataFrame()

authors_list= []
dep_of_authors_list = []


#create a lists of all authors and their respective departments
for index,row in authors_excel_file.iterrows():
    
    authors_list.append(row[1])
    dep_of_authors_list.append(row[2])
    
print(authors_list)
print(dep_of_authors_list)
#read file into new file that contains Nr, Title, Type of publication and authors

for index,row in publications_RIS_excel_file.iterrows():
    
    number = row[0]
    publication_type = row[2][3:]
    title = row[3][3:]
    
    ### authors
    
    author_iterator = 4
    #find first author, e.g. if entry 4 is a second title
    while row[author_iterator][:3] != "AU:" and row[author_iterator][:3] != "A2:":
        author_iterator += 1
        
    #create a list of all authors for this publication row   
    current_authors_list = []
    current_dep_list = []
    current_author_codes_list = []
    
    
    while row[author_iterator][:3] == "AU:" or row[author_iterator][:3] == "A2:":
        new_author = row[author_iterator][3:]
        
        #turn "last name, first name" into "first name second name"
        new_author_sorted = new_author[(new_author.find(",")+2):]+" "+new_author[:new_author.find(",")]
        
        #add current author to the list of authors in this publication
        current_authors_list.append(new_author_sorted)
        
        #assign department from "researchers without titles"-excel, or "unknown" if not listed there, or no department is specified there
        if new_author_sorted in authors_list and isinstance(dep_of_authors_list[authors_list.index(new_author_sorted)], str):
            dep_of_new_author = dep_of_authors_list[authors_list.index(new_author_sorted)].split(", ")
        else:
            dep_of_new_author = ["unknown"]
        
        current_dep_list.append(dep_of_new_author)
        
        
        if new_author_sorted in authors_list:
            current_author_codes_list.append("A"+str(authors_list.index(new_author_sorted)+1))
        
        #check if this is a colaboration, which is the case, when no departments are shared between authors
        
        author_iterator += 1
        
        
    
    delimiter = ', '
    authors_string = delimiter.join(current_authors_list)
    departments_string = current_dep_list
    author_code_string = delimiter.join(current_author_codes_list)

    
    new_entry = pd.DataFrame(data={ "Number": [number],
                                    "Type": [publication_type],
                                    "Title": [title],
                                    "Authors": [authors_string],
                                    "Author code": [author_code_string]
                                    , "Departments": [departments_string]
                                    })
    
    
    pubs_and_auths_excel_file = pubs_and_auths_excel_file._append(new_entry)
    
    
    
    if authors_string.find(",") != -1:
        multiple_auths_excel_file = multiple_auths_excel_file._append(new_entry)
    
    
    #remove the unknown from the department list to obtain the known departments
    known_departments = [s for s in current_dep_list if s != ['unknown']]
    
    
    #if there are at least authors from knwon departments
    collaboration = False
    if len(known_departments) > 1:
        #check each individual department
        for each_author in range(len(known_departments)):
            check = []
            for each_dep_of_author in range(len(known_departments[each_author])):
                #check each other author
                for other_author in range(len(known_departments)):
                    #don't check for itself
                    if each_author != other_author:
                        #check if it is  
                        if not (known_departments[each_author][each_dep_of_author] in known_departments[other_author]):
                            check.append(True)
                        else:
                            check.append(False) 
                            
                
            if all(check):
                    collaboration = True
                    
                    
    if collaboration:
            collabs_excel_file = collabs_excel_file._append(new_entry)  
     
pubs_and_auths_excel_file.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_publications/publications and authors.xlsx", index=False)
multiple_auths_excel_file.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_publications/publications with multiple authors.xlsx", index=False)    
collabs_excel_file.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_publications/publications with collaborations.xlsx", index=False)    
print("finished authors from publications")

