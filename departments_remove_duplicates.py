import pandas as pd


input_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/departments_filtered and ordered.xlsx", header=None)



#fill two lists:
#list one contains all entries with only one department (containing no comma)
#list two contains all others and is processed further down
single_departments = []
multiple_departments = []

manual_addition = ["Experimentalforschung",
                   "Data, Process and Knowledge Management",
                   "Rechnungswesen, Steuern und Jahresabschlussprüfung",
                   "Rechenintensive Methoden",
                   "Wirtschaftsinformatik und Operations Management",
                   "Familienunternehmen",
                   "Finance, Accounting and Statistics",
                   "Finance, Banking and Insurance",
                   "Europainstitut",
                   "Europäisches Steuerrecht",
                   "Österreichisches und Internationales Steuerrecht",
                   "Internationales Steuerrecht",
                   "Marketing-Management",
                   "Marketing und Customer Analytics",
                   "Marketing und KonsumentInnenforschung",
                   "Public Management und Governance",
                   "Raum- und Immobilienwirtschaft",
                   "Strategie, Technologie und Organisation",
                   "Steuerpolitik",
                   "Supply Chain Management",
                   "Umsatzsteuerrecht",
                   "Unternehmensrecht I",
                   "Unternehmenssteuerrecht",
                   "Urban Management and Governance",
                   "Zentrum für Wirtschaftssprachen",
                   "Zivil- und Zivilverfahrensrecht VI",
                   "Zivil- und Zivilverfahrensrecht V",
                   "Zivil- und Zivilverfahrensrecht IV",
                   "Zivil- und Zivilverfahrensrecht III",
                   "Zivil- und Zivilverfahrensrecht II",
                   "Zivil- und Zivilverfahrensrecht I",
                   "Zivil- und Zivilverfahrensrecht"
                   ]

skipped_entries = ["Wirtschaftsuniversität",
                   "Rektor/in",
                   "Senat",
                   "VR für Finanzen und Universitätsentwicklung",
                   "VR für Lehre und Studierende",
                   "VR für Forschung und Personal",
                   "WU Executive Academy",
                   "DP Sekretariat Wirtschaftskommunikation",
                   "Project Management Group",
                   "Programmmanagement und Lehr-/Lernsupport"]


replaced = {
    "Zivil- und Zivilverfahrensrecht VI": "Zivil- und Zivilverfahrensrecht",
    "Zivil- und Zivilverfahrensrecht V": "Zivil- und Zivilverfahrensrecht",
    "Zivil- und Zivilverfahrensrecht IV": "Zivil- und Zivilverfahrensrecht",
    "Zivil- und Zivilverfahrensrecht III": "Zivil- und Zivilverfahrensrecht",
    "Zivil- und Zivilverfahrensrecht II": "Zivil- und Zivilverfahrensrecht",
    "Zivil- und Zivilverfahrensrecht I": "Zivil- und Zivilverfahrensrecht",
    "Feichter": "Institut für Unternehmensführung",
    "Grabner": "Institut für Unternehmensführung",
    "Speckbacher": "Institut für Unternehmensführung",
    "Unternehmensrecht I": "Unternehmensrecht",
    
    }

single_departments.extend(manual_addition)
single_departments.extend(skipped_entries)

#sort each line into those that contain only a single department, or multiple ones
for index,row in input_excel_file.iterrows():
    #remve brackets
    while(row[1].find("(")!=-1):
        start = row[1].find("(")
        end = row[1].find(")")+1
        print("removing ***" + row[1][start:end] + "*** from " + row[1])
        row[1] = row[1].replace(row[1][start:end], "").strip()
    
    if row[1].find(",") == -1:
        single_departments.append(row[1])
    else:
        multiple_departments.append(row[1])

print("single: ")
print(single_departments)
print()
print("multiple: ")
print(multiple_departments)

print("novel departments:")

#remove the known departments, commas and spaces from multiple departments and print them, so they can be added to "manual_addition"
for multi_dep in multiple_departments:
    
    for sin_dep in single_departments:
        multi_dep = multi_dep.replace(sin_dep, "")
        
    contains_novel_dep =False
    for char in multi_dep:
        if char != ' ' and char != ',':
            contains_novel_dep = True
            break
    
    if contains_novel_dep:
        while multi_dep[0] == "," or multi_dep[0] == " ":
            multi_dep = multi_dep[1:]
            
        while multi_dep[len(multi_dep)-1] == "," or multi_dep[len(multi_dep)-1] == " ":
            multi_dep = multi_dep[:(len(multi_dep)-1)]
        
        print("novel: "+multi_dep)
        



#replace values, that are inconclusive
for replaced_value in replaced.keys():
    while replaced_value in single_departments:
        single_departments[single_departments.index(replaced_value)] = replaced[replaced_value]

#and remove duplicates
single_departments = list(set(single_departments))

#remove entries, that are no departments (see list "skipped_entries")        
for skipped in skipped_entries:
    single_departments.remove(skipped)

single_departments.sort()

#turn departments_list_excel, skipped_list and replaced list into excels
departments_list_excel = pd.DataFrame(zip(range(len(single_departments)),single_departments)) 
skipped_departments_list_excel = pd.DataFrame(zip(range(len(skipped_entries)),skipped_entries))
replaced_keys = list(replaced.keys())
replaced_values = list(replaced.values())
replaced_departments_list_excel = pd.DataFrame(zip(range(len(replaced_keys)), replaced_keys, replaced_values))



departments_list_excel.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/departments_list.xlsx", index=False)  
skipped_departments_list_excel.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/skipped_departments_list.xlsx", index=False)
replaced_departments_list_excel.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/replaced_departments_list.xlsx", index=False)

print("finished")