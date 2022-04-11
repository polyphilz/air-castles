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
specific actions. For Air Castles, a single Worker runs any time a request to
the page is made. At a high level, the Worker:

1. Extracts the contents from the actual Notion site
2. Adds the URL slugs mapped to each post
3. Makes small changes to the CSS/DOM
4. Republishes the modified contents to https://aircastles.xyz

This process is wicked fast: edits to the Air Castles Notion page usually
appear on the live site in ~1 second or less.

The Worker requires a JS object containing key-value pairs of custom URL slugs
to Notion page IDs. Every time I create a new post (which, at the moment, is
every single day), I'd have to create the post on the Notion page, get the
Notion page ID, add the slug to Notion page ID mapping in the `SLUGS_TO_PAGES`
JS object specified in the Worker script (e.g. `'day9': '<notion-page-id>'`),
and then redeploy the Worker on the Cloudflare dashboard.

That's way too much work, so I made a few Python scripts that automates this.

## The Python Scripts

### Building the Worker Script

[`build_worker.py`](worker-utils/worker_utils/build_worker/build_worker.py)
does a few things:

- It uses the Notion API to gather all the posts from the inline database
nested in the main Air Castles Notion page
- An object mapping URL slugs to the Notion page IDs for each post gathered
in the above step is created
- It reads in [`workerTemplate.js`](worker/workerTemplate.js), copying each
line over to [`resolvedWorker.js`](worker/resolvedWorker.js), except when it
comes across a line in the template JS containing a sentinel marker:
`/* ~+_insertion-marker_+~ */`. This line is replaced with a JavaScript const
object containing the object mapping created in the above step

### Uploading the Worker Script

`upload_worker.py` uses the Cloudflare API to upload the newly created Worker
script to my Cloudflare account.

## CLI

I don't want to have to run both the build and upload scripts, so
[`update-script.sh`](./update-script.sh) was created to do this for me. If the
build script errors out for any reason, the upload script won't be run.
