import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.imdb.com/chart/top/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

# Check for a 200 status code to ensure the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <script> tag with type "application/ld+json"
    script_tag = soup.find("script", type="application/ld+json")
    
    # Check if the tag was found and extract its contents
    if script_tag:
        json_content = script_tag.string  # Extract the contents as text

        try:
            # Parse the JSON content to a Python dictionary
            json_data = json.loads(json_content)
            
            # Extract all 'name' attributes under each 'item' in 'itemListElement'
            names = []
            if "itemListElement" in json_data:
                for element in json_data["itemListElement"]:
                    item = element.get("item", {})
                    name = item.get("name")
                    if name:
                        names.append(name)

            # Print all names found
            print("Names under itemListElement:")
            for name in names:
                print(name)
                
            # Optionally, save the names to a file
            with open("names.txt", "w", encoding="utf-8") as file:
                for name in names:
                    file.write(name + "\n")
                
            print("Names saved to names.txt")
        
        except json.JSONDecodeError:
            print("Failed to decode JSON.")
    else:
        print("No JSON-LD <script> tag found.")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
