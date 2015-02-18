"""
Summary Footnotes
-------------

Fix handling of footnote links inside article summaries.
Option to either remove them or make them link to the article page.
Also never show the footnotes themselves in the summary.
"""

from pelican import contents
from pelican import signals
from bs4 import BeautifulSoup
from six import text_type

def initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('SUMMARY_FOOTNOTES_MODE',
                              'link')
    if pelican:
        pelican.settings.setdefault('SUMMARY_FOOTNOTES_MODE',
                                    'link')

    orig_summary = contents.Content.summary
    contents.Content.summary = \
            property(lambda instance:
                        get_summary(instance, orig_summary),
                     orig_summary.fset, orig_summary.fdel,
                     orig_summary.__doc__)


def transform_summary(summary, article_url, site_url, mode):
    summary = BeautifulSoup(summary, 'html.parser')
    footnotes_div = summary.findAll('div', {'class':'footnote'})
    footnote_links = summary.findAll('a', {'rel':'footnote'})
    if footnotes_div or footnote_links:
        for div in footnotes_div:
            div.extract()
        for link in footnote_links:
            if mode == 'remove':
                link.extract()
            elif mode == 'link':
                # only rewrite once
                if link['href'][0] == '#':
                    link['href'] = "%s/%s%s" % (site_url,
                                                article_url,
                                                link['href'])
            else:
                raise Exception("Unknown summary_footnote mode: %s" % mode)
        return text_type(summary)
    return None


def get_summary(self, orig_summary):
    summary = orig_summary.fget(self)
    new_summary = transform_summary(summary,
                                    self.url,
                                    self.settings['SITEURL'],
                                    self.settings["SUMMARY_FOOTNOTES_MODE"])
    if new_summary is not None:
        return new_summary
    else:
        return summary


def register():
    signals.initialized.connect(initialized)
