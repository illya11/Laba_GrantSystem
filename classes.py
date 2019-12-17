class User:
    def __init__ (self, name, login, password):
        self.__name = name
        self.__login = login
        self.__password = password
    
    @property
    def name (self):
        return self.__name
    
    def enter(self, login, password):
        if (login==self.__login and password == self.__password):
            return True
        else:
            return False
        
class Admin (User):
    def __init__ (self, name, login, password):
        User.__init__(self, name, login, password)

class Client (User):
    def __init__ (self, name, login, password):
        User.__init__(self, name, login, password)
    
    def __str__ (self):
        return (self.name)

class Project:
    def __init__ (self, author, name, summ, expertMark):
        self.__author = author
        self.__name = name
        self.__summ = summ
        self.__expertMark = expertMark
    
    @property
    def author (self):
        return self.__author
    
    @property
    def name (self):
        return self.__name
    
    @property
    def summ (self):
        return self.__summ
    
    @summ.setter
    def summ (self, summ):
        self.__summ = summ
        
    @property
    def expertMark (self):
        return self.__expertMark
    
    def __str__ (self):
        return ("Имя проекта: {} \nСоздатель проекта: {} \nСумма проекта: {} \nОценка экспертов: {} \n".format(self.__name, self.__author, self.__summ, self.__expertMark))


        