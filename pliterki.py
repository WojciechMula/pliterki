#!/usr/bin/env python
# -*- coding: ISO-8859-2 -*-
#
# Wojciech Muła
#
# Released under GNU GPL license
#
# $Id: pliterki.py,v 1.2 2006-09-27 18:55:34 wojtek Exp $

README = r"""
pliterki
========

.. contents::

Introduction
------------------------------------------------------------------------

*Pliterki* is a specialized spellchecker for polish language. It's main purpose
is fixing polish text by adding missing diacritical characters. If you don't
speak polish and do not work with polish text, you won't find this program
useful.

The rest of README is written in polish.

Wprowadzenie
------------------------------------------------------------------------

*Pliterki* zostały pomyślane głównie do uzupełnienia brakujących znaków
diakrytycznych, czyli popularnych ,,ogonków''. Ich ręczne dostawianie jest
uciążliwe, a ponadto bardzo łatwo coś przeoczyć. Siłę programu najlepiej
widać przy poprawianiu tekstów całkowicie wyzbytych polskich znaków
diakrytycznych.

W dalszej części README będzie używane określenie ,,polskie litery'', które
co prawda nie jest poprawne, ale za to bardziej zwięzłe od ,,polskich znaków
diakrytycznych''.

Wymagania
------------------------------------------------------------------------

1. aspell (http://aspell.net)
2. Python w wersji 2.3 lub nowszej
3. polski słownik do aspella; polecam http://www.kurnik.pl/slownik,
   a jeśli używasz Debiana, zainstaluj pakiet ``aspell-pl``
4. rozszerzenie do Pythona o nazwie aspell-python
   http://www.republika.pl/wmula/proj
5. trochę miejsca w ``$HOME``

Opcje programu
------------------------------------------------------------------------

Sposób użycia::

	pliterki [opcje] PLIKI


Opcje:

-h, --help     - pomoc
-r, --readme   - wyświetlenie README
-v, --version  - wersja programu
-n             - tryb nieinteraktywny
-H, --html     - przetwarzanie pliku HTML
-q, --quiet    - program nie wypisuje nic na ekranie użycie tej opcji implikuje tryb nieinteraktywny
-a, --all       - sprawdzane są również słowa zawierająca polskie znaki
-s, --spell     - słowa zawierające polskie znaki są sprawdzane przez aspella (wówczas program działa podobnie do aspell check)
-d             - pyta o pisownię w przypadku, gdy nie udało się znaleźć podobnych słów w słowniku


Pliki są nadpisywane, do nazwa kopii oryginału doklejana jest tylda.

Podstawy
------------------------------------------------------------------------

Program mając dane ,,polskawe'' słowo tworzy listę możliwych słów
zawierających polskie litery, następnie weryfikuje swoje domysły sprawdzając
wszystko w słowniku i ostatecznie:

* Jeśli z listy zostanie tylko jedno słowo, wówczas dokonywana jest
  automatyczna podmiana (np. 'ktory' -> 'który').
* Jeśli lista zawiera więcej niż jedną opcję, wówczas użytkownik proszony
  jest o wybór (np. 'ktora' -> 'która' ale również 'którą'). Więcej w sekcji
  `Tryb interaktywny`_.

Domyślnie przetwarzane są wyłącznie te słowa, które nie zawierają żadnej
polskiej litery, a więc składają się jedynie ze znaków z podstawowego
alfabetu a..z, A..Z.

Można to zmienić podając opcję ``-a``, wówczas także słowa zawierające polskie
litery są spolszczane. Użyteczne, gdy piszemy w miarę poprawnie, ale zdarza
nam się ,,gubić'' polskie literki.

Pamięć podręczna
------------------------------------------------------------------------

Bardzo istotną cechą pliterek jest używanie pamięci podręcznej, dzięki czemu
nie ma potrzeby odpytywać za każdym razem aspella --- w efekcie uzyskuje się
znaczne przyspieszenie, szczególnie jeśli poprawiane jest kilka tekstów pod
rząd, albo tekst jest długi i wracamy do jego korekty kilka razy.

Pamięć podręczna jest zachowywana na dysku, w katalogu ``$HOME/.pliterki/``.

Można skasować pliki z tego katalogu jeśli zajmują za dużo miejsca albo
uruchamianie programu trwa za długo (szybkość wczytywania tych plików
jest ściśle uzależniona od Pythona).

Tryb nieinteraktywny
------------------------------------------------------------------------

W tym trybie wykonywane są **wyłącznie** automatyczne zamiany.

_`Tryb interaktywny`
------------------------------------------------------------------------

W tym trybie również wykonywane są automatyczne zamiany, ale jeśli dla
danego słowa istnieje więcej niż jedno słowo, to użytkownik jest proszony
o wybranie jednego.

Jeśli zostanie podana opcja ``-d``, to w przypadku gdy nie uda się znaleźć
żadnego słowa, użytkownik jest proszony o wpisanie jakiegoś, nie
występującego w słowniku.

Poniżej ,,zrzut ekranu'' z trybu interaktywnego::

 ################################################################################
 'Pliterki' zostały pomyślane głównie do uzupełnienia brakujących znaków
 diakrytycznych, czyli popularnych "ogonków". Ich ręczne dostawianie jest
 uciążliwe, a ponadto bardzo łatwo coś przeoczyć. Sile programu najlepiej
 						 ^^^^
 widac przy poprawianiu tekstow calkowicie wyzbytych polskich znakow
 diakrytycznych.
 
 W dalszej czesci README bedzie uzywane okreslenie "polskie litery", ktore
 co prawda nie jest poprawne, ale za to bardziej zwiezle od "polskich znakow
 === 12.5%% ======================================================================
 Enter - bez zmian
 1) siłę
 2) sile
 3) silę
 
 R - zamień; A - zamień wszystkie; A <numer> - zamień wszystkie na słowo z listy
 I - ignoruj wszystkie
 X - nie pokazuj tego menu
 C - kontynnuj zamianę bez interakcji
 Q - przerwij
 >
 ################################################################################

Na górze ekranu wyświetlany jest fragment pliku, aktualnie przetwarzane
słowo jest podkreślone. Poniżej wyświetlana jest ponumerowana lista
dostępnych słów.

Naciśnięcie Entera powoduje pozostawienie słowa bez zmian.

Wydanie polecenie **R** lub **A** (rozmiar liter nie ma znaczenia)
wymaga wpisania słowa; jeśli nie będzie ono należało do słownika
zostaniemy ostrzeżeni. Po zatwierdzeniu, **R** spowoduje zamianę
podświetlanego słowa, natomiast **A** zamianę tego i wszystkich
następnych.

Polecenia **I** spowoduje, że zaznaczone słowo zostanie uznane za
poprawne i więcej nie będziemy nękani pytaniami o jego pisownię.

Polecenie **A <numer>** (spacja nie jest wymagana) jest szczególnie
pożyteczne jeśli widzimy, że na liście znajdują się słowa, które na
pewno w przetwarzanym tekście nie wystąpią.  Np. dla ,,lub'' lista
propozycji to: ,,łub'' i ,,lub'' --- to pierwsze nie jest zbyt
powszechne.

**UWAGA!** Słowa dodane poleceniami **R** i **A**, oraz te które zostały
zignorowane poleceniem **I** nie są nigdzie zapisywane. Co więcej, jeśli
sprawdzamy wiele plików, to jesteśmy pytani czy skasować te słowa przed
przystąpieniem do sprawdzania następnego pliku. Można wówczas skasować,
pozostawić słowa i również ustawić, by program automatycznie kasował lub
nigdy nie kasował obu zbiorów słów.

Polecenie **X** ukrywa menu --- jest wyświetlana tylko lista słów.

Polecenie **C** przerywa pracę interaktywną i powoduje przejście
w tryb nieinteraktywny.

Polecenie **Q** przerywa pracę programu.

Licencja
------------------------------------------------------------------------

Program jest rozpowszechniany na licencji GNU GPL (Powszechnej Publicznej
Licencji GNU).


Historia zmian
------------------------------------------------------------------------

20.01.2005
	* rozszerzenie możliwości funkcji generującej prawdopodobne polskie słowa

17.01.2005
	* znaczne przyspieszenie i ulepszenie funkcji generującej
	  prawdopodobne polskie słowa
	* sprawdzania plików HTML-owych (opcja ``-H`` lub ``--html``);
	  sprawdzany i modyfikowany jest wyłącznie tekst między tagami
	  oraz treść atrybutów *title* i *alt*
	* możliwość wpisania słowa, gdy program nic nie wymyśli
	  (opcja ``-d``)


Autor
------------------------------------------------------------------------

Wojciech Muła, wojciech_mula#poczta!onet!pl ('#' = '@', '!' = '.')

$Id: pliterki.py,v 1.2 2006-09-27 18:55:34 wojtek Exp $
"""

import sys, struct

