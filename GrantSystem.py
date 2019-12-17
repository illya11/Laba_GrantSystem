import classes
import telebot
import time

token = "906442663:AAFmPyIfbU9kk3oO5mQVATqG8528fUsxjLM"

users = []
projects = []
minSum = 4
grantFond = 13000
currentUser = None
#adminLoggedIn = False

admin = classes.Admin('admin','admin','admin')

currentUsers = []

def is_admin (tel_id):
    for user_id, role, user in currentUsers:
        if (tel_id == user_id and role == 'admin'):
            return True
    return False

def is_user (tel_id):
    for user_id, role, user in currentUsers:
        if (tel_id == user_id and role == 'user'):
            return True
    return False

def addCurrentUser (user_id, role, login, password):
    if role == 'user':
        user = findUser (login, password)
        currentUsers.append((user_id, role, user))
    elif role == 'admin':
        user = admin
        currentUsers.append((user_id, role, user))

def delCurrentUser (tel_id):
    for user_id, role, user in currentUsers:
        if (tel_id == user_id):
            currentUsers.remove((user_id, role, user))
            return True
    return False

def getCurrentUser (tel_id):
    for user_id, role, user in currentUsers:
        if (tel_id == user_id and role == 'user'):
            return user
    return None


def addUser (name, login, password):
    users.append(classes.Client(name, login, password))

def findUser (login, password):
    for user in users:
        if user.enter(login, password) == True:
            return user
    return False

def addProject (user, prjName, prjSum, expertMark):
    projects.append(classes.Project(user, prjName, prjSum, expertMark))

def showProjects ():
    result = ''
    for project in projects:
        result += str(project) + '\n'
    return (result)

def generateResult():
    totalsum = 0
    for prj in projects:
        totalsum += prj.summ
    
    if totalsum > grantFond:
        results = 'Результаты:'
        totalsum = grantFond
        marks = []
        for prj in projects:
            if prj.expertMark not in marks:
                marks.append(prj.expertMark)
        while totalsum > 0:
            max_mark = max(marks)
            for prj in projects:
                if prj.expertMark == max_mark:
                    prj.summ = min (prj.summ, totalsum)
                    totalsum -= prj.summ
                    results += '\n' + str(prj)
            marks.remove(max_mark)
    else:
        results = ('Все проекты получили свои гранты!')
    return results
            

addUser ('Иван', 'i.van', '123')
addUser ('Катя', 'kate', 'qwerty')
addUser ('Игорь', 'i.gor', 'qwerty123')

currentUser = findUser('i.van', '123')
addProject (currentUser, 'Chess', 2000, 4)

currentUser = findUser('kate', 'qwerty')
addProject (currentUser, 'GreenHouse', 9000, 10)

currentUser = findUser('i.gor', 'qwerty123')
addProject (currentUser, 'NotePad++', 3000, 6)


login = ''
password = ''

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для работы с ботом необходимо авторизироватся.\nВыполни команду /login')

@bot.message_handler(commands=['login'])
def login_msg(message):
    bot.send_message(message.chat.id, 'Введите свой логин:')
    bot.register_next_step_handler(message, get_login)

def get_login(message):
    global login
    login = message.text
    bot.send_message(message.chat.id, 'Введите свой пароль:')
    bot.register_next_step_handler(message, get_pass)
    
def get_pass(message):
    global login
    global password
    #global adminLoggedIn
    global currentUser
    password = message.text
    if login == 'admin' and password == 'admin':
        addCurrentUser (message.chat.id, 'admin', login, password)
        #adminLoggedIn = True
        msg  = 'Добро пожаловать!\n'
        msg += 'В рамках управления проектами, вы можете выполнить следующие комманды:\n'
        msg += '/addUser - для добавления нового пользователя в базу\n'
        msg += '/showProjects - для отображения всех заявок по проектам\n'
        msg += '/setGrantFond - для установки новой суммы гранта\n'
        msg += '/generateResult - для формирования списка победителей\n'
        msg += '/logout - для выхода из учетной записи'
        bot.send_message(message.chat.id, msg)
    elif findUser (login, password) != False:
        addCurrentUser (message.chat.id, 'user', login, password)
        currentUser = findUser (login, password)
        msg  = 'Приветствую, ' + str(currentUser) + '!\n'
        msg += 'В рамках работы с проектами, вы можете выполнить следующие комманды:\n'
        msg += '/addProject - для подачи своего проекта\n'
        msg += '/logout - для выхода из учетной записи'
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, 'К сожалению, запись с таким логином и паролем не найдена. Попробуйте еще раз.')

