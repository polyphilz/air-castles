import requests

from ..lib.file_paths import RESOLVED_WORKER_PATH
from ..secrets.cloudflare import ACCOUNT_ID, WORKER_SCRIPT_NAME, EMAIL, AUTH_KEY


def main():
    with open(RESOLVED_WORKER_PATH, "r") as f:
        url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{WORKER_SCRIPT_NAME}"
        headers = {
            "X-Auth-Email": EMAIL,
            "X-Auth-Key": AUTH_KEY,
            "Content-Type": "application/javascript",
        }

        res = requests.put(url, headers=headers, data=f.read())
        if not res.json()["success"]:
            print("Worker Script failed to be uploaded to Cloudflare.")
            raise

        print("Worker Script successfully uploaded to Cloudflare.")


if __name__ == "__main__":
    main()