class SimpleTerm:
	"""SimpleTerm watch terminal's size. Has also some useful methods"""
	__default_width, __default_height = 80, 25
	
	ESC = '\x1b'
	BEL = '\x07'
	def __init__(self, fd=None):
		"""fd - tty descriptor; if None sys.stdout is used"""
		if fd:
			self.fd = fd
		else:
			from sys import stdout
			if stdout.isatty():
				self.fd = stdout
			else:
				self.fd = None

		self.has_fcntl = self.has_env = False
		
		if self.fd != None:
			try:
				# try to import 'nix fcntl & termios
				# in order to use console ioctl
				import fcntl, termios
				self.has_fcntl = True
			except ImportError:
				pass

			try:
				# are env variables set?
				import os
				os.environ['LINES']
				os.environ['COLUMNS']
				self.has_env = True
			except KeyError:
				pass

			
			try:
				# set hook for SIGWINCH if it is possible
				import signal
				def handler(signum, frame):
					self.__width, self.__height = self.__getsize()
				signal.signal(signal.SIGWINCH, handler)
			except ImportError:
				pass

		self.__width, self.__height = self.__getsize()
				
	def __getsize(self):
		"""retreive current terminal size"""

		height = width = 0
		if self.has_fcntl:
			import fcntl, struct, termios
		
			bytes = fcntl.ioctl(self.fd, termios.TIOCGWINSZ, "\000"*8)
			height, width = struct.unpack('hh4x', bytes)
		elif self.has_env:
			height	= os.environ['LINES']
			width	= os.environ['COLUMNS']

		if height <= 0 or width <= 0:
			return (self.__default_width, self.__default_height)
		else:
			return (width, height)
		
	def clear(self):
		"""Clear screen"""
		if self.fd:
			self.fd.write(self.ESC+'[H')	# clear screen
			self.fd.write(self.ESC+'[2J')	# move cursor to left-upper corner
			self.fd.flush()
	
	def width(self):
		"""width of terminal"""
		return self.__width
	
	def height(self):
		"""height of terminal"""
		return self.__height
	
	def size(self):
		"""width and height of terminal"""
		return (self.__width, self.__height)
	
	def settitle(self, title):
		"""set xterm title"""
		try:
			import os
			if os.environ['TERM'] == 'xterm':
				self.fd.write(self.ESC + ']2;' + title + self.BEL)
				self.fd.flush()
		except:
			pass

Terminal = SimpleTerm()

class Filter:
	"""
	Filter process file and depending on its structure
	returns a text's "dead fields" -- the pieces of text
	that *must not* be modified.
	"""
	def __init__(self):
		self.reset()
	
	def reset(self):
		"""Reset automat state"""
		raise RuntimeError('Abstract method called')
	
	def process_line(self, text):
		"""Process line"""
		raise RuntimeError('Abstract method called')

class HTMLFilter(Filter):
	"""
	HTMLFilter leaves regular text and 
	contents of title and alt attributes
	"""
	def reset(self):
		self.state		= 'text'	# initial state

		import re
		self.re_split	= re.compile(r"\s+|<!--|-->|<\?|\?>|<|>|\"|title|TITLE|alt|ALT|=")
		self.re_ws		= re.compile(r"\s+")

# process_line realizes a Mealy's automat. It's states are:
#
# * text (regular text we want to check)
# * comment
# * php
# * tag (HTMLtag)
# * title/alt (title and alt attributes inside tag)
# * = (character)
# * string (string enclosed in "")
#
# Input signals (tokens) are:
# * <!--		- start of comment
# * -->			- end of comment
# * <?			- start of server-side includes
# * ?>			- end of server-side includes
# * <			- start of tag
# * >			- end of tag
# * "			- start/end of string
# * title|TITLE	- attribute
# * alt|ALT		- attribute
# * =			- character
# * whitespaces	- set of continous whitespaces
# * others		- all other tokens
#
# Ouput signals are:
# 1. open range
# 2. close range
# 3. remove last opened, not closed range

	def tokenize(self, line, regexp):
		"""
		Works like re.split, but also leaves nonmatched substrings.
		"""
		result = []
		ps = 0
		pe = 0
		for match in regexp.finditer(line):
			s = match.start()
			e = match.end()

			if s > pe: result.append(line[pe:s])

			result.append(line[s:e])
			ps, pe = s, e
		
		if pe < len(line):
			result.append(line[pe:])

		return result

	def process_line(self, text):
	
		class Ranges:
			"""List of ranges"""
			def __init__(self):
				self.__list		= []
				self.__finished	= True

			def start(self, s):
				"start new range"
				if not self.__finished:
					raise RuntimeError("Range %d not finished" % len(self.__list))
				self.__list.append( (s, None) )
				self.__finished	= False

			def end(self, e):
				"finish opened range"
				s, _ = self.__list[-1]
				self.__list[-1] = (s,e)
				self.__finished	= True
			
			def cancel(self):
				"nullify opened range"
				del self.__list[-1]
				self.__finished	= True

			def isfinished(self):
				"return true if there is an not closed range"
				return self.__finished

			def list(self):
				"return list of ranges; adjecent ranges are glued"
				if self.__finished:
					if len(self.__list) < 2: 
						return self.__list
					else:
						tmp = []
						start,end = self.__list[0]
						for s,e in self.__list[1:]:
							if end != s:
								tmp.append( (start, end) )
								start, end =  s, e
							else:
								end = e

						return tmp + [(start, end)]
				else:
					raise RuntimeError('List unfinished!')
	
		pos = 0
		ranges = Ranges()
		if self.state in ['comment', 'php', 'tag']:
			# comment, php or tag has started in previous line
			ranges.start(pos)

		tokens = self.tokenize(text, self.re_split)
		for input in tokens:
			if self.state == 'text':
				if input == '<!--':
					ranges.start(pos)
					self.state = 'comment'
				elif input == '<?':
					ranges.start(pos)
					self.state = 'ssi'
				elif input == '<':
					ranges.start(pos)
					self.state = 'tag'

			elif self.state == 'ssi':
				if input == '?>':
					ranges.end(pos + len(input))
					self.state = 'text'

			elif self.state == 'comment':
				if input == '-->':
					ranges.end(pos + len(input))
					self.state = 'text'

			elif self.state == 'tag':
				if input == '>':
					ranges.end(pos + len(input))
					self.state = 'text'
				elif input in ['title','TITLE','alt','ALT']:
					self.state = 'title/alt'

			elif self.state == 'title/alt':
				if input == '>':
					ranges.end(pos + len(input))
					self.state = 'text'
				elif self.re_ws.match(input):
					pass
				elif input == '=':
					self.state = '='
				else:
					self.state = 'tag'

			elif self.state == '=':
				if self.re_ws.match(input):
					pass
				elif input == '"':
					ranges.end(pos + len(input))
					self.state = 'string'
				elif input == '>':
					ranges.end(pos + len(input))
					self.state = 'text'
				else:
					self.state = 'tag'

			elif self.state == 'string':
				if input == '>':
					ranges.cancel()
					self.state = 'text'
				elif input == '"':
					ranges.start(pos)
					self.state = 'tag'

			else:
				raise RuntimeError('Automat error, unknown state %s' % self.state)

			pos = pos + len(input)
		
		if not ranges.isfinished():
			ranges.end(pos)
		return ranges.list()

class RAW:
	"""
	Random Access Words
	"""
	
	def __init__(self, text):
		self.__lengthchanged = False	# length of string changed: update is needed
		self.__stringchanged = False	# string is changed: update is needed
		self.__str		= text		# string representation
		self.__fields		= [ (text, (0,len(text)), None) ]

	def __split(self, text, regexp, Match=True, NotMatch=False):
		result = []
		ps = 0
		pe = 0
		for match in regexp.finditer(text):
			s = match.start()
			e = match.end()

			if s > pe: result.append( (text[pe:s], (0,0), NotMatch) )

			result.append( (text[s:e], (0,0), Match) )
			ps, pe = s, e
	
		if pe < len(text):
			result.append( (text[pe:], (0,0), NotMatch) )

		return result
	
	def __update(self):
		if self.__lengthchanged:
			start = 0
			for index, item in enumerate(self.__fields):
				substring, _, type = item
			
				s = start
				l = len(substring)
				self.__fields[index] = (substring, (s,l), type)
				start = start + l

		if self.__stringchanged:
			self.__str = "".join([substring for substring,_,_ in self.__fields])
	
	def split_field(self, index, regexp, Match, NotMatch):
		"""split given field"""
		self.__lengthchanged	= True
		self.__stringchanged	= True
		
		text	= self.__fields[index][0]
		tmp		= self.__split(text, regexp, Match, NotMatch)
		self.__fields = self.__fields[:index] + tmp + self.__fields[index+1:]

	def split_fields(self, pred, regexp, Match, NotMatch):
		"""
		Split field if pred (callable) is true.
		If pred is None all fields are splitted.
		Pred gets following argumens: substring, start, end, optional.
		"""
		if pred:
			indexes = [i for i in xrange(len(self.__fields)) if pred(*self.__fields[i])]
		else:
			indexes = range(len(self.__fields))

		indexes.reverse()
		for i in indexes:
			self.split_field(i, regexp, Match, NotMatch)
	
	def split_constant_field(self, index, list, Inside, Outside):
		"""
		List is a list of pairs: start index, end index. Each pair
		define field which has Inside type.

		Example:

		Let field 'index' contains text "11 != 152" and list is
		[(0,2), (6,9)], Inside=='number', Outside=='other'.
		Method will split field into list:

			[("11", (..), 'number'),
			 (" != ", (..), 'other'),
			 ("152", (..), 'number']
		"""
		if list == None or len(list) == 0:
			substring, se, _ = self.__fields[index]
			self.__fields[index] = (substring, se, Outside)
			return
		
		self.__lengthchanged	= True
		self.__stringchanged	= True

		text = self.__fields[index][0]
		tmp  = []

		ps = 0
		pe = 0
		for i, item in enumerate(list):
			s, e = item
			if s > e or s < pe:
				raise ValueError("Invalid range (%d,%d) at index %d" % (s, e, i) )

			if s > pe:
				tmp.append( (text[pe:s], (0,0), Outside) )

			tmp.append( (text[s:e], (0,0), Inside) )
			ps, pe = s, e
		
		if pe < len(text):
			tmp.append( (text[pe:], (0,0), Outside) )

		self.__fields = self.__fields[:index] + tmp + self.__fields[index+1:]
	
	def __iter__(self):
		"""start iteration"""
		self.__update()
		self.__index = 0
		return self
	
	def next(self):
		"""next iteration"""
		if self.__index >= len(self.__fields):
			raise StopIteration

		field = self.__fields[self.__index]
		self.__index = self.__index + 1
		return field

	def __getitem__(self, index):
		self.__update()
		return self.__fields[index]

	def __setitem__(self, index, value):
		"""
		setitem support two kinds of types:
		1. object[index] = string -- overrides substring field
		2. object[index] = (string, type) -- overrides both substring
		                                     and type fields
		"""
		import types
		if isinstance(value, types.StringType):
			substring = value
			type = self.__fields[index][2]
		else:
			substring, type = value

		self.__stringchanged = True
		self.__lengthchanged = self.__lengthchanged or len(substring) != len(self.__fields[index][0])
		
		self.__fields[index] = (substring, (0,0), type)
	
	def __delitem__(self, index):
		del self.__fields[index]
	
	def __len__(self):
		return len(self.__fields)

	def __str__(self):
		self.__update()
		return self.__str

