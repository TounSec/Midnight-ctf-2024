import random

def encrypt(l, s):
  random.seed(s)
  t = list(l)
  random.shuffle(t)
  return t

def decrypt(l, s):
  random.seed(s)
  r = list(range(len(l)))
  random.shuffle(r)
  a = [0] * len(l)
  for i, x in zip(r, l): 
    a[i] = x
  return a


t = [1,2,3,4,5,6,7,8]
t = encrypt(t, 123)
print(t)
t = decrypt(t, 123)
print(t)