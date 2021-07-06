# revpi-power-distribution

This repo contains code for implementing a RevPi Core 3 module as a power distribution diagnostics handler for the ship sensor system. The RevPi will receive data from the power distribution modules in the form of GPIO signals. This data will include self-reported voltage and current from the AC rectifier, and may include data from the 24V-12V converter and the UPS as applicable. The RevPi will then broadcast the data over a wired Ethernet connection using UDP. The RevPi module takes the place of the Siemens LOGO PLC currently being used in the system.
