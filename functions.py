import random
import string

def generate_random_string():
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(6))

print(generate_random_string())
