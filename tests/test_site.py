import hashlib
import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urljoin, urlsplit

from tools import site

ROOT = Path(__file__).resolve().parents[1]


class HTML(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.repositories = []
        self.ids = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-repo' in attrs:
            self.repositories.append(attrs['data-repo'])
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src', 'action', 'poster'):
            if attrs.get(key):
                self.links.append(attrs[key])


def article_text(source):
    class Content(HTMLParser):
        depth = 0
        text = ''
        ignored = 0

        def handle_starttag(self, tag, attrs):
            if tag in ('script', 'style'):
                self.ignored += 1
            if tag == 'div':
                if dict(attrs).get('class') == 'entry-content' or self.depth:
                    self.depth += 1

        def handle_endtag(self, tag):
            if tag in ('script', 'style'):
                self.ignored -= 1
            if tag == 'div' and self.depth:
                self.depth -= 1

        def handle_data(self, data):
            if self.depth and not self.ignored:
                self.text += data
    parser = Content()
    parser.feed(source)
    return hashlib.sha256(' '.join(parser.text.split()).encode()).hexdigest()


def api_rows(count):
    return [dict(name=f'project-{i}', html_url=f'https://github.com/UncleGene/project-{i}',
                 description=None, language=None, fork=False, archived=False,
                 has_pages=False, homepage=None, private=False,
                 owner={'login': 'UncleGene'}) for i in range(count)]


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'data/repositories.json').read_text())
        self.groups = json.loads((ROOT / 'data/domains.json').read_text())

    def test_build_is_reproducible_and_complete(self):
        generated = site.render(self.catalog, self.groups)
        self.assertEqual(generated, (ROOT / 'index.html').read_text())
        names = HTML(generated).repositories
        self.assertEqual(sorted(names), sorted(r['name'] for r in self.catalog['repositories']))
        self.assertEqual(len(names), len(set(names)))

    def test_unknown_repository_is_visible_and_content_is_escaped(self):
        repo = dict(self.catalog['repositories'][0], name='new-project',
                    html_url='https://github.com/UncleGene/new-project',
                    description='<script>alert("x")</script>', pages=None)
        self.catalog['repositories'].append(repo)
        generated = site.render(self.catalog, self.groups)
        self.assertIn('Other projects', generated)
        self.assertIn('data-repo="new-project"', generated)
        self.assertIn('&lt;script&gt;', generated)
        self.assertNotIn('<script>', generated)

    def test_bad_or_duplicate_repository_is_rejected(self):
        repos = self.catalog['repositories']
        with self.assertRaises(ValueError):
            site.validate_repositories(repos + [repos[0]])
        for key, value in [('html_url', 'javascript:alert(1)'), ('has_pages', 'yes'),
                           ('name', '../../escape')]:
            bad = dict(repos[0], **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                site.validate_repositories([bad])

    def test_live_pages_links_include_concur_slides(self):
        source = site.render(self.catalog, self.groups)
        self.assertIn('href="https://unclegene.github.io/concur/rency/"', source)
        self.assertIn('href="https://unclegene.github.io/bullseye_encyclopedia/"', source)
        self.assertIn('href="/blog/"', source)
        self.assertIn('href="https://youtu.be/TV5LEjN6d1U"', source)
        self.assertNotIn('<script', source)

    def test_refresh_fetches_every_page(self):
        rows = api_rows(101)
        with patch.object(site, 'fetch_json', side_effect=[rows[:100], rows[100:]]) as fetch:
            result = site.fetch_repositories(self.groups)
        self.assertEqual(len(result), 101)
        self.assertEqual(fetch.call_count, 2)
        self.assertIn('page=2', fetch.call_args.args[0])

    def test_failed_refresh_preserves_last_good_inventory(self):
        for stage in ('first page', 'second page', 'Pages probe'):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'repositories.json'
                path.write_text('last good inventory')
                if stage == 'first page':
                    responses = [OSError('network failure')]
                elif stage == 'second page':
                    responses = [api_rows(100), OSError('network failure')]
                else:
                    rows = api_rows(1)
                    rows[0]['has_pages'] = True
                    responses = [rows]
                with patch.object(site, 'fetch_json', side_effect=responses):
                    with patch.object(site, 'urlopen', side_effect=OSError('Pages network failure')):
                        with self.assertRaises(OSError):
                            site.refresh(path, self.groups)
                self.assertEqual(path.read_text(), 'last good inventory')

    def test_unavailable_pages_do_not_appear_as_live_sites(self):
        repo = next(r for r in self.catalog['repositories'] if r['name'] == 'concur')
        repo['pages']['status'] = 404
        source = site.render(self.catalog, self.groups)
        self.assertIn('Pages unavailable (HTTP 404)', source)
        self.assertNotIn('href="https://unclegene.github.io/concur/rency/"', source)
        self.assertIn('href="https://youtu.be/TV5LEjN6d1U"', source)


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / 'data/blog-migration.json').read_text())

    def test_all_original_routes_resolve_and_redirects_do_not_loop(self):
        for old, new in self.manifest['routes'].items():
            target = ROOT / new.lstrip('/') / 'index.html'
            self.assertTrue(target.is_file(), new)
            source = target.read_text()
            self.assertNotIn('http-equiv="refresh"', source, new)
            self.assertIn(f'<link rel="canonical" href="https://unclegene.github.io{new}">', source)
            if old != '/' and old != new:
                redirect = (ROOT / old.lstrip('/') / 'index.html').read_text()
                self.assertIn(f'url={new}', redirect)
                self.assertIn(f'href="{new}"', redirect)

    def test_article_text_and_comment_identifiers_preserved(self):
        self.assertEqual(len(self.manifest['articles']), 15)
        for path, expected in self.manifest['articles'].items():
            source = (ROOT / 'blog' / path).read_text()
            self.assertEqual(article_text(source), expected['text_sha256'], path)
            for identifier in expected['comment_identifiers']:
                self.assertIn(identifier, source, path)

    def test_no_obsolete_sidebar_or_widgets_remain(self):
        for path in (ROOT / 'blog').rglob('*.html'):
            source = path.read_text()
            for forbidden in ('twitter-timeline', 'twitter-share-button', 'twitterWidgets',
                              'platform.twitter.com', 'feeds.delicious.com', 'id="delicious"'):
                self.assertNotIn(forbidden, source, str(path))
            self.assertIn('href="/"', source, str(path))
        self.assertNotIn('renderDeliciousLinks', (ROOT / 'blog/javascripts/octopress.js').read_text())

    def test_local_links_and_css_assets_resolve(self):
        for path in [ROOT / 'index.html', *(ROOT / 'blog').rglob('*.html')]:
            source_url = 'https://unclegene.github.io/' + path.relative_to(ROOT).as_posix()
            parsed = HTML(path.read_text())
            self.assertEqual(len(parsed.ids), len(set(parsed.ids)), str(path))
            for link in parsed.links:
                url = urlsplit(urljoin(source_url, link))
                if url.netloc != 'unclegene.github.io' or url.path.startswith(('/concur/', '/bullseye_encyclopedia/')):
                    continue
                target = ROOT / url.path.lstrip('/')
                self.assertTrue(target.is_file() or (target / 'index.html').is_file(), f'{path}: {link}')
        for path in [ROOT / 'stylesheets/showcase.css', *(ROOT / 'blog/stylesheets').rglob('*.css')]:
            base = 'https://unclegene.github.io/' + path.relative_to(ROOT).as_posix()
            for link in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)', path.read_text()):
                url = urlsplit(urljoin(base, link))
                if url.netloc == 'unclegene.github.io':
                    self.assertTrue((ROOT / url.path.lstrip('/')).is_file(), f'{path}: {link}')

    def test_feeds_ids_links_and_sitemap(self):
        ns = {'a': 'http://www.w3.org/2005/Atom', 's': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        expected_ids = {'atom.xml': self.manifest['feed_entry_ids'], **self.manifest['category_feeds']}
        for filename, ids in expected_ids.items():
            for copy in (filename, 'blog/' + filename):
                source = (ROOT / copy).read_text()
                feed = ET.fromstring(source)
                self.assertEqual([e.text for e in feed.findall('a:entry/a:id', ns)], ids, copy)
                self.assertNotIn('platform.twitter.com', source, copy)
                for link in feed.findall('.//a:link', ns):
                    self.assertTrue(link.attrib['href'].startswith('https://unclegene.github.io/'), copy)
                    url = urlsplit(link.attrib['href'])
                    target = ROOT / url.path.lstrip('/')
                    self.assertTrue(target.is_file() or (target / 'index.html').is_file(), f'{copy}: {url.path}')
                self_link = feed.find('a:link[@rel="self"]', ns)
                self.assertEqual(self_link.attrib['href'], 'https://unclegene.github.io/' + copy)
        sitemap = ET.parse(ROOT / 'sitemap.xml').getroot()
        urls = [e.text for e in sitemap.findall('s:url/s:loc', ns)]
        self.assertIn('https://unclegene.github.io/', urls)
        for route in set(self.manifest['routes'].values()):
            self.assertIn('https://unclegene.github.io' + route, urls)
        self.assertNotIn('203.softover.com', (ROOT / 'robots.txt').read_text())

    def test_compatibility_assets_are_preserved(self):
        for filename, signature in self.manifest['assets'].items():
            self.assertEqual(hashlib.sha256((ROOT / filename).read_bytes()).hexdigest(), signature, filename)


if __name__ == '__main__':
    unittest.main()
