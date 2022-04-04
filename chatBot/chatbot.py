from difflib import SequenceMatcher, get_close_matches
import json
from random import randint
import re


# Se cargan los datos de las preguntas y respuestas del bot
preguntas = open("preguntas.json", 'r')
preguntas_data = preguntas.read()
respuestas = open("respuestas.json", 'r')
respuestas_data = respuestas.read()


# Para normalización de texto 
tildes, vocales = "áäéëíïóöúü", "aaeeiioouu"
transformacion = str.maketrans(tildes, vocales)

# Se crea la clase del bot y sus respectivas funciones
class bot:
    # Se cargan los datos para poder procesarlos
    def __init__(self, preguntas, respuestas):
        self.preguntas_obj = json.loads(preguntas)
        self.respuestas_obj = json.loads(respuestas)

    # Se saluda
    def getResponse(self, user_input):
        # Se ve si el usuario está realidando una pregunta
        asking = self.isAsking(user_input)
        # Quitar las tildes de los textos
        message_list = user_input.translate(transformacion)
        # Se separa las palabras de lo que introdujo el usuario
        message_list = message_list.split()
        # Se quitan los caracteres especiales y las mayúsculas
        for i in range(len(message_list)):
            message_list[i] = re.sub('[^A-Za-z0-9]+', '', message_list[i].lower())
        
        # Variable para manejar el key que mejor se adapte al input del usuario
        best_key = ""
        # Variables para comparar los ratios entre textos
        lastRatio = 0
        newRatio = 0

        # Condicional para ver si el usuario esta preguntando o respondiendo
        if(asking):
            keys = []
            for key in self.respuestas_obj.keys():
                keys.append(key)

            # Iteración para elegir la mejor key
            for i in message_list:
                for j in keys:

                    newRatio = SequenceMatcher(None, i, j).ratio()

                    if(newRatio >= lastRatio):
                        lastRatio = newRatio
                        best_key = j


            self.response = self.chooseResponse(best_key, asking)   
            # print(best_key, lastRatio, self.respuestas_obj[best_key])       
            

        else:
            keys = []
            for key in self.preguntas_obj.keys():
                keys.append(key)

            # Iteración para elegir la mejor key
            for i in message_list:
                for j in keys:

                    newRatio = SequenceMatcher(None, i, j).ratio()

                    if(newRatio >= lastRatio):
                        lastRatio = newRatio
                        best_key = j

            self.response = self.chooseResponse(best_key, asking)   
            # print(best_key, lastRatio, self.respuestas_obj[best_key])  

        
        
        return self.response

    # Para ver si el usuario está preguntando 
    def isAsking(self, user_input):
        if('?' in user_input):
            return True
        else:
            return False
        
    def chooseResponse(self, best_key, isAsking):

        if(isAsking):
            if(len(self.respuestas_obj[best_key]) > 1):

                n = randint(1, len(self.respuestas_obj[best_key]))
                return self.respuestas_obj[best_key][n-1]
            else:
                return self.respuestas_obj[best_key][0]
        else:
            if(len(self.preguntas_obj[best_key]) > 1):

                n = randint(1, len(self.preguntas_obj[best_key]))
                return self.preguntas_obj[best_key][n-1]
            else:
                return self.preguntas_obj[best_key][0]

# Creación del Objeto y Bucle Infinito
chatbot = bot(preguntas_data, respuestas_data)

while True:
    print("Bot: " + chatbot.getResponse(input("Usuario: ")))

