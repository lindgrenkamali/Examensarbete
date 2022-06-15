import os

def negative_files():
    with open("negative.txt", 'w') as f:
        for filename in os.listdir("NegativeCSGO"):
            f.write("negative/" + filename + "\n")