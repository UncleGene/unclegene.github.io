"""Build the static showcase or refresh its public GitHub inventory (stdlib only)."""

import argparse
import json
import re
import tempfile
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from statistics import median
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'UncleGene'
ORIGIN = 'https://unclegene.github.io'
RECENCY_WINDOW = 10


def https_url(value):
    if not isinstance(value, str):
        raise ValueError('URL must be text')
    url = urlsplit(value)
    if url.scheme != 'https' or not url.netloc or url.username or url.password:
        raise ValueError(f'Expected an absolute HTTPS URL: {value!r}')
    return value


def commit_timestamp(value):
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if date.tzinfo is None:
        raise ValueError('Commit timestamps must include a timezone')
    return date.timestamp()


def activity_midpoint(repo):
    dates = [commit_timestamp(commit['date']) for commit in repo['recent_commits']]
    return median(dates) if dates else float('-inf')


def validate_repositories(repositories):
    if not isinstance(repositories, list) or not repositories:
        raise ValueError('Expected a nonempty repository list')
    seen = set()
    for repo in repositories:
        name = repo['name']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or name in ('.', '..'):
            raise ValueError(f'Invalid repository name: {name!r}')
        if name.lower() in seen:
            raise ValueError(f'Duplicate repository: {name}')
        seen.add(name.lower())
        if repo['html_url'] != f'https://github.com/{OWNER}/{name}':
            raise ValueError(f'Unexpected repository URL for {name}')
        for key in ('fork', 'archived', 'has_pages'):
            if not isinstance(repo[key], bool):
                raise ValueError(f'{name}: {key} must be boolean')
        for key in ('description', 'language'):
            if repo[key] is not None and not isinstance(repo[key], str):
                raise ValueError(f'{name}: {key} must be text or null')
        commits = repo['recent_commits']
        if not isinstance(commits, list) or len(commits) > RECENCY_WINDOW:
            raise ValueError(f'{name}: expected at most {RECENCY_WINDOW} recent commits')
        commit_shas = set()
        for commit in commits:
            if not re.fullmatch(r'[0-9a-f]{40}', commit['sha']) or commit['sha'] in commit_shas:
                raise ValueError(f'{name}: invalid or duplicate commit SHA')
            commit_shas.add(commit['sha'])
            commit_timestamp(commit['date'])
        pages = repo['pages']
        if pages is not None:
            if not repo['has_pages']:
                raise ValueError(f'{name}: Pages URL without Pages enabled')
            https_url(pages['url'])
            if type(pages['status']) is not int or not 100 <= pages['status'] <= 599:
                raise ValueError(f'{name}: invalid HTTP status')


def fetch_json(url):
    request = Request(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'UncleGene-showcase'})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_recent_commits(name):
    try:
        rows = fetch_json(f'https://api.github.com/repos/{OWNER}/{name}/commits?per_page={RECENCY_WINDOW}')
    except HTTPError as error:
        with error:
            if error.code == 409 and json.load(error).get('message') == 'Git Repository is empty.':
                return []
        raise
    if not isinstance(rows, list):
        raise ValueError(f'{name}: invalid commit listing')
    return [{'sha': row['sha'], 'date': row['commit']['committer']['date']} for row in rows]


def check_pages(url):
    request = Request(https_url(url), method='HEAD', headers={'User-Agent': 'UncleGene-showcase'})
    try:
        with urlopen(request, timeout=30) as response:
            https_url(response.url)
            return response.status
    except HTTPError as error:
        with error:
            return error.code


def fetch_repositories(domains):
    repositories = []
    page = 1
    while True:
        rows = fetch_json(f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&sort=full_name&page={page}')
        if not isinstance(rows, list):
            raise ValueError('GitHub returned an invalid repository listing')
        for row in rows:
            if row['private'] or row['owner']['login'].lower() != OWNER.lower():
                raise ValueError('GitHub returned a private or non-owned repository')
            repo = {key: row[key] for key in ('name', 'html_url', 'description', 'language', 'fork', 'archived', 'has_pages')}
            repo['pages'] = None
            if row['has_pages']:
                default = ORIGIN + '/' if row['name'].lower() == 'unclegene.github.io' else ORIGIN + '/' + row['name'] + '/'
                override = domains['overrides'].get(row['name'], {})
                homepage = row.get('homepage')
                candidate = override.get('pages_url') or (homepage if homepage and homepage.startswith('https://') else default)
                repo['pages'] = {'url': https_url(candidate), 'status': check_pages(candidate)}
            repo['recent_commits'] = fetch_recent_commits(repo['name'])
            repositories.append(repo)
        if len(rows) < 100:
            break
        page += 1
    validate_repositories(repositories)
    return sorted(repositories, key=lambda r: r['name'].lower())


def refresh(path, domains):
    repositories = fetch_repositories(domains)
    catalog = {'checked_at': datetime.now(timezone.utc).date().isoformat(), 'repositories': repositories}
    content = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False, encoding='utf-8') as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)
    temporary_path.replace(path)


