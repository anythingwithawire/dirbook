import os
from glob import glob
from pyPDF2 import PdfFileReader, PdfFileWriter

#from PyPDF2 import PdfReader, PdfWriter

'''
def merge(path, output_filename):
    output = PdfFileWriter()

    for pdffile in glob(path + os.sep + '*.pdf'):
        if pdffile == output_filename:
            continue
        print("Parse '%s'" % pdffile)
        document = PdfFileReader(open(pdffile, 'rb'))
        for i in range(document.getNumPages()):
            output.addPage(document.getPage(i))

    print("Start writing '%s'" % output_filename)
    with open(output_filename, "wb") as f:
        output.write(f)
'''

PAGEWIDTH = 120                                         # total characers to build each line
MAXDEPTH = 6                                            # max depth to build TOC
INDENT = 2                                              # num chars to indent each level

dirs = []


# returns a list of directories and filenames of pdf files without ".pdf" extension
# filenames are appended with "*"
def listdirs(basedir):
    for it in os.scandir(basedir):
        if it.is_dir():
            dirs.append(it.path)
            for file in os.listdir(it):
                if len(file) >= 4 and file[-4:] == ".pdf":
                    dirs.append(it.path + "/" + str(file[:-4]) + "*")
                    print(it.path + "/" + str(file))

            listdirs(it)
    return dirs

# makes a TOC for all pdf files in a directory sructure
def makeBook():
    pagecount = 1
    stack = []
    c = os.getcwd()
    c = '/home/gareth/Downloads/'
    listdir = []
    tmpDirs = listdirs(c)
    for l in tmpDirs:
        listdir.append(l.replace(c, ''))                    # strip off directory info above the selected dir

    if listdir:
        d = listdir[0].split('/')                           # setup working variables
        depth = len(d)
        startCount = depth - 1
        count = depth
        lastDepth = depth - 1

        for l in listdir:
            line = ""
            d = l.split('/')
            depth = len(d)
            delta = depth - lastDepth
            entry = str(d[-1:][0])                          # strip out dir or filename for toc entry
            if delta > 0:                                   # deeper nesting
                for pp in range(abs(delta)):
                    stack.append(1)
                count = 1
            if delta < 0:                                   # shallower nesting
                for pp in range(abs(delta)):
                    count = stack.pop()
                count = stack.pop()
                stack.append(count+1)
            if delta == 0:                                  # same depth
                count = stack.pop()
                stack.append(count+1)
            for level in range(depth - 1):                  # make indent
                for i in range(INDENT):
                    line = line + " "
            for level in range(depth):
                line = line + str(stack[level])             # add level number
                if depth - level > 1:                       # add "." if not last level
                    line = line + "."
            count = count + 1                               # inc count
            if entry[-1:] != "*":
                line = line + " " + entry
            for fill in range(PAGEWIDTH - len(line) - len(entry)):      # fill in blanks to mke line width
                line = line + " "
            if entry[-1:] == "*":
                line = line + " " + entry
            lastDepth = depth
            if (depth <= MAXDEPTH):                         # only show if less than max depth
                #pdf.addpage()
                #pdf.addpdffile()
                print(line)

    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    makeBook()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
