import kivy
kivy.require('2.0.0')
import os
import gc
import weakref
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import psycopg2
from kivy.config import Config
from database import connectDB
from functools import partial
from kivy.core.window import Window


# Config.set('graphics', 'width', '600')
# Config.set('graphics', 'height', '400')


#region MISCELANIOUS FUNCTIONS AND VARIABLES

#region Messages
invalidRegister = 'Please fill in all inputs with valid information.'
invalidUserPass = 'User and/or Password incorrect.'
error = 'Some weird error ocurred, please try again.'
registerSuccess = 'Account created successfully.'
loginSuccess = 'You have successfully loged in.'
existEmail = 'Email alredy exist.'
existUser = 'Username alredy exist.'
logged = ['not logged' , None]
lessonsCounterBoxes = 0
lessonTopic = ""
globalLessonNumber = 1

info = {
    'ger_nouns': {
        '1': [
            ['País', 'Das Land'], ['Región', 'Die Region'],
            ['Provincia', 'Die Provinz'], ['Ciudad', 'Die Stadt'],
            ['Pueblo', 'Das Dorf'], ['Calle', 'Die Strasse'],
            ['Plaza', 'Der Platz'], ['Avenida', 'Die Allee'],
            ['Monumento', 'Das Denkmal'], ['Fuente', 'Die Quelle'],
            ['Aeropuerto', 'Der Flughafen'], ['Estación', 'Der Bahnhof'],
            ['Puerto', 'Der Hafen'], ['Metro', 'Die U-Bahn'],
            ['Parque', 'Der Park'], ['Aparcamiento', 'Der Parkplatz'],
            ['Hospital', 'Das Krankenhaus'], ['Panaderia', 'Die Bäckerei'],
            ['Cine', 'Das Kino'], ['Teatro', 'Das Theater'],
            ['Restaurante', 'Das Restaurant'], ['Tienda', 'Das Geschäft']
        ],
        '2': [
            ['Casa', 'Das Haus'], ['Puerta', 'Die Tür'],
            ['Ventana', 'Das Fenster'], ['Pared', 'Die Wand'],
            ['Suelo', 'Der Boden'], ['Techo', 'Die Zimmerdecke'],
            ['Tejado', 'Das Dach'], ['Chimenea', 'Der Schornstein'],
            ['Balcón', 'Der Balkon'], ['Pasillo', 'Der Flur']
            
        ],
        '3': [
            ['Salón', 'Das Wohnzimmer'], ['Comedor', 'Das Esszimmer'],
            ['Dormitorio', 'Das Schlafzimmer'], ['Baño', 'Das Badezimmer'],
            ['Despacho', 'Das Arbeitszimmer'], ['Escalera', 'Die Treppe'],
            ['Garaje', 'Die Garage'], ['Cocina', 'Die Küche'],
            ['Jardín', 'Der Garten'], ['Patio', 'Der Hinterhof']
        ],
        '4': [
            ['Padre', 'Der Vater'], ['Madre', 'Die Mutter'],
            ['Hermano', 'Der Bruder'], ['Hermana', 'Die Schwester'],
            ['Hijo', 'Der Sohn'], ['Hija', 'Die Tochter'],
            ['Hijos', 'Die Kinder'], ['Padres', 'Die Eltern'],
            ['Hermanos', 'Die Geschwister'], ['Familia', 'Die Familie'],
            ['Primo/a', 'Der Cousin'], ['Nieto', 'Der Enkel'],
            ['Nieta', 'Die Enkelin'], ['Abuelo', 'Der Großvater'],
            ['Abuela', 'Die Großmutter'], ['Familiares', 'Die Vertrauten']
        ],
        '5': [
            ['Perro', 'Der Hund'], ['Gato', 'Die Katze'],
            ['Caballo', 'Das Pferd'], ['Cerdo', 'Das Schwein'],
            ['Raton', 'Die Maus'], ['Abeja', 'Die Biene'],
            ['Pescado', 'Dr Disch'], ['Pajaro', 'Der Vogel'],
            ['Animal', 'Das Tier'], ['Mascota', 'Das Haustier']
        ],
        '6': [
            ['Vehiculo', 'Das Fahrzeug'], ['Cosa', 'Zeug'],
            ['Encendedor', 'Feuerzeug'], ['Juguete', 'Das Spielzeug'],
            ['Tejido', 'Das Strickzeug'], ['Herramienta', 'Das Wekzeug'],
            ['Tambores', 'Das Schlagzeug'], ['Utensilios de escritura', 'Das Schreibzeug'],
            ['Traje de Baño', 'Das Badezeug'], ['La cosa verde', 'Das Grünzeug']
        ],
        '7': [
            ['Pan', 'Das Brot'], ['Pizza', 'Die Pizza'],
            ['Azucar', 'Der Zucker'], ['Sal', 'Das Salz'],
            ['Carne', 'Das Fleisch'], ['Hamburguesa', 'Der hamburger'],
            ['Tomate', 'Die Tomate'], ['Patata', 'Die Kartoffel'],
            ['Lechuga', 'Der Salat'], ['Fideos', 'Die Nudeln'],
            ['Arroz', 'Der Reis'], ['Agua', 'Das Wasser'],
            ['Jugo', 'Der Saft'], ['Jugo de Manzana', 'Der Apfelsaft'],
            ['Cerveza', 'Das Bier'], ['Vino', 'Der Wein'],
            ['Té', 'Der Tee'], ['Café', 'Der Kaffee']
        ],
        '8': [
            ['Vehículo', 'Das Fahrzeug'], ['Avión', 'Das Flugzeug'],
            ['Auto', 'Das Auto'], ['Camión', 'Der Lastwagen'],
            ['Camioneta', 'Der Truck'], ['Bus', 'Der Bus'],
            ['Trén', 'Der Zug'], ['Barco', 'Das Schiff'],
            ['Bicicleta', 'Das Fahrrad'], ['Motocicleta', 'Das Motorrad'],
            ['Scooter', 'Der Roller'], ['Moto', 'Das Moto'],
            ['Metro', 'Der U-Bahn'], ['Taxi', 'Das Taxi']
        ]
    },
    'ger_verbs': {
        '1': [
            ['Teclar', 'Schlüssel'], ['Saludar', 'Grüßen'],
            ['Programar', 'Programm'], ['Trabajar', 'Arbeiten']
        ],
        '2': [
            ['Comer', 'Essen'], ['Cocinar', 'Kochen'],
            ['Limpiar', 'Aufräumen'], ['Cortar', 'Schneiden'],
            ['Poner', 'Einstellen'], ['Agarrar', 'Greifen'],
            ['Soltar', 'Veröffentlichung'], ['Traer', 'Bringen'],
            ['Calentar', 'Wärmen'], ['Cocer', 'Aufkochen']
        ],
        '3': [
            ['Subir', 'Steig'], ['Bajar', 'Raus'],
            ['Viajar', 'Reisen'], ['Esperar', 'Warten'],
            ['Caminar/Ir', 'Gehen'], ['Correr', 'Laufen'],
            ['Conducir', 'Führen'], ['Moverse', 'Bewegung']
        ],
        '4': [
            ['Comprar', 'Kaufen'], ['Yo compro', 'Ich Kaufe'],
            ['Tu compras', 'Du Kaufst'], ['El compra', 'Er Kauft'],
            ['Nosotros compramos', 'Wir Kaufen'], ['Ustedes compran', 'Ihr Kaufst'],
            ['Ellos compran', 'Sie Kaufen'], ['Vender', 'Verkaufen'],
            ['Yo vendo', 'Ich Verkaufe'], ['Tu vendes', 'Verkaufst'],
            ['El vende', 'Er Verkauft'], ['Nosotros vendemos', 'Wir Verkaufen'],
             ['Ustedes Venden', 'Ihr Verkaufst'], ['Ellos venden', 'Sie Verkaufen']
        ]
    },
    'ger_pronouns': {
        '1': [
            ['Yo', 'Ich'], ['Tu o Usted', 'Du oder Sie'],
            ['El', 'Er'], ['Ella', 'Sie'],
            ['El/Ella neutro', 'Es'], ['Nosotros', 'Wir'],
            ['Ustedes', 'Ihr'], ['Ellos/Ellas', 'Sie']
        ],
        '2': [
            ['Mi(ich)', 'meine'], ['Tu(du)', 'deine'],
            ['Su(er)', 'seine'], ['Su(sie)', 'ihre'],
            ['Su(es)', 'seine'], ['Nuestro(wir)', 'unsere'],
            ['Vuestro(ihr)', 'eure'], ['Su(sie)', 'ihre'],
            ['Su(Sie)', 'ihre']
        ]
    }
}
lessons = [
    {'title':'Aleman-Sustantivos', 'section': 'ger_nouns', 'numbers': [
        'Lección 1: Localidades', 'Lección 2: Hogar 1',
        'Lección 3: Hogar 2', 'Lección 4: Familia',
        'Lección 5: Animales', 'Lección 6: Herramientas',
        'Lección 7: Alimentos', 'Lección 8: Vehiculos'
         ]},
    {'title':'Aleman-Verbos', 'section': 'ger_verbs', 'numbers': [
        'Lección 1: Trabajo', 'Lección 2: Comida',
        'Lección 3: Moverse', 'Lección 4: Comprar'
        ]},
    {'title':'Aleman-Pronombres', 'section': 'ger_pronouns', 'numbers': [
        'Lección 1: Personales', 'Lección 2: Posesivos Fem'
        ]}
]
#endregion

