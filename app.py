from core.pdf_handler import PDFHandler
from core.parser import StatementParser

pdf =  PDFHandler.prepare_pdf(
    "data/uploads/adarsh-statement.pdf",
    password=input("Password : ")
)

parser = StatementParser()

result = parser.parse(pdf)

print(result)






# pdf_path = "data/uploads/statement-axis.pdf"

# password = input("Enter PDF Password : ")

# try:
#     ready_pdf = PDFHandler.prepare_pdf(pdf_path, password=password)
    
#     print("PDF Ready!", ready_pdf)

# except ValueError as e:
#     print(e)