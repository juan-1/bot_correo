#bot que recibe un correo y lo notifica por telegram

import telegram  #se obtiene de https://github.com/python-telegram-bot/python-telegram-bot
from telegram.ext import *
import imaplib #para enlace IMAP 
import email
import os
from time import sleep
ultimo_mail_registrado='0'

def conex():
	global ultimo_mail_registrado
	while True:
		# Conexión a la cuenta de correo
		mail = imaplib.IMAP4_SSL('imap.gmail.com') # Servidor IMAP de GMAIL
		PASS_MAIL=os.environ.get('MAIL_PASS')#se toma de una variable de entorno
		mail.login("correo@gmail.com",PASS_MAIL)
		# Lista mensajes de correo electrónico
		mail.list()
		# Selección de bandeja de entrada por defecto en GMAIl
		mail.select('inbox')
		#busca todos los mensajes
		resultados, datos = mail.search(None, "ALL")
		#lista los id de los mensajes
		ids = datos[0] 
		id_lista = ids.split() # separa los id
		ultimo_mail = id_lista[-1]
		if ultimo_mail != ultimo_mail_registrado:
			ultimo_mail_registrado=ultimo_mail
			resultados, datos = mail.fetch(ultimo_mail, "(RFC822)")
			mensaje = datos[0][1]
			#lee el mensaje
			email_mensaje = email.message_from_bytes(mensaje)
			#se obtiene la direccion de correo de quien lo envia y el asunto del correo
			notificacion="Tienes un nuevo correo: \n\n"+"Para: \n"+email_mensaje['To']+'\n'+"\nDe: \n"+str(email.utils.parseaddr(email_mensaje['From']))+'\n'+ "\nAsunto: \n" +email_mensaje['Subject']
			notifica(notificacion)
		mail.logout()
		sleep(5)#espera 5 segundo antes de volver a actualizar la lista de correos


def notifica(notificacion):
	#en token debe ir el token que da BotFather al crear el bot 
	mi_bot = telegram.Bot(token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxcl')
	mi_bot_comprueba= Updater(mi_bot.token)

	def inicio(bot, update, pass_chat_data=True):
		#se manda un mensaje al grupo de telegram con el asunto y direccion de quien envia el correo
		bot.sendMessage(chat_id=00000000, text=notificacion)
		#chat_id debe tener el valor del id del grupo o persona a la que se va a mandar la notificacion

	inicio(mi_bot, mi_bot_comprueba)

conex()
