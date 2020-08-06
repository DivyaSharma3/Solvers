import numpy as np
import re

def get_string(filename):

  file = open(filename,'r')
  text = file.read(10000000)

  return text


def get_incidence(string):

  letters = "abcdefghijklmnopqrstuvwxyz"
  occurrences = [ len(re.findall(char, string)) for char in letters ]

  return occurrences

def frequency_vector(incidence_vector):

  total_chars = np.sum(incidence_vector)
  freq_vector = [ iv / total_chars for iv in incidence_vector]

  return freq_vector

def cosine(vector1, vector2):

  dotProd = np.dot(vector1, vector2)
  magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
  cos = dotProd / magnitude

  return cos

def rot(string, shift):

  # Applies a rotational shift (Caesar cipher) to a string

  letters = 26
  result = ""

  for c in string:
    # Convert character to number with ord.
    new = ord(c)

    # Check if new is between a-z or A-Z
    if (new >=  ord('a') and new <= ord('z')):
      start = ord('a')

    elif (new >= ord('A') and new <= ord('Z')):
      start = ord('A')

    # If it isn't a letter, just add it without changing it
    else:
      result += chr(new)
      continue

    # Apply the shift to the letter
    old_difference = new - start
    new_difference = (old_difference + shift) % letters
    new = start + new_difference

    # chr() returns the character associated with a Unicode value. Opposite of ord().
    result += chr(new)

  return result

def compare_rotated_frequencies(fn_encrypt, fn_reference):

    result    = np.zeros(26)
    encrypted = get_string(fn_encrypt)
    reference = get_string(fn_reference)

    freq_reference = frequency_vector(get_incidence(reference))

    for i in range(26):

        new_text = rot(encrypted, i)
        new_frequency = frequency_vector(get_incidence(new_text))
        result[i] = cosine(new_frequency, freq_reference)

    return result

def get_shift(cosine_array):
    return(np.argmax(cosine_array))

if __name__ == "__main__":

  result = compare_rotated_frequencies("Test.txt", "TestReference.txt")
  shift  = get_shift(result)
  print(rot(get_string("Test.txt"), shift))
