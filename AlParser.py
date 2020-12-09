#!/usr/bin/python3
import re, random, codecs, os, datetime


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def off():
	exit()


class ALParser(object):
	# Переменные{

	# Переменные настройки

	test_data: bool = False  # Использование Default файлов
	output_setting: str = "print" #Вывод ошибок и/или предупреждений print - печать(вывод на экран), file:./text.log - файл, array - запись в специальный массив, ост. = print
	split_symbols: list = ['-*-VET-*-', '\-{}-/', '{-:-}', '{\-/}', '{-:-}', '?-%-?',
						   '%']  # Символы раздела: 0 - строка ветвления, 1 - разделитель между вопросами и ответами,
	#							 2 - разделитель между регулярными выражениями(вопросами) и числом эмоций,
	#							 3 - разделитель между вариантами ответов,
	#							 4 - разделитель между ответами и эмоциями,
	#							 5 - функция 6 - переменная(символ с двух сторон)

	# Пути к основным файлам

	path: str
	file_var_path: str
	file_string_path: str

	# Пути к файлам(default)

	__main_path: str = "./main.al"
	__main_string: str = "./string.al"
	__main_var: str = "./var.al"

	# Массивы со строками

	__file_aoq: list
	__file_var: list
	__file_string: list

	# Переменные, необходимые для работы класса

	__ps_crypt: dict  # Это для псевдо-шифрования. (Защита от копирования) //Лучше не трогать!!!
	em = emoc = __str_num = 0
	__str_num2 = -1
	err_array: list = [] #Массив ошибок и/или предупреждений

	# }

	# Приватные методы{

	# Метод для зашифровки текста //Пока не реализовано!!!
	def __encode_text(self, text: str) -> str:
		return text

	# Метод для расшифровки текста //Это тоже пока не реализовано!!!
	def __decode_text(self, text: str) -> str:
		return text

	# Метод вывода ошибок и/или предупреждений.
	def __output(self, text: str, status: str = "err", setting: str = "None", exit_arg: bool = False) -> None:

		if setting == "None":
			setting = self.output_setting

		if status == "err" or status == "-":
			out = "[ERR:]"
		elif status == "warning" or status == "!":
			out = "[WARNING:]"
		elif status == "success" or status == "+":
			out = "[SUCCESS:]"
		else:
			out = ""

		all_out_text = "%s %s" % (out, text)

		if setting == "print":
			print(all_out_text)
		elif setting[0:4] == "file":
			out_o = setting.split(":")
			try:
				f = open(out_o[1], 'a')
				f.write("%s : %s\n" % (all_out_text, datetime.datetime.today()))
			except:
				setting = "print"
				self.__output("File, `%s` not found!" % out_o)
		elif setting == "array":
			self.err_array.append("%s : %s" % (all_out_text, datetime.datetime.today()))
		else:
			print(all_out_text)

		if exit:
			exit()

	# Метод инициализации
	def __init__(self, path: str = "", file_var_path: str = "", file_string_path: str = "",
				 test_data: bool = False, out_setting: str = "print") -> None:
		super(ALParser, self).__init__()
		self.test_data = test_data
		self.file_var_path = file_var_path
		self.file_string_path = file_string_path
		self.path = path
		self.output_setting = out_setting
		if self.test_data:
			self.path = self.__main_path
			self.file_var_path = self.__main_var
			self.file_string_path = self.__main_string

		# Создание массивов со строками файлов
		else:
			try:
				with open(self.path, 'r') as file:
					self.__file_aoq = self.__decode_text(file.read().split('\n'))
			except:
				self.__output("File `main` not found!", exit_arg = True)
			try:
				with open(self.file_string_path, 'r') as file:
					self.__file_string = self.__decode_text(file.read().split('\n'))
			except:
				self.__output("File `string` not found!", "warning")
			try:
				with open(self.file_var_path, 'r') as file:
					self.__file_var = self.__decode_text(file.read().split('\n'))
					tmp = []
				for i in range(len(self.__file_var)):
					if len(self.__file_var[i]) != 0:
						if self.__file_var[i][0] != "#":
							tmp.append(self.__file_var[i].split(":"))
				self.__file_var = dict(tmp)
			except:
				self.__output("File `var` not found!", "warning")

	# Функция счёта эмоций, если захотеть можно даже понять, что тут происходит.
	def __emoc_calc(self):
		if self.em == 0:
			self.emoc = 1
		elif 0 < self.em < 25:
			self.emoc = 2
		elif self.em > 25:
			self.emoc = 3
		elif 0 > self.em > -25:
			self.emoc = 4
		elif -25 > self.em > -75:
			self.emoc = 5
		else:
			self.emoc = 6

	# Функция парсинга. Страшная и ужасная, сюда лучше не лезть!
	def __reader(self, text: str) -> str:
		arr_aoq = self.__file_aoq
		result = ""
		__str_num = 0
		self.__str_num2 = self.__str_num2 + 1
		for line in arr_aoq:
			__str_num = arr_aoq.index(line)
			answer_array = []
			if len(line) != 0:
				if line[0] != "#":
					if self.split_symbols[0] in line:
						line = line.replace(self.split_symbols[0], "")
					arr = line.split(self.split_symbols[1])
					arr[0] = arr[0].split(self.split_symbols[2])
					arr[1] = arr[1].split(self.split_symbols[3])

					for i in range(len(arr[1])):
						arr[1][i] = arr[1][i].split(self.split_symbols[4])

					if re.match(r"(" + str(arr[0][0]) + ")", text):
						self.em = self.em + int(arr[0][1])
						for i in range(len(arr[1])):
							if re.match(r"(" + str(arr[1][i][1]) + ")", str(self.emoc)) or str(arr[1][i][1]) == "0":
								if len(arr[1][i]) == 2:
									answer_array.append(arr[1][i][0])
								elif len(arr[1][i]) == 3:
									__str_num2 = self.__str_num2
									if str(arr[1][i][2]) == str(__str_num2) or str(arr[1][i][2]) == "0":
										answer_array.append(arr[1][i][0])
						out_str = answer_array[random.randint(0, len(answer_array) - 1)]
						# Здесь происходит парсинг определенных клюючевых строк.
						for xou in range(1, 50):
							if self.split_symbols[5] in out_str:
								res_ran = re.findall(r'\?-%-\?[a-zA-Z0-9]*\([^)]*\)', out_str)
								for str_in in res_ran:
									out_str = out_str.replace(str_in, "")
									str_in = str_in.replace(self.split_symbols[5], "")
									if xou == 1:
										try:
											exec("%s" % str_in)
										except NameError:
											self.__output("Function `%s` is not found!" % str_in, "err")
										except Exception as e:
											self.__output("%s" % str(e), 'err')

							if self.split_symbols[6] in out_str:
								res_ran = re.findall(r'\%([a-z0-9A-Z.-]*)\%', out_str)
								for str_in in res_ran:
									str_in = "%" + str(str_in) + "%"
									try:
										lines = self.__file_var
										for x, y in lines.items():
											if x == str_in:
												out_str = out_str.replace(x, y)
									except:
										isTRUE = False
							if "STRING" in out_str:
								res_ran = re.findall(r'STRING-[0-9]+', out_str)
								for str_in in res_ran:
									gstring_num = str_in.replace("STRING-", "")
									try:
										lines = self.__file_string
										str_rand_r = lines[int(gstring_num) - 1]
									except:
										isTRUE = False
									out_str = out_str.replace(str_in, str_rand_r)
							if "RAND" in out_str:
								res_ran = re.findall(r'RAND-\[[0-9]+\,[0-9]+\]', out_str)
								for str_in in res_ran:
									arr_rand_m = str_in.replace("RAND-[", "").replace("]", "").split(",")
									gstring_num = random.randint(int(arr_rand_m[0]), int(arr_rand_m[1]))
									try:
										lines = self.__file_string
										str_rand_r = lines[int(gstring_num) - 1]
									except:
										isTRUE = False
									out_str = out_str.replace(str_in, str_rand_r)
						result = out_str
						self.__str_num2 = __str_num
		return result

	# }

	# Методы{
	# Метод чтения файла
	def read(self, text: str) -> str:
		self.__emoc_calc()
		text = text.lower()
		result = self.__reader(text)
		try:
			return codecs.escape_decode(bytes(result, "utf-8"))[0].decode("utf-8")
		except:
			return result

	# Метод создания строки файла парсинга
	def create(self, question: str, emoc: int, dict_answer: dict) -> str:
		result = "%s%s%s%s" % (question, self.split_symbols[2], emoc, self.split_symbols[1])
		for x in dict_answer:
			result = "%s%s%s%s%s" % (result, x, self.split_symbols[4], dict_answer[x], self.split_symbols[3])
		return result[:-5]


# }


