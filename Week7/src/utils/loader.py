from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    Docx2txtLoader
)

def load_document(path):
    if path.endswith(".pdf"):
        return PyPDFLoader(path).load()
    elif path.endswith(".txt"):
        return TextLoader(path).load()
    elif path.endswith(".csv"):
        return CSVLoader(path).load()
    elif path.endswith(".docx"):
        return Docx2txtLoader(path).load()
    else:
        raise ValueError("Unsupported file type")