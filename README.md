# Schnibble

Schnibble is a project aimed at providing useful Python APIs for processing
python bytecode. Schnibble is named after the adventure game *Woodruff and the
Schnibble of Azimuth*. You may find the project curious though it is quite
incomplete at this stage.

## Abstract interpretation

Abstract interpretation refers to executing a program with an abstract
execution system. Instead of concrete values, *abstract* value are produced.
Instead of taking one of a set of possible branches, *all* branches are taken.

Abstract interpretation is an useful tool in static analysis.

## Contributions

I'm interested in knowing about issues. If you find a problem please open
a ticket on github. If you'd like to contribute code please create a github
*fork* and create a pull request.

### Supported platforms

Schnibble works on CPython 2.7 (ironically selected due to its stability)
on any OS platform. Support for Pypy will be investigated later. Python 3.x
support is a plan for later period after all of the basics are supported on
a stable bytecode set.
