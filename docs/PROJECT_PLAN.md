# User homepage and legacy blog

Status: M1 and M2 published to GitHub Pages on 2026-10-19; live checks passed.
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

## Repository inventory and current groups

Source: public [GitHub repositories API](https://api.github.com/users/UncleGene/repos?type=owner&per_page=100&sort=full_name).
The response contains 13 repositories (fewer than one full 100-item page),
all owned, public, non-fork, and non-archived. None has GitHub topic tags.
These groups are therefore curated from repository descriptions and READMEs;
they are not presented as GitHub-supplied topics.

| Domain | Repositories | Pages status |
| --- | --- | --- |
| Talks and concurrency | `concur` | Featured embedded talk; `/concur/rency/` returns 200 |
| Digital preservation and shooting sports | `bullseye_encyclopedia` | [Published site](https://unclegene.github.io/bullseye_encyclopedia/) returns 200 |
| Search and language | `bise`, `rhymes`, `rhymeapp` | No Pages flag |
| Learning and practice | `drill` | No Pages flag |
| Writing and personal site | `unclegene.github.io` | [Root site](https://unclegene.github.io/) returns 200; include blog link |
| Web security | `last_line` | Historical Rails 3-era library |
| Legacy code quality and analysis | `flay-actionpack`, `flay-haml`, `flay-js`, `flay_haml`, `tax_code` | Historical tools, activity-ordered; compatibility unverified |

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
Separate practice applications from security libraries and concurrency work.
Order sections by accepted D2 activity scoring and retain a visible legacy
analysis compatibility note independently of their position. Identify
`last_line` as Rails 3-era (`rails ~> 3.1`); do not imply verified support for
modern Rails. The Rails constraint is verified in its public gemspec.

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
`https://youtu.be/TV5LEjN6d1U`. Under M2, give this a featured layout within its activity-ordered section
with an accessible, responsive YouTube embed, no playback on page load, and visible
slides, repository and direct video links when playback is unavailable.
Embed construction follows [YouTube player documentation](https://developers.google.com/youtube/player_parameters)
and [privacy-enhanced mode documentation](https://support.google.com/youtube/answer/171780).

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

M1 implementation quality review: all 13 public repositories render in five
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

## M1 acceptance evidence

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

M1 final gates: documentation sync and scope checks passed for R1–R4/D1/M1.
Simplification retained the dependency-free generator, shared test fixtures,
and explicit configuration; no unused infrastructure was introduced. Independent
review passed after the category-feed correction and added network-failure
coverage. All 13 tests, full-repository Ruff checks and staged whitespace checks
pass. Keyboard testing confirmed visible focus on the homepage's skip link.

## M2 — Correct taxonomy and highlight the concurrency talk

Status: acceptance complete locally; independent review passed. Trigger: user feedback on drill/last_line classification,
aging developer tools, and talk visibility. Requirements affected: R1, R2;
R3 and the accepted D1 migration stay unchanged.

Evidence: `drill`'s `app.rb` handles student practice/exercise actions; its README
calls it an evolving Sinatra example. `last_line.gemspec` declares
`rails ~> 3.1`; its README describes controller GET whitelisting and CSRF
checks. Sources: [drill source](https://github.com/UncleGene/drill/blob/master/app.rb),
[last_line gemspec](https://github.com/UncleGene/last_line/blob/master/last_line.gemspec).
User confirms the analysis projects are old; modern compatibility is unverified,
not established broken. Do not equate a curated historical label with GitHub's
archived flag.

Selected slice: one homepage presentation correction. Ranked candidates:
1. Correct misleading categorization/compatibility expectations (R1).
2. Make the requested talk prominent and embeddable (R2).
3. Recheck generated output, responsive layout and documentation.
These form a single reviewable M2 release. No backend, custom player scripts,
blog changes, external repository writes or publishing changes are needed.

Acceptance: all 13 public repositories still appear once; drill is in Learning
& practice, last_line in Web security with its Rails constraint; Legacy code
quality & analysis explicitly says modern compatibility is unverified. Sections
follow the D2 activity rule. Concur retains its featured layout with the supplied recording
embedded at a usable mobile/desktop size, accessible title, no page-load playback and
working direct-video/slides links. Full tests, lint, simplification, delegated
review and local commit remain completion gates.

Quality guard: pass; the user's requested corrections resolve the prior
editorial assumptions. Next action: review the local preview; publish when authorized.

M2 presentation evidence (before recency amendment, independent review passed): 15 tests passed, including new
red/green checks for corrected categories, legacy ordering and notes, and the
featured embed. Full-repository Ruff and whitespace checks pass. Chrome
verified the local poster, its play action loading the YouTube player, and
actual video playback (then paused). The feature fits a 390px screen with a
344×200 player and a 320px screen with a 274×200 player; no horizontal overflow.
A local poster in the iframe's `srcdoc` provides a visible play target before
the external player loads. Selecting it navigates the iframe to YouTube;
playback may require the provider's Play control as well. The source thumbnail
is YouTube's public thumbnail for the user-specified video.

Simplification: repository/slides/video links share one rendering path; the
existing HTML parser now checks frame attributes too. The single featured talk
uses native iframe navigation with no new scripts or player framework.
M2 scope covers homepage taxonomy, compatibility labels, talk presentation and
activity ordering; all blog and compatibility files remain untouched.

M2 presentation review checkpoint (before recency amendment): independent
review passed with no blocking findings; 15 tests, Ruff and whitespace checks
passed. No correction commit was created before the user added the recency
requirement. The pending M2 release now includes the D2 amendment below.

## D2 — Order domains by contribution midpoint

Status: accepted. Date: 2026-10-18. Context: the user identified that concur is
old and requested section ordering by the midpoint of the last N contributions,
superseding the earlier fixed first-talk/last-tools presentation.
Decision: the user accepted the proposed N=10 rule with “go”: use the median
UTC committer timestamp of the last ten default-branch commits per repository,
without author filtering. An even sample averages its middle two timestamps;
a shorter history uses all available commits. A domain uses the newest member
repository midpoint. Sort descending, then by domain title and ID for ties;
empty histories come last. Card order within a domain remains curated.

Consequences: refresh needs one public commit-list request per repository,
stores SHA/date evidence, and fails without replacing inventory if history
retrieval fails. Only GitHub's explicit empty-repository response is treated
as an empty history. The featured talk moves with its domain. Historical
compatibility statements remain independent: the measured code-quality
midpoint is May 2018 due to flay-actionpack's history, placing it second in the
current snapshot. Dates are activity midpoints, not last-updated claims.

Alternatives: latest-commit dates overreact to isolated updates; fixed domain
positions contradict the user's recency request. A wider N=20 window would
weight older work more; the user accepted N=10. This is a transparent activity
heuristic rather than a judgment of software compatibility.

Follow-up: R1/R2 and M2 use D2; refresh/build implementation and tests must prove
median scoring, newest-member aggregation, deterministic ties, short/empty
history, input validation and atomic failure behavior. Reference:
[GitHub list commits](https://docs.github.com/en/rest/commits/commits#list-commits).

M2 amendment validation: current tests cover the accepted scoring rule and
retained featured embed. Renewed independent review passed with no blocking
findings. No publishing or remote repository edits are included.

D2 verification: the full public refresh completed successfully for all 13
repositories, capturing up to ten commit SHAs/timestamps each. All 20 tests,
full-repository Ruff and whitespace checks passed. Chrome confirmed the seven
sections and their visible midpoint dates are in descending score order;
concur remains a featured player within the fourth section in this snapshot.
The presentation-only review was followed by a renewed review of the scoring
and refresh changes; its final verdict is pass, including documentation
corrections. The accepted release is ready for its local commit. No type checker is configured.

Final M2 publication checkpoint: `master`, release `b7cd150`. User authorized
publication on 2026-10-19. The release was pushed to `origin/master`, and
[Pages deployment](https://github.com/UncleGene/unclegene.github.io/actions/runs/39266995141)
completed successfully for that revision. The live homepage contains all 13
repositories and activity-based ordering. Ten additional live checks passed
for the blog, a migrated article, its old redirect, main/category feed pairs,
showcase CSS, talk poster, and a blog image. All 20 tests and full-repository
Ruff passed again before pushing. No remaining release action is required.
Live site: https://unclegene.github.io/ ; archive: https://unclegene.github.io/blog/ .
Earlier local-only checkpoints above describe their state before publication.
