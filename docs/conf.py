from path import path
import logging

release = '0.0.0'
project = u'arduino-rttl-player'
copyright = u'2011, ponty'
author = 'ponty'


# logging.basicConfig(level=logging.DEBUG)

needs_sphinx = '1.0'

extensions = [
    'sphinxcontrib.gtkwave',
    #'sphinx.ext.intersphinx',
    #              'sphinxcontrib.eagle',
    #'sphinx.ext.autodoc',
    #'sphinxcontrib.programoutput',
    #'sphinx.ext.graphviz',
    #'sphinx.ext.autosummary',
]
# intersphinx_mapping = {'http://docs.python.org/': None,
#'http://packages.python.org/sphinxcontrib-programoutput/' : None,
#}

source_suffix = '.rst'
master_doc = 'index'


exclude_patterns = ['_build/*']

html_theme = 'default'
html_static_path = []

# intersphinx_mapping = {
#    'ansi': ('http://packages.python.org/sphinxcontrib-ansi', None)}


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')


# latex build settings
latex_documents = [
    ('index', '%s.tex' % project, u'%s Documentation' % project,
     author, 'manual'),
]

# remove blank pages from pdf
# http://groups.google.com/group/sphinx-
# dev/browse_thread/thread/92e19267d095412d/d60dcba483c6b13d
latex_font_size = '10pt,oneside'

latex_elements = dict(
    papersize='a4paper',
)
