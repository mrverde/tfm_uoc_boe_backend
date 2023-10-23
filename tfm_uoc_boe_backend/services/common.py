
def read_txt_file(path: str) -> str:
    file = open(path, 'r')
    data = file.read()
    file.close()
    return data
