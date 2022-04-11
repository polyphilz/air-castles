import json
import requests

from ..lib.file_paths import TEMPLATE_WORKER_PATH, RESOLVED_WORKER_PATH
from ..secrets.notion import (
    AIR_CASTLES_MAIN_ID,
    AIR_CASTLES_DB_ID,
    NOTION_VERSION,
    AUTH_TOKEN,
)


def get_posts():
    """Queries the Air Castles Notion page inline database for all posts.

    Returns:
        A res object containing a list of posts if successful, else an empty
            object.
    """
    url = f"https://api.notion.com/v1/databases/{AIR_CASTLES_DB_ID}/query"
    headers = {
        "Authorization": AUTH_TOKEN,
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers).json()


def create_slugs_to_page_ids_dict(posts):
    """Creates a mapping between URL slugs and Notion page IDs.

    The slugs do not include the leading "/". The starting dictionary will
    always have: `"": AIR_CASTLES_MAIN_ID` as an entry as this maps the core
    aircastles.xyz/ site to the associated public Notion page. The rest of the
    slugs generated will be for subpages (i.e. blog posts).

    Parameters:
        posts (List[Object]): A list of Notion post objects.

    Returns:
        slugs_to_page_ids (Object<str, str>): A dictionary containing URL slug
            to Notion page ID pairs.
    """
    slugs_to_page_ids = {
        "": AIR_CASTLES_MAIN_ID,
    }

    for post in posts:
        # Get the Notion page ID
        page_id = post["url"].split("-")[-1]

        # Get the URL slug. This code's a bit fragile; it's entirely dependent
        # on the titles of posts being of the format: "Day XX: <Title>"
        post_title = post["properties"]["Name"]["title"][0]["text"]["content"]
        # The day number part of the title still has the ":" at the end after
        # the string split, hence the [:-1] to remove the ":"
        post_day_number = post_title.split(" ")[1][:-1]
        slug = f"day{post_day_number}"

        # Add slug/page ID pair to the dictionary
        slugs_to_page_ids[slug] = page_id

    return slugs_to_page_ids


def resolve_worker_js_file(slugs_to_page_ids):
    """Creates a finalized Worker Script JS file using a template and the slugs
           to Notion page IDs dictionary.

    Parameters:
        slugs_to_page_ids (Object<str, str>): A dictionary containing URL slug
            to Notion page ID pairs.

    Outputs a file: "resolvedWorker.js"
    """
    with open(TEMPLATE_WORKER_PATH) as in_file, open(
        RESOLVED_WORKER_PATH, "w+"
    ) as out_file:
        for line in in_file:
            if "~+_insertion-marker_+~" in line:
                out_file.write("const SLUGS_TO_PAGES = ")
                json.dump(slugs_to_page_ids, out_file, indent=2, sort_keys=True)
                out_file.write(";\n")
            else:
                out_file.write(line)


def main():
    # Get all posts
    posts = get_posts()
    if not posts:
        print("Failed to build Worker Script - Notion API database query error")
        return

    # Create the URL slug to Notion page ID mappings for each post
    slugs_to_page_ids = create_slugs_to_page_ids_dict(posts["results"])

    # Write each line of workerTemplate.js to resolvedWorker.js except when the
    # sentinel marker is hit, in which case a JS const `SLUGS_TO_PAGES` will be
    # written instead using the slugs_to_page_ids dictionary created above.
    resolve_worker_js_file(slugs_to_page_ids)


if __name__ == "__main__":
    main()
