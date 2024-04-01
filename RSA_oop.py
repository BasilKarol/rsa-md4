import sympy

class RSA:
    def __init__(self):
        self.p, self.q = self.diff_primes()
        self.N = self.p * self.q
        self.gcd = self.extended_euclidean_algorithm(65537, (self.p - 1) * (self.q - 1))
        self.pub = (self.N, 65537)
        self.prv = self.solve_diofantine(65537, (self.p - 1) * (self.q - 1))

    def prime(self, min):
        prime = sympy.randprime(min, 10 * min)
        return prime

    def diff_primes(self):
        min = 2 ** 64
        p = self.prime(min)
        q = self.prime(min)

        while p == q:
            q = self.prime(min)

        return p, q

    def extended_euclidean_algorithm(self, a, b):
        if b == 0:
            return a, 1, 0

        gcd, x1, y1 = self.extended_euclidean_algorithm(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    def solve_diofantine(self, a, b):
        gcd, d, y = self.extended_euclidean_algorithm(a, b)

        if gcd == 1:
            return d, self.p, self.q
        else:
            return None

    def encrypt(self, message):
        c = pow(message, self.pub[1], self.N)
        return c

    def decrypt(signature, public_key): #tu zmieniłam bo żle zamieniało podpis na hash a teraz działa
        modulus, exponent = public_key
        decrypted_hash = pow(signature, exponent, modulus)
        return decrypted_hash
    ## nowa funkcja do generowania podpisu
    def generate_sign(self, check_sum, another_prv=None):
        if another_prv:
            d, p, q = another_prv
        else:
            d, p, q = self.prv
        return pow(check_sum, d, p * q)
        
    def generate_keys(self):
        # Kod generowania kluczy RSA
        # Zwraca klucz prywatny i klucz publiczny
        private_key = 'PRYWATNY KLUCZ RSA:\n' + ' '.join( map(str, self.prv) )
        public_key = "PUBLICZNY KLUCZ RSA:\n" + ' '.join( map(str, self.pub ) )
        return private_key, public_key
