""" This modules defines all the periodic tasks running in the server"""

import datetime

from grove.email_manager.email_sender import send_mail

from main import app, redis_sv


class Task:
    """
    This class defines a task that should be performed
    by a house member
    """

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.name}: {self.description}"


class Person:
    """This class defines a person living in Grove House"""

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def send_email(self, tsk: Task):
        """Sends an email informing a person of a certain task

        Parameters
        ----------
        tsk: Task
            The task to notify person with
        """
        print(f"Sending email to {self} with Task: {tsk}")
        send_mail(self.email, "GroveHouse - " + tsk.name, tsk.description)

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return self.__str__()


CLEANING_TASKS = [
    Task("Limpeza", "Esta semana fazer a limpeza do WC superior"),
    Task("Limpeza", "Esta semana fazer a limpeza do WC inferior"),
    Task("Limpeza", "Esta semana fazer a limpeza da cozinha e das escadas"),
]

PERSONS = [
    Person("Paulo", "paulocosta15896@gmail.com"),
    Person("Carlos", "diogomdgomes@gmail.com"),
    Person("Bruno", "bruno.miguel19995@gmail.com"),
    Person("Diogo", "diogosilv30@gmail.com"),
]


def _load():
    """Loads a file holding the persons list order for the cleaning tasks"""
    # Try to get from redis
    lst_str = redis_sv.get("people")
    if lst_str is None:
        return ["Carlos", "Paulo", "Diogo", "Bruno"]
    # Convert bytes to str, and split string into a list
    return lst_str.decode("utf-8").split(";")


def _sort():
    """Sorts 'PERSONS' according to persons order in the file obtained by `_load`"""

    # Load file
    target = _load()
    # Make lowercase
    target = [el.lower() for el in target]
    # Create empty list of size 'target'
    new_list = [None] * len(target)
    for person in PERSONS:
        new_list[target.index(person.name.lower())] = person

    return new_list


def _push_list_forward(lst):
    """
    Makes the last element of a list the first one,
    moving every element a position foward. Then saves the list in redis server.
    """
    # push forward
    lst = lst[-1:] + lst[:-1]
    # save in redis
    redis_sv.set("people", ";".join(lst))


@app.task
def cleaning():
    """
    Periodic task to inform everyone about their weekly cleaning tasks
    """
    _push_list_forward(_load())
    persons = _sort()
    for i, task in enumerate(CLEANING_TASKS):
        persons[i].send_email(task)


@app.task
def warn_tuition_fees():
    """
    Periodic task to remind everyone to pay the monthly tuition fees
    """
    # Create task for everyone and send email
    [
        p.send_email(
            Task("Propinas", "Não te esqueças de pagar as propinas até ao final do mês")
        )
        for p in PERSONS
    ]


@app.task
def send_light_mileage():
    """
    Periodic task to remind 'Diogo' about sending the eletric mileage to eletrical supplier
    """
    [
        p.send_email(
            Task(
                "Contagem luz", "Não te esqueças de enviar a contagem da luz até amanhã"
            )
        )
        for p in PERSONS
        if p.name.lower() == "diogo"
    ]


@app.task
def send_internet_money():
    """
    Periodic task to remind everyone to pay the internet bill. (Send money to 'Bruno')
    """
    # Send email about giving money to 'Bruno' (internet)
    [
        p.send_email(Task("Pagar internet", "Não te esqueças de enviar 9,73€ ao Bruno"))
        for p in PERSONS
        if p.name.lower() != "bruno"
    ]


@app.task
def cleaning_lady():
    """
    Periodic task to remind everyone that the cleaning lady comes the next day
    """

    if ((datetime.date.today().isocalendar()[1]) % 2) != 0:

        # Send email
        [
            p.send_email(
                Task(
                    "Limpeza Cátia",
                    "Não te esqueças que amanhã a Cátia vem limpar a casa",
                )
            )
            for p in PERSONS
        ]


@app.task
def pay_the_rent():
    """
    Periodic task to remind everyone to pay the rent until the next day
    """
    [
        p.send_email(Task("Pagar Renda", "Não te esqueças de pagar a renda até amanhã"))
        for p in PERSONS
    ]
