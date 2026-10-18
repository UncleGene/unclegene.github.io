# Eugene Kalenkovich — projects and writing

A static GitHub Pages user homepage with all public repositories grouped by
subject. The original **203** blog lives at `/blog/`, including its 15 articles,
archives, categories, downloads, and Atom feed.

## Preview

Requires Python 3.10 or newer. No package installation or original Octopress
build environment is needed.

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. The generated HTML, CSS, and blog files are served
directly by GitHub Pages; `.nojekyll` disables unnecessary Jekyll processing.
Commit and push the reviewed files to the repository's configured publishing
branch to publish. Local changes alone do not update the live site.

## Update the directory

```sh
python3 tools/site.py refresh
python3 -m unittest discover -s tests -v
```

`refresh` reads all pages of the public owned-repository listing from GitHub,
checks Pages URLs, updates `data/repositories.json`, and rebuilds `index.html`.
Network or API failures stop the refresh and leave the last valid inventory
intact. It uses public endpoints without credentials; API rate limits can
require retrying later. Pages availability is a snapshot from the last refresh.

Edit `data/domains.json` to change curated groups, descriptions, or verified
Pages destinations, then rebuild without a network request:

```sh
python3 tools/site.py build
```

GitHub topics are currently empty, so domain membership is curated. New public
repositories appear under **Other projects** until assigned. Forks, archived,
and renamed repositories remain visible. The homepage contains no JavaScript
or visitor-side GitHub API calls.

`concur` publishes its presentation at
<https://unclegene.github.io/concur/rency/>. Its `/concur/` root has no index
page and returns 404; that is not a failed slides deployment. The showcase
links to the slides and the [recorded talk](https://youtu.be/TV5LEjN6d1U).

## Blog compatibility

Old article, archive, category, and pagination URLs serve static redirect pages
to `/blog/`. JavaScript redirects preserve query strings and fragments; meta
refresh and a visible link provide fallbacks. These are HTTP 200 pages rather
than server-side 301 redirects. Existing `/blog/archives/` is the single archive
URL. The old `/atom.xml` and seven category feed URLs remain valid feeds, with
stable article IDs. Migrated copies live under `/blog/`, including category
feeds such as `/blog/categories/ruby/atom.xml`.

The root asset directories intentionally remain byte-for-byte compatibility
copies for cached pages and feed readers. Blog pages use their own assets under
`/blog/`; those may be adjusted without changing the historical asset URLs.
`data/blog-migration.json` records the original routes, article text hashes,
comment identifiers, feed entry IDs, and compatibility asset hashes against
baseline commit `ea70b0d`.

Twitter and Delicious sidebars and loaders are removed. Article quotations of
tweets remain as ordinary text and links, without widget scripts. The old live
GitHub sidebar is replaced with a link to the complete project directory.
Historical comment identifiers are preserved; the availability of third-party
comments and old embedded media depends on their providers. The previous
custom domain, `203.softover.com`, requires separate DNS/hosting control to
redirect; this repository cannot redirect requests that never reach it.

## Checks

```sh
python3 -m unittest discover -s tests -v
ruff check tools tests
```

Tests cover inventory completeness, escaped metadata, API pagination, failed
refresh preservation, Pages/talk links, article text and comment preservation,
legacy destinations, local links and CSS assets, feeds, sitemap, and removed
widgets. Ruff is optional development tooling; it is not needed to build or
serve the site. There is no separate type-check configuration.

See [the project plan](docs/PROJECT_PLAN.md) for requirements and the migration
decision.