class SpellerEditor:

	def __init__(self, file_handle, re_split1, split1, re_split2, split2, re_mark, mark, filter=None):

		self.regexp_split1	= re_split1
		self.regexp_split2	= re_split2
		self.regexp_mark	= re_mark
		self.split1_val		= split1
		self.split2_val		= split2
		self.mark_val		= mark

		if filter:
			filter.reset()

		self.Lines = []
		for line in file_handle:
			if line[-1] == os.linesep:
				line = line[:-1]

			if filter:
				ranges = filter.process_line(line)
			else:
				ranges = None
	
			self.Lines.append( (line, ranges) )

	def edit(self, line_num):
		if not isinstance(self.Lines[line_num][0], RAW):

			line, ranges = self.Lines[line_num]
			tmp = RAW(line)

			tmp.split_constant_field(0, ranges, '__fixed__', None)

			tmp.split_fields(lambda dummy1,dummy2,type: type==None, self.regexp_split1, self.split1_val, None)
			tmp.split_fields(lambda dummy1,dummy2,type: type==None, self.regexp_split2, self.split2_val, None)
			for index, item in enumerate(tmp):
				substring, _, type = item
				if type == None:
					if self.regexp_mark.match(substring):
						tmp[index] = (substring, self.mark_val)
					else:
						tmp[index] = (substring, '__other__')

			self.Lines[line_num] = (tmp, ranges)
		
	def save(self, line_num):
		if isinstance(self.Lines[line_num][0], RAW):
			tmp, ragnes = self.Lines[line_num]
			text = str(tmp)

			# recalculate ranges
			ranges = []
			for _, sl, type in tmp:
				if type == '__fixed__':
					s,l = sl
					e   = s + l
					ranges.append( (s,e) )

			self.Lines[line_num] = (text, ranges)
	
	def __len__(self):
		return len(self.Lines)

	def __getitem__(self, line_num):
		return self.Lines[line_num][0]

	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.Lines):
			raise StopIteration
		
		f = self.Lines[self.index][0]
		self.index = self.index + 1
		return f
	
	def line(self, line_num):
		if isinstance(self.Lines[line_num][0], RAW):
			return str(self.Lines[line_num][0])
		else:
			return self.Lines[line_num][0]
	
	def iterlines(self):
		for line, _ in self.Lines:
			if isinstance(line, RAW):
				yield str(line)
			else:
				yield line

def clone_case(word1, word2):
	"""
	Sets same case of word2's letters, as word1 has.
	For example clone_case("HaXoRs","python") returns "PyThOn"

	If word1 is not upper/lower/capitlize and it's length is different
	then word2's length then unchanged word2 is returned.
	"""
	
	if word1.isupper():
		return word2.upper()
	elif word1.islower():
		return word2.lower()
	elif word1[0].isupper() and word1[1:].islower():
		return word2.capitalize()
	elif len(word1) == len(word2):
		word2 = list(word2)
		for i in xrange(len(word1)):
			if word1[i].isupper():
				word2[i] = word2[i].upper()
			else:
				word2[i] = word2[i].lower()
		return "".join(word2)
	else:
		return word2

def comb(list):
	"""
	Generator returns all possible combinations of
	elements from lists.
	List is a list of lists (or tuples, or string).

	For example:

	>>> for i in comb( ['abc','de','f'] ):
	>>> ...   print i
	>>> ...
	['a', 'd', 'f']
	['b', 'd', 'f']
	['c', 'd', 'f']
	['a', 'e', 'f']
	['b', 'e', 'f']
	['c', 'e', 'f']
	"""
	n	= len(list)
	max	= [len(item) for item in list]
	current	= [0]*n
	run	= True
	while run:
		yield [list[i][current[i]] for i in xrange(n)]
		
		carry = 1
		for i in xrange(n):
			current[i] = current[i] + carry
			if current[i] == max[i]:
				current[i] = 0
				carry = 1
			else:
				carry = 0
				break
		if carry == 1:
			break

import sets

