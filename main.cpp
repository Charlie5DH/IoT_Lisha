#include <Arduino.h>
#include <Filters.h>

#define NZEROS 4
#define NPOLES 4
#define GAIN   2.400388646e+03
static float xv[NZEROS+1], yv[NPOLES+1];

int adcVal = 0;
float adcOffset = 2.5*5/1023;
float adcVal_filtered = 0;
float adcVal_filteredPoinOne = 0;
int time = 0;
/*******************************************************************************
 * Function:      ButterworthFilter
 * Description:   This function uses the Butterworth filter and returns a new
 *                value for an individual floating point value.
 * Parameters:    float input - value to be converted
 * Globals:       None
 * Returns:       float - new value that has been converted
 * 
 * coefficients will vary depending on sampling rate
 * and cornering frequencies
 ******************************************************************************/
static float ButterworthFilter(float input)   //1 Hz
  { 
     /*
    *filtertype	=	Butterworth
    *passtype	=	Lowpass
    *order	=	4
    *samplerate	=	20
    *corner1	=	1  
    */
    xv[0] = xv[1];
    xv[1] = xv[2]; 
    xv[2] = xv[3]; 
    xv[3] = xv[4]; 
    xv[4] = (float)input / GAIN;
    yv[0] = yv[1]; 
    yv[1] = yv[2]; 
    yv[2] = yv[3]; 
    yv[3] = yv[4]; 
    yv[4] =   (float)(xv[0] + xv[4]) + 4 * (xv[1] + xv[3]) + 6 * xv[2]
                  + ( -0.4382651423 * yv[0]) + (  2.1121553551 * yv[1])
                  + ( -3.8611943490 * yv[2]) + (  3.1806385489 * yv[3]);
    return yv[4];
  }

  static float ButterworthFilterFPointTwo(float input)    //0.5 Hz
  { 
    /*
    *filtertype	=	Butterworth
    *passtype	=	Lowpass
    *order	=	4
    *samplerate	=	20
    *corner1	=	0.5  
    */
    xv[0] = xv[1];
    xv[1] = xv[2]; 
    xv[2] = xv[3]; 
    xv[3] = xv[4]; 
    xv[4] = (float)input / 3.201129162e+04;
    yv[0] = yv[1]; 
    yv[1] = yv[2]; 
    yv[2] = yv[3]; 
    yv[3] = yv[4]; 
    yv[4] =   (float)(xv[0] + xv[4]) + 4 * (xv[1] + xv[3]) + 6 * xv[2]
                     + ( -0.6630104844 * yv[0]) + (  2.9240526562 * yv[1])
                     + ( -4.8512758825 * yv[2]) + (  3.5897338871 * yv[3]);
    return yv[4];
  }

void setup() {
  Serial.begin(115200);
  Serial.flush();
}

void loop() {

adcVal = analogRead(A1);
adcVal_filtered = ButterworthFilter(adcVal*5/1023);
// adcVal_filteredPoinOne = ButterworthFilterFPointTwo(adcVal*5/1023);
// Serial.println(adcVal_filtered);
delay(50);
 time = time + 50;
 if(time == 200)
 {
  Serial.println(adcVal_filtered);
  time = 0;
 }
}

