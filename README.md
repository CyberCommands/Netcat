# Replacing Netcat
[![Python3.x](https://img.shields.io/badge/python-3.x-FADA5E.svg?logo=python)](https://www.python.org/) [![PEP8](https://img.shields.io/badge/code%20style-pep8-red.svg)](https://www.python.org/dev/peps/pep-0008/)

Netcat is the utility knife of networking, so it’s no surprise that shrewd systems administrators remove it from their systems. Such a useful tool would be quite an asset if an attacker managed to find a way in. With it, you can read and write data across the network, meaning you can use it to execute remote commands, pass files back and forth, or even open a remote shell. On more than one occasion, I’ve run into servers that don’t have Netcat installed but do have Python. In these cases, it’s useful to create a simple network client and server that you can use to push files or a listener that gives you command-line access. If you’ve broken in through a web application, it’s definitely worth dropping a Python callback to give you secondary access without having to first burn one of your trojans or backdoors.

### Disclaimer

This tool is only for testing and educational purposes only and can be used where strict consent has been given. I am not responsible for any misuse or damage caused by this tool.

## Installation

```
git clone https://github.com/CyberCommands/Netcat.git
```
```
cd Netcat/
```
```
sudo python3 netcat.py -h
```

