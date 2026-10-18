# User homepage and legacy blog

Status: M1 complete locally; acceptance and independent review passed; not published.
Full `/blog/` migration approved on 2026-10-18.
Request: replace the root blog with a showcase of all public repositories,
grouped by topic/domain, including project Pages links and the legacy blog.
Remove the blog's Twitter and Delicious sections.

## Verified baseline — 2026-10-18

- Branch `master`, starting HEAD `ea70b0d`; initially clean working tree.
- Published Octopress output only: 29 HTML documents, including 15 dated
  articles. No project guide, plan, source generator, test suite, package
  manifest, or deployment workflow is present.
- Root blog title and author: `index.html:8` and `index.html:9`.
- Root-relative CSS, feed, scripts and images need migration handling:
  `index.html:21`–`index.html:28`, `stylesheets/screen.css:1`.
- All 29 HTML documents mention the former domain, `203.softover.com`.
  Sitemap and robots also point there: `sitemap.xml:91`, `robots.txt:4`.
- `/archives/` and `/blog/archives/` both exist; merge their migration targets
  into one `/blog/archives/` rather than creating `/blog/blog/archives/`.
- One root-relative link targets another project, `/concur/rency`
  (`2013/12/07/rails-shadow-facets-of-concurrency/index.html:102`). It must
  not receive the blog prefix. Its current availability is not verified.
- Disqus uses historical URL identifiers, e.g.
  `2013/12/07/rails-shadow-facets-of-concurrency/index.html:267`.
  Preserve identifiers to avoid detaching existing comment threads.

## Repository inventory and proposed groups

