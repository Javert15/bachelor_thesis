import pandas as pd


authors_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_researchers/researchers_without_titles.xlsx")
departments_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/departments_list.xlsx")
replaced_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/replaced_departments_list.xlsx")
skipped_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/skipped_departments_list.xlsx")

output_excel_file = pd.DataFrame() 
authors_w_deps_excel_file = pd.DataFrame()

departments_list_id = []
departments_list_name = []
departments_list_count = []
departments_list_members = []

author_code_dict = {}
author_w_deps_dict = {}

replaced_departments_dict = {}
skipped_departments_list = []


#create a list containing a list for each department
for index,row in departments_excel_file.iterrows():
    #add for each row a list containing department number, department name, number of members, name of members
    departments_list_id.append(row[0])
    departments_list_name.append(row[1])
    departments_list_count.append(0)
    departments_list_members.append("")
    
    
#create a dict containing all replaced departments
for index,row in replaced_excel_file.iterrows():
    #add for each row a list containing department number, department name, number of members, name of members
    replaced_departments_dict[row[1]]=row[2]

#create a list containing all skipped departments
for index,row in skipped_excel_file.iterrows():
    #add for each row a list containing department number, department name, number of members, name of members
    skipped_departments_list.append(row[1])




#add each author to his departments
for index,row in authors_excel_file.iterrows():
    author_code_dict[row[1]]=row[0]
    
    if isinstance(row[2], str):
        #remve brackets
        while(row[2].find("(")!=-1):
            start = row[2].find("(")
            end = row[2].find(")")+1
            row[2] = row[2].replace(row[2][start:end], "").strip()
        
        
        dep_with_comma = ["Data, Process and Knowledge Management",
        "Rechnungswesen, Steuern und Jahresabschlussprüfung",
        "Finance, Accounting and Statistics",
        "Finance, Banking and Insurance",
        "Strategie, Technologie und Organisation"]
        
        
        comma_deps = []
        for comma_dep in dep_with_comma:
            
            if row[2].find(comma_dep) != -1:
                comma_deps.append(comma_dep)
                row[2] = row[2].replace(comma_dep, "")

        current_dep_list = row[2].split(", ")
        
        while "" in current_dep_list:
            current_dep_list.remove("")
            
        while " " in current_dep_list:
            current_dep_list.remove(" ")
        
        current_dep_list.extend(comma_deps)
        
        
        for department in current_dep_list:
            department = department.strip()
            
            if department in skipped_departments_list:
                #skip "departments", that are, rector, senat, ...
                print("skipped "+department)
            elif department in replaced_departments_dict.keys():
                #replace from replaced departments
                department = replaced_departments_dict[department]
                
                #add to department list
                pos = departments_list_name.index(department)
                departments_list_count[pos] += 1
                if departments_list_members[pos] != "":
                    departments_list_members[pos] = departments_list_members[pos]+", "
                departments_list_members[pos] = departments_list_members[pos]+row[1]
                
                #and generate the inverse list: authors with their departments
                if row[1] in author_w_deps_dict:
                    #check to not add a duplicate
                    logged_departments = author_w_deps_dict[row[1]].split("; ")
                    if not (department in logged_departments):
                        author_w_deps_dict[row[1]] = author_w_deps_dict[row[1]]+"; "+department
                else:
                    author_w_deps_dict[row[1]] = department
                
            else:
                
                #add to department list
                pos = departments_list_name.index(department)
                departments_list_count[pos] += 1
                if departments_list_members[pos] != "":
                    departments_list_members[pos] = departments_list_members[pos]+", "
                departments_list_members[pos] = departments_list_members[pos]+row[1]
                
                #and generate the inverse list: authors with their departments
                if row[1] in author_w_deps_dict:
                    #check to not add a duplicate
                    logged_departments = author_w_deps_dict[row[1]].split("; ")
                    if not (department in logged_departments):
                        author_w_deps_dict[row[1]] = author_w_deps_dict[row[1]]+"; "+department
                else:
                    author_w_deps_dict[row[1]] = department
                
for i in departments_list_id:
    new_entry = pd.DataFrame(data={ "Number": [departments_list_id[i]],
                        "Name": [ departments_list_name[i]],
                        "Count": [departments_list_count[i]],
                        "Members": [departments_list_members[i]]
                                    })
    output_excel_file = output_excel_file._append(new_entry, ignore_index=True)
    


for author_key in author_w_deps_dict.keys():
    new_aut_entry = pd.DataFrame(data={ "Number": [author_code_dict[author_key]],
                        "Name": [author_key],
                        "Departments": [author_w_deps_dict[author_key]]
                                    })
    authors_w_deps_excel_file = authors_w_deps_excel_file._append(new_aut_entry, ignore_index=True)
  
    
output_excel_file.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/departments_with_members.xlsx", index=False)  

authors_w_deps_excel_file.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_researchers/researchers_with_cleaned_up_departments.xlsx", index=False)  


print("finished")