# [a-ząćęłńóśżź][ąćęłńóśżź][a-ząćęłńóśżź]
# all possible neigbours of polish diacritical characters
pl_triples = sets.Set([
'ała', 'ałb', 'ałc', 'ałd', 'ałe', 'ałf', 'ałg', 'ałk',
'ałm', 'ałn', 'ało', 'ałp', 'ałs', 'ałt', 'ału', 'ałw',
'ały', 'ałz', 'ałą', 'ałż', 'ałć', 'ałę', 'ałó', 'aśa',
'aśb', 'aśc', 'aśk', 'aśl', 'aśm', 'aśn', 'aśp', 'aśr',
'aśw', 'aśz', 'aśż', 'aść', 'aśń', 'aźb', 'aźc', 'aźd',
'aźg', 'aźk', 'aźl', 'aźm', 'aźn', 'aźr', 'aźw', 'aźz',
'aźż', 'aźć', 'aźń', 'aża', 'ażb', 'ażc', 'ażd', 'aże',
'ażg', 'ażi', 'ażk', 'ażl', 'ażm', 'ażn', 'ażo', 'ażp',
'ażr', 'ażs', 'ażu', 'aży', 'ażz', 'ażą', 'ażł', 'ażż',
'ażę', 'ażń', 'ażó', 'aća', 'aćc', 'aćk', 'aćm', 'aćp',
'aćw', 'aćz', 'aćż', 'ańb', 'ańc', 'ańd', 'ańk', 'ańm',
'ańs', 'ańt', 'ańz', 'ańż', 'ańć', 'aów', 'bąb', 'bąc',
'bąd', 'bąk', 'bąs', 'bła', 'błb', 'błc', 'błe', 'błk',
'bło', 'błp', 'błs', 'błu', 'bły', 'błą', 'błę', 'błó',
'bśc', 'bśl', 'bśm', 'bźd', 'bża', 'bżd', 'bże', 'bży',
'bżą', 'bżę', 'bęb', 'bęc', 'będ', 'bęk', 'bób', 'bód',
'bóg', 'bói', 'bój', 'ból', 'bór', 'bós', 'bót', 'bów',
'bóz', 'bół', 'bóś', 'bóż', 'cąc', 'cąz', 'cąż', 'cła',
'cłe', 'cło', 'cłu', 'cźn', 'cże', 'cęg', 'cęt', 'cór',
'ców', 'cóz', 'cóż', 'dąb', 'dąc', 'dąk', 'dąl', 'dąs',
'dąw', 'dąz', 'dął', 'dąż', 'dąć', 'dła', 'dłb', 'dłc',
'dłe', 'dłk', 'dło', 'dłs', 'dłu', 'dły', 'dłą', 'dłę',
'dłó', 'dśc', 'dśl', 'dśm', 'dśn', 'dśp', 'dśr', 'dśw',
'dźa', 'dźb', 'dźc', 'dźe', 'dźg', 'dźi', 'dźk', 'dźm',
'dźn', 'dźo', 'dźp', 'dźr', 'dźs', 'dźw', 'dźz', 'dźą',
'dźż', 'dźę', 'dźń', 'dża', 'dżc', 'dżd', 'dże', 'dżi',
'dżk', 'dżl', 'dżm', 'dżn', 'dżo', 'dżp', 'dżr', 'dżu',
'dży', 'dżz', 'dżą', 'dżż', 'dżę', 'dżó', 'dęb', 'dęc',
'dęd', 'dęg', 'dęk', 'dęl', 'dęt', 'dęł', 'dęć', 'dób',
'dój', 'dól', 'dór', 'dós', 'dów', 'dóz', 'dół', 'eła',
'ełb', 'ełc', 'ełd', 'ełe', 'ełg', 'ełk', 'ełl', 'ełm',
'ełn', 'eło', 'ełp', 'ełs', 'ełt', 'ełu', 'eły', 'ełz',
'ełą', 'ełł', 'ełź', 'ełż', 'ełę', 'ełń', 'ełó', 'eśc',
'eśk', 'eśl', 'eśm', 'eśn', 'eśp', 'eśr', 'eśw', 'eśz',
'eśż', 'eść', 'eśń', 'eźb', 'eźc', 'eźd', 'eźg', 'eźl',
'eźm', 'eźn', 'eźr', 'eźw', 'eźz', 'eźż', 'eźć', 'eża',
'eżb', 'eżc', 'eżd', 'eże', 'eżg', 'eżi', 'eżk', 'eżl',
'eżm', 'eżn', 'eżo', 'eżp', 'eżr', 'eżs', 'eżu', 'eżw',
'eży', 'eżz', 'eżą', 'eżł', 'eżż', 'eżę', 'eżó', 'ećc',
'ećd', 'ećk', 'ećm', 'ećp', 'ećs', 'ećw', 'ećz', 'ećż',
'eńc', 'eńd', 'eńk', 'eńm', 'eńs', 'eńt', 'eńz', 'eńż',
'eós', 'eów', 'eóś', 'fąf', 'fże', 'fór', 'fów', 'gąb',
'gąc', 'gąd', 'gąg', 'gąs', 'gąz', 'gła', 'głb', 'głe',
'gło', 'głs', 'głu', 'gły', 'głz', 'głą', 'głż', 'głę',
'głó', 'gśc', 'gźl', 'gża', 'gże', 'gżo', 'gży', 'gżą',
'gżę', 'gżó', 'gęb', 'gęd', 'gęg', 'gęs', 'gęz', 'gęś',
'gód', 'gój', 'gól', 'gór', 'gów', 'góz', 'gół', 'góż',
'hąs', 'hła', 'hłb', 'hłe', 'hło', 'hłs', 'hłu', 'hły',
'hłą', 'hłę', 'hłó', 'hśk', 'hśw', 'hże', 'hćc', 'hćm',
'hćz', 'hćż', 'hęc', 'hęd', 'hęt', 'hęć', 'hód', 'hór',
'hów', 'iąb', 'iąc', 'iąd', 'iąg', 'iąj', 'iąk', 'iąl',
'iąp', 'iąs', 'iąt', 'iąw', 'iąz', 'iął', 'iąś', 'iąź',
'iąż', 'iąć', 'iła', 'iłb', 'iłc', 'iłe', 'iłg', 'iłk',
'iłl', 'iło', 'iłs', 'iłu', 'iły', 'iłz', 'iłą', 'iłł',
'iłż', 'iłę', 'iłó', 'iśc', 'iśk', 'iśl', 'iśm', 'iśn',
'iśt', 'iśw', 'iśz', 'iśł', 'iśż', 'iść', 'iźd', 'iźl',
'iźn', 'iża', 'iżb', 'iżc', 'iżd', 'iże', 'iżk', 'iżm',
'iżn', 'iżo', 'iżs', 'iżu', 'iży', 'iżz', 'iżą', 'iżż',
'iżę', 'iżó', 'ićc', 'ićk', 'ićm', 'ićz', 'ićż', 'ięb',
'ięc', 'ięd', 'ięg', 'ięk', 'ięl', 'ięr', 'ięs', 'ięt',
'ięw', 'ięz', 'ięł', 'ięś', 'ięź', 'ięż', 'ięć', 'ińc',
'ińk', 'ińm', 'ińs', 'ińz', 'ińż', 'iób', 'iód', 'iól',
'iór', 'iós', 'iót', 'iów', 'ióz', 'iół', 'jąc', 'jąd',
'jąk', 'jąl', 'jąs', 'jąt', 'jąw', 'jąz', 'jął', 'jąś',
'jąż', 'jąć', 'jła', 'jłe', 'jło', 'jłu', 'jły', 'jłz',
'jłą', 'jłę', 'jłó', 'jśc', 'jśj', 'jśk', 'jśl', 'jśm',
'jśn', 'jśp', 'jśr', 'jśw', 'jść', 'jźr', 'jża', 'jże',
'jżm', 'jżo', 'jżw', 'jży', 'jżó', 'jęc', 'jęd', 'jęk',
'jęl', 'jęt', 'jęz', 'jęł', 'jęż', 'jęć', 'jńc', 'jńs',
'jów', 'józ', 'kąc', 'kąd', 'kąk', 'kąp', 'kąs', 'kąt',
'kąz', 'kąś', 'kąż', 'kła', 'kłb', 'kłe', 'kło', 'kłs',
'kłu', 'kły', 'kłą', 'kłę', 'kłó', 'kśc', 'kża', 'kże',
'kęc', 'kęd', 'kęp', 'kęs', 'kęt', 'kęś', 'kób', 'kód',
'kój', 'kól', 'kóp', 'kór', 'ków', 'kóz', 'kół', 'ląb',
'ląc', 'ląd', 'ląg', 'ląk', 'ląl', 'ląs', 'ląt', 'ląw',
'ląz', 'lął', 'ląź', 'ląż', 'ląć', 'lła', 'lłb', 'lłe',
'lło', 'lłs', 'lłu', 'lły', 'lłą', 'lłę', 'lłó', 'lśl',
'lśm', 'lśn', 'lśp', 'lśr', 'lśw', 'lśń', 'lźl', 'lźn',
'lża', 'lżb', 'lżc', 'lże', 'lżm', 'lżn', 'lżo', 'lżu',
'lży', 'lżz', 'lżą', 'lżż', 'lżę', 'lżó', 'lćc', 'lćm',
'lćw', 'lćz', 'lćż', 'lęb', 'lęc', 'lęd', 'lęg', 'lęk',
'lęl', 'lęp', 'lęs', 'lęt', 'lęz', 'lęł', 'lęś', 'lęź',
'lęż', 'lęć', 'lńc', 'lńm', 'lńz', 'lńż', 'lób', 'lóc',
'lód', 'lóg', 'lój', 'lók', 'lós', 'lót', 'lów', 'lóz',
'lóź', 'lóż', 'lóć', 'mąc', 'mąd', 'mąk', 'mąt', 'mąz',
'mąż', 'mąć', 'mła', 'mło', 'mły', 'młó', 'mśc', 'mśk',
'mśm', 'mśz', 'mśż', 'mża', 'mże', 'mżo', 'mży', 'mżą',
'mżę', 'mćp', 'męc', 'męd', 'męk', 'męs', 'męt', 'męz',
'męś', 'męż', 'męć', 'móc', 'mód', 'móg', 'mój', 'mók',
'mól', 'mór', 'mów', 'móz', 'mół', 'móż', 'nąb', 'nąc',
'nąd', 'nąl', 'nąt', 'nąw', 'nąz', 'nął', 'nąż', 'nąć',
'nły', 'nśc', 'nża', 'nżc', 'nże', 'nżk', 'nżo', 'nżu',
'nży', 'nżą', 'nżę', 'nżó', 'nęb', 'nęc', 'nęd', 'nęk',
'nęl', 'nęt', 'nęł', 'nęć', 'nóg', 'nój', 'nós', 'nót',
'nów', 'nóz', 'nóż', 'oła', 'ołb', 'ołc', 'ołd', 'ołe',
'ołf', 'ołg', 'ołh', 'ołi', 'ołj', 'ołk', 'ołl', 'ołm',
'ołn', 'oło', 'ołp', 'ołr', 'ołs', 'ołt', 'ołu', 'ołw',
'oły', 'ołz', 'ołą', 'ołł', 'ołś', 'ołż', 'ołć', 'ołę',
'ołó', 'ośb', 'ośc', 'ośk', 'ośl', 'ośm', 'ośn', 'ośp',
'ośr', 'ośw', 'ośz', 'ośż', 'ość', 'oźb', 'oźc', 'oźd',
'oźg', 'oźl', 'oźm', 'oźn', 'oźr', 'oźw', 'oźz', 'oźż',
'oźń', 'oża', 'ożb', 'ożc', 'ożd', 'oże', 'ożg', 'ożk',
'ożl', 'ożm', 'ożn', 'ożo', 'ożr', 'ożs', 'ożu', 'oży',
'ożz', 'ożą', 'ożł', 'ożż', 'ożę', 'ożó', 'oćb', 'oćc',
'oćk', 'oćm', 'oćp', 'oćs', 'oćw', 'oćz', 'oćż', 'ońc',
'ońk', 'ońm', 'ońs', 'ońz', 'ońż', 'oów', 'pąc', 'pąg',
'pąk', 'pąs', 'pąt', 'pła', 'płb', 'płc', 'płe', 'płk',
'pło', 'płs', 'płu', 'pły', 'płą', 'płę', 'płó', 'pśc',
'pża', 'pże', 'pćc', 'pćm', 'pćz', 'pćż', 'pęc', 'pęd',
'pęk', 'pęp', 'pęs', 'pęt', 'pód', 'pój', 'pók', 'pól',
'pór', 'pót', 'pów', 'póz', 'pół', 'póź', 'rąb', 'rąc',
'rąd', 'rąg', 'rąk', 'rąp', 'rąs', 'rąt', 'rąz', 'rąś',
'rąż', 'rąć', 'rła', 'rłb', 'rłe', 'rło', 'rłs', 'rłu',
'rły', 'rłą', 'rłę', 'rłó', 'rśc', 'rśn', 'rśw', 'rść',
'rźc', 'rźl', 'rźm', 'rźn', 'rźz', 'rźż', 'rża', 'rżc',
'rże', 'rżk', 'rżl', 'rżm', 'rżn', 'rżo', 'rżu', 'rży',
'rżz', 'rżą', 'rżż', 'rżę', 'rżó', 'rća', 'rćc', 'rćd',
'rćf', 'rći', 'rćk', 'rćl', 'rćm', 'rćn', 'rćp', 'rćt',
'rćw', 'rćz', 'rćż', 'ręb', 'ręc', 'ręd', 'ręg', 'ręk',
'ręn', 'ręp', 'ręs', 'ręt', 'ręz', 'ręź', 'ręż', 'ręć',
'rńc', 'rńm', 'rńz', 'rńż', 'rób', 'róc', 'ród', 'róg',
'rói', 'rój', 'ról', 'rós', 'rót', 'rów', 'róz', 'róś',
'róź', 'róż', 'róć', 'sąc', 'sąd', 'sąg', 'sąs', 'sąz',
'sąż', 'sła', 'słb', 'słe', 'sło', 'słs', 'słu', 'sły',
'słą', 'słę', 'słó', 'sźn', 'sża', 'sżc', 'sże', 'sżm',
'sżo', 'sżz', 'sżż', 'sćc', 'sćd', 'sćk', 'sćm', 'sćs',
'sću', 'sćz', 'sćż', 'sęc', 'sęd', 'sęk', 'sęp', 'sńc',
'sńm', 'sńz', 'sńż', 'sób', 'sód', 'sój', 'sól', 'sów',
'sół', 'tąc', 'tąd', 'tąg', 'tąp', 'tąz', 'tąż', 'tła',
'tłb', 'tłe', 'tło', 'tłs', 'tłu', 'tły', 'tłą', 'tłę',
'tłó', 'tża', 'tże', 'tęb', 'tęc', 'tęd', 'tęg', 'tęk',
'tęp', 'tęs', 'tęt', 'tęz', 'tęż', 'tęć', 'tóg', 'tój',
'tól', 'tóp', 'tór', 'tów', 'tóz', 'tół', 'tóż', 'uła',
'ułb', 'ułc', 'ułe', 'ułg', 'ułk', 'ułl', 'ułm', 'uło',
'ułt', 'ułu', 'uły', 'ułą', 'ułł', 'ułę', 'ułó', 'uśc',
'uśk', 'uśl', 'uśm', 'uśn', 'uśp', 'uśr', 'uśt', 'uśw',
'uśz', 'uśż', 'uść', 'uźc', 'uźd', 'uźk', 'uźl', 'uźm',
'uźn', 'uźz', 'uźż', 'uźń', 'uża', 'użb', 'użc', 'użd',
'uże', 'użg', 'użk', 'użl', 'użm', 'użn', 'użo', 'użp',
'użr', 'użs', 'użu', 'uży', 'użz', 'użą', 'użż', 'użę',
'użó', 'ućc', 'ućk', 'ućm', 'ućz', 'ućż', 'uńc', 'uńk',
'uńm', 'uńs', 'uńz', 'uńż', 'uńć', 'uów', 'vów', 'wąb',
'wąc', 'wąd', 'wąg', 'wąk', 'wąp', 'wąs', 'wąt', 'wąw',
'wąz', 'wąś', 'wąż', 'wła', 'włe', 'wło', 'włu', 'wły',
'włą', 'włó', 'wśc', 'wśl', 'wśn', 'wśp', 'wśr', 'wśw',
'wża', 'wżd', 'wże', 'wży', 'wżą', 'wżę', 'wćw', 'węb',
'węc', 'węd', 'węg', 'węk', 'węs', 'węt', 'węz', 'węź',
'węż', 'wóc', 'wód', 'wóg', 'wói', 'wój', 'wól', 'wóm',
'wór', 'wów', 'wóz', 'wół', 'wóź', 'wóż', 'xów', 'yła',
'yłb', 'yłc', 'yłe', 'yłg', 'yłk', 'yło', 'yłu', 'yły',
'yłz', 'yłą', 'yłż', 'yłę', 'yłó', 'yśc', 'yśk', 'yśl',
'yśm', 'yśn', 'yśp', 'yśr', 'yśw', 'yśz', 'yśż', 'yść',
'yźc', 'yźl', 'yźm', 'yźn', 'yźz', 'yźż', 'yźć', 'yża',
'yżb', 'yżc', 'yże', 'yżk', 'yżl', 'yżm', 'yżn', 'yżo',
'yżp', 'yżr', 'yżs', 'yżu', 'yżw', 'yży', 'yżz', 'yżą',
'yżł', 'yżż', 'yżę', 'yżó', 'yćc', 'yćm', 'yću', 'yćw',
'yćz', 'yćż', 'yńc', 'yńk', 'yńm', 'yńs', 'yńz', 'yńż',
'yów', 'ząb', 'ząc', 'ząd', 'ząg', 'ząk', 'ząl', 'ząp',
'ząs', 'ząt', 'ząw', 'ząz', 'zął', 'ząś', 'ząź', 'ząż',
'ząć', 'zła', 'złb', 'złe', 'złk', 'zło', 'złs', 'złu',
'zły', 'złz', 'złą', 'złó', 'zśc', 'zśl', 'zśm', 'zśn',
'zśp', 'zśr', 'zśw', 'zża', 'zże', 'zżo', 'zżu', 'zży',
'zżą', 'zżę', 'zżó', 'zćw', 'zęb', 'zęc', 'zęd', 'zęg',
'zęk', 'zęl', 'zęp', 'zęs', 'zęt', 'zęz', 'zęł', 'zęś',
'zęź', 'zęż', 'zęć', 'zńa', 'zńc', 'zńe', 'zńi', 'zńm',
'zńo', 'zńz', 'zńą', 'zńż', 'zńę', 'zód', 'zóg', 'zól',
'zór', 'zós', 'zów', 'zóz', 'zół', 'zóś', 'Łęg', 'ąłb',
'ąłe', 'ąłs', 'ąśc', 'ąśk', 'ąśl', 'ąśm', 'ąśn', 'ąśz',
'ąśż', 'ąść', 'ąźc', 'ąźl', 'ąźć', 'ąża', 'ążc', 'ąże',
'ążk', 'ążl', 'ążm', 'ążn', 'ążo', 'ążp', 'ążs', 'ążu',
'ąży', 'ążz', 'ążą', 'ążż', 'ążę', 'ążó', 'ąćc', 'ąćm',
'ąćz', 'ąćż', 'łąb', 'łąc', 'łąd', 'łąg', 'łąk', 'łąs',
'łąt', 'łąz', 'łąź', 'łła', 'łłb', 'łłe', 'łło', 'łłs',
'łłu', 'łły', 'łłą', 'łłę', 'łłó', 'łśl', 'łśm', 'łśn',
'łśp', 'łśr', 'łśw', 'łźl', 'łźn', 'łża', 'łże', 'łżo',
'łżu', 'łży', 'łżą', 'łżę', 'łżó', 'łćc', 'łćm', 'łćw',
'łćz', 'łćż', 'łęb', 'łęc', 'łęd', 'łęg', 'łęk', 'łęp',
'łęs', 'łęt', 'łęz', 'łęź', 'łęż', 'łńc', 'łńm', 'łńz',
'łńż', 'łób', 'łóc', 'łód', 'łóg', 'łój', 'łók', 'łós',
'łót', 'łów', 'łóz', 'łóź', 'łóż', 'łóć', 'śło', 'śże',
'śćc', 'śćd', 'śćk', 'śćm', 'śćs', 'śću', 'śćz', 'śćż',
'śńc', 'śńm', 'śńz', 'śńż', 'źże', 'źńa', 'źńc', 'źńe',
'źńi', 'źńm', 'źńo', 'źńz', 'źńą', 'źńż', 'źńę', 'żąc',
'żąd', 'żąl', 'żąp', 'żąt', 'żąw', 'żął', 'żąć', 'żła',
'żłe', 'żło', 'żły', 'żłó', 'żże', 'żżo', 'żęc', 'żęl',
'żęt', 'żęł', 'żęć', 'żńc', 'żńm', 'żńz', 'żńż', 'żóg',
'żól', 'żór', 'żów', 'żół', 'ćże', 'ęła', 'ęło', 'ęły',
'ęśc', 'ęśl', 'ęśm', 'ęśn', 'ęśz', 'ęśż', 'ęść', 'ęźb',
'ęźc', 'ęźl', 'ęźm', 'ęźn', 'ęźr', 'ęźz', 'ęźż', 'ęża',
'ężc', 'ęże', 'ężk', 'ężl', 'ężm', 'ężn', 'ężo', 'ężp',
'ężs', 'ężu', 'ęży', 'ężz', 'ężą', 'ężż', 'ężę', 'ężó',
'ęćc', 'ęćd', 'ęćk', 'ęćm', 'ęćs', 'ęćz', 'ęćż', 'ńże',
'óła', 'ółb', 'ółc', 'ółd', 'ółe', 'ółf', 'ółg', 'ółh',
'ółi', 'ółj', 'ółk', 'ółl', 'ółm', 'ółn', 'óło', 'ółp',
'ółr', 'ółs', 'ółt', 'ółu', 'ółw', 'óły', 'ółz', 'ółą',
'ółł', 'ółś', 'ółż', 'ółć', 'ółę', 'ółó', 'óśb', 'óśc',
'óśl', 'óśm', 'óść', 'óźb', 'óźc', 'óźd', 'óźm', 'óźn',
'óźz', 'óźż', 'óźń', 'óża', 'óżb', 'óżc', 'óżd', 'óże',
'óżk', 'óżm', 'óżn', 'óżo', 'óżu', 'óży', 'óżz', 'óżą',
'óżż', 'óżę', 'óżó', 'óćc', 'óćm', 'óćz', 'óćż'])

