from time import time


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print('Time working is: ', round(t2-t1, 10))
        return result
    return wrapper


class Website2:
    domain = 'google222222.com'

    def __init__(self):
        self.domain = '222222.com'
        self.pages_count = 1000000000000
        self.is_nice = True

    def __str__(self):
        return f'Website2: {self.domain}'

    def my_page(self, login):
        return f'https://{self.domain}/{login}'

    @property
    def length(self):
        return len(self.my_page('asdadsasdad'))

    @staticmethod
    def show_h1():
        return len('asdadsasdad')

    @classmethod
    def show_h2(cls):
        return 'H2:asdadsasdad'


class Website1:
    domain = 'google111111.com'

    def __init__(self):
        self.domain = '111111.com'
        self.pages_count = 1000000000000
        self.is_nice = True

    def __str__(self):
        return f'Website1: {self.domain}'

    def my_page(self, login):
        return f'https://{self.domain}/{login}'


class WebPage(Website2, Website1):
    html_size = 100

    def __init__(self):
        self.html_h1 = 'blablabla'
        self.html_title = '123123123'
        super().__init__()

    @property
    @timer
    def length(self):
        return len(self.my_page('111111111111111'))


@timer
def my_print():
    for i in range(10000):
        print(i)


my_web_page = WebPage()

# url = my_web_page.my_page('sergei4e')

print(my_web_page.length)


# my_print()
