# Beagle Access Library

## Description

From what I could tell on line, the beaglebone is set up so GPIO, lEDS, etc are setup like regular hardware on Linux

That is they're *files*

As such, I want to write a simple library that reads/writes to these files, but abstracted into simple to use classes. I couldn't find anything similar besides *examples* of doing it that way, so I thought to make one for my own sanity

It's a C++ library because a) I know C++, b) it's a common language for embedded stuff, and c) I know how to make a *library* for C/C++

## Using

As it's C++, you can build with `make`, and then link with `gcc`

