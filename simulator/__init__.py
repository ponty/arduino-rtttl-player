from path import path
from pyavrutils.arduino import Arduino, ArduinoCompileError
from pysimavr.avr import Avr
from pysimavr.sim import ArduinoSim
import csv
import logging

log = logging.getLogger(__name__)

root = path(__file__).parent.parent.abspath()


def targets():
    return Avr.arduino_targets

TEMPLATE = '''
#include <rtttl.h>

Rtttl player;

const int pinSpeaker = 13;

void setup()
{
    Serial.begin(9600);
    tone(5, 400); // to include tone lib

    snippet;

}

void loop()
{
}
'''

TEMPLATE_PLAY = '''
#include <rtttl.h>

const int pinSpeaker = 13;
const int octave = 0;

const char song_P[] PROGMEM = "$SONG$";

Rtttl player;

void setup(void)
{
    player.begin(pinSpeaker);
    player.play_P(song_P, octave);
}

void loop(void)
{
}
'''


def simulator(snippet=None, mcu=None, code=None, vcd=None):
    return ArduinoSim(snippet=snippet,
                      code=code,
                      mcu=mcu,
                      #                      f_cpu=f_cpu,
                      vcd=vcd,
                      #                      extra_lib=root,
                      template=TEMPLATE,
                      timespan=0.1,
                      )


def generate_vcd(song, vcd, mcu='atmega168', f_cpu=16000000, timespan=2, logger=lambda x: None):
    code = TEMPLATE_PLAY.replace('$SONG$', song)
    vcd = path(vcd)
    d = vcd.dirname()
    fcode = d / ('generated_code4_' + vcd.name + '.c')
    fcode.write_text(code)
    logger('writing ' + fcode)

    x = ArduinoSim(code=code,
                   mcu=mcu,
                   f_cpu=f_cpu,
                   vcd=vcd,
                   #                      extra_lib=root,
                   #                      template=TEMPLATE,
                   timespan=timespan,
                   )
    x.run()


def libsize(csvinput, outdir, mcu='atmega168', logger=lambda x: None):
    '''calculate lib size'''
    d = outdir
    f = open(csvinput, 'rb')
    reader = csv.reader(f)

    fx = open(d / 'generated_code_sizes.csv', 'wb')
    writer = csv.writer(fx)
    logger('generating ' + fx.name)

    ftempl = path(d / 'generated_template.c')
    logger('generating ' + ftempl)
    ftempl.write_text(TEMPLATE)

    for i, (snippet, comment) in enumerate(reader):
        snippet = snippet.replace('{LF}', '\n')
        fcode = d / 'generated_code4size_' + str(i) + '.c'
        path(fcode).write_text(snippet)

        msg = 'index: %s generating: %s ' % (i, fcode)
        logger(msg)

        size = simulator(snippet, mcu).size()
        empty_size = simulator('', mcu).size()

        writer.writerow([
                        comment,
                        '.. literalinclude:: ' + fcode.name,
                        size.program_bytes - empty_size.program_bytes,
                        size.data_bytes - empty_size.data_bytes,
                        ])
