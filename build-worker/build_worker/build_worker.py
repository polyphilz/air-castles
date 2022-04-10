import requests

from secrets.notion import NOTION_AIR_CASTLES_DB_ID, NOTION_AUTH_TOKEN, NOTION_VERSION


def main():
    url = f'https://api.notion.com/v1/databases/{NOTION_AIR_CASTLES_DB_ID}/query'
    headers = {
        'Authorization': NOTION_AUTH_TOKEN,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
    }
    res = requests.post(url, headers=headers)
    print(res.json())


if __name__ == "__main__":
    main()
