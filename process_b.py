import socket
from utils import simple_tcp_socket_communicator
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-start_port", "--start_port_number", help="First available port number", default=8000)
parser.add_argument("-end_port", "--end_port_number", help="Last available port number", default=8100)
parser.add_argument("-shn", "--server_host_name", help="Host Name (IP Address) of main server (Process B)", default=socket.gethostname())
parser.add_argument("-c", "--challenge", help="Challenge mode", default=True)

LOOPBACK_HOST_NAME = '127.0.0.1'

args = parser.parse_args()


def main():
    '''
    Receives an .stl file from Process A and rebounds the same contents to Process A
    '''

    # Initialize Process B object
    process_b = simple_tcp_socket_communicator.ProcessB(first_available_port_number=args.start_port_number, 
                                                        last_available_port_number=args.end_port_number, 
                                                        host_name=LOOPBACK_HOST_NAME)

    # Rebound the file from process A
    process_b.rebound_file()

    print("Done rebounding file to Process A!")


def main_challenge():
    '''
    Receives an .stl file from Process A, converts its contents to a CSV file,
    and returns that CSV file to Process A
    '''

    # Initialize Process A object
    process_b = simple_tcp_socket_communicator.ProcessB(first_available_port_number=args.start_port_number, last_available_port_number=args.end_port_number, host_name=LOOPBACK_HOST_NAME)

    # Rebound the file from process A, converting into and returning a CSV file
    process_b.rebound_csv_file()

    print("Done rebounding (csv) file to Process A")


if __name__ == "__main__":
    # Choose whether to complete challenge problem or standard problem
    if args.challenge:
        main_challenge()
    else:
        main()
