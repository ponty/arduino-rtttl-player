RTTTL_ player library for Arduino_. 


Links:
 * home: https://github.com/ponty/arduino-rtttl-player
 * documentation: http://ponty.github.com/arduino-rtttl-player

Features:
 - based on RTTTL example in Tone_ library
 - blocking mode only
 - song can be either in PROGMEM or RAM
 - support for both internal and external improved Tone_ library
 - build tests
 - examples
 - library size calculation
 - simulation
 - API documentation with doxygen
   
Basic usage
============
::

	//#include <Tone.h>
	// if Tone.h is included before this include,
	// then the external Tone library is used 
	// else the core tone()/noTone() functions.
	#include <rtttl.h>
	
	const int pinSpeaker = 13;
	const int octave = 0;
	const char song_P[] PROGMEM = 'Indiana:d=4,o=5,b=4000:e,8p,8f,8g,8p,1c6';
	
	Rtttl player;
	
	void setup(void)
	{
		player.begin(pinSpeaker);
		player.play_P(song_P, octave);
	}
	
	void loop(void)
	{
	}


Manual Installation
=======================

http://arduino.cc/en/Guide/Environment#libraries

Automatic Installation
=======================

General
----------

 * install arduino_
 * install confduino_
 * install the library::

    # as root
    python -m confduino.libinstall https://github.com/ponty/arduino-rtttl-player/zipball/master

Ubuntu
----------
::

    sudo apt-get install arduino
    sudo apt-get install python-pip
    sudo pip install confduino
    sudo python -m confduino.libinstall https://github.com/ponty/arduino-rtttl-player/zipball/master

Ubuntu uninstall
-----------------
::

    sudo python -m confduino.libremove rtttl


.. _arduino: http://arduino.cc/
.. _python: http://www.python.org/
.. _simavr: http://gitorious.org/simavr
.. _RTTTL: http://en.wikipedia.org/wiki/Ring_Tone_Transfer_Language
.. _confduino: https://github.com/ponty/confduino
.. _Tone: http://code.google.com/p/rogue-code/wiki/ToneLibraryDocumentation
