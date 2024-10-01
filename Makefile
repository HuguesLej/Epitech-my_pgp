BINARY = my_pgp

SRC = src
ALGO = $(SRC)/algo
UTILS = $(SRC)/utils

SOURCE = $(SRC)/main.py
SOURCE += $(SRC)/arg_handler.py
SOURCE += $(ALGO)/xor.py
SOURCE += $(UTILS)/little_endian.py

PYINSTALLER = pyinstaller

all: build

build:
	$(PYINSTALLER) --onefile --name $(BINARY) --distpath ./ $(SOURCE)
	rm -f $(BINARY).spec

clean:
	# Nettoie les fichiers temporaires générés par PyInstaller
	rm -rf build *.spec

fclean: clean
	rm -f $(BINARY)

re: fclean all

.PHONY: build clean fclean re
