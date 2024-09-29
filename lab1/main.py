# Option 2
# Affine cipher and Vigenere cipher
from bidict import bidict

alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
_table = {i: c for i, c in enumerate(alphabet)}
table = bidict(_table)


def affine_crypte(text: str, a: float, b: float, verbose: bool = False) -> str:
    text = text.upper()
    new_text = ''
    for c in text:
        c_index = table.inverse[c]
        new_c_index = int(c_index * a + b) % len(alphabet)
        new_c = table[new_c_index]
        new_text += new_c

        if verbose:
            print(f'{c}: {c_index} -> {new_c}: {new_c_index}')
    return new_text


def vigenere_decrypte(text: str, key: str) -> str:
    text = text.upper()
    key = key.upper()
    new_text = ''
    for i, c in enumerate(text):
        k = key[i % len(key)]
        c_index = table.inverse[c]
        k_index = table.inverse[k]
        new_c_index = (c_index - k_index + len(alphabet)) % len(alphabet)
        new_c = alphabet[new_c_index]
        new_text += new_c
    return new_text


if __name__ == "__main__":
    first_name = 'Индюков'
    a = 7
    b = 17
    print(f'Affine crypted: {first_name} ({a}, {b}) -> {affine_crypte(first_name, a, b)}')

    vigenere_code = 'ДЮЖЗЦБАРШЁИАИХЖВ'
    vigenere_key = 'ХИШ'
    print(f'Vigenere decrypted: {vigenere_code} ({vigenere_key}) -> {vigenere_decrypte(vigenere_code, vigenere_key)}')
