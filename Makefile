BIN = my_pgp

SRC = src

MAIN = $(SRC)/main.py

all: build

build:
	@cp $(MAIN) $(BIN)
	@chmod +x $(BIN)
	@echo -e "\033[1;36m[$(BIN)]: Successfully build\033[0m"

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@echo -e "\033[1;33m[$(BIN)]: Cache files successfully cleaned\033[0m"

fclean: clean
	@rm -f $(BIN)
	@echo -e "\033[1;33m[$(BIN)]: Binary file successfully cleaned\033[0m"

re: fclean all

.PHONY: all build clean fclean re