def render(catalog, domains):
    repositories = catalog['repositories']
    validate_repositories(repositories)
    by_name = {r['name']: r for r in repositories}
    seen = set()
    groups = []
    for group in domains['groups']:
        names = [n for n in group['repos'] if n in by_name]
        if seen.intersection(names) or len(names) != len(set(names)):
            raise ValueError('A repository is assigned to more than one group')
        seen.update(names)
        if names:
            groups.append((group, names))
    other = [r['name'] for r in repositories if r['name'] not in seen]
    if other:
        groups.append(({'id': 'other', 'title': 'Other projects', 'description': 'More public work, ready to explore.'}, other))
    scores = {r['name']: activity_midpoint(r) for r in repositories}
    groups.sort(key=lambda item: (-max(scores[name] for name in item[1]), item[0]['title'].casefold(), item[0]['id']))
    navigation = ''.join(f'<a href="#{escape(g["id"])}">{escape(g["title"])}</a>' for g, _ in groups)
    sections = []
    for number, (group, names) in enumerate(groups, 1):
        cards = []
        for name in names:
            repo = by_name[name]
            override = domains['overrides'].get(name, {})
            description = override.get('description') or repo['description'] or 'Public project repository.'
            tags = [repo['language']] if repo['language'] else []
            tags += [label for flag, label in [('fork', 'Fork'), ('archived', 'Archived')] if repo[flag]]
            if override.get('note'):
                tags.append(override['note'])
            pages = repo['pages']
            site_link = ''
            if pages:
                if 200 <= pages['status'] < 300:
                    label = override.get('pages_label', 'Visit site')
                    site_link = f'<a class="site-link" href="{escape(pages["url"])}">{escape(label)} <span aria-hidden="true">↗</span></a>'
                else:
                    site_link = f'<span class="unavailable">Pages unavailable (HTTP {pages["status"]})</span>'
            elif repo['has_pages']:
                site_link = '<span class="unavailable">Pages URL not yet verified</span>'
            if override.get('video_url'):
                site_link += f'<a href="{escape(https_url(override["video_url"]))}">Watch the talk <span aria-hidden="true">↗</span></a>'
            links = f'<div class="project-links"><a href="{escape(repo["html_url"])}">Repository <span aria-hidden="true">↗</span></a>{site_link}</div>'
            notice = f'<p class="compatibility-note">{escape(override["notice"])}</p>' if override.get('notice') else ''
            if name == 'concur':
                embed_url = https_url(override['video_embed_url'])
                poster = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="strict-origin-when-cross-origin"><title>Play the concurrency talk</title><style>html,body,a{{margin:0;width:100%;height:100%;display:block}}a{{position:relative;background:#17241a;color:white;font:600 16px system-ui}}img{{width:100%;height:100%;object-fit:cover}}span{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#203e29;padding:14px 22px;border:1px solid #b8c9ac;border-radius:4px;white-space:nowrap}}a:focus-visible span{{outline:3px solid white;outline-offset:5px}}</style></head><body><a href="{escape(embed_url)}?autoplay=1" aria-label="Play Rails: Shadow Facets of Concurrency"><img src="/images/concur-talk.jpg" alt=""><span>▶ Play talk</span></a></body></html>'''
                cards.append(f'''<article class="talk-feature" data-repo="concur">
  <div class="talk-video"><iframe src="{escape(embed_url)}" srcdoc="{escape(poster)}" title="Rails: Shadow Facets of Concurrency — Eugene Kalenkovich at Rocky Mountain Ruby 2013" width="640" height="360" referrerpolicy="strict-origin-when-cross-origin" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
  <div class="talk-copy"><p class="eyebrow">Featured talk · Rocky Mountain Ruby 2013</p><h3>Rails: Shadow Facets of Concurrency</h3><p>Explore the concurrency pitfalls hidden behind Rails’ convenience, from simple surprises to problems that catch experienced developers.</p><p class="talk-context"><code>concur</code> · The recording, slides, and original Rails sandbox.</p>{links}</div>
</article>''')
            else:
                cards.append(f'''<article class="project" data-repo="{escape(name)}">
  <div class="project-top"><span class="project-icon" aria-hidden="true">↗</span><span class="project-tags">{escape(' · '.join(tags))}</span></div>
  <h3>{escape(name)}</h3>
  <p>{escape(description.strip())}</p>{notice}
  {links}
</article>''')
        score = max(scores[name] for name in names)
        if score == float('-inf'):
            activity = '<p class="activity-date">No commit history</p>'
        else:
            date = datetime.fromtimestamp(score, timezone.utc)
            activity = f'<p class="activity-date">Activity midpoint · <time datetime="{date.isoformat()}">{date:%b %Y}</time></p>'
        group_notice = f'<p class="domain-notice">{escape(group["notice"])}</p>' if group.get('notice') else ''
        sections.append(f'''<section class="domain" id="{escape(group['id'])}" aria-labelledby="{escape(group['id'])}-title">
  <div class="domain-heading"><span class="section-number" aria-hidden="true">{number:02}</span><div><h2 id="{escape(group['id'])}-title">{escape(group['title'])}</h2><p>{escape(group['description'])}</p>{activity}</div><span class="count">{len(names):02}</span></div>
  {group_notice}<div class="project-grid">{''.join(cards)}</div>
</section>''')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Eugene Kalenkovich's public projects: code quality, concurrency, search, digital preservation, and the 203 blog archive.">
  <title>Eugene Kalenkovich — Projects & writing</title>
  <link rel="canonical" href="{ORIGIN}/">
  <link rel="icon" href="/favicon.png">
  <link rel="stylesheet" href="/stylesheets/showcase.css">
  <link rel="alternate" type="application/atom+xml" title="203 blog" href="/blog/atom.xml">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="shell">
  <header class="site-header"><a class="wordmark" href="/">EK<span aria-hidden="true">.</span></a><span class="identity">Eugene Kalenkovich <span>/ UncleGene</span></span><nav aria-label="Main"><a href="#projects">Projects</a><a href="/blog/">Writing</a><a href="https://github.com/UncleGene">GitHub <span aria-hidden="true">↗</span></a></nav></header>
  <main id="main">
    <section class="intro" aria-labelledby="intro-title"><p class="eyebrow"><span aria-hidden="true">●</span> A collection of public work</p><h1 id="intro-title">Code, curiosity,<br>and things worth <em>keeping.</em></h1><div class="intro-bottom"><p>Tools, experiments, and recovered knowledge.<br>A directory of what I build, explore, and write.</p><a class="text-link" href="#projects">Explore {len(repositories)} repositories <span aria-hidden="true">↓</span></a></div></section>
    <div class="directory" id="projects"><div class="directory-label"><h2>Project directory</h2><span>{len(repositories):02} repositories / {len(groups):02} domains</span></div><p class="directory-note">Domains ordered by recent commit activity.</p><nav class="domain-nav" aria-label="Project domains">{navigation}</nav></div>
    {''.join(sections)}
    <section class="blog-feature" aria-labelledby="blog-title"><div class="blog-mark" aria-hidden="true">203<span>THE ARCHIVE</span></div><div><p class="eyebrow">Writing · 2013–2015</p><h2 id="blog-title">Notes from an earlier web.</h2><p>The original 203 blog. Fifteen posts on services, software design, Ruby, Rails, and a few things in between.</p><a class="text-link" href="/blog/">Read the blog archive <span aria-hidden="true">↗</span></a></div></section>
  </main>
  <footer class="site-footer"><p>Eugene Kalenkovich <span>/ Built with curiosity.</span></p><p>Public repository directory · Checked {escape(catalog['checked_at'])} <a href="https://github.com/UncleGene">GitHub ↗</a></p></footer>
</div>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'refresh'])
    args = parser.parse_args()
    path = ROOT / 'data/repositories.json'
    domains = json.loads((ROOT / 'data/domains.json').read_text())
    if args.command == 'refresh':
        refresh(path, domains)
    catalog = json.loads(path.read_text())
    (ROOT / 'index.html').write_text(render(catalog, domains))
    print(f'Built showcase with {len(catalog["repositories"])} public repositories.')


if __name__ == '__main__':
    main()
