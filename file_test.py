import os
import subprocess

file_flag=1
# Covers scenario of having the file, and reaching the end of the file
if os.path.isfile('./sample.env') is True and file_flag == 1:
    return_value = os.system("rm sample.env")
    if return_value == 0:
        print('Output of the remove operation succeeded.')
    elif return_value == 1:
        print('Output of the remove operation failed.')
# Covers the scenario where the file does not exist, and it is the beginning of the file
elif os.path.isfile('./sample.env') is False and file_flag == 0:
    return_value = os.system("cp variables.env sample.env")
    if return_value == 0:
        print('Output of the create operation succeeded.')
    elif return_value == 1:
        print('Output of the create operation failed.')

