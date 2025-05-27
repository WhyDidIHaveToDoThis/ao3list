import sendlink

def downloadpages(ids, numpages=1):
    """Download specified tag excluding tons of fandoms"""
    with open('excludelink.txt') as f:
        base = f.readlines()
    for id in ids:
        base.append(id)
        url = ''.join(base)
        sendlink.testiflink(url)
        sendlink.downloadfromlink(url, numpages)


def gettagid(url):
    """Gets tag id from link"""
    divide = url.split("&tag_id=")
    id = divide[1].strip()
    return id


if __name__ == "__main__":

    userinput1 = input('Specify tag, link with tag, or file containing either.\n')
    output = []

    if userinput1.endswith('.txt'):
        with open(userinput1) as f:
            idfile = f.readlines()
        for id in idfile:
            if id.startswith('http'):
                output.append(gettagid(id.strip()))
            else:
                output.append(id.strip())

    elif userinput1.startswith('http'):
        output.append(gettagid(userinput1.strip()))
    
    else:
        output.append(userinput1.strip())

    numpages = int(input('Specify number of pages to download.\n'))

    print(output, numpages)
    downloadpages(output, numpages)