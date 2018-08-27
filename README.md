# OpenSSH-Enumeration

Vulnerability: http://seclists.org/oss-sec/2018/q3/124
Orignial POC: https://bugfuzz.com/stuff/ssh-check-username.py


## Getting Started

```
python Openssh.py -h
```
## Usage 
```
usage: Openssh.py [-h] [--port PORT] [-u USERNAME] [-U USERLIST] [-o OUTPUT]
                  hostname
--port 22 default
-u root default

positional arguments:
  hostname

optional arguments:
  -h, --help            show this help message and exit
  --port PORT
  -u USERNAME, --username USERNAME
                        input a single username
  -U USERLIST, --userlist USERLIST
                        input a username file
  -o OUTPUT, --output OUTPUT
                        output file
```


### Prerequisites

What things you need to install the software and how to install them

```
Python 2.7.15
git clone https://github.com/knadt/OpenSSH-Enumeration
```

## Exampe

Check one username with on port 22 host 127.0.0.1
```
python Openssh.py 127.0.0.1 -u root
```
Check a list of usernames on port 22 host 127.0.0.1 and create an output file
```
python Openssh.py 127.0.0.1 -U username.txt --port 22 -o ~/Desktop/validusers.txt.txt
```

## Authors

* **Matthew Daley** - *Initial work* - [Matthew Daley](https://bugfuzz.com/stuff/ssh-check-username.py)

* **Patrick Sukop** - *Current Version* [Patrick Sukop](https://github.com/knadt/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

