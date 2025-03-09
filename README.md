# Basic2Python
Convert old Basic programs into Pyhton using Python

After watching https://youtu.be/3kdM9wyglnw, I must admit it inspired me.

I started wondering if it was possible to create a Basic-to-Python converter in Python.

There’s only one way to find out: just try it ☺ !

However, since there are many different BASIC dialects, and considering that several programs use BASIC to write and call assembly in memory—or use machine-specific resources—I decided to proceed with an iterative development approach.

So, let's begin with a simple first version.

We will target the Amstrad CPC's Locomotive BASIC 1.1 (https://en.wikipedia.org/wiki/Locomotive_BASIC) for starters, and initially handle only simple instructions: CLS, PRINT, INPUT, etc.

Each iteration will have a source Basic program located in the “ProgramsToConvert” folder and an expected target.

The conversion script takes as input the path of the .bas file (encoded in UTF-8) to be converted and produces a file named “ConversionResult.py” in the local directory.
