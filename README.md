It's fragile, so we need to diff screenshots of the nav bar for mobile and web.
If Notion changes their divs layout then this whole thing can just break.

Every time a new subpage (post) is created, a script needs to be run that grabs
the Notion page ID for this new subpage and adds to worker.js the correct
slug/id kv pair.

- Write a Python script that runs the Notion API cURL command above and collects the JSON output
- It'll parse through the output and create `slugs_to_pages.txt`. Simple text file with mappings
- Then it'll create a new worker.js and output it in \_workerout

- Some outer shell process then has to run the above script, cd into \_workerout, use cloudflare api
  to upload the new worker, then cd ../ all in 1
