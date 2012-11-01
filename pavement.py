from paved import *
from paved.dist import *
from paved.docs import *
from paved.pycheck import *
from paved.util import *
from paver.easy import *
from pyavrutils import support
from sphinxcontrib import paverutils
import logging
import os
import paver.doctools
import paver.misctasks
import paver.virtual
sys.path.insert(0, path('.').abspath())
import simulator

#logging.basicConfig(level=logging.DEBUG)


options(
    sphinx=Bunch(
        docroot='docs',
        builddir="_build",
        ),
    pdf=Bunch(
        builddir='_build',
        builder='latex',
    ),
    )

options.paved.clean.rmdirs += ['.tox',
                                 'dist',
                                 'build',
                                 ]

options.paved.clean.patterns += ['*.pickle',
                                 '*.doctree',
                                 '*.gz',
                                 'nosetests.xml',
                                 'sloccount.sc',
                                 '*.pdf', '*.tex',
                                 '*.png',

                                 'generated_*', # generated files

                                 '*.axf',
                                 '*.elf',
                                 '*.o',
                                 '*.a',
                                 '*.eep',
                                 '*.hex',
                                 '*.lss',
                                 '*.map',
                                 '*.lst',
                                 '*.sym',
                                 '*.vcd',
                                 'sgm7_hwconf.h',
                                 '*.bak', # cheetah
                                 '*.zip',
                                 'distribute_setup.py',
                                 ]

options.paved.dist.manifest.include.remove('distribute_setup.py')
options.paved.dist.manifest.include.remove('paver-minilib.zip')

docroot = path(options.sphinx.docroot)
root = path(__file__).parent.parent.abspath()
examples = support.find_examples(root)


@task
@needs(
       'cog',
       'sloccount',
       'sim',
       'libsize',
##       'snippet',
       'build_test',
#       'boards',
       'doxy',
       'html',
       'pdf',
       'nose')
def alltest():
    'all tasks to check'
    pass


@task
@needs('sphinxcontrib.paverutils.html')
def html():
    pass


@task
@needs('sphinxcontrib.paverutils.pdf')
def pdf():
    fpdf = list(path('docs/_build/latex').walkfiles('*.pdf'))[0]
    d = path('docs/_build/html')
    d.makedirs()
    fpdf.copy(d)


@task
def doxy():
    path('docs/_build/html/doxy').makedirs()
    sh('doxygen doxy.ini')


#@task
#def snippet():
#    '''generate screenshots from code snippets'''
#    f = docroot / 'code_examples.csv'
#    sim.snippet_doc(f, docroot, logger=info)


@task
def libsize():
    f = docroot / 'code4size.csv'
    simulator.libsize(f, docroot, logger=info)



ARDUINO_VERSIONS = [
                  '0022',
                  '0023',
                  '1.0',
                  ]


@task
def build_test():
    old_home = os.environ['ARDUINO_HOME']
    for ver in ARDUINO_VERSIONS:
        os.environ['ARDUINO_HOME'] = path('~/opt/arduino-{0}'.format(ver)).expanduser()
        csv = docroot / 'generated_build_test_{0}.csv'.format(ver)
        support.build2csv(
                          examples,
                          csv,
                          logdir=docroot / '_build' / 'html',
                          logger=info,
#                          extra_lib='rtttl',
                          )
    os.environ['ARDUINO_HOME'] = old_home


#@task
#def boards():
#    for ver in ARDUINO_VERSIONS:
#        support.set_arduino_path('~/opt/arduino-{0}'.format(ver))
#        csv = docroot / 'generated_boards_{0}.csv'.format(ver)
#        support.boards2csv(csv, logger=info)


@task
def sim():
    simulator.generate_vcd(
                        song='Indiana:d=4,o=5,b=4000:e,8p,8f,8g,8p,1c6',
                        vcd='docs/generated_indy.vcd',
                        logger=info,
                        )