@bot.message_handler(commands=['addProject'])
def addProject_msg(message):
    global currentUser
    currentUser = getCurrentUser (message.chat.id)
    if (currentUser != None):
        bot.send_message(message.chat.id, 'Введите имя проекта:')
        bot.register_next_step_handler(message, PrjName_msg)
    else:
        bot.send_message(message.chat.id, 'Необходимо войти, чтоб добавить свой проект.')

PrjName = ''
PrjSum = 0
PrjMark = 0

def PrjName_msg(message):
    global PrjName
    PrjName = message.text
    bot.send_message(message.chat.id, 'Введите сумму проекта:')
    bot.register_next_step_handler(message, PrjSum_msg)

def PrjSum_msg(message):
    global PrjSum
    PrjSum = int(message.text)
    bot.send_message(message.chat.id, 'Введите оценку проекта:')
    bot.register_next_step_handler(message, PrjMark_msg)

def PrjMark_msg(message):
    global PrjName
    global PrjSum
    global PrjMark
    PrjMark = int(message.text)
    if (PrjMark >= minSum):
        addProject (getCurrentUser (message.chat.id), PrjName, PrjSum, PrjMark)
        bot.send_message(message.chat.id, 'Проект добавлено!')
    else:
        bot.send_message(message.chat.id, 'К сожалению, у проекта очень низкая оценка, мы не можем его добавить.')
    PrjName = ''
    PrjSum = ''
    PrjMark = '' 
      
@bot.message_handler(commands=['showProjects'])
def showProjects_msg(message):
    if (is_admin(message.chat.id)):
        bot.send_message(message.chat.id, showProjects())
    else:
        bot.send_message(message.chat.id, 'Только у администратора есть доступ к списку проектов.')

@bot.message_handler(commands=['setGrantFond'])
def setGrantFond_msg(message):
    if (is_admin(message.chat.id)):
        bot.send_message(message.chat.id, 'Введите новую сумму гранта')
        bot.register_next_step_handler(message, setGrant)
    else:
        bot.send_message(message.chat.id, 'Только у администратора есть доступ к этой команде.')

def setGrant (message):
    global grantFond
    grantFond = int(message.text)
    bot.send_message(message.chat.id, 'Сумма изменена.')

@bot.message_handler(commands=['addUser'])
def addUser_msg(message):
    if (is_admin(message.chat.id)):
        bot.send_message(message.chat.id, 'Введите имя пользователя:')
        bot.register_next_step_handler(message, userName_msg)
    else:
        bot.send_message(message.chat.id, 'Только у администратора есть доступ к этой команде.')

userName = ''
userLogin = ''
userPass = ''

def userName_msg(message):
    global userName
    userName = message.text
    bot.send_message(message.chat.id, 'Введите логин:')
    bot.register_next_step_handler(message, userLogin_msg)

def userLogin_msg(message):
    global userLogin
    userLogin = message.text
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, userPass_msg)

def userPass_msg(message):
    global userName
    global userLogin
    global userPass
    userPass = message.text
    addUser (userName, userLogin, userPass)
    bot.send_message(message.chat.id, 'Пользователя добавлено!')
    userName = ''
    userLogin = ''
    userPass = ''

@bot.message_handler(commands=['generateResult'])
def generateResult_msg(message):
    if (is_admin(message.chat.id)):
        bot.send_message(message.chat.id, generateResult())
    else:
        bot.send_message(message.chat.id, 'Только у администратора есть доступ к этой команде.')

"""
@bot.message_handler(commands=['logout'])
def logout_msg(message):
    global currentUser
    global adminLoggedIn
    global login
    global password
    currentUser = None
    adminLoggedIn = False
    login = ''
    password = ''
    bot.send_message(message.chat.id, 'Вы успешно вышли из своей записи.')
"""
@bot.message_handler(commands=['logout'])
def logout_msg(message):
    if (delCurrentUser (message.chat.id)):
        bot.send_message(message.chat.id, 'Вы успешно вышли из своей записи.')
    else:
        bot.send_message(message.chat.id, 'Что то пошло не так:(')

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print ('Found exception:')
        print(e)
        time.sleep(15)




