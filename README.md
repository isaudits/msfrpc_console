# Description
A remote msfconsole written in Python 2.7 to connect to the msfrcpd server of metasploit.
This tool gives you the ability to load modules permanently as daemon on your server like autopwn2.
Although it gives you the ability to remotely use the msfrpcd server you may consider using it locally with a ssh or mosh shell because certificate validation is not enabled.

Note that remote msfconsole can also be obtained by just using the msfd daemon, however the daemon has limitations:
 - It is unauthenticated; Doing it this way, we can still at least have basic authentication protecting our daemon without having to use SSH tunnel.
 - Using the msf-rpc daemon we can launch the daemon as a service via script that also loads a resource file or processes a series of initialization commands to the daemon
    - Hint hint...Maybe we have a social engineering server and we always want a generic meterpreter handler listening
 - We can launch the client console with a resource file from the client workstation
 - This tool can be imported as a module into other python applications to provide quick and easy interaction with a MSF-RPC server

This is a modified port of the [msf-remote-console](https://github.com/Luis-Hebendanz/msf-remote-console) tool written by Luis Hebendanz:
- Original source of [msf-remote-console](https://github.com/Luis-Hebendanz/msf-remote-console) included as a subtree
    - Essentially, we just re-wrote the main module to allow it to be imported as a module in other scripts
    - All the heavy lifting is done by the original, unmodified source
    - The above project has been abandoned in favor of just using msfd (we still think it has valid uses as explained above)
- Source of the [pymetasploit](https://github.com/Mikaayenson/pymetasploit) dependency included as a subtree
    - Updated fork of original [pymetasploit](https://github.com/allfro/pymetasploit)
    - no separate clone and install of pymetasploit required

### Features
- Optimized delivery & execution of commands.
- Has all msf commands implemented even future ones. This is possible through the structure of the rpc api.
- Browse through your command history with the up and down arrow key.
- It feels like the normal msfconsole!


# Example output
```
[*] Connecting to server:
 Host => myDomain.com,
 Port => 55553,
 User => msf,
 Pwd => ***,
 SSL => True

[+] Successfully connected
[*] Console id: 19
     ,           ,
    /             \
   ((__---,,,---__))
      (_) O O (_)_________
         \ _ /            |\
          o_o \   M S F   | \
               \   _____  |  *
                |||   WW|||
                |||     |||


       =[ metasploit v4.12.22-dev-52b81f3                 ]
+ -- --=[ 1577 exploits - 906 auxiliary - 272 post        ]
+ -- --=[ 455 payloads - 39 encoders - 8 nops             ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]


msf > 
```

# Usage
Usage: msfrpc-console.py [options]
```
Options:
  -h, --help            show this help message and exit
  -r RESOURCE, --resource=RESOURCE
                        Path to resource file
  -u USERNAME, --user=USERNAME
                        Username specified on msfrpcd
  -p PASSWORD, --pass=PASSWORD
                        Password specified on msfrpcd
  -s, --ssl             Enable ssl
  -P PORT, --port=PORT  Port to connect to
  -H HOST, --host=HOST  Server ip
  -e, --exit            Exit after executing resource script
```
If parameters are not specified, the following defaults are used:
- username = "msf"
- password = "msf"
- port = 55553
- host = "127.0.0.1"
- ssl = False

With the -r option you specify a resource script to load from your computer into the console.

With the -e option, the console will exit automatically after running the resource script.

Also don't forget to start your msfrpcd server first:
```
msfrpcd -U msf -P msf -p 55553
```

--------------------------------------------------------------------------------

Copyright 2018

Matthew C. Jones, CPA, CISA, OSCP, CCFE

IS Audits & Consulting, LLC - <http://www.isaudits.com/>

TJS Deemer Dana LLP - <http://www.tjsdd.com/>

Included submodules subject to their own copyright / licensing:
- [msf-remote-console README](modules/msf-remote-console/README.md)
- [pymetasploit README](modules/pymetasploit/README.md)

--------------------------------------------------------------------------------

Except as otherwise specified by included submodule licensing:

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
