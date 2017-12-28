from django.test import TestCase

# Create your tests here.
l = [10,11,8,12]
# def func(x):
#     return x>10
# print(list(filter(func,l)))
# print(list(filter(lambda x:x>10,l)))


t1 = (('a'),('b'))
t2 = (('c'),('d'))
print(list(zip(t1,t2)))
c=lambda t:{t[0]:t[1]}
d=map(c,zip(t1,t2))
print (list(d))



print(list(map(lambda t:{t[0],t[1]},zip(t1,t2))))