# millennium-coinmech-programmer
Programmer-Hardware for Coinmech found in Nortel/Quortech Millennium Payphones

## Hardware
The PCB fits a [dirtypcbs.com](http://dirtypcbs.com) 5x5 protopack-panel. You can order a copy of the board directly at dirtypcbs.com using [this link](http://dirtypcbs.com/store/designer/details/13026/1100/millennium-payphone-coinmech-programmer).

In fact, the PCB is just a carrier for a common red, chinese FTDI232R-board. You will also need to add a pinheader or barrel-connector (to get power from the payphone or inject 12V directly - not both though!).

A limited amount of fully assembled and tested PCBs are available for purchase by contacting me at `martin @ $github-username$  .de`

## Software
In the long run, the programmer will be used with the web-platform running at [http://millennium.management/](http://millennium.management/). In the meantime, feel free to use the python-scripts provided in the `tests`-folder.

### Requirements
* python3
* pylibftdi
* libftdi

It is recommended, that you install the provided `99-libftdi.rules`-files in the udev-rule-folder (eg. `/etc/udev/rules.d/`). That way, any attached FTDI-device is available to users in the `dialout`-group. If you choose to not install the udev-rule (or to install the rule but to not put your user in the `dialout`-group), the python-scripts will need `root` to run.

### Known issues
* The dumper-example just outputs the contents of the validator-EEPROM onto the console in hex-notation and does not write a file.
* There is no script yet to write the dump of a validator back into the device. It's not difficult to do this - but if you want to roll your own script in the meantime, please be advised, that it is not known yet, what all fields of the validator do. If in doubt, only overwrite the coin-definitions and nothing else. Also, please be aware, that changing the fist Byte of the EEPROM to anything else than `0x03` might brick your device.
