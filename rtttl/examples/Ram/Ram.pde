//#include <Tone.h>  // the core tone()/noTone() are used.
#include <rtttl.h>

const int pinSpeaker = 13;
const int octave = 0;

// this solution is not recommended:
// the song is stored in program memory and then copied into RAM 
const char song[] =
		"Indiana:d=4,o=5,b=250:e,8p,8f,8g,8p,1c6,8p.,d,8p,8e,1f,p.,g,8p,8a,8b,8p,1f6,p,a,8p,8b,2c6,2d6,2e6,e,8p,8f,8g,8p,1c6,p,d6,8p,8e6,1f.6,g,8p,8g,e.6,8p,d6,8p,8g,e.6,8p,d6,8p,8g,f.6,8p,e6,8p,8d6,2c6";

Rtttl player;

void setup(void)
{
	player.begin(pinSpeaker);
	player.play(song, octave);
}

void loop(void)
{
}