def systemMessage(message=None):
    if message!=None:
        pop = Popup(title='System Message',
                    content=Label(text=message),
                    size_hint=(None, None), size=(400, 250))
    else:
        pop = Popup(title='System Message',
                  content=Label(text="Something went wrong in the code...."),
                  size_hint=(None, None), size=(400, 250))

    pop.open()

def compareWords(word, correctWord, proximityIndex=0.7):
    wordToAnalize = list(word)
    rightWord = list(correctWord)
    hits = 0
    proximity_index = proximityIndex
    hits_factor = proximity_index*len(wordToAnalize)

    #Fill the smaller word with spaces
    if len(wordToAnalize)>len(rightWord):
        for i in range(len(wordToAnalize)-len(rightWord)):
            rightWord.append('')
                
    elif len(rightWord)>len(wordToAnalize):
        for i in range(len(rightWord)-len(wordToAnalize)):
            wordToAnalize.append('')

    #Compares letter to letter
    for i in range(len(rightWord)):
        if rightWord[i] == wordToAnalize[i]:
            hits = hits+1

    hits_factor = proximity_index*len(wordToAnalize)

    if hits > hits_factor:
        guess = True
    else:
        guess = False

    return guess


class MyLessonBox(GridLayout):
    
    def __init__(self, **kwargs):
        super(MyLessonBox, self).__init__(**kwargs)
        self.cols = 2
        self.add_buttons()

    def add_buttons(self):
        global lessonsCounterBoxes
        id_number = 0
        for lesson in lessons[lessonsCounterBoxes]['numbers']:
            button = Button(text=lesson)
            id_number += 1       
            button.bind(on_release=partial(self.go_btn, id_number))
            self.add_widget(button)   
        lessonsCounterBoxes += 1 

    def go_btn(self, number, *args):
        wm.switch_to(screens[5], direction="up")
        MyLabelText.add_label_text(MyLabelText, number)
        


