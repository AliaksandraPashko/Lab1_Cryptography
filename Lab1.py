from collections import defaultdict


def read_file():
    text_result = ''
    filename = 'original_text.txt'
    file = open(filename, 'r')
    for line in file:
        text_result += line
    text_result = ''.join(filter(str.isalpha, text_result.upper()))
    return text_result


def write_to_file(mode):
    if mode == 'e':
        file = open('encrypt_text.txt', 'w')
        file.write(encrypt_text)
    else:
        file = open('decrypt_text.txt', 'w')
        file.write(decrypt_text)
    file.close()


def encrypt_symbol(i):
    return alphabet[(alphabet.index(text[i]) + alphabet.index(key[(i + 1) % len(key)])) % len(alphabet)]


def Vigenere_encryption():
    encrypt_result = ''
    for i in range(0, len(text)):
        encrypt_result += encrypt_symbol(i)
    return encrypt_result


def decrypt_symbol(i):
    return alphabet[(alphabet.index(encrypt_text[i]) - alphabet.index(key[(i + 1) % len(key)])) % len(alphabet)]


def Vigenere_decryption():
    decrypt_result = ''
    for i in range(0, len(encrypt_text)):
        decrypt_result += decrypt_symbol(i)
    return decrypt_result


def Kasiski_method():
    lgramms = defaultdict(list)
    l = 3
    while l < 7:  # while l < len(encrypt_text)/2
        for i in range(0, len(encrypt_text) - l):
            str = ''
            j = i + l
            str += encrypt_text[i:j]
            if str in l_gramms:
                lgramms[str].append(i - lgramms.get(str)[-1])
            else:
                lgramms[str].append(i)
        l += 1
    return lgramms


def GCD(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors


def count_GCD():
    l_gramms_gcd = defaultdict(int)
    for l__key in l_gramms:
        if len(l_gramms[l__key]) != 1:
            for gcd_item in l_gramms[l__key]:
                divisors = GCD(gcd_item)
                for divisor in divisors:
                    if divisor > 3:
                        l_gramms_gcd[divisor] += 1
    print(sorted(l_gramms_gcd.items(), key=lambda x: x[1], reverse=True))


alphabet = 'А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я'
alphabet = alphabet.split(',')
text = read_file()

key = input('Input key: ')

encrypt_text = Vigenere_encryption()
write_to_file('e')

decrypt_text = Vigenere_decryption()
write_to_file('d')

l_gramms = defaultdict(list)
l_gramms = Kasiski_method()
count_GCD()
