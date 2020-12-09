from AlParser import *

Parser = ALParser("./data/main.al", "./data/var.al", "./data/string.al")
print(Parser.read("привет"))
print(Parser.create(question="привет|как дела", emoc=0, dict_answer={"Отлично!": "1|2", "Хорошо": "[1-6]"}))