def possible_plwords(word):
	# polish diacritical characters (PDC) that may appear
	# at begin and end of word
	allowed_at_begin = 'ćłńóśżź'
	allowed_at_end   = 'ąćęłńśżź'

	# latin characters used instead of PDC
	platin = 'acelnosz'

	# platin -> PDC
	repl   = {'a':'aą',
	          'c':'cć',
		  'e':'eę',
		  'l':'lł',
		  'n':'nń',
		  'o':'oó',
		  's':'sś',
		  'z':'zżź'}

	L  = list(word)

	# make list of possible chars at end and begin of word
	if L[0] in 'clnosz':	# without_PDC(allowed_at_begin)
		L[0] = repl[L[0]]
	if L[-1] in 'acelnsz':	# without_PDC(allowed_at_end)
		L[-1] = repl[L[-1]]
	
	# make list of possible PDC insied of word
	for i in xrange(1,len(word)-1):
		if L[i] not in platin:
			continue

		a,X,c = word[i-1:i+2]
		# create all possible triples with neigbours a and c
		for b in repl[X]:
			if a+b+c in pl_triples:
				L[i] += b

	# return list

	tmp = []
	for i in comb(L):
		tmp.append( "".join(i) )
	
	return tmp


class Speller:
	"""
	Speller wrapper. Provides cache for both check() and suggest() methods.
	"""

	def __init__(self, speller, dict_cache=None, sugg_cache=None):
		self.speller = speller

		self.__dict_cache	= dict_cache
		self.__sugg_cache	= sugg_cache
		self.dict = {}
		self.sugg = {}

		import cPickle
		if self.__sugg_cache:
			try:
				self.sugg = cPickle.load( open(self.__sugg_cache, 'r') )
			except (IOError, EOFError):
				self.sugg = {}

		if self.__dict_cache:
			try:
				self.dict = cPickle.load( open(self.__dict_cache, 'r') )
			except (IOError, EOFError):
				self.dict = {}
			
	def save_dict(self, file=None):
		import cPickle
		if file == None:
			file = self.__dict_cache
		if file != None:
			cPickle.dump(self.dict, open(file, 'w'), cPickle.HIGHEST_PROTOCOL)
	
	def save_sugg(self, file=None):
		import cPickle
		if file == None:
			file = self.__sugg_cache
		if file != None:
			cPickle.dump(self.sugg, open(file, 'w'), cPickle.HIGHEST_PROTOCOL)

	def check(self, word):
		lword = word.lower()
		if not self.dict.has_key(lword):
			self.dict[lword] = self.speller.check(lword)
		
		return self.dict[lword]
	
	def suggest(self, word):
		lword = word.lower()
		if not self.sugg.has_key(lword):
			self.sugg[lword] = self.speller.suggest(lword)
		
		return self.sugg[lword]

