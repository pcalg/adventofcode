from collections import defaultdict

from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 7, test)

def get_size(directory_structure, files_in_directory, d):

    stack = [d]

    #cur_total = sum(files_in_directory[d])

    sizes = {}

    cur_total = 0

    while len(stack) > 0:
        cur_d = stack.pop()
        #print(stack)
        cur_total += sum(files_in_directory[cur_d])

        sizes[cur_d] = cur_total

        for sub_d in directory_structure[cur_d]:
            if sub_d not in sizes:
                stack.append(sub_d)


    # for sub_d in directory_structure[d]:
    #     s = get_size(directory_structure, files_in_directory, sub_d)
    #     cur_total += s
    print(f"result: {cur_total}")
    return cur_total

# def directory_sizes(directory_structure, files_in_directory):
#
#     result = []
#
#     print(directory_structure.keys())
#
#     for d in list(directory_structure.keys()):
#         print("processing", d)
#         size = get_size(directory_structure, files_in_directory, d)
#         result.append(size)
#
#     return result




class PuzzleDay7(PuzzleInterface):

    def solve_part_1(self):
        pass

    def solve_part_2(self):
        pass


#puzzle = PuzzleDay6(puzzle_input)

#print(f"Solution {puzzle.solve_part_1()}")
#print(f"Solution {puzzle.solve_part_2()}")


#cur_dir = ""
cur_dir_list = []
all_dirs = []
directory_structure = {}
files_in_directory = defaultdict(list)

for line in puzzle_input:
    if line.startswith("$"):
        print(f"command: {line}")
        command_parts = line.split(" ")
        if command_parts[1] == "cd" and command_parts[2] == "..":
            print(f"pre dirs: {cur_dir_list}")
            cur_dir_list.pop()
            print(f"after dirs: {cur_dir_list}")
        elif command_parts[1] == "cd":
            cur_dir = command_parts[2]
            if cur_dir not in directory_structure:
                directory_structure[cur_dir] = []
                all_dirs.append(cur_dir)

            if cur_dir == "/":
                cur_dir_list = ["/"]
            else:
                cur_dir_list.append(cur_dir)
    else:
        # file or dir
        # add to dictionary
        command_parts = line.split(" ")

        if command_parts[0] == "dir":
            print(f"dir: {line}")

            directory_structure[cur_dir_list[-1]].append(command_parts[1])
        else:
            print(f"file: {line}")
            files_in_directory[cur_dir].append(int(command_parts[0]))



print("---")
print(directory_structure.keys())

all_sizes = []
for d in all_dirs:
    print(f"hi: {d}")

    s = get_size(directory_structure, files_in_directory, d)
    print(s)

    all_sizes.append(s)

#r = directory_sizes(directory_structure, files_in_directory)

total = 0
for fs in all_sizes:
    if fs <= 100000:
        total += fs

print(total)
#print(r)
#print(directory_structure.keys())