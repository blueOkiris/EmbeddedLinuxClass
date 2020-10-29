# HW08

## Blinking an LED

> What make command will start your PRU code running?

`make TARGET=hello.pru0`

> What will stop it

`make` which calls `make clean` I believe

> Now modify the code to toggle P9_31 in the same way.

Couldn't get some GPIO to work (P9_31 included), so I'm using P9_23.

My version is in `hw08/pru-examples/02/hell0.pru0.c`

> Set the __delay_cycles() to 0

> How fast can you toggle the pin?

Slow

> Is there jitter1?

Maybe

> Is it stable?

Possibly

## PWN Generator

> Now run the example in [6] but move the output pin to P9_31

> Do a ‘scope capture with the delays added to make the waveform symmetric and at 50 MHz.

> Comment on how stable the waveform is

Stable

> What’s the Std Dev?

1

> Is there jitter.

Maybe
