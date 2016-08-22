import re


# Text related fixings

def fix_ellipsis(text):
    fixed_text = re.sub(r'([.,;?!])([^\W\d_])', r'\1 \2', text, flags=re.UNICODE)
    fixed_text = re.sub(r'([^\.])(\.\.) ', r'\1... ', fixed_text, flags=re.UNICODE)
    return re.sub(r'([^\.])(\.\.\.\.+) ', r'\1... ', fixed_text, flags=re.UNICODE)


# Word related fixings

def remove_repeated_letters(word):
    # Do not remove repeated letters only if letters are r, s, m, n or c
    regex = r'([^\W\drsmnc])\1+'
    return re.sub(regex, r'\1', word, re.UNICODE)