class PolishSpeller:
	def __init__(self, speller, sugg_cache=None):
		self.speller	= speller
		self.sugg	= {}
		self.repl	= {}
		self.__sugg_cache = sugg_cache

		if self.__sugg_cache:
			import cPickle
			try:
				self.sugg = cPickle.load( open(self.__sugg_cache, 'r') )
			except (IOError, EOFError):
				self.sugg = {}
	
	def save_sugg(self, file=None):
		import cPickle
		if file == None:
			file = self.__sugg_cache
		if file != None:
			cPickle.dump(self.sugg, open(file, 'w'), cPickle.HIGHEST_PROTOCOL)

	def __suggest(self, word):
		lword = word.lower()
		word_list = possible_plwords(lword)
		self.sugg[lword] = [word for word in word_list if self.speller.check(word)]

	def add_replacement(self, word, replacement):
		self.repl[word] = [replacement]
	
	def clear_replacement(self):
		self.repl = {}

	def suggest(self, word):
		if self.repl.has_key(word):
			return self.repl[word]

		lword = word.lower()
		if not self.sugg.has_key(lword):
			self.__suggest(lword)

		return self.sugg[lword]


VERSION = "$Revision: 1.2 $"

def fileok(filename):
	"""Check if we can try to check file"""
	if not os.path.exists(filename): # dosn't exist
		Info("Plik '%s' nie istnieje." % filename)
		return False
	if not os.path.isfile(filename): # is not file
		Info("'%s' nie jest plikiem." % filename)
		return False
	elif os.path.getsize(filename) == 0:
		Info("Plik '%s' jest pusty." % filename)
		return False
	else:
		return True

def Question(prompt, options, default=None, propagate_break=True):
	"""
	prompt  - string
	options - list of tuples:
	           1. value
	           2. string or list of strings assinged to value
	              first string is displaying
	default_value	- value returned on press Enter
	propagate_break	- Ctrl-C is propagate to caller
	"""

	values = {}
	opt = []
	df  = None
	for value, item in options:
		if isinstance(item, types.StringType):
			item = [item]

		if not isinstance(item, (types.ListType, types.TupleType)):
			raise TypeError("list or tuple is required")

		if df == None and value == default:
			if len(item[0]) == 1:
				opt.append(item[0].upper())
			else:
				opt.append(item[0])
		else:
			if len(item[0]) == 1:
				opt.append(item[0].lower())
			else:
				opt.append(item[0])

		for string in item:
			values[string.lower()] = value

	prompt = "%s [%s] " % (prompt, "/".join(opt))
	while True:
		try:
			try:
				input = raw_input(prompt).lower()
			except EOFError:
				print
				continue
		
			if input == '' and default != None:
				return default

			tmp = input.strip()
			if values.has_key(tmp):
				return values[tmp]

		except KeyboardInterrupt:
			if propagate_break:
				raise KeyboardInterrupt
			print

def QuestionYesNo(prompt, default=None, propagate_break=True):
	"""Common used"""
	if default not in [None, True, False]:
		default = None
	return Question(prompt, [(True, ['t','y','tak','yes']), (False, ['n','nie','no'])], default, propagate_break)

def QueryString(prompt, valid=None, propagate_break=True):
	while True:
		try:
			input = raw_input(prompt)
			if valid != None:
				if valid(input): return input
			else:
				return input

		except KeyboardInterrupt:
			if propagate_break:
				raise KeyboardInterrupt
			print

def tmpfilename(path, name, postfix=''):
	"""
	Returns a name for temporary file.
	'name' and 'postfix' are optional strings glued with tmpname;
	"""
	from random import randint
	from os.path import exists
	from os import sep

	while True:
		rand = "%06x" % randint(0, 0xffffff)
		name = path + sep + name + rand + postfix
		if not exists(name):
			return name

REPLACE			= 1
REPLACE_USER	= 2
REPLACE_ALL		= 3
NON_INTERACTIVE	= 4
ABORT			= 5
DO_NOTHING		= 6
IGNORE			= 7
IGNORE_ALL		= 8
	
def format_list(list, preferable_height, max_width, colsep=' '):
	"""
	Format list *tries* to break list of string into columns that
	spans at the most 'preferable_height' lines and summary width
	of text is not wider then 'max_width'; colsep specifies string
	inserted beetwens columns.
	
	Text in columns is right-aligned.
	
	On success returns list of strings, None on fail.
	"""
	
	def split_list(list, max_width, cols, colsep):
		"""
		Break list into 'cols' columns. The max_width limits width
		of text. Returns None if break is impossible.
		"""
		if cols == 1: # don't break
			return list

		n = (len(list)+cols-1)/cols	# max number of items in single column

		# can't fill all columns (there is a colmn's "overful" or "underful")
		if (n*(cols-1) > len(list)) or (n*cols < len(list)):
			return None
		
		columns = []
		for i in xrange(cols):
			start = i*n
			columns.append(list[start:start+n])

		# too wide
		if len(columns[-1]) < n:
			columns[-1] += ['']*(n-len(columns[-1]))

		lengths	= [0]*cols
		for i in xrange(cols):
			lengths[i] = max([ len(item) for item in columns[i] ])

		if sum(lengths) + (cols-1)*len(colsep) > max_width:
			return None
		else:
			result = []
			for i in xrange(n):
				tmp = ["%*s" % (-lengths[index], item[i]) for index, item in enumerate(columns)]
				result.append(colsep.join(tmp))
			return result

	if len(list) <= preferable_height:	# ok
		return list

	cols	= 2
	prev	= None
	while True:
		curr = split_list(list, max_width, cols, colsep)
		
		if curr == None:
			return prev
		elif len(curr) <= preferable_height:
			return curr
		else:
			cols = cols + 1
			prev = curr
#fed

