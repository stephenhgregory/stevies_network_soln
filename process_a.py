from typing import AnyStr
from utils import simple_tcp_socket_communicator, file_utils
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("-og_cad_fname", "--original_cad_filename", help="Original CAD Filename", default='assets/cad_mesh.stl')
parser.add_argument("-new_cad_fname", "--new_cad_filename", help="New CAD Filename", default='assets/output.stl')
parser.add_argument("-new_csv_fname", "--new_csv_filename", help="New CSV Filename", default='assets/output.csv')
parser.add_argument("-start_port", "--start_port_number", help="First available port number", default=8000)
parser.add_argument("-end_port", "--end_port_number", help="Last available port number", default=8100)
parser.add_argument("-shn", "--server_host_name", help="Host Name (IP Address) of main server (Process B)", default='192.168.1.162')
parser.add_argument("-c", "--challenge", help="Challenge mode", default=True)

LOOPBACK_HOST_NAME = '127.0.0.1'

args = parser.parse_args()


def main():
    '''
    Sends the contents of an .stl file to Process B, and waits to receive the same
    contents back from Process B. Then, verifies equivalence between the two files.
    '''
    # Initialize Process A
    process_a = simple_tcp_socket_communicator.ProcessA(first_available_port_number=args.start_port_number, 
                                            last_available_port_number=args.end_port_number, 
                                            host_name=LOOPBACK_HOST_NAME, 
                                            original_cad_filename=args.original_cad_filename, 
                                            new_cad_filename=args.new_cad_filename)    

    # Send and receive the CAD file to/from process B
    process_a.send_and_receive_file()

    # Check whether the original and returned files are equivalent
    assert file_utils.is_same(args.original_cad_filename, args.new_cad_filename)

    print("Task complete. The two files are equivalent!")


def main_challenge():
    '''
    Sends the contents of an .stl file to Process B, and waits to receive the contents
    of the file converted into a CSV file from Process B. Does not verify the contents
    of the returned CSV file.
    '''

    # Initialize Process A
    process_a = simple_tcp_socket_communicator.ProcessA(first_available_port_number=args.start_port_number, 
                                            last_available_port_number=args.end_port_number, 
                                            host_name=LOOPBACK_HOST_NAME, 
                                            original_cad_filename=args.original_cad_filename, 
                                            new_csv_filename=args.new_csv_filename)    

    # Send the CAD file to and receive the CSV file from process B
    process_a.send_and_receive_csv_file()

    # Makes sure that we got and saved a new, non-empty CSV file
    assert os.path.exists(args.new_csv_filename) and os.stat(args.new_csv_filename).st_size > 0

    print("New, non-empty CSV file exists! Check the file manually to see if it worked")


if __name__ == "__main__":

    # Choose whether to complete challenge problem or standard problem
    if args.challenge:
        main_challenge()
    else:
        main()
