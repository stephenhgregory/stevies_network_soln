''' Contains classes & functions for server objects used for Machina Labs .stl file transport '''

import socket
import time
from typing import AnyStr, Tuple
import os
import filecmp
from . import file_utils


class TCPSocketUser():
    '''General class for object that communicates over TCP Sockets'''

    def __init__(self, first_available_port_number: int, last_available_port_number: int, host_name: AnyStr):

        self.port_number = first_available_port_number
        self.first_available_port_number = first_available_port_number
        self.last_available_port_number = last_available_port_number
        self.host_name = host_name
        self.connected = False

    def bind(self):
        # Create socket object and bind to the port number
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host_name, self.port_number))

    def connect(self):
        # Create socket object and connect to the port number
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((self.host_name, self.port_number))

    def increment_port_number(self):
        ''' Simply increments the port_number to use (until a point)'''
        if self.port_number < self.last_available_port_number:
            self.port_number += 1
        else:
            self.port_number = self.first_available_port_number

    def send_file(self, send_filename: AnyStr):
        '''Sends the contents of a file along the opened socket. '''

        # Open the file for sending
        send_file = open(send_filename, 'rb')

        # Send the file 1024 bytes at a time, until the whole file is sent
        print('Sending cad data...')
        data_chunk = send_file.read(1024)
        while(data_chunk):
            print("Sending cad data...")
            self.s.send(data_chunk)
            data_chunk = send_file.read(1024)
        # Finally, close the original file
        send_file.close()
        print("Done sending cad data!")

    def receive_file(self, receive_filename: AnyStr):
        '''Receives a file from the opened socket, saving the contents to a new file.'''

        # Listen for client connection
        self.s.listen(5)

        # Open the (new) file for receiving
        receive_file = open(receive_filename, 'wb')

        while(True):

            # Connect with client
            print('Waiting to establish TCP connection...')
            conn, addr = self.s.accept()
            self.connected = True
            print(f'Established connection with {addr}.')
            print('Receiving bytes...')

            # Receive the data (1024 bytes at a time)
            data_chunk = conn.recv(1024)
            while (True):
                print("Receiving bytes...")
                receive_file.write(data_chunk)
                if len(data_chunk) < 1024:
                    break
                data_chunk = conn.recv(1024)

            print('Done receiving bytes')

            # Finally, close the (new) file, socket, and leave the function
            receive_file.close()
            self.s.close()
            return

    def delete_file(self, filename):
        ''' Simply deletes a file (if it exists) '''
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("File to be deleted can't be found!")


class ProcessA(TCPSocketUser):
    '''Subclass of 'TCPSocketUser' that satisfies the conditions of "Process A" in Machina Labs assignment'''

    def __init__(self, first_available_port_number: int, last_available_port_number: int, host_name: AnyStr, 
                original_cad_filename: AnyStr, new_cad_filename: AnyStr = None, new_csv_filename: AnyStr = None):
        super().__init__(first_available_port_number, last_available_port_number, host_name)
        self.original_cad_filename = original_cad_filename
        self.new_cad_filename = new_cad_filename
        self.new_csv_filename = new_csv_filename

    def send_file(self):
        ''' Overrides TCPSocketUser.send_file to throw an exception. '''
        raise AttributeError('\'ProcessA\' object has no attribute \'send_file\'')

    def receive_file(self):
        ''' Overrides TCPSocketUser.receive_file to add the new cad file name. '''
        raise AttributeError('\'ProcessA\' object has no attribute \'receive_file\'')

    @file_utils.function_timer
    def send_and_receive_file(self):
        ''' 
        Simply sends and receives the CAD file to/from Server B 
        '''
        # Connect to the port
        super().connect()

        # Send the .stl file to Process B
        super().send_file(self.original_cad_filename)

        # Increment the port number (TCP ports need time to open up after closing)
        super().increment_port_number()

        # Bind to the new port
        super().bind()

        # Receive the new csv file
        super().receive_file(self.new_cad_filename)

    @file_utils.function_timer
    def send_and_receive_csv_file(self):
        ''' 
        Sends an .stl file to Process B, and receives a .csv version of the contents
        of the file in return.
        '''
        # Connect to the port
        super().connect()

        # Send the .stl file to Process B
        super().send_file(self.original_cad_filename)

        # Increment the port number (TCP ports need time to open up after closing)
        super().increment_port_number()

        # Bind to the new port
        super().bind()

        # Receive the new csv file
        super().receive_file(self.new_csv_filename)


class ProcessB(TCPSocketUser):
    '''Subclass of 'TCPSocketUser' that satisfies the conditions of "Process B" in Machina Labs assignment'''

    def __init__(self, first_available_port_number: int, last_available_port_number: int, host_name: AnyStr):
        super().__init__(first_available_port_number, last_available_port_number, host_name)

    def send_file(self):
        ''' Overrides TCPSocketUser.send_file to throw an exception. '''
        raise AttributeError('\'ProcessB\' object has no attribute \'send_file\'')

    def receive_file(self):
        ''' Overrides TCPSocketUser.receive_file to add the new cad file name. '''
        raise AttributeError('\'ProcessB\' object has no attribute \'receive_file\'')

    def rebound_file(self):
        ''' 
        Performs "rebound" operation, receiving and immediately sending back file to 
        Process A
        '''

        # First, receive the file
        super().bind()
        super().receive_file('temporary_file.stl')

        # TCP can take minutes to release a socket
        super().increment_port_number()

        # Then, send the file back
        super().connect()
        super().send_file('temporary_file.stl')

        # Finally, delete the file
        super().delete_file('temporary_file.stl')

    def rebound_csv_file(self):
        ''' 
        Performs "rebound" operation, receiving and immediately sending back file to
        Process A
        '''

        # First, receive the file
        super().bind()
        super().receive_file('temporary_cad_file.stl')

        # TCP can take minutes to release a socket
        super().increment_port_number()

        # Convert the temporary file into a csv file
        file_utils.convert_stl_to_csv(stl_filename='temporary_cad_file.stl', new_csv_filename='temporary_csv_file.csv')

        # Then, send the file back
        super().connect()
        super().send_file('temporary_csv_file.csv')

        # Finally, delete the files
        super().delete_file('temporary_csv_file.csv')
        super().delete_file('temporary_cad_file.stl')