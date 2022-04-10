# Air Castles

aircastles.xyz is my microblog. It's built using a public Notion page combined
with a Cloudflare Worker that enables me to:

1) Use a custom domain name and custom "pretty" URL slugs for each post
2) Get (lightweight) analytics from Cloudflare just to see what traffic is like
3) Customize the CSS and add/remove elements from the DOM

## The Notion Page

The actual Notion page itself contains an inline database and some text +
callout blocks. The inline database is the main meat of the site, housing all
the blog posts. Posts can be opened up as their own individual pages as per how
Notion has implemented it; when they are, the URL should have that post's
associated slug appended to it (e.g. https://aircastles.xyz/day1).

## The Cloudflare Worker

Cloudflare Workers are self-contained bits of JavaScript that run upon
specific actions. For Air Castles, a single worker runs any time a request to
the page is made. The worker extracts the contents from the actual Notion site,
adds the slug support and makes some changes to the CSS/DOM, and republishes
the modified contents on https://aircastles.xyz. This process is wicked fast;
edits to the Air Castles Notion page usually appear on the live site in <= 1
second.

The Cloudflare Worker requires a JS object containing a custom URL slug to
Notion page ID mapping. Every time I create a new post (which, at the moment,
is every single day), I'd have to create the post on the Notion page, get the
Notion page ID, add the slug to Notion page ID mapping in the `SLUG_TO_PAGE`
JS object specified in the Worker script (e.g. `'day9': '<notion-page-id>'`),
and then redeploy the Worker on the Cloudflare dashboard.

That's way too much work, so I made a Python script that automates this...

## The Python Script

### Building the Worker Script

[`build_worker.py`](build-worker/build_worker/build_worker.py) does a few
things:

- It uses the Notion API to read all the contents from the inline database
contained in the main Air Castles Notion page
- Using the JSON output from above, it generates a simple text file
`slugs_to_pages.txt` containing a key-value mapping of custom slugs to Notion
page IDs. For my use case, I was content with my custom slugs just being
`/day1`, `/day2`, etc.
- It reads in `workerTemplate.js` and replaces `SLUG_TO_PAGE` with the actual
mappings contained in `slugs_to_pages.txt`; it then outputs this worker file
into [`_out`](_out/) as `worker.js`

### Uploading the Worker Script

`upload_worker.py` uses the Cloudflare API to upload the newly created worker
script to Cloudflare.

## CLI

I don't want to have to run both the build and upload worker scripts, so a
command-line utility, `.deploy.sh`, was created to do this.
