import pandas as pd

class Publication:
    def __init__(self, id, type, title, authors):
        self.id = id
        self.type = type
        self.title = title
        self.authors = authors

    
    def __str__(self):
        authors_string = '; '.join(map(str, self.authors))
        return f"{self.id}, {self.type}, '{self.title}', {authors_string}"
    
    def kg_for_excel(self, relation_author_publication):
        all_entries = pd.DataFrame()
        for author in self.authors:
            
            new_entry = pd.DataFrame(data={"Source": [author],
                                           "Relation": [relation_author_publication],
                                           "Sink": [self.title],
                                           })
            
            all_entries = all_entries._append(new_entry)
        
        return all_entries
    
    def kg_for_gexf(self, DG, relation_author_to_publication):
        
        DG.add_node("p"+str(self.id), type="pub", label="p"+str(self.id), title=self.title, publication_type=self.type)
        
        for author in self.authors:
            DG.add_node(author, label=author, type="aut")
            DG.add_edge(author,"p"+str(self.id), relation=relation_author_to_publication)
        
    def kg_for_text(self, relation_author_to_publication):
        output = []
        
        for author in self.authors:
            output.append(f"{author} {relation_author_to_publication} {self.title}\n")
        
        return output
    
    def kg_for_text_code(self, authors, relation_author_to_publication, relation_name):
        output = []
        
        
        for author in self.authors:
            for aut in authors:
                if aut.name == author:
                    author_id = aut.id
            output.append(f"a{author_id} {relation_author_to_publication} p{self.id}\n")
        output.append(f"p{self.id} {relation_name} {self.title}\n")
        return output
    
    def kg_for_text_code_wo_title(self, authors, relation_author_to_publication, relation_name):
        output = []
        
        
        for author in self.authors:
            for aut in authors:
                if aut.name == author:
                    author_id = aut.id
            output.append(f"a{author_id} {relation_author_to_publication} p{self.id}\n")
        
        return output