show_menu = True
def QueryUser(suggestions, line_number, field_index):
	global show_menu
	substring, (start,length), _ = File[line_number][field_index]

	def get_range():
		if show_menu:
			menu_height = 9+len(sugg_list)
		else:
			menu_height = 3+len(sugg_list)
		context_lines = Terminal.height() - menu_height - 2
		first_line = max(line_number - context_lines/2, 0)

		return xrange(first_line, first_line+context_lines)

	def calc_size():
		if start + length > Terminal.width() - 10:
			shift = start + length - Terminal.width()/2
		else:
			shift = 0
		proc  = "%0.1f%%" % ((100.0 * line_number)/len(File))
		word  = "%s (%d/%d)" % (substring, field_index+1, len(File[line_number]))
		delim = "=== " + proc + " = " + word + " " + "="*(Terminal.width()-8-len(proc)-len(word))

		return shift, delim

	shift, delim = calc_size()

	if len(suggestions):
		sugg_list = ["%d) %s" % (index+1, item) for index, item in enumerate(suggestions)]
		tmp = format_list(sugg_list, 7, Terminal.width())
		if tmp:
			sugg_list = tmp
	else:
		sugg_list = ['Nie udało się znaleźć podobnego słowa w słowniku']
	
	lines_range = get_range()

	while 1:
		try:
			Terminal.clear()
			for line in lines_range:
				try:
					print File.line(line)[shift:shift+Terminal.width()].replace('\t', ' ')
					if line == line_number:
						print " "*(start-shift) + "^"*length
				except IndexError:
					print
					
			print delim
			print "Enter - bez zmian"
			for item in sugg_list:
				print item

			if show_menu:
				print
				if len(suggestions):
					print "R - zamień; A - zamień wszystkie; A <numer> - zamień wszystkie na słowo z listy"
				else:
					print "R - zamień; A - zamień wszystkie"
				print "I - ignoruj wszystkie"
				print "X - nie pokazuj tego menu"
				print "C - kontynnuj zamianę bez interakcji"
				print "Q - przerwij"
	
			try:
				input = raw_input("> ")
			except EOFError:
				continue

			if input == '': # Enter
				return (None, DO_NOTHING)

			def toint(string):
				try:
					return int(string)
				except ValueError:
					return None

			index = toint(input)
			if index != None and index > 0 and index <= len(suggestions):
				return (suggestions[index-1], REPLACE)

			input = input.strip().upper()
			if input == 'Q':
				return (None, ABORT)
			elif input == 'C':
				return (None, NON_INTERACTIVE)
			elif input == 'X':
				show_menu = not show_menu
				lines_range = get_range()
				shift, delim = calc_size()
			elif input == 'I':
				return (None, IGNORE_ALL)
			elif input[0] == 'A':
				if len(input) > 1 and len(suggestions) > 0:
					index = toint(input[1:])
					if index != None and index > 0 and index <= len(suggestions):
						return (suggestions[index-1], REPLACE_ALL)
				else:
					try:
						answer = QueryString("Zamień wszystkie wystąpienia '%s' na: " % substring).strip()
						if answer != '':
							if len(suggestions) > 0 and not speller.check(answer):
								if QuestionYesNo("Podane słowo nie znajduje się w słowniku. Czy pomimo to użyć go", True, False):
									return (answer, REPLACE_ALL)
							else:
								return (answer, REPLACE_ALL)
					except KeyboardInterrupt:
						pass
				shift, delim = calc_size()
			elif input == 'R':
				try:
					answer = QueryString("Zamień '%s' na: " % substring).strip()
					if answer != '':
						if len(suggestions) > 0 and not speller.check(answer):
							if QuestionYesNo("Podane słowo nie znajduje się w słowniku. Czy pomimo tego użyć go?", True, False):
								return (answer, REPLACE_USER)
						else:
							return (answer, REPLACE_USER)
				except KeyboardInterrupt:
					pass
			
		except KeyboardInterrupt:
			print
			return (None, NON_INTERACTIVE)

def ProgressBar(current_val, min_val, max_val, mode=1):
	try:
		x = float(current_val)/(max_val-min_val)
	except ZeroDivisionError:
		x = 0.0

	if mode == 0:
		# [=======.......] 40.1%
		p = "%6.1f%%" % (100*x)
		n = Terminal.width() - len(p) - 3
		d = int(n*x)
		r = n - d
		output = "[" + "="*d + "."*r + "]" + p
	elif mode == 1:
		# [======= 40.1 % .....]
		p = " %0.1f%% " % (100*x)
		n = Terminal.width() - 3
		d = int(n*x)
		r = n - d
		tmp = "="*d + "."*r
		pos = (n-len(p))/2
		output = '[' + tmp[:pos] + p + tmp[pos+len(p):] + ']'
		
	sys.stdout.write(output + '\r')
	sys.stdout.flush()

class AbortProgram:
	pass

def CheckFile():
	global replace_list, ignore_list
	interactive		= options['interactive']

	for line_number in xrange(len(File)):

		if not interactive and not options['quiet']:
			ProgressBar(line_number, 0, len(File))

		File.edit(line_number)
		
		more_options = []

		# automatic conversion of single replacement pairs
		n = len(File[line_number])
		w = '|/-\\'
		for index, field in enumerate(File[line_number]):
			substring, _, type = field
		
			if not options['quiet']:
				sys.stdout.write('%c\r' % w[index % len(w)] )
				sys.stdout.flush()

			# do not check short words
			if len(substring) < options['ignore_shorter_then']:
				continue

			if ignore_list.has_key(substring):
				continue

			if replace_list.has_key(substring):
				File[line_number][index] = replace_list[substring]
				continue

			# if program works like regular speller
			# check spelling of other words
			if (options['spellchecker'] and type == '__other__') or (len(substring) > 10 and type == 'check'):
				if not speller.check(substring):
					more_options.append(index)
				continue
			
			# do not check not marked words
			if type != 'check':
				continue
			
			lsubstring	= substring.lower()
			props		= pl_speller.suggest(substring)

			if len(props) == 0:
				if options['spellchecker'] and not speller.check(substring):
					more_options.append(index)
				continue
			elif len(props) == 1:
				if props[0] != lsubstring:
					File[line_number][index] = clone_case(substring, props[0])
			else:
				more_options.append(index)
			
		if (len(more_options) == 0) or not interactive:
			File.save(line_number)
			continue

		# interaction with user -- he must choose something
		for index in more_options:
			substring, start, type = File[line_number][index]

			sys.stdout.write('%c\r' % w[index % len(w)] )
			sys.stdout.flush()
			
			if ignore_list.has_key(substring):
				continue

			if replace_list.has_key(substring):
				File[line_number][index] = replace_list[substring]
				continue

			if type == 'check':
				props = pl_speller.suggest(substring)
				if len(props) == 1:
					File[line_number][index] = clone_case(substring, props[0])
					continue
			if type == '__other__' or len(props) == 0:
				props = speller.suggest(substring)

			if len(props) == 0 and not options['ask_unknown']:
				continue
				
			word, action = QueryUser(props, line_number, index)

			if action == DO_NOTHING:
				pass

			# replace -- case must be preserved
			elif action == REPLACE:
				File[line_number][index] = clone_case(substring, word)

			# replace with user input
			elif action == REPLACE_USER:
				File[line_number][index] = word

			# add replacement pair and replace with user input
			elif action == REPLACE_ALL:
				File[line_number][index] = tmp = clone_case(substring, word)
				replace_list[substring] = word

			# ignore all: add pair word -> word
			elif action == IGNORE_ALL:
				ignore_list[substring] = True

			# switch to non-interactive mode
			elif action == NON_INTERACTIVE:
				interactive = False
				break

			# abort program
			elif action == ABORT:
				raise AbortProgram
			else:
				raise NotImplementedError

		File.save(line_number)
		#eol

	if not interactive:
		print

HELP = """%s [opcje] PLIKI

-h, --help      pomoc

-r, --readme    wyświetlenie README

-v, --version   wersja programu

-n              tryb nieinteraktywny

-H,--html       przetwarzanie pliku HTML

-q,--quiet      program nie wypisuje nic na ekranie
                użycie tej opcji implikuje tryb nieinteraktywny

-a,--all        sprawdzane są również słowa zawierająca polskie znaki

-s,--spell      słowa zawierające polskie znaki są sprawdzane przez
                aspella (wówczas program działa podobnie do aspell check)
				
-d              pyta o pisownię w przypadku, gdy nie udało się
                znaleźć podobnych słów w słowniku
"""

