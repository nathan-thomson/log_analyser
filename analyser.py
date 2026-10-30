import re

with open("samples/sample_auth.log", "r") as file:
    for line in file:
        match = re.search(r'Failed password', line) #searches for "Failed password" in each line
        
        if match:
            print(line.strip())  
        
    
    





