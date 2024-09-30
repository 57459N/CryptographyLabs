# Option 2
# Affine and Vigenere cipher

from abc import ABC, abstractmethod


def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd, s1, t1 = extended_gcd(b % a, a)
    s = t1 - (b // a) * s1
    t = s1
    return gcd, s, t


def mod_inverse(a: int, m: int):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


class BaseCipher(ABC):
    @abstractmethod
    def encrypt(self, text: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, text: str) -> str:
        pass


class AffineCipher(BaseCipher):
    def __init__(self, alphabet: str, key: tuple[int, int]) -> None:
        self.int_to_char = {i: c for i, c in enumerate(alphabet)}
        self.char_to_int = {c: i for i, c in enumerate(alphabet)}
        self.key = key

    def encrypt(self, text: str, verbose: bool = False) -> str:
        a, b = self.key
        new_text = ''
        for c in text:
            c_index = self.char_to_int[c]
            new_c_index = int(c_index * a + b) % len(self.int_to_char)
            new_c = self.int_to_char[new_c_index]
            new_text += new_c

            if verbose:
                print(f'{c}: {c_index} -> {new_c}: {new_c_index}')
        return new_text

    def decrypt(self, text: str, verbose: bool = False) -> str:
        a, b = self.key
        m = len(self.int_to_char)
        a_inv = mod_inverse(a, m)
        text = text.upper()
        new_text = ''
        for c in text:
            c_index = self.char_to_int[c]
            new_c_index = (a_inv * (c_index + m - b)) % m
            new_c = self.int_to_char[new_c_index]
            new_text += new_c

            if verbose:
                print(f'{c}: {c_index} -> {new_c}: {new_c_index}')
        return new_text


class VigenereCipher(BaseCipher):
    def __init__(self, alphabet: str, key: str) -> None:
        self.int_to_char = {i: c for i, c in enumerate(alphabet)}
        self.char_to_int = {c: i for i, c in enumerate(alphabet)}
        self.key = key

    def encrypt(self, text: str) -> str:
        new_text = ''
        for i, c in enumerate(text):
            k = self.key[i % len(self.key)]
            c_index = self.char_to_int[c]
            k_index = self.char_to_int[k]
            new_c_index = (c_index + k_index) % len(self.int_to_char)
            new_c = self.int_to_char[new_c_index]
            new_text += new_c
        return new_text

    def decrypt(self, text: str) -> str:
        m = len(self.int_to_char)
        new_text = ''
        for i, c in enumerate(text):
            k = self.key[i % len(self.key)]
            c_index = self.char_to_int[c]
            k_index = self.char_to_int[k]
            new_c_index = (c_index - k_index + m) % m
            new_c = self.int_to_char[new_c_index]
            new_text += new_c
        return new_text


if __name__ == "__main__":
    # alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    # Affine
    first_name = 'Индюков'
    first_name = first_name.upper()
    a = 7
    b = 17
    a_crypter = AffineCipher(alphabet, (a, b))

    affine_encrypted = a_crypter.encrypt(first_name)
    affine_decrypted = a_crypter.decrypt(affine_encrypted)
    print(f'Affine encryption: {first_name} ({a}, {b}) -> {affine_encrypted}')
    print(f'Affine decryption: {affine_encrypted} ({a}, {b}) -> {affine_decrypted}')

    print()
    # Vigenere
    vigenere_code = 'ДЮЖЗЦБАРШЁИАИХЖВ'
    vigenere_key = 'ХИШ'
    v_crypter = VigenereCipher(alphabet, 'ХИШ')

    vigenere_decrypted = v_crypter.decrypt(vigenere_code)
    vigenere_encrypted = v_crypter.encrypt(vigenere_decrypted)
    print(f'Vigenere decryption: {vigenere_code} ({vigenere_key}) -> {vigenere_decrypted}')
    print(f'Vigenere encryption: {vigenere_decrypted} ({vigenere_key}) -> {vigenere_encrypted}')
