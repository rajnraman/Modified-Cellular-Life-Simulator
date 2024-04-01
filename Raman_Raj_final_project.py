"""
Raj Raman (R11670402) | Final Project | 11/29/2022

Multithreading

Problem:

You are tasked with creating a Python program capable of executing the first 100 steps of a modified cellular life
simulator. This simulator will receive the path to the input file as an argument containing the starting cellular
matrix. The program must then simulate the next 100 time-steps based on the algorithm discussed below.
The simulation is guided by a handful of simplistic rules that will result in a seemingly complex
simulation of cellular organisms.

    Rules:

    1) Any position in the matrix with a hyphen ‘-’ is considered “dead” during the current time step.
    2) Any position in the matrix with a plus sign ‘+’ is considered “alive” during the current time step.
    3) If an “alive” square has two, four, or six living neighbors, then it will be “alive” in the next time step.
    4) If a “dead” square has a prime number of living neighbors, then it continues to be “alive” in the next
    time step.
    5) Every other square dies or remains dead, causing it to be “dead” in the next time step.

    Implementation of: Multithreading

    Your solution must also make use of the multiprocessing module and spawn a total number of threads
    equivalent to the number specified by the user in the -t option. Keep in mind that your program running
    normally would be considered running serially, in other words on a single thread.
"""

import argparse
import copy
from multiprocessing import Pool


def main():
    print("Project :: R11670402")
    # command line arguments
    parser = argparse.ArgumentParser(description='description')
    parser.add_argument('-i', "--input", required=True)
    parser.add_argument('-o,', "--output", required=True)
    parser.add_argument('-t', "--threads", type=int, default=1)
    args = parser.parse_args()
    matrix_orig = []
    # read file, append each row to matrix_orig
    with open(args.input, 'r') as f:  # args.input
        for row in f.read().strip().split("\n"):
            matrix_orig.append(list(row))
        MAXProcess = args.threads  # number of threads to process, inputted by user
        rows = len(matrix_orig)  # length of rows
        cols = len(matrix_orig[0])  # length of columns
        # the below statements are converting the '+' characters to integer 1, and '-' character to integer 0
        for a, row in enumerate(matrix_orig):
            for b, cell in enumerate(row):
                if cell == '+':
                    matrix_orig[a][b] = 1
                else:
                    matrix_orig[a][b] = 0
        time_step = 0  # initialize time step to 0
        # Assign number of process
        pool = Pool(processes=MAXProcess)
        poolList = list()  # list of lists
        # we have to predefine the rows we are packaging so that send the poolList as a parameter to pool.map
        final = copy.deepcopy(matrix_orig)  # allocating memory for matrix_orig
        while time_step < 100:
            # below, we are basically sending only 3 rows at a time to be processed by processRow function
            for i in range(rows):
                lineA = final[(i - 1) % rows]  # row below (above) middle
                lineB = final[i]  # middle row (row we are looking at)
                lineC = final[(i + 1) % rows]  # row above (below) middle
                threeArrays = [lineA, lineB, lineC]  # pack data into threeArrays
                poolList.append(threeArrays)  # append (add) to poolList
            # We will iterate through each row and perform our function on it
            # final will store the results
            final = pool.map(processRow, poolList)
            poolList.clear()  # clear original matrix data for list to update with new info
            time_step += 1  # update time step

        # create output file and write the matrix into file character by character line by line in matrix
        # we are converting the integer 1 and 0 back to + and -
        output = open(args.output, 'w')
        for i in range(rows):
            for j in range(cols):
                if final[i][j] == 1:
                    final[i][j] = '+'
                else:
                    final[i][j] = '-'
                output.write(final[i][j])
            output.write('\n')


# this function will go through each row and assign the right operand
def processRow(threeArrays):
    cols = len(threeArrays[1])
    mat = [0] * cols  # matrix consists of integer 0 for the number of columns]
    for j in range(cols):
        middle_array = threeArrays[1]  # assigns the middle row passed in threeArrays as the middle array. It is the array we are updating
        # "1" is current row we are looking at or updating (middle of three lines we are sending)
        up = 0  # 1st row (top row passed in threeArrays)
        down = 2  # 3rd row (bottom row passed in threeArrays)
        left = (j - 1) % cols  # left index of current position in matrix
        right = (j + 1) % cols  # right index of current position in matrix
        # neighbors_sum holds integer value of the surrounding neighbors that I will be summing up
        neighbors_sum = (threeArrays[up][left] + threeArrays[up][j] + threeArrays[up][right] + threeArrays[1][left] +
                         threeArrays[1][right] + threeArrays[down][left] + threeArrays[down][j] + threeArrays[down][right])
        # now, logic is applied (as specified in instructions) and mat will hold updated integer (1 or 0)
        if middle_array[j] == 0 and (neighbors_sum == 2 or neighbors_sum == 3 or neighbors_sum == 5 or neighbors_sum == 7):
            mat[j] = 1
        elif middle_array[j] == 1 and (neighbors_sum == 2 or neighbors_sum == 4 or neighbors_sum == 6):
            mat[j] = 1
        else:
            mat[j] = 0
    return mat


if __name__ == '__main__':
    main()
