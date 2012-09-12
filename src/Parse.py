import Filter
import random
import Database
import Ball
import Excuses
from subprocess import check_output

class Parse:
	
	def __init__(self, bus, chatNumber):
		self.bus = bus
		self.chatNumber = chatNumber
		self.db = Database.Data()
		self.commands = self.db.ToDict('commands')
		self.ball = Ball.ball()
		self.excuses = Excuses.excuse()
	
	def Start(self, body):
		#Important commands can only be run if line is started with the word
		token = body[0].lower();

		if token == '!create':
			string = ""
			length = len(body) - 2
			for i in range(length):
				string = string + body[i+2] + " "
			string.strip()
			self.commands["!"+body[1].lower()] = string
			self.Reply("Created !" + body[1])
			self.db.SaveDict(self.commands, 'commands')
			self.Reply("Saved commands to file")

		elif token == "!list":
			string = ""
			for i in self.commands:
				string = string + i + " "
			self.Reply(string.lower())
			
		elif token == "!save":
			self.db.SaveDict(self.commands, 'commands')
			self.Reply("Saved commands to file")

		elif token == "!reload":
			self.commands = self.db.ToDict('commands')
			self.Reply("Reloaded command file")

		elif token == "!delete":
			del self.commands['!' + body[1].lower()]

		else:
			for i in body:
				word = i.lower()
				if word == "!fortune":
					string = check_output(['fortune','-n','100'])
					self.Reply(string)

				elif word == "!excuse":
					self.Reply(self.excuses.get())

				elif word == "!8ball":
					self.Reply(self.ball.get())

				elif word in self.commands:
					self.Reply(self.commands[i.lower()])

	def Reply(self, message):
		string = "CHATMESSAGE " + self.chatNumber + " " + message
		self.bus.Invoke(string)
		
	def SetChatNumber(self, chatNumber):
		self.chatNumber = chatNumber