if __name__ == "__main__":
	import os
	import os.path
	import sys
	import re
	import types

	###
	### Parse program arguments
	###
	prog = os.path.basename(sys.argv[0])
	if len(sys.argv) == 1:
		print HELP % prog
		sys.exit(1)
	
	options = {}
	options['use_cache']	= True	# disabled

	try:
		home = os.environ['HOME']
		if home[-1] != os.sep:
			home += os.sep
	except KeyError:
		home = '.' + os.sep
	
	options['cache_path']	= home + '.pliterki'
	
	# cache for speller.check() results
	options['cache_dictionary'] = 'dict'

	# cache for speller.suggest() results
	options['cache_suggestions'] = 'sugg'
	
	# cache for polish_speller.suggest() results
	options['cache_pl_suggestions'] = 'plsugg'

	# ignore words shorter (relation < ) then given value
	options['ignore_shorter_then'] = 2

	# don't ask about spell of totally unknown words
	options['ask_unknown']	= False

	# options sets from command line
	options['interactive']	= True
	options['quiet']		= False
	options['spellchecker']	= False 
	options['checkall']		= False 
	options['HTMLfilter']	= False 

	skip = 1
	for arg in sys.argv[1:]:
		if arg in ['-h','--help']:
			print HELP % prog
			sys.exit(0)
		if arg == '-w':
			tmp = README % (HELP % 'pliterki')
			print tmp.replace('&', '&amp').replace('<', '&lt').replace('>','&gt')
			sys.exit(0)
		if arg in ['-r','--readme']:
			print README % (HELP % 'pliterki')
			sys.exit(0)
		elif arg in ['-v','--version']:
			print VERSION
			sys.exit(0)
		elif arg in ['-s','--spell']:
			options['spellchecker']	= True and not options['checkall']
			skip = skip + 1
		elif arg == '-n':
			options['interactive']	= False
			skip = skip + 1
		elif arg in ['-a','--all']:
			options['checkall']		= True
			options['spellchecker']	= False
			skip = skip + 1
		elif arg in ['-q','--quiet']:
			options['quiet'] = True
			options['interactive']	= False
			skip = skip + 1
		elif arg in ['-H','--html']:
			options['HTMLfilter']	= True
			skip = skip + 1
		elif arg in ['-d']:
			options['ask_unknown'] = True
			skip = skip + 1
		else:
			break

	FileList = sys.argv[skip:]
	
	if not sys.stdout.isatty(): # be quiet if we don't write on tty
		options['quiet']		= True
		options['interactive']	= False
	
	###
	### Define 'Die' function depending on quiet settings
	###
	if options['quiet']:
		def Die(s):
			sys.exit(1)
		def Info(s, n):
			pass
	else:
		def Die(string):
			sys.stderr.write(string + os.linesep)
			sys.exit(1)
		def Info(string, new_line=True, flush=False):
			if new_line:
				print string
			else:
				print string,
			if flush:
				sys.stdout.flush()

	###
	### Check settings
	###
	if not os.path.exists(options['cache_path']):
		try:
			Info("Tworzę katalog '%s'..." % options['cache_path'], False)
			os.makedirs(options['cache_path'])
			Info("ok")
		except OSError:
			e = sys.exc_info()
			Die('%s: %s' % (str(e[0]), str(e[1])))
	elif not os.path.isdir(options['cache_path']):
		Die("'%s' nie jest katalogiem." % options['cache_path'])
	
	if len(FileList) == 0:
		Die("Podaj nazwę pliku.")
	
	###
	### Try to import aspell-python module
	###
	try:
		import aspell
	except:
		e = sys.exc_info()
		Die('%s: %s' % (str(e[0]), str(e[1])))
	
	try:
		import locale
		locale.setlocale(locale.LC_ALL, 'pl_PL')
	except:
		Die('Nie mogę zmienić ustawiń na jęzk polski.')
	
	###
	### Create speller wrapper and polish-specific speller
	###
	try:
		def getsize(path):
			"Returns a formatted file size"
			try:
				size = os.path.getsize(path)
				if size > 1024*1024:
					return "%0.1fMiB" % (float(size)/(1024*1024))
				elif size > 1024:
					return "%0.1fKiB" % (float(size)/1024)
				else:
					return "%dB" % size
			except os.error:
				return ''

		if options['use_cache']:
			info  = []
			path1 = options['cache_path'] + os.sep + options['cache_dictionary']
			if not os.path.isfile(path1):
				path1 = None
			else:
				info.append('słownika (%s)' % getsize(path1))

			path2 = options['cache_path'] + os.sep + options['cache_suggestions']
			if not os.path.isfile(path2):
				path2 = None
			else:
				info.append('podpowiedzi (%s)' % getsize(path2))
			
			path3 = options['cache_path'] + os.sep + options['cache_pl_suggestions']
			if not os.path.isfile(path3):
				path3 = None
			else:
				info.append('polskich podpowiedzi (%s)' % getsize(path3))
		
			if not options['quiet'] and info:
				Info("Odtwarzam dane: " + ", ".join(info))
		else:
			path1 = path2 = path3 = None
			
		speller		= Speller( aspell.Speller('lang', 'pl'), path1, path2)
		pl_speller	= PolishSpeller(speller, path3)
		replace_list	= {}
		ignore_list		= {}
	except KeyboardInterrupt:
		Die("Przerwany")
	
	###
	### Load file(s)
	###

	# matches whitespaces (using on first stage of line split)
	whitespaces	= re.compile(r'\s+')
	# matches punctuators (using on second stage of line split)
	punctuators	= re.compile(r'[,.?!:;\'"<>(){}\[\]$%^&@~|\\/*+-]+')
	if options['checkall']:
		# mark all words contains letters
		probably_pl	= re.compile(r'^[ąćęłńóśżćĄĆĘŁŃÓŚŻĆA-Za-z]+$')
	else:
		# mak wods contains letter but without polish letters (default) 
		probably_pl	= re.compile(r'^[A-Za-z]+$')

	default_answer = None
	for file_num, filename in enumerate(FileList):
		if file_num > 0 and default_answer == None:
			tmp = [ ('clear',	['Tak','t']),\
			        ('leave',	['Nie','n']),\
					('always',	['Zawsze','z']),\
					('never',	['niGdy','g']) ]
			print file_num
			ans = Question("Skasować słowa zamieniane lub ignorowane?", tmp, 'always', False)
			if ans == 'clear':
				clear = True
			elif ans == 'leave':
				clear = True
			elif ans == 'always':
				clear = True
				default_answer = True
			elif ans == 'never':
				clear = False
				default_answer = False
		else:
			clear = None

		if clear or default_answer:
			replace_list	= {}
			ignore_list		= {}

		try:
			Info("Wczytywanie pliku '%s' (%d/%d)..." % (filename, file_num+1, len(FileList)), False)
			if not fileok(filename):
				continue

			if options['HTMLfilter']:
				File = SpellerEditor(open(filename, 'r'), whitespaces, 'W', punctuators, 'P', probably_pl, 'check', HTMLFilter())
			else:
				File = SpellerEditor(open(filename, 'r'), whitespaces, 'W', punctuators, 'P', probably_pl, 'check')
		
			Info("ok, wczytano %d linii (%s)" % (len(File), getsize(filename)))

		except KeyboardInterrupt:
			if QuestionYesNo('Przerwać przetwarzanie plików', False, False):
				Die("Przerwany")
		except IOError:
			e = sys.exc_info()
			Info('%s: %s' % (str(e[0]), str(e[1])))

		try:
			Terminal.settitle("Sprawdzanie pliku '%s'" % filename)
			CheckFile()
		except (AbortProgram, KeyboardInterrupt):
			if QuestionYesNo('Zakończyć program bez zapisywania pamięci podręcznej', False, False):
				Die("Przerwane")
		else:
			Info("Zapisywanie pliku '%s'..." % filename, False)
			tmpname = tmpfilename('.', filename+'-')
			try:
				file = open(tmpname, 'w')
				for line in File.iterlines():
					file.write(line + os.linesep)
				file.close()
			except OSError:
				e = sys.exc_info()
				Die('%s: %s' % (str(e[0]), str(e[1])))

			try:
				if os.path.exists(filename+'~'):
					os.unlink(filename+'~')
				os.rename(filename, filename+'~')
			except KeyboardInterrupt:
				e = sys.exc_info()
				Info('%s: %s' % (str(e[0]), str(e[1])))
				Info("Zmieniony tekst został zachowany w pliku '%s'." % tmpname)
				continue
			
			try:
				os.rename(tmpname, filename)
			except OSError:
				os.rename(filename+'~', filename)
				e = sys.exc_info()
				Info('%s: %s' % (str(e[0]), str(e[1])))
				Info("Zmieniony tekst został zachowany w pliku '%s'." % tmpname)

			Info("ok", flush=True)
	
	path = options['cache_path'] + os.sep + options['cache_dictionary']
	Info("Zapisywanie słownika do '%s'..." % path, False)
	try:
		tmpname = tmpfilename('.', 'tmp-')
		speller.save_dict(tmpname)
	except:
		e = sys.exc_info()
		Info('%s: %s' % (str(e[0]), str(e[1])))
	else:
		os.rename(tmpname, path)
		Info("ok", flush=True)
	
	path = options['cache_path'] + os.sep + options['cache_suggestions']
	Info("Zapisywanie podpowiedzi do '%s'..." % path, False)
	try:
		tmpname = tmpfilename('.', 'tmp-')
		speller.save_sugg(tmpname)
	except:
		e = sys.exc_info()
		Info('%s: %s' % (str(e[0]), str(e[1])))
	else:
		os.rename(tmpname, path)
		Info("ok", flush=True)
		
	path = options['cache_path'] + os.sep + options['cache_pl_suggestions']
	Info("Zapisywanie polskich podpowiedzi do '%s'..." % path, False)
	try:
		tmpname = tmpfilename('.', 'tmp-')
		pl_speller.save_sugg(tmpname)
	except:
		e = sys.exc_info()
		Info('%s: %s' % (str(e[0]), str(e[1])))
	else:
		os.rename(tmpname, path)
		Info("ok", flush=True)

# vim: ts=4 shiftwidth=4 nowrap
