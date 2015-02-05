"""
Summary Footnotes
-------------

Fix handling of footnote links inside article summaries.
Option to either remove them or make them link to the article page.
"""

from pelican import signals
from pelican.contents import Content, Article
from BeautifulSoup import BeautifulSoup
from six import text_type

def initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('SUMMARY_FOOTNOTES_MODE',
                              'link')
    if pelican:
        pelican.settings.setdefault('SUMMARY_FOOTNOTES_MODE',
                                    'link')

def transform_summary(summary, article_url, site_url, mode):
    summary = BeautifulSoup(summary)
    footnote_links = summary.findAll('a', {'rel':'footnote'})
    if footnote_links:
        for link in footnote_links:
            if mode == 'remove':
                link.extract()
            elif mode == 'link':
                link['href'] = "%s/%s%s" % (site_url,
                                            article_url,
                                            link['href'])
            else:
                raise Exception("Unknown summary_footnote mode: %s" % mode)
        return text_type(summary)
    return None

def summary_footnotes(instance):
    mode = instance.settings["SUMMARY_FOOTNOTES_MODE"]

    if type(instance) == Article:
        # Monkeypatch in the rewrite on the summary because when this is run
        # the content might not be ready yet if it depends on other files
        # being loaded.
        instance._orig_get_summary = instance._get_summary
        
        def _get_summary(self):
            summary = self._orig_get_summary()
            new_summary = transform_summary(summary,
                                            self.url,
                                            self.settings['SITEURL'],
                                            mode)
            if new_summary is not None:
                return new_summary
            else:
                return summary

        funcType = type(instance._get_summary)
        instance._get_summary = funcType(_get_summary, instance, Article)

def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(summary_footnotes)
