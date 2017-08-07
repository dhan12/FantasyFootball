This holds a few scripts related to fantasy football.

Modes
====================
So far, there are three "modes".

1. Draft
--------------------
Run `./run.bash draft`

Use this during and/or in preparation of an auction draft.

2. Trade
--------------------
Run `./run.bash trade`

Use this to generate trade proposals.

3. Stength of schedule
--------------------
Run `./run.bash schedule`

This generates a strength of schedule map.

Data 
====================
All of this fantasy data is based on data. Some of it may be obtained from the internet, and others may be your custom data.

Parsers
---------
See `./src/parsers/`

The parser scripts convert raw text downloaded from different websites into formatted csv files.

Raw data
---------
See `./data-raw/`

Raw data downloaded from a few websites are placed here.

Processed data
---------
See `./data-processed/`

Data convered from the data-raw files are saved here. 

These files are generated, and subject to modification.
