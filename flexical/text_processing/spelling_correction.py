import re


# Text related fixings

def fix_ellipsis(text):
    fixed_text = re.sub(r'([.,;?!])([^\W\d_])', r'\1 \2', text, flags=re.UNICODE)
    fixed_text = re.sub(r'([^\.])\.\.([^\.])', r'\1...\2', fixed_text, flags=re.UNICODE)
    return re.sub(r'([^\.])\.\.\.\.+([^\.])', r'\1...\2', fixed_text, flags=re.UNICODE)


# Word related fixings

def remove_repeated_letters(word):
    # Do not remove repeated letters only if letters are r, s, m, n, c or z
    no_repeat_regex = r'([^\W\drsmnczf])\1+'
    word = re.sub(no_repeat_regex, r'\1', word, re.UNICODE)

    one_repeat_regex = r'([drsmnczf])\1\1+'
    word = re.sub(one_repeat_regex, r'\1\1', word, re.UNICODE)

    return word
