# sex52

controls the logitech x52 pro for linux, if getting permissions errors, set up a udev rule:

`/etc/udev/rules.d/20-sex52.rules`

`ATTRS{idVendor}=="06a3", ATTRS{idProduct}=="0762", OWNER="coghex"`

then reload:

`udevadm control --reload-rules && udevadm trigger`

run with:

`python sex52`

only tested with python3
