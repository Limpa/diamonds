import requests 

# sending get request and saving the response as response object 
r = requests.get("http://diamonds.etimo.se/api/boards/2") 
  
# extracting data in json format 
print(r.json())
