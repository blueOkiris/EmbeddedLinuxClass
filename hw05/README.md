# HW05 Answers Document

## Project

> Add a project (or two) to the Project page (see Moodle). Put your name on projects you are interested in doing.

I may change this later, but at the moment I am unable to edit the project page.

I've mentioned some project ideas in class though:

 1. Building an Android's head

    - Take a rubber halloween mask and put it over a head "skeleton" where the mouth can be moved into a few positions with servos

    - Use speech recognition to create a text stream input

    - Feed it into a chat bot program. I could probably find an open source one online as writing my own could be out of scope unless it's just super barebones like `if(strcmp(voiceInput, "hello") = 0) { say("hello"); }`

    - Use speech synthesis to redirect the chat bot text output to a speaker

    - *Seems* like a lot more work than it actually __would__ be. The chat bot is really the only super complex thing there.

 2. Robot Dog (Fetch Bot)

    - Lot's of things could be here and make it out of scope, so only one should be implemented: playing fetch.

    - "Dog" has a robot body that can move different directions

    - Uses camera and the OpenCV library to do object tracking on a green ball

    - Moves body to search for and move to ball, playing "fetch"

## Make

> Do the http://elinux.org/EBC_make exercise and put your Makefile in your repo

### Part A

> Build and run “Hello World” from the command line.

`gcc -g -c app.c -o app.o`

> In the above gcc command, name the target, dependency and command.

Target: app.o

Dependency: app.c

Command: `gcc` or I suppose more specifically `gcc -g -c <dependency> -o <target>`

> What does the –c option (from the previous step) tell the compiler to do?

It compiles the c source to an object file

> Link the object file and produce the final executable.

`gcc -g app.o -o app.arm`

The rest is making the Makefile, which is continued and added to in part B

## Part B

The next part requires making a makefile that compiles the `app.arm` file, but using variables, generic rules, phonies, etc.

I've elected to make the program a little more complicated so the Makefile can also be a bit more interesting as well by introducing header files

All I've done is move the C files into a `src` folder and made a second header/c file that has a `print_hello_world` function, nothing super crazy. Also I created a separate folder for object files since there's two of them now

The Makefile and project can be found in `hw05/make/`
