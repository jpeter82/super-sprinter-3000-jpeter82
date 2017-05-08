

def read_from_file(file_name, separator=';'):
    '''
    Read file content and return it as list of lines.
        @param    file_name    string    The name of the file to be read from.
        @param    separator    string    The separator used in the file.
        @return                list      List of lines stripped from end-of-line character.
    '''
    with open(file_name, 'r', encoding='utf-8') as f:
        data = [line.strip('\n').split(separator) for line in f.readlines()]
    return data


def write_to_file(what, file_name, separator=';'):
    '''
    Write one or multiple lines to file
        @param    what         list      List of lines(!)
        @param    file_name    string    The name of the file to be written to.
        @param    separator    string    The separator used in the file.
        @return                boolean   True if process is successful, otherwise False.
    '''
    what = [[change_eol(data) for data in line] for line in what]
    data = list(map(lambda x: x + '\n', [separator.join([str(item) for item in line]) for line in what]))

    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.writelines(data)
    except:
        status = False
    else:
        status = True

    return status


def change_eol(string, mode=0):
    '''
    Change end of line character for HTML break line, vica versa.
    Needed because of differencies in storing and presentation.
        @param     string    string    The string to be modified.
        @param     mode      int       Defines which way should the replacement be done.
        @return              string    The modified string.
    '''
    br1 = "<br />"
    br2 = "<br>"

    if mode == 0:
        string = string.replace("\r\n", br1).replace("\n\r", br1).replace("\r", br1).replace("\n", br1)
    elif mode == 1:
        string = string.replace(br1, "\r\n")
        string = string.replace(br2, "\r\n")
    else:
        raise ValueError('Unsupported mode.')

    return string


def main():
    pass

if __name__ == '__main__':
    main()
