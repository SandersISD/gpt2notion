import requests
import json

class NotionDatabase:

    def __init__(self,key,id,name = "untitled",dry_run: bool = False):

        self.key = key
        self.id = id
        self.name = name
        self.dry_run = dry_run
        self.header = {
            "Authorization": "Bearer " + self.key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def create_page(self,page_prop: dict):

        print("Creating a Page in Notion Database with id:\t" + self.name)
        
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": { "database_id": self.id },
            "properties": page_prop
        }

        if self.dry_run:
            print(json.dumps(page_data, indent=2))
            return None
        else:
            response = requests.post(url, headers=self.header, json=payload)
            print(response.status_code)
            print(response.text)
            return response 
    
    def query_pages(self, create_file : bool = False):
        url = "https://api.notion.com/v1/databases/"+self.id+"/query"

        payload = {"page_size": 100}

        response = requests.post(url, headers=self.header, json=payload)
        # print(response.status_code)
        # print(response.text)        
        if create_file:
            with open('database_dumps/'+self.name+'.json', 'w', encoding='utf8') as file:
                json.dump(response.json(), file, ensure_ascii=False, indent=4)

        pages=[]
        for items in response.json()["results"]:
            pages.append(items)
        return pages
