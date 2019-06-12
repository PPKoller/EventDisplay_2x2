# EventDisplay_2x2
Event display for neutrino events in the ArgonCube 2x2 Demonstrator.

usage: event_display_protoND_raw.py [-h] [-a] [-c COLOR] [-l] [-e EVENT] [-ND]
                                    [-FD]
                                    root_file

positional arguments:
  root_file

optional arguments:
  -h, --help            show this help message and exit
  -a, --animation       See a 360 deg orbit animation.
  -c COLOR, --color COLOR
                        Select the tree entry to use as color. Default: dq.
  -l, --logscale        Show logarithmic scaled colorbar.
  -e EVENT, --event EVENT
                        Select the event number. Default: 0.
  -ND, --NearDetector   Show DUNE-ND shape.
  -FD, --FarDetector    Show DUNE-FD shape.

example: python event_display_protoND_raw.py MINERvA_2x2_100evt.root -c dq -l -e 3 -ND -FD
