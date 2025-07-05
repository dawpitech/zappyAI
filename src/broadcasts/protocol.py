def decipherMessage(message) :
    msgList = caesarCipher(message, -1).split(':')
    result = coordsToInt(msgList[0])
    for i in range(1, len(msgList)) :
        result = f"{result}:{msgList[i]}"
    return result

def cipherMessage(message) :
    msgList = message.split(':')
    result = intToCoords(int(msgList[0]))
    for i in range(1, len(msgList)) :
        result = f"{result}:{msgList[i]}"
    return caesarCipher(result, 1)

def coordsToInt(coords):
    adresses = {
        "44.87493101875373,-0.5826042495044681" : 0,
        "44.874290892831205,-0.5788331992663709" : 1,
        "44.874707835956244,-0.5798722328876327" : 2,
        "44.87286625673911,-0.5830951451886301" : 3,
        "44.87448365353479,-0.5784116881311951" : 4,
        "44.87471912956438,-0.5810014664225926" : 5
        }
    if coords in adresses :
        return adresses[coords]
    else :
        return -1

def intToCoords(value):
    value %= 6
    adresses = {
        0 : "44.87493101875373,-0.5826042495044681",
        1 : "44.874290892831205,-0.5788331992663709",
        2 : "44.874707835956244,-0.5798722328876327",
        3 : "44.87286625673911,-0.5830951451886301",
        4 : "44.87448365353479,-0.5784116881311951",
        5 : "44.87471912956438,-0.5810014664225926"
        }
    if value in adresses :
        return adresses[value]
    else :
        return ""

def caesarCipher(msg, n) :
    return ''.join(chr((ord(c) + n) % 128) for c in msg)

if __name__ == "__main__":
    print(decipherMessage(cipherMessage("4:ji gou ji:")))
