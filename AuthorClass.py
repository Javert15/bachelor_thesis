import pandas as pd

class Author:
    def __init__(self, id, name, departments):
        self.id = id
        self.name= name
        self.departments = departments
        

    
    def __str__(self):
        departments_string = '; '.join(map(str, self.departments))
        return f"{self.id}, {self.name}, {departments_string}"
    
    
    
            
    def check_department(self, list_departments):
        check = False
        for department in self.departments:
            if department in list_departments:
                check = True
        
        if check:
            return True
        else:
            return False
    
    def kg_for_excel(self, relation_author_to_department):
        all_entries = pd.DataFrame()
        for department in self.departments:
            new_entry = pd.DataFrame(data={"Source": [self.name],
                                           "Relation": [relation_author_to_department],
                                           "Sink": [department],
                                           })
            
            all_entries = all_entries._append(new_entry)
            
        return all_entries
        
        
    def kg_for_gexf(self, DG, relation_author_to_department):
        for department in self.departments:
            DG.add_edge(self.name, department, relation=relation_author_to_department)
            DG.nodes[department]['type'] = "dep"
        
        DG.nodes[self.name]['label'] = self.name
        DG.nodes[self.name]['id'] = self.id
        
    def kg_for_text(self, relation_author_to_department):
         
        output = []
        
        for department in self.departments:
            output.append(f"{self.name} {relation_author_to_department} {department}\n")
        return output
    
    def kg_for_text_code(self, departments, relation_author_to_department, relationship_name):
         
        output = []
        
        for department in self.departments:
            output.append(f"a{self.id} {relation_author_to_department} d{departments.index(department)}\n")
        return output