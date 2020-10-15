# HW06 Answers

## Project Page

I added another idea for a project, using the bone as an Arcade Fighting stick.

Essentially you make the bone appear as a USB HID and send controller inputs based on the bone's GPIO which are wired to arcade buttons in a joystick.

One can also place the buttons in a nice wooden enclosure for structure

## Watch

> Watch’s Julia’s YouTube video[1] “What Every Driver Developer Should Know about RT”. Be ready to answer questions

1. Where does Julia Cartwright work?

National Instruments (Hey! That's where I'll be working!)

2. What is PREEMPT_RT?

It's a patch for the Linux kernel to give it some RTOS-like capabilities

3. What is mixed criticality?

From the video:

> There are two different degrees of time sensitiveness

Real-time and non-real-time

4. How can drivers misbehave?

They share information between real-time stuff and regular linux stuff on the same driver stacks.

5. What is Δ in Figure 1?

Latency. Time from event to code essentially

6. What is Cyclictest?

It's a test used to characterize delta.

It takes a timestamp, sleeps, and then takes a new timestamp. The difference between the difference between the timestamps and the sleep time is delta.

7. What is plotted in Figure 2?

The difference between preempt_rt and regular kernel for the cyclictest

8. What is dispatch latency? Scheduling latency?

Amount of time between hardware firing to interrupt vs the time from the interrupt to the CPU to execute the task

9. What is mainline?

It's a model for showing long-running interrupts

10. What is keeping the External event in Figure 3 from starting?

A non-critical IRQ

11. Why can the External event in Figure 4 start sooner?

Non-critical IRQ code has been extracted from the specific IRQ calling part. Thus, the other IRQ can also trigger.

## 

