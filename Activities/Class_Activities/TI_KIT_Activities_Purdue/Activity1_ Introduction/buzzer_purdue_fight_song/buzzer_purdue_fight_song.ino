/*
 Grove Buzzer

 The example uses a buzzer to play melodies. It sends a square wave of the 
 appropriate frequency to the buzzer, generating the corresponding tone.
 
 The circuit:
 * Buzzer attached to Pin 39 (J14 plug on Grove Base BoosterPack)

 * Note:
 
 This example code is in the public domain.
 
 http://www.seeedstudio.com/depot/Grove-Buzzer-p-768.html
 
*/
 
/* Macro Define */
#define BUZZER_PIN               39            /* sig pin of the Grove Buzzer */

int length = 59;         /* the number of notes */
char notes[] = "dewgabbcccgatb bbagabbaewgwea ddewgabbbccgab ewgedgbdebagg "; /*notes in the song. Use a space for rests*/
int beats[] = { 2, 2, 2, 3, 1, 2, 2, 2, 1, 1, 2, 1, 1, 5, 1, 4, 2, 2, 3, 1, 2, 2, 2, 1, 1, 2, 1, 1, 5, 1, 3, 1, 2, 2, 3, 1, 2, 1, 1, 2, 2, 2, 2, 5, 1, 3, 1, 2, 2, 2, 2, 2, 2, 3, 1, 3, 1, 5, 1 }; /*length of each note. 1 = quarter note*/
int tempo = 200;

/* the setup() method runs once, when the sketch starts */
void setup()
{
  /* set buzzer pin as output */
  pinMode(BUZZER_PIN, OUTPUT);       
}

void loop()
{
  //Loop through each note
  for(int i = 0; i < length; i++) 
  {
    //space indicates a pause
    if(notes[i] == ' ') 
    {
      delay(beats[i] * tempo);
    } 
    else 
    {
      playNote(notes[i], beats[i] * tempo);
    }
    delay(tempo / 2);    /* delay between notes */
  }
}

/* play tone */
void playTone(int tone, int duration) 
{
  for (long i = 0; i < duration * 1000L; i += tone * 2) 
  {
    digitalWrite(BUZZER_PIN, HIGH);
    delayMicroseconds(tone);
    digitalWrite(BUZZER_PIN, LOW);
    delayMicroseconds(tone);
  }
}

/* List of the notes in the song */
/* w = F sharp, t = A sharp */
char names[] = { 'c', 'd', 'e', 'f', 'w', 'g', 'a', 't', 'b', 'C' };

/* Match the notes to the wavelength of the soundwave in cm */
/* Note: This code assumes that sharps are half steps between notes */
int tones[] = { 1915, 1700, 1519, 1432, 1354, 1275, 1136, 1075, 1014, 956 };

void playNote(char note, int duration) 
{
  
  
  // play the tone corresponding to the note name
  for (int i = 0; i < 10; i++) 
  {
    if (names[i] == note) 
    {
      playTone(tones[i], duration);
    }
  }
}
