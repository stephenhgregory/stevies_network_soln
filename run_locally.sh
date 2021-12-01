# Simple script to run Process A and Process B on the same local machine.
# This file completes both the standard and challenge versions of the Machina Labs network problem.

# 1. Run the non-challenge version
# 1.1. Run Process B and Process A
python process_b.py & 
python process_a.py

# 2. Run the challenge version
# 2.1. Run Process B and Process A
python process_b.py -c & 
python process_a.py -c