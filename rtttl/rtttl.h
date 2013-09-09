#pragma once

#if defined(ARDUINO) && ARDUINO >= 100
# include "Arduino.h"
#else
# include "WProgram.h"
# include "pins_arduino.h"
#endif

#include <avr/pgmspace.h>
#include <notes.h>

#define isdigit(n) (n >= '0' && n <= '9')

inline char read_byte(const char *p, bool pgm)
{
	if (pgm)
		return pgm_read_byte(p);
	else
		return *p;
}

const prog_uint16_t notes[] PROGMEM =
{	0, //
	NOTE_C4, //
	NOTE_CS4, //
	NOTE_D4, //
	NOTE_DS4, //
	NOTE_E4, //
	NOTE_F4, //
	NOTE_FS4, //
	NOTE_G4, //
	NOTE_GS4, //
	NOTE_A4, //
	NOTE_AS4, //
	NOTE_B4, //

	NOTE_C5, //
	NOTE_CS5, //
	NOTE_D5, //
	NOTE_DS5, //
	NOTE_E5, //
	NOTE_F5, //
	NOTE_FS5, //
	NOTE_G5, //
	NOTE_GS5, //
	NOTE_A5, //
	NOTE_AS5, //
	NOTE_B5, //

	NOTE_C6, //
	NOTE_CS6, //
	NOTE_D6, //
	NOTE_DS6, //
	NOTE_E6, //
	NOTE_F6, //
	NOTE_FS6, //
	NOTE_G6, //
	NOTE_GS6, //
	NOTE_A6, //
	NOTE_AS6, //
	NOTE_B6, //

	NOTE_C7, //
	NOTE_CS7, //
	NOTE_D7, //
	NOTE_DS7, //
	NOTE_E7, //
	NOTE_F7, //
	NOTE_FS7, //
	NOTE_G7, //
	NOTE_GS7, //
	NOTE_A7, //
	NOTE_AS7, //
	NOTE_B7, //

	2*NOTE_C7, //
	2*NOTE_CS7, //
	2*NOTE_D7, //
	2*NOTE_DS7, //
	2*NOTE_E7, //
	2*NOTE_F7, //
	2*NOTE_FS7, //
	2*NOTE_G7, //
	2*NOTE_GS7, //
	2*NOTE_A7, //
	2*NOTE_AS7, //
	2*NOTE_B7, //
	0
};

/*
 *
 * playing RTTTL music files in blocking mode
 * http://en.wikipedia.org/wiki/Ring_Tone_Transfer_Language
 *
 * based on Tone library demo
 *
 */
class Rtttl
{
	uint8_t _pinSpk;
#ifdef _Tone_h
	Tone m_tone;
#endif

public:
	Rtttl()
	{
		//		this->begin(tonePin);
	}

	void begin(uint8_t tonePin)
	{
		this->_pinSpk = tonePin;
#ifdef _Tone_h
		//		Serial.println("begin");
		//		Serial.println(tonePin, DEC);
		this->m_tone.begin(tonePin);
		//		Serial.println("begin");
#endif

	}

#ifdef _Tone_h
	void _tone(uint16_t freq)
	{
		//		Serial.println(freq);
		this->m_tone.play(freq);
	}

	void _noTone()
	{
		//		Serial.println("1stop");
		this->m_tone.stop();
	}
#else
	void _tone(uint16_t freq)
	{
		//		Serial.println(freq);
		tone(this->_pinSpk, freq);
	}

	void _noTone()
	{
		//		Serial.println("2stop");
		noTone(this->_pinSpk);
	}
#endif

	void play_P(const prog_char *p, uint8_t octave_offset = 0)
	{
		_play(p, octave_offset, true);
	}
	void play(const char *p, uint8_t octave_offset = 0)
	{
		_play(p, octave_offset, false);
	}

	void _play(const prog_char *p, uint8_t octave_offset, bool pgm)
	{
		// Absolutely no error checking in here

		byte default_dur = 4;
		byte default_oct = 6;
		int bpm = 63;
		int num;
		long wholenote;
		long duration;
		byte note;
		byte scale;

		// format: d=N,o=N,b=NNN:
		// find the start (skip name, etc)

		while (read_byte(p, pgm) != ':')
			p++; // ignore name
		p++; // skip ':'

		// get default duration
		if (read_byte(p, pgm) == 'd')
		{
			p++;
			p++; // skip "d="
			num = 0;
			while (isdigit(read_byte(p, pgm)))
			{
				num = (num * 10) + (read_byte(p, pgm) - '0');
				p++;
			}
			if (num > 0)
				default_dur = num;
			p++; // skip comma
		}

		// get default octave
		if (read_byte(p, pgm) == 'o')
		{
			p++;
			p++; // skip "o="
			num = read_byte(p, pgm) - '0';
			p++;
			if (num >= 3 && num <= 7)
				default_oct = num;
			p++; // skip comma
		}

		// get BPM
		if (read_byte(p, pgm) == 'b')
		{
			p++;
			p++; // skip "b="
			num = 0;
			while (isdigit(read_byte(p, pgm)))
			{
				num = (num * 10) + (read_byte(p, pgm) - '0');
				p++;
			}
			bpm = num;
			p++; // skip colon
		}

		// BPM usually expresses the number of quarter notes per minute
		wholenote = (60 * 1000L / bpm) * 4; // this is the time for whole note (in milliseconds)

		// now begin note loop
		while (read_byte(p, pgm))
		{
			// first, get note duration, if available
			num = 0;
			while (isdigit(read_byte(p, pgm)))
			{
				num = (num * 10) + (read_byte(p, pgm) - '0');
				p++;
			}

			if (num)
				duration = wholenote / num;
			else
				duration = wholenote / default_dur; // we will need to check if we are a dotted note after

			// now get the note
			note = 0;

			switch (read_byte(p, pgm))
			{
			case 'c':
				note = 1;
				break;
			case 'd':
				note = 3;
				break;
			case 'e':
				note = 5;
				break;
			case 'f':
				note = 6;
				break;
			case 'g':
				note = 8;
				break;
			case 'a':
				note = 10;
				break;
			case 'b':
				note = 12;
				break;
			case 'p':
			default:
				note = 0;
			}
			p++;

			// now, get optional '#' sharp
			if (read_byte(p, pgm) == '#')
			{
				note++;
				p++;
			}

			// now, get optional '.' dotted note
			if (read_byte(p, pgm) == '.')
			{
				duration += duration / 2;
				p++;
			}

			// now, get scale
			if (isdigit(read_byte(p, pgm)))
			{
				scale = read_byte(p, pgm) - '0';
				p++;
			}
			else
			{
				scale = default_oct;
			}

			scale += octave_offset;

			if (read_byte(p, pgm) == ',')
				p++; // skip comma for next note (or we may be at the end)

			// now play the note

			if (note)
			{
				_tone(pgm_read_word(&notes[(scale - 4) * 12 + note]));
				delay(duration);
				_noTone();
			}
			else
			{
				delay(duration);
			}
		}
	}
};

