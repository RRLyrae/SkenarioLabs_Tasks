import cv2
import pytesseract
import glob
from pathlib import Path
import csv
import re

pytesseract.pytesseract.tesseract_cmd = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
# ------------------------------------------------------------------------------------------
# For reading images of different formats (all in the same folder):
imdir = Path("C:/Users/Diana Crowe/PycharmProjects/textDetection/")
ext = ['png', 'jpeg', 'gif']    # image formats here

files = []                                      # creating a list for the image files
for e in ext:
    # print(str(imdir) + '\*.' + e) # uncomment to check what kind of image files we are looking for
    files.extend(glob.glob(str(imdir) + '\*.' + e))

images = [cv2.imread(fil) for fil in files]   # reading the image files into a list
# ------------------------------------------------------------------------------------------

# pytesseract only accepts RGB values and opencv is in BGR
# so, we need to convert before we can send the image to the pytesseract library:
images = [cv2.cvtColor(imx, cv2.COLOR_BGR2RGB) for imx in images]

# writing the data read by tesseract into a text file
data_folder = Path("C:/Users/Diana Crowe/PycharmProjects/textDetection/data.txt")
text_file = open(data_folder, "w")                # open text file

for i in images:
    text_file.write(pytesseract.image_to_string(i))
text_file.close()                                   # close file

# Finding the line containing the total area in our text file
file_name = "data.txt"

# key words that we are looking for to find the total area:
total_area = ['TOTAL', 'total', 'Total', 'Approximate Area']    # edit to add more keywords if needed

# using try catch except to handle file not found error.
# entering try block
try:
    # opening and reading the file
    file_read = open(file_name, "r")

    # reading file content line by line.
    lines = file_read.readlines()

    new_list = []
    idx = 0

    # looping through each line in the file
    for line in lines:

        # if the line has the input string, get the index of that line and put the
        # line into a newly created list
        for text in total_area:
            if text in line:
                new_list.insert(idx, line)
                idx += 1

    # closing file after reading
    file_read.close()

    # if length of new list is 0 that means the input string wasn't found in the text file
    for text in total_area:
        if len(new_list) == 0:
            print("\n\"" + text + "\" is not found in \"" + file_name + "\"!")
            print()

# entering except block if input file doesn't exist
except:
    print("\ncannot find Total Area information!")

# writing the Total Area data into a text file
data_folder2 = Path("C:/Users/Diana Crowe/PycharmProjects/textDetection/total_area.txt")
t_area = open(data_folder2, "w")                # open text file
lineLen = len(new_list)
for i in range(lineLen):
    t_area.write(new_list[i])
t_area.close()                                   # close file

# ...but I was asked for a csv file, so here it is:
data_folder3 = Path("C:/Users/Diana Crowe/PycharmProjects/textDetection/total_area.csv")

# This version of txt to csv is edited out because it also separates each element of the lines by commas
#f = open(data_folder3, 'w')         # open the file in the write mode
#writer = csv.writer(f)              # create the csv writer
#for i in range(lineLen):
#    writer.writerow(new_list[i])    # write a row to the csv file
#f.close()                           # close the file

# I like this version of txt to csv better as each line from my txt file is kept intact
# and each line is separated by the next one by a comma
with open(data_folder2, 'r') as reader:
    text = reader.read()

text = re.sub(r"(...)\n", r"\1,", text)
print(text)

with open(data_folder3, 'w') as writer:
    writer.write(text)