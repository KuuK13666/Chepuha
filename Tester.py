from typing import Callable



def limmiter( lim:int ):
    def wapper(func:Callable):
        def inner(*args, **kwargs):
            nonlocal lim
            if lim==0:
                return'Eror'
            else:
                res=3*func(*args,**kwargs)
                lim-=1
            return res
        return inner
    return wapper
@limmiter(6)
def funtic(a):
    return 'hui'


def Deco(func:Callable):
    def wrapper():
        res=func()
        print('SOSI')
        return res
    return wrapper
@Deco
def Fr():
    return 'hui'
@Deco
def F():
    return '123'

print('deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable'=='deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable')
#print(Fr())
#print(F())
for i in range(10):
    print(funtic(3)+' '+str(i+1))