class MyTitle(FloatLayout):
    instances = []
    
    def __init__(self, **kwargs):
        super(MyTitle, self).__init__(**kwargs)
        self.__class__.instances.append(weakref.proxy(self))
        self.add_title()
        # self.add_evaluation_info()

    def add_title(self):
        self.label = Label(text=f"Chapter {LessonScreen1.counter}", pos_hint={'top':1, 'x':0.1}, size_hint=(0.8, 0.7))
        self.add_widget(self.label)

    def delete_title(self):
        self.label = Label(text=f"Chapter {LessonScreen1.counter}", pos_hint={'top':1, 'x':0.1}, size_hint=(0.8, 1))
        self.remove_widget(self.label)



class MyLabelText(GridLayout):
    instances = []
    buttonInstances = []
    def __init__(self, **kwargs):
        super(MyLabelText, self).__init__(**kwargs)
        self.__class__.instances.append(weakref.proxy(self))
        self.cols = 4

    def add_label_text(self, lessonNumber, *args):
        global globalLessonNumber
        global lessonTopic
        #CLEAR ALL THE PREVIOUS LABELS AND TEXTINPUT
        for instance in self.instances:
            instance.clear_widgets()
        #SET lessonTopic FOR 'info'
        if globalLessonNumber == 1:
            lessonTopic = 'ger_nouns'
        elif globalLessonNumber == 2:
            lessonTopic = 'ger_verbs'
        elif globalLessonNumber == 3:
            lessonTopic = 'ger_pronouns'

        for instance in self.instances:
            i = 0
            for to_study in info[lessonTopic][str(lessonNumber)]:
                i += 1
                instance.add_widget(Button(text=to_study[0], disabled=True))
                text_input = TextInput(multiline=False, write_tab=False)
                instance.add_widget(text_input)

