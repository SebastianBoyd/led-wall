/* -*- mode: c++; c-basic-offset: 4; indent-tabs-mode: nil; -*-
 * Simple example how to use the spixels library
 */

 #include "led-strip.h"
 
 #include <unistd.h>  // for usleep()
 #include <vector>

 #include <typeinfo>
 #include <iostream>
 
 #define FRAME_RATE 20
 
 using namespace spixels;
 using namespace std;
 
 int main() {
     // If you are using WS2801, then you need CreateDMAMultiSPI() instead,
     // as these strips are finicky with timings.
     //
     // See include/multi-spi.h
     MultiSPI *spi = CreateDirectMultiSPI();
 
     // Connect LED strips with 144 LEDs to connector P1 and P2
     // Choose the type of LEDs from the factory name.
     //
     // See include/led-strip.h

     int pins[] = {13, 16, 22, 24, 25, 5, 18, 4, 17, 23};

     LEDStrip *lights[10];
     for (unsigned int i = 0; i < 10; ++i) {
        lights[i] = CreateAPA102Strip(spi, pins[i], 80);
     }
 
     for (unsigned int i = 0; /**/; ++i) {
        const int pos = i % 80;

         for (unsigned int j = 0; j < 10; ++j) {
            lights[j]->SetPixel(pos, 0x000000);

            lights[j]->SetPixel(pos+1, 255, 0, 0);
            lights[j]->SetPixel(pos+2, 0, 255, 0);
            lights[j]->SetPixel(pos+3, 0, 0, 255);
         }
 
     
         spi->SendBuffers();  // Send all pixels out at once.
         usleep(1000000 / FRAME_RATE);
     }
 
     delete spi;
 }
 