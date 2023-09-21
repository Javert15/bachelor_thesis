import requester_functions as rf


publications = rf.generate_publications_db()
authors = rf.generate_authors_db()

pub_request=publications
aut_request=authors


pub_request, aut_request, dep_connections = rf.get_collaborations_and_remove_excess(pub_request, aut_request)



title = "collaborations" 

rf.generate_KG_excl(pub_request, aut_request, title, "isAuthorOf", "isAffiliatedWith")
rf.generate_KG_gexf(pub_request, aut_request, title, "isAuthorOf", "isAffiliatedWith", "isinDep", True, dep_connections)
rf.generate_KG_text(pub_request, aut_request, title, "isAuthorOf", "isAffiliatedWith")

print("finished requester")
