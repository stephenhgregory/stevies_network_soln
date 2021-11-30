''' Contains utility functions for file manipulation/analytics '''

from typing import Any, AnyStr, List, Tuple
import filecmp
import time
import numpy as np
from stl import mesh


def is_same(filename1: AnyStr, filename2: AnyStr) -> bool:
    '''Check whether two files are equivalent'''
    return filecmp.cmp(filename1, filename2)


def function_timer(func):
    def wrapper_function(*args, **kwargs):
        t1 = time.time()
        func(*args,  **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
    return wrapper_function


def load_points(stl_filename: AnyStr) -> List[Tuple]:
    '''
    Given an .stl filename, load all of the points in the file as a list of tuples
    '''
    # First, open the .stl file as a mesh
    stl_mesh = mesh.Mesh.from_file(stl_filename)

    # Then, extract the points in the mesh
    points = np.around(np.unique(stl_mesh.vectors.reshape([int(stl_mesh.vectors.size/3), 3]), axis=0), 2)

    # Convert the numpy array into a list of lists for the points
    points_as_list_of_lists = points.tolist()

    # Finally, convert the list of lists to a list of tuples
    points_as_list_of_tuples = [tuple(points) for points in points_as_list_of_lists]

    return points_as_list_of_tuples


def save_points_to_csv(new_csv_filename: AnyStr, stl_points: List[List]) -> None:
    '''
    Given a list of tuples representing the points in an stl file,
    saves the points to a csv file.
    '''

    # Open the new csv file to be saved
    with open(new_csv_filename, 'w') as new_csv:
        # Loop over each point
        for point_set in stl_points:
            # Print each line to the new_csv file
            print(f'{point_set[0]:.4f}, {point_set[1]:.4f}, {point_set[2]:.4f}', file=new_csv)

    print('Done saving points to new_csv file')


def convert_stl_to_csv(stl_filename: AnyStr, new_csv_filename: AnyStr) -> None:
    '''
    Given an .stl file, converts the .stl mesh into a list of tuples representing the 
    components of each point in the mesh, then saves that list of tuples to a  csv file
    '''
    # First, load the points as a list of tuples
    points = load_points(stl_filename=stl_filename)

    # Then, save those points to a csv file
    save_points_to_csv(new_csv_filename=new_csv_filename, stl_points=points)

    return