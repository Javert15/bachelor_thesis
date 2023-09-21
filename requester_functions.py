import pandas as pd
import networkx as nx
from AuthorClass import Author
from PublicationClass import Publication
        
def generate_publications_db():
    pubs_and_auths_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_publications/publications and authors.xlsx")
    
    publications_db = []
    
    for index,row in pubs_and_auths_excel_file.iterrows():
        
        authors = row[3].split(", ")
        stripped_authors = []
        
        for author in authors:
            stripped_authors.append(author.strip())
            
        
        publications_db.append(Publication(row[0],row[1], row[2],stripped_authors))
        
    
    print("generated publications")
    return publications_db

def generate_authors_db():
    authors_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/merged_researchers/researchers_with_cleaned_up_departments.xlsx")

    authors_db= []
    
    for index,row in authors_excel_file.iterrows():
        
        authors_db.append(Author(row[0], row[1].strip(), row[2].split("; ")))
    
    
    print("generated authors")
    return authors_db

def generate_department_list():
        
        departments_excel_file = pd.read_excel("C:/Users/43677/Dropbox/_Bac Arbeit/data/departments/departments_list.xlsx")
        
        departments=[]
        
        for index,row in departments_excel_file.iterrows():
            departments.append(row[1])
        
        return departments

def request_department(publications, authors, list_of_requested_departments):
    authors_list = []
    for author in authors:
        if author.check_department(list_of_requested_departments):
            authors_list.append(author.name)
            
    
    selected_publication_list = []
    for publication in publications:
        for pub_author in publication.authors:
            
            if pub_author in authors_list:
                selected_publication_list.append(publication)
                
    print("limited publications to selected departments")
    return selected_publication_list


def get_departments_of_authors(aut_request):
    
    departments=[]
    
    for author in aut_request:
        for department in author.departments:
            departments.append(department)
    departments = list(set(departments))
    
    return departments 
def filtered_department_from_authors(authors, list_of_requested_departments):
    authors_list = []
    for author in authors:
        
        filtered_departments = []
        
        if author.check_department(list_of_requested_departments):
            for department in author.departments:
                if department in list_of_requested_departments:
                    filtered_departments.append(department)
            
            author.departments=filtered_departments
            authors_list.append(author)
        
                
    print("limited publications to selected departments")
    return authors_list


def find_author(author, author_list):
    author_obj = None
    for aut in author_list:
        if aut.name == author:
            author_obj = aut
            break
    
    return author_obj
    
def replace_author (pub_request, old_author, new_author):
    
    for publication in pub_request:
        if old_author in publication.authors:
            publication.authors[publication.authors.index(old_author)]=new_author 
    
    print("replaced "+old_author+" with "+new_author)
    return pub_request
        

def select_collaborations(publications, authors):
    authors = update_authors(authors, publications)
    publications = remove_authors_without_department(publications, authors)
    
    collaboration_publications = []
    
    for publication in publications:
        if len(publication.authors)>1:
            
            current_authors = publication.authors.copy()
            
            for author in current_authors:
                current_authors.remove(author)
                other_authors = current_authors
                
                author_obj = find_author(author, authors)
                
                
                if author_obj != None:
                    for other_author in other_authors:
                        
                        other_author_obj = find_author(other_author, authors)#find other author in authors list
                        
                        if other_author_obj != None:
                            if other_author_obj.check_department(author_obj.departments) == False:
                                collaboration_publications.append(publication)
                                
            
    
    print("selected only the collaboration works")
    
    collaboration_publications=list(set(collaboration_publications))
    
    return collaboration_publications
    
def remove_pub_with_one_author_in_filter(pub_request, aut_request, filter):
    publications_with_multiple_authors = []
    for publication in pub_request:
        if len(publication.authors) != 1:
            counter = 0
            
            for author in publication.authors:
                aut = find_author(author, aut_request)
                if (aut != None):
                    print(aut)
                    print(aut.departments)
                    if aut.departments[0] in filter:
                        counter += 1
            
            if counter >1:
                publications_with_multiple_authors.append(publication)
                
    return publications_with_multiple_authors
    
    
def update_authors(authors, pub_request):
    
    list_authors_in_publications = []
    for publication in pub_request:
        list_authors_in_publications.extend(publication.authors)
    
    #remove duplicates
    list_authors_in_publications = list(set(list_authors_in_publications))
    
    output_authors_list = []
    
    for author in authors:
        if author.name in list_authors_in_publications:
            output_authors_list.append(author)
    
    print("updated authors")
    return output_authors_list

