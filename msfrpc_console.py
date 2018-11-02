#!/usr/bin/env python

import time
import sys
from optparse import OptionParser

try:
    try:
      import readline
    except ImportError:
      import pyreadline as readline
except ImportError:
    print "[-] Readline module is not installed!"
    print "[*] Install on Linux with: pip install readline"
    print "[*] Install on Windows with: pip install pyreadline"
    sys.exit()

try:
    import modules
    from MsfConsole import MsfConsole
    from ReadInputThread import ReadInputThread
    from metasploit.msfrpc import MsfRpcError
except ImportError as msg:
    print "[-] Error importing " + str(msg)
    sys.exit()

#
class Session():
    # Hardcoded default credentials
    username = "msf"
    password = "msf"
    port = "55553"
    host = "127.0.0.1"
    ssl = True

    # Variables
    msfconsole = None

    def __init__(self, username=username, password=password, port=port, host=host, ssl=ssl, resource=None, exit_after_rc=False):
        
        self.username=username
        self.password=password
        self.port=port
        self.host=host
        self.ssl=ssl
        self.resource=resource
        self.exit=exit_after_rc
        
        
        if __name__ == '__main__':
            self.get_options()
        self.connect_msfconsole()
    
    def get_options(self):
        ###
        # Command line argument parser
        ###
        parser = OptionParser()
        parser.add_option("-u", "--user", action="store", type="string", dest="username", default=self.username, help="Username specified on msfrpcd")
        parser.add_option("-p", "--pass", action="store", type="string", dest="password", default=self.password, help="Password specified on msfrpcd")
        parser.add_option("-s", "--ssl", action="store_true", dest="ssl", default=self.ssl, help="Enable ssl")
        parser.add_option("-P", "--port", action="store", type="string", dest="port", default=self.port, help="Port to connect to")
        parser.add_option("-H", "--host", action="store", type="string", dest="host", default=self.host, help="Server ip")
        parser.add_option("-r", "--resource", action="store", type="string", dest="resource", help="Path to resource file")
        parser.add_option("-e", "--exit", action="store_true", dest="exit", help="Exit after executing resource script")
        (options, args) = parser.parse_args()
        
        self.username = options.username
        self.password = options.password
        self.port = options.port
        self.host = options.host
        self.ssl = options.ssl
        self.resource = options.resource
        self.exit = options.exit

    def connect_msfconsole(self):
        # Objects
        self.msfconsole = MsfConsole(self.username, self.password, self.port, self.host, self.ssl)

        # Connect to msfrpcd
        if self.msfconsole.connect() is False:
            #sys.exit()
            return

        # If -r flag is given
        if self.resource is not None:
            self.msfconsole.load_resource(self.resource)
            time.sleep(3)

            if self.exit is True:
                self.msfconsole.disconnect()
                #sys.exit()
                return

        # Add directory auto completion
        readline.parse_and_bind("tab: complete")

        # Go to main menu
        self.exec_menu('main_menu')

    # Executes menu function
    def exec_menu(self, choice):
        # If empty input immediately go back to main menu
        if choice == '':
            self.menu_actions['main_menu'](self)
        else:
            # Execute selected function out of dictionary
            try:
                self.menu_actions[choice](self)
            # If given input isn't in dictionary
            except KeyError:
                print '[-] Invalid selection, please try again.'
                time.sleep(1)
                self.menu_actions['main_menu'](self)

    # Main Menu
    def main_menu(self):
        try:
            # Create read thread
            readThread = ReadInputThread(self.msfconsole.get_path())
            readThread.start()

            try:
                while True:
                    # Get command user types in
                    command = readThread.get_command()

                    # If command is not empty break out of loop
                    if command:
                        break

                    # Run in background and read possible output from msfrpcd
                    if self.msfconsole.read_output():
                        # Found data to read
                        readThread.set_path(self.msfconsole.get_path())
            except ValueError:
                pass

            if command == "quit":
                self.msfconsole.disconnect()
                sys.exit()
            # If command not empty send it to msfrpcd
            if command:
                self.msfconsole.exec_command(command)

            # Go to this menu again
            self.exec_menu('main_menu')

        # Connection is only valid for 5 minutes afterwards request another one
        except MsfRpcError:
            print "[*] API token expired requesting new one..."
            if self.msfconsole.connect() is False:
                sys.exit()
            self.exec_menu('main_menu')
        except KeyboardInterrupt:
            self.msfconsole.disconnect()
            sys.exit()

    # Dictionary of menu entries
    menu_actions = {
        'main_menu': main_menu
    }

# Execute main
if __name__ == '__main__':
    try:
        Session()
    except KeyboardInterrupt:
        print "[-] Interrpted execution"
        exit(0)
    
    except AttributeError as msg:
        print "[-] You have to be connected to the server " + str(msg)
        exit(1)