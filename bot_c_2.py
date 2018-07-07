
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import psutil
import subprocess
import imaplib #para enlace IMAP 
import email
import os
from time import sleep
ultimo_mail_registrado='0'
autentico='0'


actualiza = Updater(token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
despachador = actualiza.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def autenticar(bot, actualiza, args):
	global autentico
	usuarios={"user1":"1234", "user2":"5678"}
	if len(args) >= 2:
		try:
			if usuarios[args[0]] == args[1]:
					autentico="3s4ut3nt1c0_pu3d3_3ntr4r"
			else:
				us_pass_incorrecto(bot, actualiza, 0)
		except KeyError:
			us_pass_incorrecto(bot, actualiza, 1)
	else:
		us_pass_incorrecto(bot, actualiza, 1)

def us_pass_incorrecto(bot, actualiza, us_pa):
	if us_pa == 0:
		bot.sendMessage(chat_id=actualiza.message.chat_id, text='usuario o password incorrecto..!')
	if us_pa == 1:
		bot.sendMessage(chat_id=actualiza.message.chat_id, text='No autorizado..!')

def inicio(bot, actualiza):
	bot.sendMessage(chat_id=actualiza.message.chat_id, text='hola, soy un bot privado ;)')

def eco(bot, actualiza):
	bot.sendMessage(chat_id=actualiza.message.chat_id, text=actualiza.message.text)

def memoria_cpu(bot, actualiza, args):
	global autentico
	autenticar(bot, actualiza, args)
	if autentico == "3s4ut3nt1c0_pu3d3_3ntr4r":
		cpu_info=psutil.cpu_percent()
		memoria_info=subprocess.getoutput("free -m")
		cadena='Uso de CPU: '+str(cpu_info)+'%\n'+'Uso de memoria RAM: \n'+str(memoria_info)
		bot.sendMessage(chat_id=actualiza.message.chat_id, text=cadena)
		autentico = '0'

def procesos(bot, actualiza, args):
	global autentico
	autenticar(bot, actualiza, args)
	if autentico == "3s4ut3nt1c0_pu3d3_3ntr4r":
		#Es necesario tener el programa atop instalado para que funcione esta instruccion
		crear_doc=subprocess.getoutput("atop 1 1 > procesos.txt")
		archivo=open("procesos.txt", 'rb')
		bot.sendMessage(chat_id=actualiza.message.chat_id, text='te paso los procesos ;)')
		bot.sendDocument(chat_id=actualiza.message.chat_id, document=archivo)
		archivo.close()
		autentico = '0'

def invalido(bot, actualiza):
	bot.sendMessage(chat_id=actualiza.message.chat_id, text='Comando invalido..!')

def terminar(bot, actualiza, args):
	global autentico
	autenticar(bot, actualiza, args)
	if autentico == "3s4ut3nt1c0_pu3d3_3ntr4r":
		try:
			comando="kill "+args[2]
			subprocess.getoutput(comando)
			bot.sendMessage(chat_id=actualiza.message.chat_id, text='Terminando proceso '+args[2])
			autentico = '0'
		except IndexError:
			bot.sendMessage(chat_id=actualiza.message.chat_id, text='Necesito el proceso que quieres matar..!')
			autentico = '0'

def lista(bot,actualiza, args):
	global autentico
	autenticar(bot, actualiza, args)
	if autentico == "3s4ut3nt1c0_pu3d3_3ntr4r":
		cadena="\nLista de comandos:\n /inicio <sin argumentos>\n/rendimiento <usuario password>\n/procesos <usuario password>\n/mata <usuario password proceso_a_matar>\n__"
		bot.sendMessage(chat_id=actualiza.message.chat_id, text=cadena)
		autentico = '0'


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
	mi_bot = telegram.Bot(token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	mi_bot_comprueba= Updater(mi_bot.token)

	def inicio(bot, update, pass_chat_data=True):
		#se manda un mensaje al grupo de telegram con el asunto y direccion de quien envia el correo
		bot.sendMessage(chat_id=0000000000, text=notificacion)
		#chat_id debe tener el valor del id del grupo o persona a la que se va a mandar la notificacion

	inicio(mi_bot, mi_bot_comprueba)



inicio_comando=CommandHandler('inicio', inicio)#define el comando
despachador.add_handler(inicio_comando)#agrega el comando
eco_comando=MessageHandler(Filters.text, eco)
despachador.add_handler(eco_comando)
info_comando=CommandHandler('rendimiento', memoria_cpu, pass_args=True)
despachador.add_handler(info_comando)
procesos_comando=CommandHandler('procesos', procesos, pass_args=True)
despachador.add_handler(procesos_comando)
matar_comando=CommandHandler('mata', terminar, pass_args=True)
despachador.add_handler(matar_comando)
lista_comando=CommandHandler('lista', lista, pass_args=True)
despachador.add_handler(lista_comando)
comando_invalido=MessageHandler(Filters.command, invalido)#debe ir al final
despachador.add_handler(comando_invalido)
actualiza.start_polling()#inicia el bot
conex()
