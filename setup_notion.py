import requests
import json

class NotionDatabase:

    def __init__(self,key,id,name = "untitled",dry_run: bool = False):

        self.key = key
        self.id = id
        self.name = name
        self.dry_run = dry_run

    def createPage(self,page_prop: dict):

        header = {
            "Authorization": "Bearer " + self.key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        print("Creating a Page in Notion Database with id:\t" + self.name)
        
        url = "https://api.notion.com/v1/pages"
        page_data = {
            "parent": { "database_id": self.id },
            "properties": page_prop
        }

        if self.dry_run:
            print(json.dumps(page_data, indent=2))
            return None
        else:
            req = requests.post(url, headers=header, json=page_data)
            print(req.status_code)
            print(req.text)
            return req 