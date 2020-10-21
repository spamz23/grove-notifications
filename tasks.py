import numpy as np
import collections

def load_list():
    return np.loadtxt("lista.txt", dtype="str", delimiter=",")

def update_list(lst):
    lst = list(lst)
    return lst[-1:] + lst[:-1]

def save_list(lst):
    np.savetxt("lista.txt", lst, fmt="%s")

def send_email(person:Person):
    ...

def get_person_wc(lst):
    return [t for t in person_list if t.name.lower() == lst[0].lower()][0]

def get_person_stairs(lst):
    return [t for t in person_list if t.name.lower() == lst[1].lower()][0]


def task():
    #fazer load da lista para ver a ordem atual
    lst = load_list()
    #alterar a lista para a nova ordem
    lst = update_list(lst)
    #salvar a lista na nova ordem para na proxima semana ser carregada para novos emails
    save_list(lst)
    # obter a quem enviar email e o que vai fazer
    person_wc = get_person_wc(lst)
    person_stairs = get_person_stairs(lst)
    # Send email


Person = collections.namedtuple('Person', ['name', 'email']) 
Paulo = Person('Paulo', 'paulo_5_cesar@hotmail.com') 
Carlos = Person('Carlos', 'carlos.moreira12@hotmail.com') 
Bruno = Person('Bruno', 'bruno.miguel19995@gmail.com') 
Diogo = Person('Diogo', 'diogosilv30@gmail.com') 
person_list = [Paulo, Carlos, Bruno, Diogo]