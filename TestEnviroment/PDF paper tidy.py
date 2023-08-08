from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize

FileName = "Test Title.pdf"

reader = PdfReader(f'./SourceFile/{FileName}')

for page in range(len(reader.pages)):
    page = reader.pages[page]
    sentence = sent_tokenize(page.extract_text())
    print("\n" * 2)
    for text in range(len(sentence)):
        print(sentence[text])
        if text % 20 == 0 and text != 0:
            print("\n" * 2)
            input("type any key to continue ...")
            print("\n" * 2)
