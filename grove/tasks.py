import numpy as np

from datetime import timedelta

from grove.email_manager.email_sender import send_mail

from main import app

class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.name}: {self.description}"


class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def send_email(self, tsk: Task):
        
        print(f"Sending email to {self} with Task: {tsk}")
        return send_mail(
            self.email, "GroveHouse - " + tsk.name, tsk.description
        )

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return self.__str__()




CLEANING_TASKS = [
    Task("Limpeza", "Esta semana fazer a limpeza do WC superior"),
    Task("Limpeza", "Esta semana fazer a limpeza do WC inferior"),
    Task("Limpeza", "Esta semana fazer a limpeza das escadas"),
]

PERSONS = [
    Person("Paulo", "paulo_5_cesar@hotmail.com"),
    Person("Carlos", "carlos.moreira12@hotmail.com"),
    Person("Bruno", "bruno.miguel19995@gmail.com"),
    Person("Diogo", "diogosilv30@gmail.com"),
]


def load(filename="grove/core/list.txt"):
    return list(np.loadtxt(filename, dtype="str", delimiter=","))


def sort():
    # Load file
    target = load()
    # Make lowercase
    target = [el.lower() for el in target]
    # Create empty list of size 'target'
    new_list = [None] * len(target)
    for person in PERSONS:
        new_list[target.index(person.name.lower())] = person

    return new_list


def push_list_forward(lst, filename="grove/core/list.txt"):
    lst = lst[-1:] + lst[:-1]
    np.savetxt(filename, lst, fmt="%s")


@app.task
def cleaning():
    push_list_forward(load())
    persons = sort()
    for i, task in enumerate(CLEANING_TASKS):
        if task is not None:
            persons[i].send_email(task) 


    

@app.task
def warn_tuition_fees():
    # Create task for everyone and send email
    [p.send_email(Task("Propinas", "Não te esqueças de pagar as propinas até ao final do mês")) for p in PERSONS]


@app.task
def send_light_mileage():
    # Send email to 'Diogo' about eletricity 
    [p.send_email(Task("Contagem luz", "Não te esqueças de enviar a contagem da luz até amanhã")) for p in PERSONS if p.name.lower()=="diogo"]

@app.task
def send_internet_money():
    # Send email about giving money to Bruno (internet)
    [p.send_email(Task("Pagar internet", "Não te esqueças de enviar 9,08€ ao Bruno")) for p in PERSONS if p.name.lower()!="bruno"]


@app.task
def test():
    [p.send_email(Task("TESTE ", "test")) for p in PERSONS if p.name.lower()=="bruno"]