Source: public [GitHub repositories API](https://api.github.com/users/UncleGene/repos?type=owner&per_page=100&sort=full_name).
The response contains 13 repositories (fewer than one full 100-item page),
all owned, public, non-fork, and non-archived. None has GitHub topic tags.
These groups are therefore curated from repository descriptions and READMEs;
they are not presented as GitHub-supplied topics.

| Domain | Repositories | Pages status |
| --- | --- | --- |
| Code quality and analysis | `flay-actionpack`, `flay-haml`, `flay-js`, `flay_haml`, `tax_code` | No Pages flag |
| Web applications and concurrency | `concur`, `drill`, `last_line` | `concur`: default URL returns 404; `/concur/rency/` returns 200 |
| Search and language | `bise`, `rhymes`, `rhymeapp` | No Pages flag |
| Digital preservation and shooting sports | `bullseye_encyclopedia` | [Published site](https://unclegene.github.io/bullseye_encyclopedia/) returns 200 |
| Writing and personal site | `unclegene.github.io` | [Root site](https://unclegene.github.io/) returns 200; include blog link |

`flay_haml` remains included because all public repositories are in scope;
its description identifies it as renamed to `flay-haml`. Label that status
without assuming the obsolete homepage URL is authoritative.

The Bullseye README confirms the preservation project's subject and published
URL. The `concur` README describes a Rails concurrency sandbox. Public HTTP
HEAD checks verified the three Pages responses above on the assessment date.
Pages-enabled metadata alone does not establish that a default URL is live.
Custom Pages domains require explicit verification rather than guessing.

## Requirements

### R1 — Discover public work

Status: active. Type: core. Priority: high.

Visitors can browse every public repository owned by UncleGene at `/`, grouped
by domain. Each entry has a repository link and a concise factual description.
Include renamed repositories and this site's repository. Missing descriptions
receive a curated factual summary; do not invent product capabilities.

Given the captured inventory, when the homepage renders, then all 13 unique
repositories appear exactly once and the groups explain their subject areas.
Use responsive semantic HTML with keyboard-visible focus and readable contrast.

### R2 — Reach published project sites

Status: active. Type: core. Priority: high.

Repository entries with Pages also show site availability separately from the
repository link. Verified sites receive a working site link. Pages-enabled
projects with a failing URL receive an explicit unavailable status and retain
their repository link; do not present their broken site as a working demo.
Verify any custom domain before using it. Recheck during implementation.

Given Bullseye's successful verification, its entry links to its published site.
The `concur` Pages branch has no root `index.html`, but does contain
`rency/index.html`. The verified slides destination is
`https://unclegene.github.io/concur/rency/`; use it instead of the project root.
Its entry also links to the user-supplied recording at
`https://youtu.be/TV5LEjN6d1U` (a link, keeping the homepage free of embeds).

### R3 — Preserve writing and access

Status: active (full `/blog/` migration approved). Type: core. Priority: high.

The homepage links prominently to the legacy `203` blog. Preserve all 15
articles, images, downloadable files, categories, archives, pagination and feed.
Preserve article wording and historical comment identifiers. Remove the Twitter
timeline and Delicious sidebar sections, their loaders, and exclusive helper
code. Retain the blog's recognizable styling and add a link to the showcase.

Given an old article URL, visitors can still reach that article. Given a blog
page, internal links and local assets resolve to their intended destinations.
Cross-project links retain their project paths. Verify Twitter/Delicious widget
markup and requests are absent from every blog page.

### R4 — Keep updates maintainable

Status: active. Type: data-integrity. Priority: medium.

Keep a checked-in repository inventory and explicit domain overrides, with a
small documented refresh/build command. Fetch all API pages when refreshing;
validate and replace the inventory only after a complete successful fetch.
Keep the last valid inventory on API/network failure. New/unclassified public
repositories remain visible in an Other projects group until curated.
Render repository content as escaped text. Serve the generated showcase
without requiring visitor-side GitHub API calls, credentials or JavaScript.

## Feasibility and proposed structure

Moving the blog one level deeper is feasible with static files. GitHub Pages
[serves HTML/CSS/JavaScript and supports both account and project sites](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
No original Octopress build environment needs to be restored.

Implemented layout (D1):

```text
/                         repository showcase
/blog/                    legacy blog landing page
/blog/2013/...             relocated articles (also 2014 and 2015)
/blog/archives/            unified archive
/blog/categories/...       categories
/blog/posts/...            pagination
/blog/atom.xml             canonical blog feed
/blog/{images,stylesheets,javascripts,downloads}/...
/2013/..., /2014/..., ...   compatibility pages for old HTML URLs
/atom.xml                  valid compatibility feed for existing subscribers
```

Rewrite known blog-owned paths in HTML, CSS and feed content using an explicit
route map. Update canonical URLs, feed links, search scope, sitemap and robots
to HTTPS on `unclegene.github.io`; preserve historical identifiers independently.
Keep existing static asset URLs working for cached pages/feed consumers.
Retain one canonical archive path. Keep sibling project routes outside the map.

Compatibility pages use a canonical link, immediate meta refresh, and a visible
destination link. Static redirect pages are HTTP 200, not server-side 301s;
GitHub Pages offers no application server here. The old custom domain can only
be redirected if its owner controls its hosting/DNS; this repository cannot
guarantee access through that domain. Old root `/` necessarily becomes the
showcase, with a prominent route to the blog.

Alternative: only put the blog landing page at `/blog/`, retaining article,
category and asset URLs at the root. That preserves article addresses directly
and reduces migration work, but the blog remains spread across the root
namespace. The showcase is the same under either choice.

## Impact and scope

This is a local project improvement: root entry point, blog routes and assets,
feed/discovery metadata, curated inventory, maintenance docs and validation.
There are no prior requirements or decisions to supersede. Public repository
discovery provides the value; preserving writing protects existing readers.

Do not change other repositories, their Pages settings, DNS, article prose,
or GitHub account topics. No SPA framework, backend, new analytics service or
original Octopress restoration is needed. No deployment or push is authorized
by this planning artifact.

## Delivery and acceptance

M1 — One cohesive, reviewable homepage release (R1–R4): generate the grouped
showcase, preserve the blog using the chosen URL policy, remove obsolete
sidebars, document refresh and local preview, and verify compatibility.

Ranked work candidates within this milestone:

1. Resolve and implement blog preservation: greatest existing-reader regression
   risk and determines the root replacement's compatibility contract.
2. Deliver the complete grouped showcase and verified site links: main new
   visitor value; uses the preserved blog's agreed destination.
3. Finish inventory refresh and repeatable validation: maintains completeness
   and proves the full release, after route and content contracts are settled.

The selected implementation slice is the cohesive M1 release; these candidates
are its ordered work, not separate infrastructure-only milestones.

Checks required before acceptance:

- Compare generated entries against all public owned repositories in inventory;
  check uniqueness, escaping, grouping and Pages statuses.
- Check all 15 article bodies survived migration, every original HTML route has
  a working destination, and canonical/archive mappings have no redirect loops.
- Crawl local HTML/CSS/feed links and assets, distinguishing sibling-project
  links from blog-owned paths; report external failures separately.
- Parse feeds and sitemap; verify public URLs, valid old feed compatibility,
  unchanged historical feed entry IDs and comment identifiers.
- Verify removed sidebar widgets do not load scripts or leave dead markup.
- Check desktop and narrow layouts, keyboard navigation, and rendering with
  visitor JavaScript disabled. Recheck published project URLs.
- Run the full new validation suite, simplify the implementation, review the
  final diff for correctness and scope, and update this plan with evidence.

Implementation quality review: all 13 public repositories render in five
domains; every original HTML route is accounted for; 15 article texts,
historical comment IDs, feed entry IDs and 71 compatibility assets are
verified against the baseline manifest. The main and seven category feeds
are available at both historical and migrated URLs. The checked-in generator and
13-test suite cover the requirements. There is no separate type-check gate.

## Checkpoint

Branch `master`, baseline HEAD `ea70b0d`. M1 is included in the local release
commit containing this checkpoint; use `git log -1` for its revision. No remote
repositories or hosting settings were changed. Recommended next action: review
the local preview and publish the release when authorized.

## D1 — Self-contained blog namespace

Status: accepted. Date: 2026-10-18.
Context: the repository root must become a project showcase while published
writing remains reachable and the legacy blog has a clear home.
Decision: the user selected a full `/blog/` migration. Old HTML addresses will
serve static compatibility redirects; the old feed and asset addresses remain
usable. Remove the Twitter and Delicious sections as explicitly requested.
Alternative: moving only the landing page would avoid article redirects but
leave blog routes scattered across the showcase namespace.
Consequences: rewrite and validate blog-owned paths, retain historical IDs, and
maintain static compatibility files. Redirect responses remain HTTP 200.
Follow-up: implement M1 and record validation evidence before acceptance.

## Acceptance evidence

- `python3 tools/site.py refresh`: 13 public repositories; all three configured
  Pages destinations returned successful responses, including concur's slides.
- `python3 -m unittest discover -s tests -v`: 13 tests passed. Tests were
  introduced before implementation and initially failed on the missing
  generator. Initial migration checks found an old Bootstrap icon path and
  inline Twitter loader; both were corrected before the green run.
- `ruff check tools tests`: passed. No typed-code toolchain is configured.
- Chrome local preview: desktop 1710px, mobile 390px; no horizontal overflow.
  The blog also fits 390px and images load. A 320px archive copy with script
  tags removed confirms readable content and visible fallback navigation.
- Old article navigation preserved the test query string and `#content`
  fragment while reaching the migrated article.
- External comment/media availability is provider-dependent. No push or
  production deployment has occurred.

Review correction: seven category-specific feeds were added to the migration
and compatibility checks; all feed entry IDs and self/entry URLs are verified.
Inherited whitespace is normalized in new text asset copies; root compatibility
asset bytes remain unchanged.

Final gates: documentation sync and scope checks passed for R1–R4/D1/M1.
Simplification retained the dependency-free generator, shared test fixtures,
and explicit configuration; no unused infrastructure was introduced. Independent
review passed after the category-feed correction and added network-failure
coverage. All 13 tests, full-repository Ruff checks and staged whitespace checks
pass. Keyboard testing confirmed visible focus on the homepage's skip link.
