import re
import long_responses as long
import random

from telethon import TelegramClient, events
import apidata

client = TelegramClient('session, apidata.api_id, apidata.api_hash')
@client.on(events.NewMessage(chats-apidata.chat_name))

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Conteggio di quante parole sono presenti in ogni messaggio predefinito
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calcolo della percentuale di parole riconosciute nel messaggio
    percentage = float(message_certainty) / float(len(recognised_words))

    # Controllo delle parole richieste nella string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Deve contenere le parole richieste, o essere una risposta singola
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}


    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Risposte -------------------------------------------------------------------------------------------------------
    response('Ciao! Come posso aiutarti?', ['Buongiorno', 'Buonasera', 'Hey', 'Salve', 'Ciao'], single_response=True)
    response('Puoi spiegarmi che tipo di problema hai?', ['ho', 'problemi', 'ordine'], single_response=True)
    response('Hai inserito correttamente il codice nell apposito spazio prima del pagamento?', ['servizio', 'codice', 'promozione'], required_words=['aiuto'])
    response('Ok, prova a metterlo. Grazie per esserti messo in contatto con il nostro assistente virtuale', ['bene', 'no', 'saluti'], single_response=True)
    response('Un consulente ti contattera a breve', ['continuo', 'si','parlare', 'consulente'], required_words=['parlare', 'consulente'])

    # Risposte lunghe
    response(long.R_B, ['voglio', 'consulenza'], required_words=['consulenza'])
    response(long.R_C, ['come', 'ti', 'aiuto?'], required_words=['come', 'aiuto'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')
    print(highest_prob_list)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def unknown():
    response = ['Scusa, puoi ripetere la tua domanda?', 'Non sono sicuro di quello che hai scrito'][random.randrange(2)]

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing
while True:
    print('Bot: ' + get_response(input('Tu: ')))