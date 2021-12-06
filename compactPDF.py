#!/usr/bin/env python3
# Author: Aupi Santiago
# This utility is very useful when
# you want to avoid repeating pdf sheets with the same page number.
# Normally this happens when the pdf
# is generated from a presentation with transitions on each page

# HOW TO USE
# (on cmd/bash) ./compactPDF.py <file1> <file2> ... <fileN>

# Or you can just run the script as main program and follow the steps


try:
    import PyPDF2
    from sys import argv
    import os
except(ModuleNotFoundError):
    print("PyPDF2 not installed. Install it with: pip install PyPDF2")
    exit()

try:
    #print(os.getcwd(),'\n')
    if __name__ == '__main__' and len(argv)==1:
        file_name = input("PDF name: ")
        files = [file_name]
    else:
        files = [argv[i].split('.')[-2]+'.pdf'.replace('\\','')
                 for i in range(1,len(argv))]

    width, height = 720, 540
    
    for _file_name in files:
        file = open(_file_name,'rb')
        pdf = PyPDF2.PdfFileReader(file)
        
        new_pdf = PyPDF2.PdfFileWriter()
        
        pdf_length = pdf.getNumPages()

        pages = []
        #loop all pages
        for i in range(0, pdf_length): 
            page_ = pdf.getPage(i)
            num = page_.extractText().split('\n')
            number_ = num[-2] # num of the page
            number_ = number_.split('/')[0]
            if(number_.isdigit()):
                number_ = int(number_)
            pages.append(number_)
            
        k = 0
        j = 0
        while k < pdf_length-1:   
            if(pages[k] != pages[k+1]):
                new_pdf.addPage(pdf.getPage(k))
                # scale to a fix widht and height
                new_pdf.getPage(j).scaleTo(width, height)
                j += 1
            k+=1
            
        # last page
        new_pdf.addPage(pdf.getPage(k))
        new_pdf.getPage(j).scaleTo(width, height)

        output_name = _file_name.split('.')[-2]+'_compact.pdf'
        output_file = open(output_name, 'wb')
        new_pdf.write(output_file)
        
        output_file.close() #closing files
        file.close()

        print(f"PDF compacted: {_file_name} ---> {output_name}")
    
except(FileNotFoundError):
    print("Archivo no encontrado.")

except(KeyboardInterrupt):
    file.close()
    output_file.close()
    exit()
   
