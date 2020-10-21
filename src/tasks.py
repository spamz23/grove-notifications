import numpy as np
import schedule
import time


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
        self.tasks = []

    def add_task(self, tsk: Task):
        self.tasks.append(tsk)

    def send_email(self):
        return self

    def __str__(self):
        return f"{self.name} ({self.email}) with tasks: {self.tasks}"
    def __repr__(self):
        return self.__str__()

    def clean_tasks(self):
        self.tasks=[]
        return self
TASKS = [Task("WC-CIMA", "limpar wc"), Task("escadas", "dwdqw"), Task("nova task", "323")]

PERSONS = [
    Person("Paulo", "paulo_5_cesar@hotmail.com"),
    Person("Carlos", "carlos.moreira12@hotmail.com"),
    Person("Bruno", "bruno.miguel19995@gmail.com"),
    Person("Diogo", "diogosilv30@gmail.com"),
]



def load(filename="list.txt"):
    return list(np.loadtxt(filename, dtype="str", delimiter=","))

def sort():
    # Load file
    target=load()
    # Make lowercase
    target=[el.lower() for el in target]
    # Create empty list of size 'target'
    new_list=[None] * len(target)
    for person in PERSONS:
        new_list[target.index(person.name.lower())]=person

    return new_list


def push_list_forward(lst, filename="list.txt"):
    
    lst=lst[-1:] + lst[:-1]
    np.savetxt("list.txt", lst, fmt="%s")


def task():
    push_list_forward(load())
    persons=sort()
    for i, task in enumerate(TASKS):
        persons[i].add_task(task)

    notified_persons=[person.send_email() for person in persons if len(person.tasks)!=0]
    print("Sent email to:", notified_persons)
    PERSONS=[p.clean_tasks() for p in persons]


task()

schedule.every(5).seconds.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)
