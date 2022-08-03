import os
import textwrap
from glob import glob
from pdfrw import PdfReader, PdfWriter
import PyPDF2
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas



PAGEWIDTH = 95                                         # total characers to build each line
MAXDEPTH = 7                                            # max depth to build TOC
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
                    #print(it.path + "/" + str(file))

            listdirs(it)
    return dirs

# makes a TOC for all pdf files in a directory sructure
def makeBook():
    #file = PdfFileWriter()

    pagecount = 1
    stack = []
    c = os.getcwd()
    c = '/home/gareth/Downloads/'
    listdir = []
    tmpDirs = listdirs(c)
    lines = []
    y = 10
    mycanvas = Canvas('/home/gareth/PycharmProjects/dirbook/toc.pdf', pagesize=A4)
    mycanvas.setFont("Courier", 8)
    mycanvas.setFillColor(black)
    if tmpDirs:
        d = (tmpDirs[0].replace(c, '')).split('/')                           # setup working variables
        depth = len(d)
        startCount = depth - 1
        count = depth
        lastDepth = depth - 1
        oldpagenum = 1

        for z in tmpDirs:
            x = z
            oldpagenum = pagecount
            if z[-1:] == '*':
                x = z.replace('*', '.pdf')
                pdf = PdfReader(x)
                oldpagenum = pagecount
                #print("&&& " + str(len(pdf.pages)))
                pagecount = pagecount + len(pdf.pages)

            l = z.replace(c, '')  # strip off directory info above the selected dir

            #print("### " + l)

            line = ""
            d = l.split('/')
            depth = len(d)
            delta = depth - lastDepth
            entry = str(d[-1:][0])                          # strip out dir or filename for toc entry
            if delta > 0:                                  #'/home/gareth/PycharmProjects/dirbook/toc.pdf' # deeper nesting
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
                titlepage = line
                for fill in range(PAGEWIDTH - len(line)):      # fill in blanks to mke line width
                    line = line + " "
                #insert page
                pagecount = pagecount + 1
            if entry[-1:] == "*":
                for fill in range(PAGEWIDTH - len(line) - len(entry) - 1):      # fill in blanks to mke line width
                    line = line + " "
                line = line + " " + entry
            lastDepth = depth
            line = line + '{:>5}'.format(str(oldpagenum))
            if (depth <= MAXDEPTH):                         # only show if less than max depth
                print(line)
                lines.append(line)
            #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

                wrapper = textwrap.TextWrapper(width=100)
                text = wrapper.wrap(text=line)
                for textline in text:
                    mycanvas.drawString(0.75 * inch, y * inch, str(textline))
                    y = y-0.15
                if y < 2.0:
                    y=10.0
                    mycanvas.showPage()
                    mycanvas.setFont("Courier", 8)
                    mycanvas.setFillColor(black)

    mycanvas.save()



    merger = PdfWriter()
    for l in tmpDirs:
        d = l.replace('*', '.pdf').split('/')
        entry = str(d[-1:][0])

        if l[-1:] != '*':
            canvas = Canvas('/home/gareth/PycharmProjects/dirbook/blankpage.pdf', pagesize=A4)
            # Set font to Times New Roman with 12-point size
            canvas.setFont("Courier", 20)
            # Draw blue text one inch from the left and ten
            # inches from the bottom
            canvas.setFillColor(black)
            wrapper = textwrap.TextWrapper(width=40)
            text = wrapper.wrap(text=entry)
            y = 10.0
            for textline in text:
                canvas.drawString(0.75 * inch, y * inch, str(textline))
                canvas.bookmarkPage(str(textline))
                #canvas.showPage()
                canvas.addOutlineEntry(str(textline), str(textline), level=0)
                y = y-0.3
            # Save the PDF file

            canvas.save()

        x = "blankpage.pdf"
        if l[-1:] == '*':
            x = l.replace('*', '.pdf')
        pdf = PdfReader(x).pages
        print(str(len(pdf)) + " : ", x)
        merger.addpages(PdfReader(x).pages)

    merger.write("book.pdf")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    makeBook()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
