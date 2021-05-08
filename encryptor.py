
def text_to_numeric_cipher(text):
    cipher ="1"
    for ch in text:
        if ord(ch)>99:
            cipher+=str(ord(ch))
        elif ord(ch)>9:
            cipher+="0"
            cipher+=str(ord(ch))
        else:
            cipher+="00"
            cipher+=str(ord(ch))

    return cipher

def numeric_cipher_to_text(numeric_cipher):
    number = int(numeric_cipher)
    text=""

    while True:
        rem = number%1000
        number = number//1000
        ch = chr(rem)
        text+=ch

        if number == 1:
            return text[::-1]


def encrypt(x, y, p):
    res = 1  
    x = x % p
     
    if (x == 0) :
        return 0
 
    while (y > 0) :
 
        if ((y % 2) == 1) :
            res = (res * x) % p

        y = y//2  
        x = (x * x) % p
         
    return res


def decrypt(x, y, p):
    res = 1    
    x = x % p
     
    if (x == 0) :
        return 0
 
    while (y > 0) :
         
        if ((y % 2) == 1) :
            res = (res * x) % p 

        y = y//2    
        x = (x * x) % p
         
    return res