def limit_to_one_department(aut_request, filter):
    
    for author in aut_request:
        #filter out departments  
        author.departments = [x for x in author.departments if x in filter]
        
        if len(author.departments) > 1:
            author.departments = [author.departments[0]]
            
    return aut_request

def remove_authors_without_department(publications, authors):
    
    authors_list = []
    for author in authors:
        authors_list.append(author.name)
    
    
    
    output_publication_list = []
    #check each author of each publication
    for publication in publications:
        selected_authors = []
        for pub_author in publication.authors:
            #if he is in the list, add him to a new author list
            if pub_author in authors_list:
                selected_authors.append(pub_author)
        
        #and replace the old author list with the new, shorter one, also add this publication to a new list
        if selected_authors != []:
            publication.authors = selected_authors
            output_publication_list.append(publication)
        
    
    print("removed authors without department")
    return output_publication_list


def add_connections_between_same_department(authors):
    
    dep_dict = {}
    
    for author in authors:
        for department in author.departments:
            if department in dep_dict.keys():
                dep_dict[department]=dep_dict[department]+", "+author.name
            else: 
                dep_dict[department]=author.name
    
    
    connections_list = []
    
    for department in dep_dict.keys():
        members = dep_dict[department].split(", ")
        old_members = [members.pop()]
        for member in members:
            #make a connection with the all members
            for old_member in old_members:
                connections_list.append([member, old_member])
            #add current member to old members
            old_members.append(member)
            
            
    print("colleagues connected")
    return connections_list

def generate_KG_excl(publications, authors, title, relation_author_to_publication, relation_author_to_department):
    KG_excel_file = pd.DataFrame() 
    
    for publication in publications:
        KG_excel_file = KG_excel_file._append(publication.kg_for_excel(relation_author_to_publication))
    

    for author in authors:
        KG_excel_file = KG_excel_file._append(author.kg_for_excel(relation_author_to_department))
    

    KG_excel_file.to_excel(f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}.xlsx", index=False)

    print("generated excel")
    
def generate_KG_gexf(publications, authors, title, relation_author_to_publication, relation_author_to_department, relation_within_department, add_publication_numbers, dep_connections=None):
    
    DG = nx.DiGraph()

    for publication in publications:
        publication.kg_for_gexf(DG, relation_author_to_publication)
    
    for author in authors:
        author.kg_for_gexf(DG, relation_author_to_department)
    
    if dep_connections != None:
        for connection in dep_connections:
            
            DG.add_edge(connection[0], connection[1], relation=relation_within_department)
            DG.add_edge(connection[1], connection[0], relation=relation_within_department)
        
    
    
    if add_publication_numbers:
        publication_per_author_dict = {}
        publication_per_department_dict = {}
        
        #create dictionary keys
        for author in authors:
            publication_per_author_dict[author.name]=[]
            for dep in author.departments:
                publication_per_department_dict[dep]=[]
        
        
        
        #go through each publication
        #add it to a dict of each author and each department
        
        for publication in publications:
            for author in publication.authors:
                if author in publication_per_author_dict.keys():
                    publication_per_author_dict[author].append(publication.title)
                    for department in find_author(author, authors).departments:
                        publication_per_department_dict[department].append(publication.title)
        
        
        #remove duplicates
        #count the publications and add the label "publication_count" to each author and department
        for aut_key in publication_per_author_dict.keys():
            publication_per_author_dict[aut_key] = list(set(publication_per_author_dict[aut_key]))
            DG.nodes[aut_key]['publication_count'] = len(publication_per_author_dict[aut_key])
        
        for dep_key in publication_per_department_dict.keys():
            publication_per_department_dict[dep_key] = list(set(publication_per_department_dict[dep_key]))
            DG.nodes[dep_key]['publication_count'] = len(publication_per_department_dict[dep_key])
        

    nx.write_gexf(DG, f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}.gexf")   
        
    print("generated gexf file for gephi")
    
def generate_KG_text(publications, authors, title, relation_author_to_publication, relation_author_to_department):
    
    with open(f'C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}.txt', 'w', encoding='utf-8') as f:
        
    
        for publication in publications:
            f.writelines(publication.kg_for_text(relation_author_to_publication))
    
        for author in authors:
            f.writelines(author.kg_for_text(relation_author_to_department))        
    
    
    print("generated text file")
    
    
    
