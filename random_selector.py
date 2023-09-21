import random


#10x write
for i in range (10):
    
    #read file
    input = open("C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/VoVeK_selected_wo_titles.txt", "r")
    
    #write header
    output = open(f"C:/Users/43677/Dropbox/_Bac Arbeit/data/requests/Entity Classification/Example {i+1}.txt", "w")
    
    #write first 220 lines
    for i in range (209):
        output.write(input.readline())
    
    #generate 3 different random numbers between 1 and 16
    deleted_lines = random.sample(range(58), 3)
    answers = []
    author = []
    
    #skip those lines, write others
    for i in range(58):
        if i in deleted_lines:
            answers.append(input.readline())
        else:
            output.write(input.readline())
    
    for x in answers:
        author.append(x.split(" ")[0])
    
    #write department names
    for i in range(3):
        output.write(input.readline())
    
    #add question
    output.write(f"Which departments would you locate {author[0]}, {author[1]} and {author[2]} in, based on their publications?\n")
    
    #write answers
    output.write("\n")
    output.write("\n")
    output.write("Answers: \n")
    for answer in answers:
        output.write(answer)
    
    #save file 
    input.close()
    output.close()
    