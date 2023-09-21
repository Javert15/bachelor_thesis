import random

input = open("C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/VoVeK_selected_wo_titles.txt", "r")

lines = input.readlines()
input.close()


elements = [] 

for line in lines:
    line = line[:(len(line) - 1)] # remove \n at the end
    elements.extend(line.split(" "))

elements = list(set(elements))


authors = []
publications = []
departments = []

for element in elements:
    if element[0] == "a" and element != "and":
        authors.append(element)
    elif element[0] == "d":
        departments.append(element)
    elif element[0] == "p":
        publications.append(element)



for j in range(10):
    
    error_lines = []
    
    for i in range(10):
        # get two random publications
        # get two random department
        # get two random authors
        
        rand_pubs = random.choices(publications, k = 2)
        rand_deps = random.choices(departments, k = 2)
        rand_auts = random.choices(authors, k = 2)
    
        option = random.randrange(1,16)
        
        
        if option == 1:
            new_line = f"{rand_auts[0]} >> {rand_auts[1]}\n"
        elif option == 2:
            new_line = f"{rand_auts[0]} >> {rand_deps[1]}\n"
        elif option == 3:
            new_line = f"{rand_pubs[0]} >> {rand_auts[1]}\n"
        elif option == 4:
            new_line = f"{rand_pubs[0]} >> {rand_deps[1]}\n"
        elif option == 5:
            new_line = f"{rand_pubs[0]} >> {rand_pubs[1]}\n"
        elif option == 6:
            new_line = f"{rand_deps[0]} >> {rand_auts[1]}\n"
        elif option == 7:
            new_line = f"{rand_deps[0]} >> {rand_deps[1]}\n"
        elif option == 8:
            new_line = f"{rand_deps[0]} >> {rand_pubs[1]}\n"
        elif option == 9:
            new_line = f"{rand_auts[0]} -- {rand_auts[1]}\n"
        elif option == 10:
            new_line = f"{rand_auts[0]} -- {rand_pubs[1]}\n"
        elif option == 11:
            new_line = f"{rand_pubs[0]} -- {rand_auts[1]}\n"
        elif option == 12:
            new_line = f"{rand_pubs[0]} -- {rand_deps[1]}\n"
        elif option == 13:
            new_line = f"{rand_pubs[0]} -- {rand_pubs[1]}\n"
        elif option == 14:
            new_line = f"{rand_deps[0]} -- {rand_auts[1]}\n"
        elif option == 15:
            new_line = f"{rand_deps[0]} -- {rand_deps[1]}\n"
        elif option == 16:
            new_line = f"{rand_deps[0]} -- {rand_pubs[1]}\n"
            
        error_lines.append(new_line) 
        
            
    error_file = open(f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/anomality detection/Test {j}_errors.txt", "w+")
    complete_file = open(f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/anomality detection/Test {j}.txt", "w+") 
    
    error_file.writelines(error_lines)
    error_file.close()
    
    all_lines = error_lines + lines
    random.shuffle(all_lines)
    complete_file.writelines(all_lines)
    complete_file.close()
    
