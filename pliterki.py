#!/usr/bin/env python
# -*- coding: ISO-8859-2 -*-
#
# Wojciech Mu�a
#
# Released under GNU GPL license
#
# $Id: pliterki.py,v 1.2 2006-09-27 18:55:34 wojtek Exp $

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

# [a-z����󶿼][����󶿼][a-z����󶿼]
# all possible neigbours of polish diacritical characters
pl_triples = sets.Set([
'a�a', 'a�b', 'a�c', 'a�d', 'a�e', 'a�f', 'a�g', 'a�k',
'a�m', 'a�n', 'a�o', 'a�p', 'a�s', 'a�t', 'a�u', 'a�w',
'a�y', 'a�z', 'a��', 'a��', 'a��', 'a��', 'a��', 'a�a',
'a�b', 'a�c', 'a�k', 'a�l', 'a�m', 'a�n', 'a�p', 'a�r',
'a�w', 'a�z', 'a��', 'a��', 'a��', 'a�b', 'a�c', 'a�d',
'a�g', 'a�k', 'a�l', 'a�m', 'a�n', 'a�r', 'a�w', 'a�z',
'a��', 'a��', 'a��', 'a�a', 'a�b', 'a�c', 'a�d', 'a�e',
'a�g', 'a�i', 'a�k', 'a�l', 'a�m', 'a�n', 'a�o', 'a�p',
'a�r', 'a�s', 'a�u', 'a�y', 'a�z', 'a��', 'a��', 'a��',
'a��', 'a��', 'a��', 'a�a', 'a�c', 'a�k', 'a�m', 'a�p',
'a�w', 'a�z', 'a�', 'a�b', 'a�c', 'a�d', 'a�k', 'a�m',
'a�s', 'a�t', 'a�z', 'a�', 'a��', 'a�w', 'b�b', 'b�c',
'b�d', 'b�k', 'b�s', 'b�a', 'b�b', 'b�c', 'b�e', 'b�k',
'b�o', 'b�p', 'b�s', 'b�u', 'b�y', 'b��', 'b��', 'b��',
'b�c', 'b�l', 'b�m', 'b�d', 'b�a', 'b�d', 'b�e', 'b�y',
'b��', 'b��', 'b�b', 'b�c', 'b�d', 'b�k', 'b�b', 'b�d',
'b�g', 'b�i', 'b�j', 'b�l', 'b�r', 'b�s', 'b�t', 'b�w',
'b�z', 'b�', 'b�', 'b�', 'c�c', 'c�z', 'c��', 'c�a',
'c�e', 'c�o', 'c�u', 'c�n', 'c�e', 'c�g', 'c�t', 'c�r',
'c�w', 'c�z', 'c�', 'd�b', 'd�c', 'd�k', 'd�l', 'd�s',
'd�w', 'd�z', 'd��', 'd��', 'd��', 'd�a', 'd�b', 'd�c',
'd�e', 'd�k', 'd�o', 'd�s', 'd�u', 'd�y', 'd��', 'd��',
'd��', 'd�c', 'd�l', 'd�m', 'd�n', 'd�p', 'd�r', 'd�w',
'd�a', 'd�b', 'd�c', 'd�e', 'd�g', 'd�i', 'd�k', 'd�m',
'd�n', 'd�o', 'd�p', 'd�r', 'd�s', 'd�w', 'd�z', 'd��',
'd��', 'd��', 'd��', 'd�a', 'd�c', 'd�d', 'd�e', 'd�i',
'd�k', 'd�l', 'd�m', 'd�n', 'd�o', 'd�p', 'd�r', 'd�u',
'd�y', 'd�z', 'd��', 'd��', 'd��', 'd��', 'd�b', 'd�c',
'd�d', 'd�g', 'd�k', 'd�l', 'd�t', 'd�', 'd��', 'd�b',
'd�j', 'd�l', 'd�r', 'd�s', 'd�w', 'd�z', 'd�', 'e�a',
'e�b', 'e�c', 'e�d', 'e�e', 'e�g', 'e�k', 'e�l', 'e�m',
'e�n', 'e�o', 'e�p', 'e�s', 'e�t', 'e�u', 'e�y', 'e�z',
'e��', 'e��', 'e��', 'e��', 'e��', 'e��', 'e��', 'e�c',
'e�k', 'e�l', 'e�m', 'e�n', 'e�p', 'e�r', 'e�w', 'e�z',
'e��', 'e��', 'e��', 'e�b', 'e�c', 'e�d', 'e�g', 'e�l',
'e�m', 'e�n', 'e�r', 'e�w', 'e�z', 'e��', 'e��', 'e�a',
'e�b', 'e�c', 'e�d', 'e�e', 'e�g', 'e�i', 'e�k', 'e�l',
'e�m', 'e�n', 'e�o', 'e�p', 'e�r', 'e�s', 'e�u', 'e�w',
'e�y', 'e�z', 'e��', 'e��', 'e��', 'e��', 'e��', 'e�c',
'e�d', 'e�k', 'e�m', 'e�p', 'e�s', 'e�w', 'e�z', 'e�',
'e�c', 'e�d', 'e�k', 'e�m', 'e�s', 'e�t', 'e�z', 'e�',
'e�s', 'e�w', 'e�', 'f�f', 'f�e', 'f�r', 'f�w', 'g�b',
'g�c', 'g�d', 'g�g', 'g�s', 'g�z', 'g�a', 'g�b', 'g�e',
'g�o', 'g�s', 'g�u', 'g�y', 'g�z', 'g��', 'g��', 'g��',
'g��', 'g�c', 'g�l', 'g�a', 'g�e', 'g�o', 'g�y', 'g��',
'g��', 'g��', 'g�b', 'g�d', 'g�g', 'g�s', 'g�z', 'g�',
'g�d', 'g�j', 'g�l', 'g�r', 'g�w', 'g�z', 'g�', 'g�',
'h�s', 'h�a', 'h�b', 'h�e', 'h�o', 'h�s', 'h�u', 'h�y',
'h��', 'h��', 'h��', 'h�k', 'h�w', 'h�e', 'h�c', 'h�m',
'h�z', 'h�', 'h�c', 'h�d', 'h�t', 'h��', 'h�d', 'h�r',
'h�w', 'i�b', 'i�c', 'i�d', 'i�g', 'i�j', 'i�k', 'i�l',
'i�p', 'i�s', 'i�t', 'i�w', 'i�z', 'i��', 'i��', 'i��',
'i��', 'i��', 'i�a', 'i�b', 'i�c', 'i�e', 'i�g', 'i�k',
'i�l', 'i�o', 'i�s', 'i�u', 'i�y', 'i�z', 'i��', 'i��',
'i��', 'i��', 'i��', 'i�c', 'i�k', 'i�l', 'i�m', 'i�n',
'i�t', 'i�w', 'i�z', 'i��', 'i��', 'i��', 'i�d', 'i�l',
'i�n', 'i�a', 'i�b', 'i�c', 'i�d', 'i�e', 'i�k', 'i�m',
'i�n', 'i�o', 'i�s', 'i�u', 'i�y', 'i�z', 'i��', 'i��',
'i��', 'i��', 'i�c', 'i�k', 'i�m', 'i�z', 'i�', 'i�b',
'i�c', 'i�d', 'i�g', 'i�k', 'i�l', 'i�r', 'i�s', 'i�t',
'i�w', 'i�z', 'i�', 'i�', 'i�', 'i�', 'i��', 'i�c',
'i�k', 'i�m', 'i�s', 'i�z', 'i�', 'i�b', 'i�d', 'i�l',
'i�r', 'i�s', 'i�t', 'i�w', 'i�z', 'i�', 'j�c', 'j�d',
'j�k', 'j�l', 'j�s', 'j�t', 'j�w', 'j�z', 'j��', 'j��',
'j��', 'j��', 'j�a', 'j�e', 'j�o', 'j�u', 'j�y', 'j�z',
'j��', 'j��', 'j��', 'j�c', 'j�j', 'j�k', 'j�l', 'j�m',
'j�n', 'j�p', 'j�r', 'j�w', 'j��', 'j�r', 'j�a', 'j�e',
'j�m', 'j�o', 'j�w', 'j�y', 'j��', 'j�c', 'j�d', 'j�k',
'j�l', 'j�t', 'j�z', 'j�', 'j�', 'j��', 'j�c', 'j�s',
'j�w', 'j�z', 'k�c', 'k�d', 'k�k', 'k�p', 'k�s', 'k�t',
'k�z', 'k��', 'k��', 'k�a', 'k�b', 'k�e', 'k�o', 'k�s',
'k�u', 'k�y', 'k��', 'k��', 'k��', 'k�c', 'k�a', 'k�e',
'k�c', 'k�d', 'k�p', 'k�s', 'k�t', 'k�', 'k�b', 'k�d',
'k�j', 'k�l', 'k�p', 'k�r', 'k�w', 'k�z', 'k�', 'l�b',
'l�c', 'l�d', 'l�g', 'l�k', 'l�l', 'l�s', 'l�t', 'l�w',
'l�z', 'l��', 'l��', 'l��', 'l��', 'l�a', 'l�b', 'l�e',
'l�o', 'l�s', 'l�u', 'l�y', 'l��', 'l��', 'l��', 'l�l',
'l�m', 'l�n', 'l�p', 'l�r', 'l�w', 'l��', 'l�l', 'l�n',
'l�a', 'l�b', 'l�c', 'l�e', 'l�m', 'l�n', 'l�o', 'l�u',
'l�y', 'l�z', 'l��', 'l��', 'l��', 'l��', 'l�c', 'l�m',
'l�w', 'l�z', 'l�', 'l�b', 'l�c', 'l�d', 'l�g', 'l�k',
'l�l', 'l�p', 'l�s', 'l�t', 'l�z', 'l�', 'l�', 'l�',
'l�', 'l��', 'l�c', 'l�m', 'l�z', 'l�', 'l�b', 'l�c',
'l�d', 'l�g', 'l�j', 'l�k', 'l�s', 'l�t', 'l�w', 'l�z',
'l�', 'l�', 'l��', 'm�c', 'm�d', 'm�k', 'm�t', 'm�z',
'm��', 'm��', 'm�a', 'm�o', 'm�y', 'm��', 'm�c', 'm�k',
'm�m', 'm�z', 'm��', 'm�a', 'm�e', 'm�o', 'm�y', 'm��',
'm��', 'm�p', 'm�c', 'm�d', 'm�k', 'm�s', 'm�t', 'm�z',
'm�', 'm�', 'm��', 'm�c', 'm�d', 'm�g', 'm�j', 'm�k',
'm�l', 'm�r', 'm�w', 'm�z', 'm�', 'm�', 'n�b', 'n�c',
'n�d', 'n�l', 'n�t', 'n�w', 'n�z', 'n��', 'n��', 'n��',
'n�y', 'n�c', 'n�a', 'n�c', 'n�e', 'n�k', 'n�o', 'n�u',
'n�y', 'n��', 'n��', 'n��', 'n�b', 'n�c', 'n�d', 'n�k',
'n�l', 'n�t', 'n�', 'n��', 'n�g', 'n�j', 'n�s', 'n�t',
'n�w', 'n�z', 'n�', 'o�a', 'o�b', 'o�c', 'o�d', 'o�e',
'o�f', 'o�g', 'o�h', 'o�i', 'o�j', 'o�k', 'o�l', 'o�m',
'o�n', 'o�o', 'o�p', 'o�r', 'o�s', 'o�t', 'o�u', 'o�w',
'o�y', 'o�z', 'o��', 'o��', 'o��', 'o��', 'o��', 'o��',
'o��', 'o�b', 'o�c', 'o�k', 'o�l', 'o�m', 'o�n', 'o�p',
'o�r', 'o�w', 'o�z', 'o��', 'o��', 'o�b', 'o�c', 'o�d',
'o�g', 'o�l', 'o�m', 'o�n', 'o�r', 'o�w', 'o�z', 'o��',
'o��', 'o�a', 'o�b', 'o�c', 'o�d', 'o�e', 'o�g', 'o�k',
'o�l', 'o�m', 'o�n', 'o�o', 'o�r', 'o�s', 'o�u', 'o�y',
'o�z', 'o��', 'o��', 'o��', 'o��', 'o��', 'o�b', 'o�c',
'o�k', 'o�m', 'o�p', 'o�s', 'o�w', 'o�z', 'o�', 'o�c',
'o�k', 'o�m', 'o�s', 'o�z', 'o�', 'o�w', 'p�c', 'p�g',
'p�k', 'p�s', 'p�t', 'p�a', 'p�b', 'p�c', 'p�e', 'p�k',
'p�o', 'p�s', 'p�u', 'p�y', 'p��', 'p��', 'p��', 'p�c',
'p�a', 'p�e', 'p�c', 'p�m', 'p�z', 'p�', 'p�c', 'p�d',
'p�k', 'p�p', 'p�s', 'p�t', 'p�d', 'p�j', 'p�k', 'p�l',
'p�r', 'p�t', 'p�w', 'p�z', 'p�', 'p�', 'r�b', 'r�c',
'r�d', 'r�g', 'r�k', 'r�p', 'r�s', 'r�t', 'r�z', 'r��',
'r��', 'r��', 'r�a', 'r�b', 'r�e', 'r�o', 'r�s', 'r�u',
'r�y', 'r��', 'r��', 'r��', 'r�c', 'r�n', 'r�w', 'r��',
'r�c', 'r�l', 'r�m', 'r�n', 'r�z', 'r��', 'r�a', 'r�c',
'r�e', 'r�k', 'r�l', 'r�m', 'r�n', 'r�o', 'r�u', 'r�y',
'r�z', 'r��', 'r��', 'r��', 'r��', 'r�a', 'r�c', 'r�d',
'r�f', 'r�i', 'r�k', 'r�l', 'r�m', 'r�n', 'r�p', 'r�t',
'r�w', 'r�z', 'r�', 'r�b', 'r�c', 'r�d', 'r�g', 'r�k',
'r�n', 'r�p', 'r�s', 'r�t', 'r�z', 'r�', 'r�', 'r��',
'r�c', 'r�m', 'r�z', 'r�', 'r�b', 'r�c', 'r�d', 'r�g',
'r�i', 'r�j', 'r�l', 'r�s', 'r�t', 'r�w', 'r�z', 'r�',
'r�', 'r�', 'r��', 's�c', 's�d', 's�g', 's�s', 's�z',
's��', 's�a', 's�b', 's�e', 's�o', 's�s', 's�u', 's�y',
's��', 's��', 's��', 's�n', 's�a', 's�c', 's�e', 's�m',
's�o', 's�z', 's��', 's�c', 's�d', 's�k', 's�m', 's�s',
's�u', 's�z', 's�', 's�c', 's�d', 's�k', 's�p', 's�c',
's�m', 's�z', 's�', 's�b', 's�d', 's�j', 's�l', 's�w',
's�', 't�c', 't�d', 't�g', 't�p', 't�z', 't��', 't�a',
't�b', 't�e', 't�o', 't�s', 't�u', 't�y', 't��', 't��',
't��', 't�a', 't�e', 't�b', 't�c', 't�d', 't�g', 't�k',
't�p', 't�s', 't�t', 't�z', 't�', 't��', 't�g', 't�j',
't�l', 't�p', 't�r', 't�w', 't�z', 't�', 't�', 'u�a',
'u�b', 'u�c', 'u�e', 'u�g', 'u�k', 'u�l', 'u�m', 'u�o',
'u�t', 'u�u', 'u�y', 'u��', 'u��', 'u��', 'u��', 'u�c',
'u�k', 'u�l', 'u�m', 'u�n', 'u�p', 'u�r', 'u�t', 'u�w',
'u�z', 'u��', 'u��', 'u�c', 'u�d', 'u�k', 'u�l', 'u�m',
'u�n', 'u�z', 'u��', 'u��', 'u�a', 'u�b', 'u�c', 'u�d',
'u�e', 'u�g', 'u�k', 'u�l', 'u�m', 'u�n', 'u�o', 'u�p',
'u�r', 'u�s', 'u�u', 'u�y', 'u�z', 'u��', 'u��', 'u��',
'u��', 'u�c', 'u�k', 'u�m', 'u�z', 'u�', 'u�c', 'u�k',
'u�m', 'u�s', 'u�z', 'u�', 'u��', 'u�w', 'v�w', 'w�b',
'w�c', 'w�d', 'w�g', 'w�k', 'w�p', 'w�s', 'w�t', 'w�w',
'w�z', 'w��', 'w��', 'w�a', 'w�e', 'w�o', 'w�u', 'w�y',
'w��', 'w��', 'w�c', 'w�l', 'w�n', 'w�p', 'w�r', 'w�w',
'w�a', 'w�d', 'w�e', 'w�y', 'w��', 'w��', 'w�w', 'w�b',
'w�c', 'w�d', 'w�g', 'w�k', 'w�s', 'w�t', 'w�z', 'w�',
'w�', 'w�c', 'w�d', 'w�g', 'w�i', 'w�j', 'w�l', 'w�m',
'w�r', 'w�w', 'w�z', 'w�', 'w�', 'w�', 'x�w', 'y�a',
'y�b', 'y�c', 'y�e', 'y�g', 'y�k', 'y�o', 'y�u', 'y�y',
'y�z', 'y��', 'y��', 'y��', 'y��', 'y�c', 'y�k', 'y�l',
'y�m', 'y�n', 'y�p', 'y�r', 'y�w', 'y�z', 'y��', 'y��',
'y�c', 'y�l', 'y�m', 'y�n', 'y�z', 'y��', 'y��', 'y�a',
'y�b', 'y�c', 'y�e', 'y�k', 'y�l', 'y�m', 'y�n', 'y�o',
'y�p', 'y�r', 'y�s', 'y�u', 'y�w', 'y�y', 'y�z', 'y��',
'y��', 'y��', 'y��', 'y��', 'y�c', 'y�m', 'y�u', 'y�w',
'y�z', 'y�', 'y�c', 'y�k', 'y�m', 'y�s', 'y�z', 'y�',
'y�w', 'z�b', 'z�c', 'z�d', 'z�g', 'z�k', 'z�l', 'z�p',
'z�s', 'z�t', 'z�w', 'z�z', 'z��', 'z��', 'z��', 'z��',
'z��', 'z�a', 'z�b', 'z�e', 'z�k', 'z�o', 'z�s', 'z�u',
'z�y', 'z�z', 'z��', 'z��', 'z�c', 'z�l', 'z�m', 'z�n',
'z�p', 'z�r', 'z�w', 'z�a', 'z�e', 'z�o', 'z�u', 'z�y',
'z��', 'z��', 'z��', 'z�w', 'z�b', 'z�c', 'z�d', 'z�g',
'z�k', 'z�l', 'z�p', 'z�s', 'z�t', 'z�z', 'z�', 'z�',
'z�', 'z�', 'z��', 'z�a', 'z�c', 'z�e', 'z�i', 'z�m',
'z�o', 'z�z', 'z�', 'z�', 'z��', 'z�d', 'z�g', 'z�l',
'z�r', 'z�s', 'z�w', 'z�z', 'z�', 'z�', '��g', '��b',
'��e', '��s', '��c', '��k', '��l', '��m', '��n', '��z',
'���', '���', '��c', '��l', '���', '��a', '��c', '��e',
'��k', '��l', '��m', '��n', '��o', '��p', '��s', '��u',
'��y', '��z', '���', '���', '���', '���', '��c', '��m',
'��z', '��', '��b', '��c', '��d', '��g', '��k', '��s',
'��t', '��z', '���', '��a', '��b', '��e', '��o', '��s',
'��u', '��y', '���', '���', '���', '��l', '��m', '��n',
'��p', '��r', '��w', '��l', '��n', '��a', '��e', '��o',
'��u', '��y', '���', '���', '���', '��c', '��m', '��w',
'��z', '��', '��b', '��c', '��d', '��g', '��k', '��p',
'��s', '��t', '��z', '��', '��', '��c', '��m', '��z',
'��', '��b', '��c', '��d', '��g', '��j', '��k', '��s',
'��t', '��w', '��z', '��', '��', '���', '��o', '��e',
'��c', '��d', '��k', '��m', '��s', '��u', '��z', '��',
'��c', '��m', '��z', '��', '��e', '��a', '��c', '��e',
'��i', '��m', '��o', '��z', '��', '��', '���', '��c',
'��d', '��l', '��p', '��t', '��w', '���', '���', '��a',
'��e', '��o', '��y', '���', '��e', '��o', '��c', '��l',
'��t', '��', '���', '��c', '��m', '��z', '��', '��g',
'��l', '��r', '��w', '��', '�e', '�a', '�o', '�y',
'�c', '�l', '�m', '�n', '�z', '궿', '��', '�b',
'�c', '�l', '�m', '�n', '�r', '�z', '꼿', '�a',
'�c', '�e', '�k', '�l', '�m', '�n', '�o', '�p',
'�s', '�u', '�y', '�z', '꿱', '꿿', '��', '��',
'��c', '��d', '��k', '��m', '��s', '��z', '��', '�e',
'�a', '�b', '�c', '�d', '�e', '�f', '�g', '�h',
'�i', '�j', '�k', '�l', '�m', '�n', '�o', '�p',
'�r', '�s', '�t', '�u', '�w', '�y', '�z', '�',
'�', '�', '�', '��', '��', '��', '�b', '�c',
'�l', '�m', '��', '�b', '�c', '�d', '�m', '�n',
'�z', '�', '��', '�a', '�b', '�c', '�d', '�e',
'�k', '�m', '�n', '�o', '�u', '�y', '�z', '�',
'�', '��', '��', '��c', '��m', '��z', '��'])

