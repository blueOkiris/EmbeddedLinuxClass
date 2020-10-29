# HW08

## Blinking an LED

> What make command will start your PRU code running?

`make TARGET=hello.pru0 start`

> What will stop it

`make TARGET=hello.pru0 stop`

> Now modify the code to toggle P9_31 in the same way.

Couldn't get some GPIO to work (P9_31 included), so I'm using P8_12 bc I can consistently get it to work.

My version is in `hw08/pru-examples/02/hell0.pru0.c`

> Set the __delay_cycles() to 0

> How fast can you toggle the pin?

T = 2.96ms

> Is there jitter1?

YES. It's a triangle wave.

> Is it stable?

Mostly. I do see some places where the signal changes, but it's pretty good

## PWN Generator

> Now run the example in [6] but move the output pin to P9_31

Once again I'm using P8_12. Modified program is in `hw08/pru-examples/05/pwm1.pru0.c`

> Do a ‘scope capture with the delays added to make the waveform symmetric and at 50 MHz.

So... my oscilloscope can only measure to around 350kHz, and as far as I know, I don't have access to one of the school's. However, I can still look at the symmetry of a wave with delay decently low. The lowest I get a reasonable signal at is 1MHz. I set the delay to 100 to get that.

![plot](pru-examples/05/IMG_003.BMP)

> Comment on how stable the waveform is

It's not very stable, though that may just be due to my limited oscilloscope

> What’s the Std Dev?

1 or 2 us

> Is there jitter.

Yes

## Controlling the PWM Frequency

Note that at this point I've fixed the P9_31 pins, so I can do the rest like I was supposed to.

> Four PWM channels are implemented in this example [7]. Each controlled by a value in the SHARED memory.

> What output pins are being driven? Hint: What bits of __R30 are being used?

Well, I see this masking being done: `__R30 |= 0x1<<ch;`, and I can see that ch is in a loop where it goes from 0 to `MAXCH` which is 4. So we know that r30 bits of 1, 2, 4, and 8 are being set, which correspond to pins: __P9_31, P9_30, P9_29, and P9_28__

> What’s the highest frequency you can get with four channels? 

> Is there jitter?

> Run the pwm-test.c program to change the on and off times. Does it work?

## Results Table

| Method   | Period | Stability | Jitter |
|:--------:|:------:|:---------:|:------:|
| Gpiod    |  2.96m |   Stable  |  Yes   |
| PRU GPIO |   1u   |  Unstable |  Yes   |
