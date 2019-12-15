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
3. polski słownik do aspella; polecam http://www.sjp.pl,
   a jeśli używasz Debiana, zainstaluj pakiet ``aspell-pl``
4. rozszerzenie do Pythona o nazwie `aspell-python`__
5. trochę miejsca w ``$HOME``

__ ../aspell-python/

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