def possible_plwords(word):
	# polish diacritical characters (PDC) that may appear
	# at begin and end of word
	allowed_at_begin = '��󶿼'
	allowed_at_end   = '���񶿼'

	# latin characters used instead of PDC
	platin = 'acelnosz'

	# platin -> PDC
	repl   = {'a':'a�',
	          'c':'c�',
		  'e':'e�',
		  'l':'l�',
		  'n':'n�',
		  'o':'o�',
		  's':'s�',
		  'z':'z��'}

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
		sugg_list = ['Nie uda�o si� znale�� podobnego s�owa w s�owniku']
	
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
					print "R - zamie�; A - zamie� wszystkie; A <numer> - zamie� wszystkie na s�owo z listy"
				else:
					print "R - zamie�; A - zamie� wszystkie"
				print "I - ignoruj wszystkie"
				print "X - nie pokazuj tego menu"
				print "C - kontynnuj zamian� bez interakcji"
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
						answer = QueryString("Zamie� wszystkie wyst�pienia '%s' na: " % substring).strip()
						if answer != '':
							if len(suggestions) > 0 and not speller.check(answer):
								if QuestionYesNo("Podane s�owo nie znajduje si� w s�owniku. Czy pomimo to u�y� go", True, False):
									return (answer, REPLACE_ALL)
							else:
								return (answer, REPLACE_ALL)
					except KeyboardInterrupt:
						pass
				shift, delim = calc_size()
			elif input == 'R':
				try:
					answer = QueryString("Zamie� '%s' na: " % substring).strip()
					if answer != '':
						if len(suggestions) > 0 and not speller.check(answer):
							if QuestionYesNo("Podane s�owo nie znajduje si� w s�owniku. Czy pomimo tego u�y� go?", True, False):
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

