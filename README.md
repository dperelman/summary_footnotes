#Summary Footnotes Plugin#

Plugin to fix footnote references in your summary. By default, they are
broken links because the footnotes are not included with the summary.
This plugin lets you either remove the links or make them point to the
full article page.

This plugin was based off the [clean_summary plugin](https://github.com/getpelican/pelican-plugins/tree/master/clean_summary).


##Settings##

This plugin has one setting, `SUMMARY_FOOTNOTES_MODE` which takes a string.
The two available modes are `"remove"` which removes all footnote links
from summaries and `"link"` (the default) which changes footnote links
in summaries to link to the footnote on the article page.


##Requirements##

Requires Beautiful Soup:

    pip install BeautifulSoup4


##Usage with Summary Plugin##

If using the summary plugin, make sure summary appears in your plugins before
clean summary. Eg.

    PLUGINS = ['summary', 'summary_footnotes', ... ]
