import re
import random


# entrada del usuario

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# calculo de probabilidad de respuestas

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    # iteracion de cada palabra por mensaje y ver si la palabra esta en lista reconocida

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1
    # porcentaje de exactitud de palabra de tantas palabra cuan segurp estoy
    percentage = float(message_certainty) / float(len(recognized_words))
    # validar la palabra y si es requerida
    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    # si es requerida se retorna su porcentaje de incidencia
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


# revisar la mayor probabilidad

def check_all_messages(message):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # hola, respuuestas dependiendo lo que diga el saludp
    response('Hello',
             ['hola', 'hello', 'hey chief', 'buenas', 'guten tag', 'bonjour'],
             single_response=True)

    response('Sad to see you go :(',
             ['chau', 'hasta luego', 'auf wiederseen', 'Goodbye', 'I am Leaving', 'Have a Good day', 'bye', 'cao',
              'see ya'],
             single_response=True)

    response('fine wbu?',
             ['how you doing', 'how', 'whats cracking?', 'yoo what up brother?'],
             required_words=['how'])

    response('in your moms house',
             ['ubicados', 'direccion', 'ubicacion', 'location', 'address', 'where', 'living'],
             single_response=True)
    response('sppreciate it man',
             ['gracias', 'te lo agradezco', 'thanks', 'okay im done', 'find information', 'whats fine'],
             single_response=True)

    response('You own the following shares: ABBV, AAPL, META, TSLA, NVDA and an ETF of the S&P 500 Index!',
             ['what stocks do I own?', 'how are my shares?', 'what companies am I investing in?',
              'what am I doing in the markets?'],
             # required_words=['stock', 'market', 'performance'])
             single_response=True)

    # maximo entre la probabilidad y cual es la respuesta que mas encaja
    best_match = max(highest_prob, key=highest_prob.get)
    # print(highest_prob)
    # se retorna probabilidad que mejor encaja
    return unknown() if highest_prob[best_match] < 1 else best_match


# si es desconocido se plantean respuestas definidas con una funcion
def unknown():
    response = ['puedes decirlo de nuevo?', 'No estoy seguro de lo quieres', 'búscalo en google a ver que tal'][
        random.randrange(3)]
    return response


# respuestas del bot
while True:
    print("Bot: " + get_response(input('You: ')))