class MyEvaluation(FloatLayout):
    pass

#endregion
#region Register
class CreateAccount(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    email = ObjectProperty(None)

    def toLoginBtn(self):
        wm.current = "login"

    def registerBtn(self):
        connection = connectDB()
        try:
            connection.tableCreate()
        except:
            print("Table alredy created")
        duplicateUser = connection.validateDB(user=self.username.text)
        duplicateEmail = connection.validateDB(mail=self.email.text)
        conditionsToRegister = (len(self.username.text)<20 and len(self.password.text)<30
                            and self.email.text.count(".")>0 and self.email.text.count("@")>0)

        if conditionsToRegister and duplicateUser==False and duplicateEmail==False:
            try:
                connection.insertUser(self.username.text, self.email.text, self.password.text)
                systemMessage(registerSuccess)
                wm.current = "login"
            except:
                systemMessage(error)
        elif duplicateUser:
            systemMessage(existUser)
        elif duplicateEmail:
            systemMessage(existEmail)
        else:
            systemMessage(invalidRegister)
#endregion
#region Login
class LoginAccount(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def loginBtn(self):
        connection = connectDB()
        try:
            connection.tableCreate()
        except:
            print("Table alredy created")
        try:
            # connection.loginDB(passw=self.password.text, user=self.username.text)
            if connection.loginDB(passw=self.password.text, user=self.username.text):
                logged[0] = 'logged'
                logged[1] = connection.obtainID(user=self.username.text)
                systemMessage(loginSuccess)
                wm.current = 'lesson1'
            else:
                systemMessage(invalidUserPass)
                logged[0] = 'not logged'
                logged[1] = None

        except:
            systemMessage(error)
            logged[0] = 'not logged'
            logged[1] = None


    def toRegisterBtn(self):
        wm.current = "register"
#endregion

#region LessonScreen1
class LessonScreen1(Screen):
    counter = 1
    chapterNumber = 1

    def next(self):
        global globalLessonNumber
        self.counter = self.chapterNumber
        if self.counter<len(lessons)+1:
            try:
                self.counter += 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {self.counter}"
                wm.current = f"lesson{self.counter}"
                globalLessonNumber = self.counter
            except:
                pass
        else:
            pass

    def go_config(self):
        wm.current = 'config'


class LessonScreen2(Screen):
    chapterNumber = 2
    def next(self):
        global globalLessonNumber
        LessonScreen1.counter = self.chapterNumber
        if LessonScreen1.counter<len(lessons):
            try:
                LessonScreen1.counter += 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {LessonScreen1.counter}"
                wm.current = f"lesson{LessonScreen1.counter}"
                globalLessonNumber = LessonScreen1.counter
            except:
                pass
        else:
            pass

    def previous(self):
        global globalLessonNumber
        LessonScreen1.counter = self.chapterNumber
        if LessonScreen1.counter>=len(lessons):
            try:
                LessonScreen1.counter -= 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {LessonScreen1.counter}"
                wm.current = f"lesson{LessonScreen1.counter}"
                globalLessonNumber = LessonScreen1.counter

            except:
                pass
        elif LessonScreen1.counter>=len(lessons)-1:
            try:
                LessonScreen1.counter -= 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {LessonScreen1.counter}"
                wm.current = f"lesson{LessonScreen1.counter}"
                globalLessonNumber = LessonScreen1.counter
            except:
                pass
        else:
            pass

class LessonScreen3(Screen):
    chapterNumber = 3
    def next(self):
        global globalLessonNumber
        LessonScreen1.counter = self.chapterNumber
        if LessonScreen1.counter<len(lessons):
            try:
                LessonScreen1.counter += 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {LessonScreen1.counter}"
                wm.current = f"lesson{LessonScreen1.counter}"
                globalLessonNumber = LessonScreen1.counter
            except:
                pass
        else:
            pass

    def previous(self):
        global globalLessonNumber
        LessonScreen1.counter = self.chapterNumber
        if LessonScreen1.counter>=len(lessons)+1:
            try:
                LessonScreen1.counter -= 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {LessonScreen1.counter}"
                wm.current = f"lesson{LessonScreen1.counter}"
                globalLessonNumber = LessonScreen1.counter
            except:
                pass
        elif LessonScreen1.counter>=len(lessons)-1:
            try:
                LessonScreen1.counter -= 1
                for instance in MyTitle.instances:
                    instance.label.text = f"Chapter {LessonScreen1.counter}"
                wm.current = f"lesson{LessonScreen1.counter}"
                globalLessonNumber = LessonScreen1.counter
            except:
                pass
        else:
            pass


class ClassRoom(Screen):
    instances = []
    def __init__(self, **kwargs):
        super(ClassRoom, self).__init__(**kwargs)
        self.__class__.instances.append(weakref.proxy(self))

    def go_back(self):
        global globalLessonNumber
        # wm.current = f"lesson{globalLessonNumber}"
        wm.switch_to(screens[globalLessonNumber+1], direction="down")

    def show_answers(self):
       for instance in MyLabelText.instances:
            i = 0
            for widget in instance.walk():
                if str(type(widget))=="<class 'kivy.uix.textinput.TextInput'>":
                    widget.text = info[lessonTopic][str(globalLessonNumber)][i][1]
                    i += 1
        
    def evaluate(self):
        evaluation = []
        totalWords = 0
        rightWords = 0
        #WE COMPARE OBJECTS AND EXTRACT TEXT FROM TEXTINPUT OBJECTS
        for instance in MyLabelText.instances:
            i = 0
            for widget in instance.walk():
                if str(type(widget))=="<class 'kivy.uix.textinput.TextInput'>":
                    wordToEvaluate =  widget.text
                    correctWord = info[lessonTopic][str(globalLessonNumber)][i][1]
                    evaluation.append(compareWords(wordToEvaluate, correctWord))
                    if compareWords(wordToEvaluate, correctWord):rightWords = rightWords + 1 
                    i += 1
        totalWords = i
        connection = connectDB()
        #WE CREATE TABLE FOR EVALUATION IF DOESN?T EXIST
        try:
            connection.tableEvaluation()
        except:
            print("Table alredy created")
        #HERE WE RECORD EVALUATION IN DATABASE
        if logged[0]=='logged':
            if connection.checkEvaluationExist(logged[1]):
                connection.updateEvaluation(logged[1], rightWords, totalWords)
            elif connection.checkEvaluationExist(logged[1])==False:
                connection.insertEvaluation(logged[1], rightWords, totalWords, rightWords*100/totalWords)
            else:
                systemMessage(error)


class ConfigScreen(Screen):
    user= ObjectProperty(None)
    mail= ObjectProperty(None)
    correct= ObjectProperty(None)
    total= ObjectProperty(None)
    percentage= ObjectProperty(None)

    def on_enter(self): #This is a special function from kivy, and we are overwritting it, we can algo use it con Kivy Language
        connection = connectDB()
        data = connection.getData(logged[1])

        self.correct.text = f"Correct Answer: {data[0]}"
        self.total.text = f"Total Answer: {data[1]}"
        self.percentage.text = f"Percentage of Success: {data[2]}"
        self.user.text = f'User: {data[3]}'
        self.mail.text = f"Mail: {data[4]}"

    def goBack(self):
        global globalLessonNumber
        LessonScreen1.counter = 1
        globalLessonNumber = LessonScreen1.counter
        wm.current = "lesson1"

    def logOut(self):
        global logged
        logged = ['not logged', None]
        wm.current = 'login'
        


#endregion

class WindowManager(ScreenManager):
    pass


wm = WindowManager()
Builder.load_file('german.kv')

screens = [LoginAccount(name='login'), CreateAccount(name='register'),
         LessonScreen1(name='lesson1'), LessonScreen2(name='lesson2'),
         LessonScreen3(name='lesson3'), ClassRoom(name='class'),
         ConfigScreen(name='config')]

for screen in screens:
    wm.add_widget(screen)

wm.current = "login"
Window.size = (600, 400)

class MyApp(App):
    def build(self):
        return wm

if __name__ == "__main__":
    MyApp().run()