-v, --version   wersja programu

-n              tryb nieinteraktywny

-H,--html       przetwarzanie pliku HTML

-q,--quiet      program nie wypisuje nic na ekranie
                u�ycie tej opcji implikuje tryb nieinteraktywny

-a,--all        sprawdzane s� r�wnie� s�owa zawieraj�ca polskie znaki

-s,--spell      s�owa zawieraj�ce polskie znaki s� sprawdzane przez
                aspella (w�wczas program dzia�a podobnie do aspell check)
				
-d              pyta o pisowni� w przypadku, gdy nie uda�o si�
                znale�� podobnych s��w w s�owniku
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
			Info("Tworz� katalog '%s'..." % options['cache_path'], False)
			os.makedirs(options['cache_path'])
			Info("ok")
		except OSError:
			e = sys.exc_info()
			Die('%s: %s' % (str(e[0]), str(e[1])))
	elif not os.path.isdir(options['cache_path']):
		Die("'%s' nie jest katalogiem." % options['cache_path'])
	
	if len(FileList) == 0:
		Die("Podaj nazw� pliku.")
	
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
		Die('Nie mog� zmieni� ustawi� na j�zk polski.')
	
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
				info.append('s�ownika (%s)' % getsize(path1))

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
		probably_pl	= re.compile(r'^[�������ʣ�Ӧ��A-Za-z]+$')
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
			ans = Question("Skasowa� s�owa zamieniane lub ignorowane?", tmp, 'always', False)
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
			if QuestionYesNo('Przerwa� przetwarzanie plik�w', False, False):
				Die("Przerwany")
		except IOError:
			e = sys.exc_info()
			Info('%s: %s' % (str(e[0]), str(e[1])))

		try:
			Terminal.settitle("Sprawdzanie pliku '%s'" % filename)
			CheckFile()
		except (AbortProgram, KeyboardInterrupt):
			if QuestionYesNo('Zako�czy� program bez zapisywania pami�ci podr�cznej', False, False):
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
				Info("Zmieniony tekst zosta� zachowany w pliku '%s'." % tmpname)
				continue
			
			try:
				os.rename(tmpname, filename)
			except OSError:
				os.rename(filename+'~', filename)
				e = sys.exc_info()
				Info('%s: %s' % (str(e[0]), str(e[1])))
				Info("Zmieniony tekst zosta� zachowany w pliku '%s'." % tmpname)

			Info("ok", flush=True)
	
	path = options['cache_path'] + os.sep + options['cache_dictionary']
	Info("Zapisywanie s�ownika do '%s'..." % path, False)
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
