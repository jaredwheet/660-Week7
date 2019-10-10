publicKey = '1234567890'
sessionKey = 'abcdefghij'

def getKey(password, encrypt = False, key = 0):

    translatedKey = ''
    key = 3 if encrypt else -3

    for character in password:
        if character.isalpha():
            num = ord(character)
            num += key 

            if character.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif character.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
                
            translatedKey += chr(num)
        else:
            translatedKey += character
    
    return translatedKey

def validateAuthenticity(cert):
    certTranslated = getKey(cert, False)
    if certTranslated == "I am a cert":
        return "server.py"
    elif certTranslated == "Hello World":
        return "client.py"
    else:
        return "Invalid certificate"

def getPublicKey():
    return publicKey