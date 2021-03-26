# Adafruit_Python_HYT939
Python Library for the HYT939 Humidity/Temperature sensor.

Partially based on the code of the Adafruit_Python_HYT939 library written by Massimo Gaggero.

**Warning**:

* read/write user reg is not implemented.

## Installation

### Setuptools
The following commands install HYT939 library *system wide*:

~~~console
git clone https://github.com/HYT939.git
cd HYT939
sudo python setup.py install or sudo python3 setup.py install
~~~

In order to install the library on the user's home directory, a *local installation* that not requires sudo/root privileges, the last command should be:

~~~console
python setup.py install --user or python3 setup.py install --user
~~~

And the library will be installed in the folder 

~~~console
$HOME/.local/lib/python*/site-packages/
~~~

### Pip

The following commands install HYT939 library *system wide*:

~~~console
git clone https://github.com/HYT939.git
cd HYT939
sudo pip install . or sudo pip3 install .
~~~

In order to install the library on the user's home directory, a *local installation* that not requires sudo/root privileges, the last command should be:

~~~console
pip install . --user or pip3 install . --user
~~~

And the library will be installed in the folder 

~~~console
$HOME/.local/lib/python*/site-packages/
~~~


## Permissions and privileges
Accessing **I2C** devices usually requires root privileges or privileged group membership. These can be obtained with:

* the use of `sudo` to run the program;
* adding the user that runs the program to the I2C's device owning group;
* creating an '**i2c**' group, assigning the i2c device to it and adding the user to that group.

### Creation of the 'i2c' group
~~~console
sudo groupadd -r i2c        # creates the 'i2c' group as a 'system' group
sudo chgrp i2c /dev/i2c*    # changes group ownership of the i2c device files
sudo chmod g+rw /dev/i2c*   # allow owning group to read/write to the devices
sudo usermod -aG i2c $USER  # add the current user to the 'i2c' group
~~~
Logout and re-login.

## Usage
~~~python
>>> from HYT939 import HYT939

>>> h = HYT939()

>>> h.read_temperature()
24.117971191406248

>>> h.read_humidity()
35.1224365234375

>>> h.read_dewpoint()
7.783974941964999
~~~

## Troubleshooting
### ArchLinux
Before reporting any bugs or issues, make sure that:

* the file */boot/config.txt* contains the line  
`dtparam=i2c_arm=on`  
Uncomment if necessary and reboot the board.


* kernel module  
`i2c-dev`  
is loaded. Otherwise, load it with:  
`sudo modprobe i2c-dev`


