import pandas as pd


input_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_researchers/merged_researchers.xlsx")
output_excel_file = pd.DataFrame() 

titles = ["(CEMS)", "(Cambridge)", "(Econ.)", "(Hons.)", "(Oxford)", "(Sciences-Po)", "(WU)", "(hon)", "(GWU)", "(NYU)", "(Harvard)", "(FH)", "(Exeter)", "(Florenz)", ",", "Coaching", "MAS", "MBA", "Ass.", "Assist.", "Assoz.", "Assoz.Prof", "B.A.", "B.S.", "B.Sc.", "BA", "BEd", "BSc.", "BSc", "Bakk.", "CM(it.)", "D.Litt.", "DDr.", "DPhil", "Dipl.-Hdl.", "Dipl.-Ing.", "Dipl.-Kff.", "Dipl.-Verk.-wirtsch.", "Dipl.-Vw.", "Dipl.-Wirt.Inform.", "Dipl.Math.", "Dipl.Wirtsch.-Math.", "Dkfm.", "Dott.", "Doz.", "Dr.-Ing.", "Dr.", "Dr", "EMA", "Hons.", "Hon", "Ing.", "J.", "LL.B.", "LL.M.", "LL.M", "LLM", "M.A.", "M.A", "M.E.S.", "M.Jur.", "M.S.", "M.Sc.", "M.Stat.", "MA.", "MA", "MIM", "MSc.", "MSc", "Mag.", "MinR", "P.G.C.E.", "PD", "Ph.D.", "PhD.", "PhD", "Priv.", "Prof.", "Prof", "Univ.", "Univ.-Ass.", "a.", "ao.", "diplômé", "em.", "h.c.", "habil.", "i.R.", "lic.", "mag.", "o.", "oec.", "phil.", "prof.", "rer.soc.oec", "techn."]



for index,row in input_excel_file.iterrows():
    
    for title in titles:
        row[1] = row[1].replace(title, "").strip()
    
    
    if row[1].find(".")!=-1:
            print(row[1])
    
    if row[1].find(",")!=-1:
            print(row[1])
    
    output_excel_file = output_excel_file._append(row, ignore_index=True)
        
    

output_excel_file.to_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_researchers/researchers_without_titles.xlsx", index=False)  
print("finished")