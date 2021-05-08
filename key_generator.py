from Crypto.Util import number #pycryptodome
def generate_primes():
    
    p = number.getPrime(1024)
    q = number.getPrime(1024)
    return p, q

def generate_public_key(phi_n):
    for i in range(1,phi_n):
        if phi_n % i != 0:
            return i  

def generate_private_key(phi_n, e):
    i=0
    while True:
        i+=1
        product = phi_n*i+1
        if product % e == 0:
            return product//e

def generate_constants(p, q):
    N = p*q
    phi_n = (p-1)*(q-1)

    return (N, phi_n)


def generate_keys():
    p, q = generate_primes()
    N, phi_n = generate_constants(p, q)

    public_key = generate_public_key(phi_n)
    private_key = generate_private_key(phi_n, public_key)

    return (public_key, private_key, N)





