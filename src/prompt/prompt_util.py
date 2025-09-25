

def getPromptTemplate(file_name) -> str:
    with open(file_name) as file:
        return file.read()