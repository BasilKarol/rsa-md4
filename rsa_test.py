import pytest
from hypothesis import given, strategies as st
from hypothesis.strategies import integers
import sympy
from RSA_oop import RSA

class TestRSA:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.rsa = RSA()

    @given(st.integers(min_value=1, max_value=10**4))
    def test_encrypt_decrypt_hypothesis(self, message):
        ciphertext = self.rsa.encrypt(message)
        decrypted_message = self.rsa.generate_sign(ciphertext)
        assert decrypted_message == message

    def test_prime(self):
        prime = self.rsa.prime(1000)
        assert sympy.isprime(prime)

    def test_diff_primes(self):
        p, q = self.rsa.diff_primes()
        assert p != q

    def test_extended_euclidean_algorithm(self):
        p, q = self.rsa.diff_primes()
        gcd, x, y = self.rsa.extended_euclidean_algorithm(65537, (p - 1) * (q - 1))
        assert gcd == 1

    def test_solve_diofantine(self):
        p, q = self.rsa.diff_primes()
        x, p, q = self.rsa.solve_diofantine(65537, (p - 1) * (q - 1))
        assert x is not None

# Wywołanie testów jednostkowych
if __name__ == "__main__":
    pytest.main()
    
    
    
    
    