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
checks Pages URLs, captures the latest ten default-branch commits per
repository, updates `data/repositories.json`, and rebuilds `index.html`.
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
and renamed repositories remain visible. Directory content and navigation
work without JavaScript or visitor-side GitHub API calls. The featured concurrency talk uses a local poster and a
standard YouTube embed, loaded after selecting Play. Direct slides and video
links stay visible alongside it.

`concur` publishes its presentation at
<https://unclegene.github.io/concur/rency/>. Its `/concur/` root has no index
page and returns 404; that is not a failed slides deployment. The showcase
features the talk with an embedded recording and direct links to
the slides and the [recorded talk](https://youtu.be/TV5LEjN6d1U).

`drill` is grouped under Learning & practice. `last_line` is grouped under Web
security and labeled Rails 3-era: its gemspec declares `rails ~> 3.1`. Modern
Rails compatibility is unverified. The old Flay plugins and code-churn tool
appear under Legacy code quality & analysis with a visible compatibility
note. These editorial labels do not change the repositories' GitHub archive
settings or claim the tools have been tested against modern applications.

## Activity ordering

Domains are ordered newest first by their most recently active member project.
A project's activity midpoint is the median UTC committer timestamp of its last
10 default-branch commits, using the history GitHub returns without an author
filter. Fewer than 10 commits use the available history; empty histories sort
last. For an even count, use the midpoint of the two central timestamps. Equal
domain scores sort by title, then ID, so build results are deterministic.
Repository cards within a domain retain their curated order.

The date displayed on a domain is its activity midpoint, not its last update.
Later maintenance commits can give an old library a newer score, so the
historical compatibility notes remain independent of the ordering. For example,
Flay ActionPack currently gives its domain a May 2018 midpoint. Membership and
descriptions remain curated in `data/domains.json`; file order does not pin a
domain's screen position. Refresh updates all histories atomically with the
inventory; history-fetch failures preserve the previous inventory too.

## Blog compatibility

Old article, archive, category, and pagination URLs serve static redirect pages
to `/blog/`. JavaScript redirects preserve query strings and fragments; meta
refresh and a visible link provide fallbacks. These are HTTP 200 pages rather
than server-side 301 redirects. Existing `/blog/archives/` is the single archive
URL. The old `/atom.xml` and seven category feed URLs remain valid feeds, with
stable article IDs. Migrated copies live under `/blog/`, including category
feeds such as `/blog/categories/ruby/atom.xml`.

Historical root assets intentionally remain byte-for-byte compatibility
files for cached pages and feed readers. Blog pages use their own assets under
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
