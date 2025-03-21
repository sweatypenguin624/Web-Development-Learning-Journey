def splitString(response: str):
    res = response.split("\n")
    ret = []
    for cl in res:
        try:
            if ord(cl[0]) >= 48 and ord(cl[0]) <= 57: 
                ret.append(cl)
        except IndexError:
            continue
        except ValueError:
            continue

    return ret

def getFacts(response: str):
    id = response.find("Questions:")
    claims = splitString(response[:id])
    questions = splitString(response[id:])
    return claims, questions