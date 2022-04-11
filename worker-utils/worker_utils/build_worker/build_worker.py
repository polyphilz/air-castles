import json
import requests

from ..lib.file_paths import TEMPLATE_WORKER_PATH, RESOLVED_WORKER_PATH
from ..secrets.notion import AIR_CASTLES_DB_ID, NOTION_VERSION, AUTH_TOKEN


def main():
    url = f'https://api.notion.com/v1/databases/{AIR_CASTLES_DB_ID}/query'
    headers = {
        'Authorization': AUTH_TOKEN,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
    }
    res = requests.post(url, headers=headers)
    blah = res.json()
    gur = {
        "": "840d969f1f064962a0d66f21228eae11",
    }
    for x in blah['results']:
        url = x['url']
        notion_page_id = url.split('-')[-1]
        print(notion_page_id)
        title = x['properties']['Name']['title'][0]['text']['content']
        blargh = title.split(' ')
        slug = f'day{blargh[1][0]}'
        print(slug)
        gur[slug] = notion_page_id

    with open(TEMPLATE_WORKER_PATH) as in_file, open(RESOLVED_WORKER_PATH, 'w+') as out_file:
        for line in in_file:
            if '~+_insertion-marker_+~' in line:
                out_file.write('const SLUGS_TO_PAGES = ')
                json.dump(gur, out_file, indent=2, sort_keys=True)
                out_file.write(';\n')
            else:
                out_file.write(line)


if __name__ == "__main__":
    main()
