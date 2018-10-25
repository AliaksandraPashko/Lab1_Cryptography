from collections import defaultdict
from matplotlib import pyplot
from scipy.stats import chisquare

rus_freq = {
    'А': 0.07821,
    'Б': 0.01732,
    'В': 0.04491,
    'Г': 0.01698,
    'Д': 0.03103,
    'Е': 0.08567,
    'Ё': 0.0007,
    'Ж': 0.01082,
    'З': 0.01647,
    'И': 0.06777,
    'Й': 0.01041,
    'К': 0.03215,
    'Л': 0.04813,
    'М': 0.03139,
    'Н': 0.0685,
    'О': 0.11394,
    'П': 0.02754,
    'Р': 0.04234,
    'С': 0.05382,
    'Т': 0.06443,
    'У': 0.02882,
    'Ф': 0.00132,
    'Х': 0.00833,
    'Ц': 0.00333,
    'Ч': 0.01645,
    'Ш': 0.00775,
    'Щ': 0.00331,
    'Ъ': 0.00023,
    'Ы': 0.01854,
    'Ь': 0.02106,
    'Э': 0.0031,
    'Ю': 0.00544,
    'Я': 0.01979,
}
lang_freq = defaultdict(float, rus_freq)
template_freq = defaultdict(float)


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


def encrypt_symbol(i, encrypt_key):
    return alphabet[(alphabet.index(text[i]) + alphabet.index(encrypt_key[(i + 1) % len(encrypt_key)])) % len(alphabet)]


def Vigenere_encryption(encrypt_key):
    encrypt_result = ''
    for i in range(0, len(text)):
        encrypt_result += encrypt_symbol(i, encrypt_key)
    return encrypt_result


def decrypt_symbol(i, decrypt_key):
    return alphabet[(alphabet.index(encrypt_text[i]) - alphabet.index([(i + 1) % len(decrypt_key)])) % len(alphabet)]


def Vigenere_decryption(decrypt_key):
    decrypt_result = ''
    for i in range(0, len(encrypt_text)):
        decrypt_result += decrypt_symbol(i, decrypt_key)
    return decrypt_result


def Kasiski_method():
    lgramms = defaultdict(list)
    l = 4
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


def GCD(x, y):
    gcd_value = 0
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if (x % i == 0) and (y % i == 0):
            gcd_value = i
    return gcd_value


def count_GCD():
    l_gramms_gcd_ = defaultdict(int)
    for l__key in l_gramms:
        if len(l_gramms[l__key]) != 1:
            for i in range(0, len(l_gramms[l__key]) - 1):
                gcd = GCD(l_gramms[l__key][i], l_gramms[l__key][i + 1])
                if gcd > 3:
                    l_gramms_gcd_[gcd] += 1
    print(sorted(l_gramms_gcd_.items(), key=lambda x: x[1], reverse=True))
    return l_gramms_gcd_


def count_template_frequency():
    temp_freq = defaultdict(int)
    for letter in encrypt_text:
        temp_freq[letter] += 1
    for key in lang_freq:
        template_freq[key] = temp_freq[key] / len(encrypt_text)


def shift(freq, j):
    return list(freq.values())[j:] + list(freq.values())[:j]


def chi_square():
    chis = [chisquare(shift(template_freq, i), list(lang_freq.values())).statistic for i in range(0, len(alphabet))]
    return chis.index(min(chis))


if __name__ == '__main__':
    alphabet = 'А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я'
    alphabet = alphabet.split(',')
    text = read_file()

    key = input('Input key: ')

    encrypt_text = Vigenere_encryption(key)
    write_to_file('e')

    decrypt_text = Vigenere_decryption(key)
    write_to_file('d')

    l_gramms = defaultdict(list)
    l_gramms = Kasiski_method()

    l_gramms_gcd = count_GCD()

    lists = sorted(l_gramms_gcd.items())
    x, y = zip(*lists)
    pyplot.plot(x, y)
    pyplot.show()
    count_template_frequency()

    key_shift = chi_square()
    key_length_variant = input('Input key length: ')
    shift(template_freq, key_length_variant)

