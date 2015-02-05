"""
Summary Footnotes
-------------

Fix handling of footnotes inside article summaries.
Option to either remove them or make them link to the article page.
"""

from pelican import signals
from pelican.contents import Content, Article
from BeautifulSoup import BeautifulSoup
from six import text_type

def summary_footnotes(instance):
    if "SUMMARY_FOOTNOTES_MODE" in instance.settings:
        mode = instance.settings["SUMMARY_FOOTNOTES_MODE"]
    else:
        mode = 'link'

    if type(instance) == Article:
        summary = BeautifulSoup(instance.summary)
        footnote_links = summary.findAll('a', {'rel':'footnote'})
        if footnote_links:
            for link in footnote_links:
                if mode == 'remove':
                    link.extract()
                elif mode == 'link':
                    link['href'] = "%s/%s%s" % (instance.settings["SITEURL"],
                                                instance.url,
                                                link['href'])
                else:
                    raise Exception("Unknown summary footnote mode: %s" % mode)
            instance._summary = text_type(summary)

def register():
    signals.content_object_init.connect(summary_footnotes)