def generate_KG_excl_code(publications, authors, title, relation_author_to_publication, relation_author_to_department, departments):
    KG_excel_file = pd.DataFrame() 
    
    for publication in publications:
        KG_excel_file = KG_excel_file._append(publication.kg_for_excel_code(relation_author_to_publication))
    

    for author in authors:
        KG_excel_file = KG_excel_file._append(author.kg_for_excel_code(relation_author_to_department))
    

    KG_excel_file.to_excel(f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}.xlsx", index=False)

    print("generated excel")
    
def generate_KG_gexf_code(publications, authors, title, relation_author_to_publication, relation_author_to_department, relation_within_department, add_publication_numbers, departments, dep_connections=None):
    
    DG = nx.DiGraph()

    for publication in publications:
        publication.kg_for_gexf_code(DG, relation_author_to_publication)
    
    for author in authors:
        author.kg_for_gexf_code(DG, relation_author_to_department)
    
    if dep_connections != None:
        for connection in dep_connections:
            
            DG.add_edge(connection[0], connection[1], relation=relation_within_department)
            DG.add_edge(connection[1], connection[0], relation=relation_within_department)
        
    
    
    if add_publication_numbers:
        publication_per_author_dict = {}
        publication_per_department_dict = {}
        
        #create dictionary keys
        for author in authors:
            publication_per_author_dict[author.name]=[]
            for dep in author.departments:
                publication_per_department_dict[dep]=[]
        
        
        
        #go through each publication
        #add it to a dict of each author and each department
        
        for publication in publications:
            for author in publication.authors:
                publication_per_author_dict[author].append(publication.title)
                for department in find_author(author, authors).departments:
                    publication_per_department_dict[department].append(publication.title)
        
        
        #remove duplicates
        #count the publications and add the label "publication_count" to each author and department
        for aut_key in publication_per_author_dict.keys():
            publication_per_author_dict[aut_key] = list(set(publication_per_author_dict[aut_key]))
            DG.nodes[aut_key]['publication_count'] = len(publication_per_author_dict[aut_key])
        
        for dep_key in publication_per_department_dict.keys():
            publication_per_department_dict[dep_key] = list(set(publication_per_department_dict[dep_key]))
            DG.nodes[dep_key]['publication_count'] = len(publication_per_department_dict[dep_key])
        

    nx.write_gexf(DG, f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}.gexf")   
        
    print("generated gexf file for gephi")
    
def generate_KG_text_code(publications, authors, title, relation_author_to_publication, relation_author_to_department, relation_name, departments, dep_request):
    
    with open(f'C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}.txt', 'w', encoding='utf-8') as f:
        
    
        for publication in publications:
            f.writelines(publication.kg_for_text_code(authors, relation_author_to_publication, relation_name))
    
        for author in authors:
            f.writelines(author.kg_for_text_code(departments, relation_author_to_department, relation_name))
            
        for department in dep_request:
            f.writelines(f"d{departments.index(department)} {relation_name} {department}\n")
    
    print("generated text file")

def generate_KG_text_code_without_pub_titles(publications, authors, title, relation_author_to_publication, relation_author_to_department, relation_name, departments, dep_request):
    
    with open(f'C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/{title}_wo_titles.txt', 'w', encoding='utf-8') as f:
        
    
        for publication in publications:
            f.writelines(publication.kg_for_text_code_wo_title(authors, relation_author_to_publication, relation_name))
    
        for author in authors:
            f.writelines(author.kg_for_text_code(departments, relation_author_to_department, relation_name))
            
        for department in dep_request:
            f.writelines(f"d{departments.index(department)} {relation_name} {department}\n")
    
    print("generated text file without titles")
    
    
def get_collaborations_and_remove_excess(pub_request, aut_request):
    
    
    pub_request = select_collaborations(pub_request, aut_request)
    aut_request = update_authors(aut_request, pub_request)
    pub_request = remove_authors_without_department(pub_request, aut_request)
    dep_connections = add_connections_between_same_department(aut_request)
    
    return pub_request, aut_request, dep_connections
    
def print_publications(pub_request, authors):
    for publication in pub_request:
        print(f"{publication.id}: {publication.title}")
        print(publication.authors)
        for author in publication.authors:
            aut_obj = find_author(author, authors)
            print(f"{aut_obj.name} in {'; '.join(aut_obj.departments)}")
        print()
   
def split_publications(publications):
    splitA = []
    splitB = []
    splitC = []
    
    
    for i in range(len(publications)):
        if i%20 ==0:
            splitA.append(publications[i])
        elif i%20 ==1:
            splitB.append(publications[i])
        else:
            splitC.append(publications[i])    
    return [splitA, splitB, splitC]