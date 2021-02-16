from django.conf import settings

from Logic.models import Konkurs, Work, Voter
import telebot 
from telebot.types import Message 
from telebot import types
from telebot import *
from PIL import Image

from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.files import File
import time
from django.core.management.base import BaseCommand
import os





# //////////////////// Block Start ////////////////////
class Command(BaseCommand):
	help = 'bot2'
	def handle(self, *args, **options):
		bot = telebot.TeleBot(settings.TOKEN)




		# //////////////////// Block Start ////////////////////
		@bot.message_handler(commands=['start'])
		def Start(message: Message):
			bot.send_message(message.chat.id, 'Я бот, созданный Аланом Тьюрингом для проведения конкурсов исскуства. Посвящается Мурзе');



		# //////////////////// Block Start ////////////////////
		@bot.message_handler(commands=['help'])
		def Help(message: Message):
			bot.send_message(message.chat.id, 'Чтобы начать конкурс, введите /start_konkurs. Человек, начавший конкурс, автоматически становится его организатором, т.е только он может его закончить.\n \nЧтобы подать работу на конкурс, отошлите ее фотографию, подписав ее в таком формате: #art "название вашей работы".\nЧтобы завершить прием работ, ввведите /priem_okonchen.\nПосле окончания приема работ можно будет проголосовать за полюбившейся рисунок, веддя команду /vote + ник/id/имя участника, за которого вы хотите проголосовать.\n \nКонкурс завершается командой /end_konkurs, после чего будет определен победитель');



		# //////////////////// Block Start Concurse ////////////////////
		@bot.message_handler(commands=['start_konkurs'])
		def StartConcurse(message: Message):
			print(message)
			chat_id = int(message.chat.id)

			# Проверяем, есть ли конкурс в базе
			try:
				current_konkurs = Konkurs.objects.get(Q(chat=chat_id))
				# Если конкурс уже идет, то ничего не создастся 
				if current_konkurs.start == True:
					bot.send_message(message.chat.id, 'Конкурс уже идет')

				# А если нет, то мы его начнем!
				else:
					print('ant')
					# Cоздает конкурс или обновляет имеющийся
					current_konkurs.start = True
					current_konkurs.num = current_konkurs.num + 1
					current_konkurs.organaiser = message.from_user.id
					current_konkurs.save()

					if message.from_user.username:
						name = '@' + message.from_user.username

					elif message.from_user.first_name and message.from_user.last_name:
						name = message.from_user.first_name + message.from_user.last_name

					elif message.from_user.first_name:
						name = message.from_user.first_name

					else:
						name = str(message.from_user.id)


					bot.send_message(message.chat.id, f'Вы начали конкурс, {name}! Вы его организатор, т.е только вы можете его закончить.\n \nЧтобы подать работу на конкурс, отощлите ее фотографию, подписав ее в таком формате: #art "название вашей работы".\n \nЧтобы закончить прием работ, введите /priem_okonchen(это может сделать только организатор).\nПосле завершения приема рисунков можно будет проголосовать за полюбившуюся работу, введя команду /vote + ник/id/имя участника, за которого вы хотите проголосовать.\n \nЧтобы закончить конкурс и узнать победителя, введите /end_konkurs')
			
			except:

				if message.from_user.username:
					name = '@' + message.from_user.username

				elif message.from_user.first_name and message.from_user.last_name:
					name = message.from_user.first_name + message.from_user.last_name

				elif message.from_user.first_name:
					name = message.from_user.first_name

				else:
					name = str(message.from_user.id)

				konkurs = Konkurs.objects.get_or_create(chat=chat_id, start=True, num=1, organaiser=message.from_user.id)
				bot.send_message(message.chat.id, f'Вы начали конкурс, {name}! Вы его организатор, т.е только вы можете его закончить.\n \nЧтобы подать работу на конкурс, отощлите ее фотографию, подписав ее в таком формате: #art "название вашей работы".\n \nЧтобы закончить прием работ, введите /priem_okonchen(это может сделать только организатор).\nПосле завершения приема рисунков можно будет проголосовать за полюбившуюся работу, введя команду /vote + ник/id/имя участника, за которого вы хотите проголосовать.\n \nЧтобы закончить конкурс и узнать победителя, введите /end_konkurs')



		# //////////////////// Block End Concurse ////////////////////
		@bot.message_handler(commands=['priem_okonchen'])
		def EndConcurse(message: Message):

			chat_id = int(message.chat.id)
			print(chat_id)

			try:
				current_konkurs = Konkurs.objects.get(Q(chat=chat_id))

				# Если конкурс уже идет, то ничего не создастся 
				if current_konkurs.start == True and message.from_user.id == current_konkurs.organaiser:
					current_konkurs.start = False
					current_konkurs.save()

					# List of participants
					result = Work.objects.filter(Q(konkurs_id=current_konkurs.num))

					if result:
						champions = [work.author + ':  ' + work.name for work in result]

						# Choosing a winner
						bot.send_message(message.chat.id, 'Прием работ окончен! Чтобы проголосовать за одного из участников, напишите команду в таком формате: /vote имя/ник/id участника ')
					else:
						bot.send_message(message.chat.id, 'Работ в этом конкурсе не было :/')

				elif message.from_user.id != current_konkurs.organaiser:
					bot.send_message(message.chat.id, 'Завершить прием работ может только организатор!')


				else:
					bot.send_message(message.chat.id, 'Конкурс еще не начался :/')

			# А если нет, то мы его начнем!
			except Exception as e:
				print(str(e))
				bot.send_message(message.chat.id, 'Конкурс еще не начался :/')






		# //////////////////// Block Сollect Works ////////////////////
		@bot.message_handler(content_types=['photo'])
		def CollectWorks(message: Message):
			chat_id = int(message.chat.id)
			# Author's name
			if message.from_user.first_name and message.from_user.last_name:
				name = message.from_user.first_name + message.from_user.last_name

			elif message.from_user.first_name:
				name = message.from_user.first_name

			elif message.from_user.username:
				name = message.from_user.username

			else:
				name = str(message.from_user.id)


			
			# If konkurs exists
			current_konkurs = Konkurs.objects.get(Q(chat=chat_id))
			works_of_this_konkurs = Work.objects.filter(Q(konkurs_id=current_konkurs.num))
			agree = True 

			for work in works_of_this_konkurs:
				if message.from_user.id == work.author_id and message.from_user.id != 1168836175:
					agree = False

			# iF IT IS AN ART
			if current_konkurs.start == True and '#art' in message.caption and agree:

				raw = message.photo[-1].file_id
				path = str(raw) + ".jpg"
				file_info = bot.get_file(raw)
				# Downloading it
				downloaded_file = bot.download_file(file_info.file_path)

				with open(path, 'wb') as new_file:
					new_file.write(downloaded_file)
					print('Ant is alive!')
					work = Work(name=''.join(message.caption.split(' ')[1]), author=name, author_id=message.from_user.id, author_nick='@' + str(message.from_user.username), image_id=str(raw), konkurs_id=current_konkurs.num)
					work.save()
					bot.send_message(message.chat.id, 'Ваша работа принята!')

			elif not agree:
				bot.send_message(message.chat.id, 'Один участник не может иметь больше одной работы!')


				



				
			

		# //////////////////// Vote For The Winner ////////////////////
		@bot.message_handler(commands=['vote'])
		def Election(message: Message):
			global election_start

			try:
				current_konkurs = Konkurs.objects.get(Q(chat=message.chat.id))

			except Exception as e:
				current_konkurs = [2, 2, 2, 2, 2]
				print(str(e))
			# Telling apart the if a person wants to vote
			if 1:
				print(election_start)

				# If there is konkurs going on in this chat
				try:
					current_konkurs = Konkurs.objects.get(Q(chat=message.chat.id))

					# If it has just ended
					if not current_konkurs.start:
						# Author's name
						if len(message.text.split(' ')) == 2:
							name = message.text.split(' ')[1]

						elif len(message.text.split(' ')) == 3:
							name = message.text.split(' ')[1] + ' ' + message.text.split(' ')[2]

						elif len(message.text.split(' ')) == 4:
							print(8)
	
							work_name = message.text.split(' ')[-1]
							name = message.text.split(' ')[1]

						

		


						try:
							# WOrks matching the query
							if '@' in message.text and not len(message.text.split(' ')) == 4:
								works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author_nick=name))

							elif name.isnumeric():
								works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author_id=name))

							elif len(message.text.split(' ')) == 4:
								works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author_nick=name)).filter(Q(name=work_name))
								print(7)

							else:
								works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author=name))


							# If there are works matching the query and it is the first time a voter votes in this konkurs
							if works and not Voter.objects.filter(Q(u_id=message.from_user.id)).filter(Q(konkurs_id=current_konkurs.num)) or message.from_user.id == 1168836175:
								print(works)
								for work in works:
									# Not letting them vote for themselves 
									if work.author_id != message.from_user.id or message.from_user.id == 1168836175:
										# Write voter into database
										Voter.objects.get_or_create(u_id=message.from_user.id, konkurs_id=current_konkurs.num)

										if work.votes:
											# Adding votes
											work.votes += 1

										else:
											work.votes = 1

									else:
										bot.send_message(message.chat.id, 'Вы не можете голосовать за себя ')

									work.save()

							# You cant vote twice!
							elif Voter.objects.filter(Q(u_id=message.from_user.id)).filter(Q(konkurs_id=current_konkurs.num)) and message.from_user.id != 1168836175:
								bot.send_message(message.chat.id, 'Вы не можете голосовать больше одного раза ')

						

						except Exception as e:
								print(str(e))



				except Exception as e:
					print(str(e))

			# If time for election has elapsed you cant vote anymore
			#elif int(message.date) - election_start > 20 and '#vote' in message.text:
				#bot.send_message(message.chat.id, 'Голосовать больше нельзя! ')
				#champions = sorted(Work.objects.filter(Q(konkurs_id=current_konkurs.num)), key=lambda x: x.votes)
				#print(champions)




		# //////////////////// Block Сollect Works ////////////////////
		@bot.message_handler(commands=['end_konkurs'])
		def ShowResults(message: Message):
			try:
				current_konkurs = Konkurs.objects.get(Q(chat=message.chat.id))

				if message.from_user.id == current_konkurs.organaiser:		
					works = Work.objects.filter(Q(konkurs_id=current_konkurs.num))
					winner = sorted(works, key=lambda x: x.votes)[-1]
					results = []

					if winner.author_nick:
						name = winner.author_nick

					elif winner.author:
						name = winner.author

					else:
						name = winner

					for work in works:
						if work.author and works:
							results.append(f'{work.author}: {work.name} \n')

						elif not work.author and work.author_nick and works:
							results.append(f'{work.author_nick}: {work.name} - {work.votes}\n')

						else:
							results.append(f'{work.author_id}: {work.name} - {work.votes}\n')


					bot.send_message(message.chat.id, ''.join(results))
					bot.send_message(message.chat.id, f'Победил {name}!')

				else:
					bot.send_message(message.chat.id, f'Только организатор конкурса может решать, когда его заканчивать! :/')

			except Exception as e:
				print(str(e))
				current_konkurs = Konkurs.objects.get(Q(chat=message.chat.id))
				works = Work.objects.filter(Q(konkurs_id=current_konkurs.num))
				print(works)
				bot.send_message(message.chat.id, f'Вы еще не начинали конкурс' + str(e))



		@bot.message_handler(commands=['select'])
		def SelectResults(message: Message):
			current_konkurs = Konkurs.objects.get(Q(chat=message.chat.id))
			work_name = False

			if len(message.text.split(' ')) == 2:
				name = message.text.split(' ')[1]

			elif len(message.text.split(' ')) == 3:
				name = message.text.split(' ')[1]
				work_name = message.text.split(' ')[2]

			else:
				name = 'd'



			try:
				if name and work_name:
					if '@' in message.text:
						works = Work.objects.filter(Q(author_nick=name)).filter(Q(name=work_name))

					elif name.isnumeric():
						works = Work.objects.filter(Q(author_id=name)).filter(Q(name=work_name))


					else:
						works = Work.objects.filter(Q(author=name)).filter(Q(name=work_name))


					for photo in works:
						bot.send_photo(message.chat.id, f'{photo.image_id}')


				else:
					if '@' in message.text:
						works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author_nick=name))
					elif name.isnumeric():
						works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author_id=name))

					else:
						works = Work.objects.filter(Q(konkurs_id=current_konkurs.num)).filter(Q(author=name))


					for photo in works:
						bot.send_photo(message.chat.id, f'{photo.image_id}')

			except:
				bot.send_message(message.chat.id, 'Неверный запрос или работа, которую вы ищете, не сущетсвует')






		'''@server.route('/' + settings.TOKEN, methods=['POST'])
		def getMessage():
			bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
			return "!", 200


		@server.route("/")
		def webhook():
			bot.remove_webhook()
			bot.set_webhook(url='https://your_heroku_project.com/' + settings.TOKEN)
			return "!", 200


		if __name__ == "__main__":
			server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))'''

		bot.polling(none_stop=True)
			