#include <iostream>
#include <string>
#include <limits>

const int _size = 4;
const int _size2 = _size * _size;

std::string* _game;

void initializeboard() {
	_game = new std::string[_size2];
	for (int i = 0; i < _size2; ++i) {
		_game[i] = std::to_string(i + 1);
	}
}

void printboard() {
	std::cout << '\n';
	for (int i = 0; i < _size2; ++i) {
		std::cout << _game[i] << '\t';
		if ((i + 1) % _size == 0)
			std::cout << '\n';
	}
	std::cout << '\n';
}

bool checkpossible() {
	for (int i = 0; i < _size2; ++i) {
		if ((i + 1) % _size != 0 && (i + 1) < _size2 && _game[i] != "X" && _game[i + 1] != "X") //horizontal stick
			return true;
		else if ((i + 4) < _size2 && _game[i] != "X" && _game[i + 4] != "X") //vertical stick
			return true;
	}
	return false;
}

int main(){
	std::cout << "Two squares game:\n\tThis game is played on a board of 4 x 4 squares. Two players take turns;\n";
	std::cout << "each of them takes turn to place a rectangle(that covers two squares) on the board, covering\n";
	std::cout << "any 2 squares. Only one rectangle can be on a square. A square cannot be covered twice. The\n";
	std::cout << "last player who can place a card on the board is the winner. By megadardery : D:\n\n";

	char _gamestate = 'y';

	while (_gamestate == 'y') {
		initializeboard();
		std::cout << "--------------------------------------\n";

		char turn = '0';

		while (checkpossible()) {
			printboard();
			if (turn == '1')
				turn = '2';
			else
				turn = '1';

			std::string raw;
			std::cout << "Player " << turn << ", Enter your next move \"x, y\": \n";

			while (true) {
				std::getline(std::cin, raw);
				std::size_t res = raw.find(',');
				if (res == std::string::npos) {
					std::cout << "Invalid input, please re-enter in this format \"x,y\": \n";
					continue;
				}
				int num1, num2;
				try {
					num1 = stoi(raw.substr(0, res));
					num2 = stoi(raw.substr(res + 1, std::string::npos));
				}
				catch (...){
					std::cout << "Invalid input, please re-enter in this format \"x,y\": \n";
					continue;
				}
				if (num1 > num2) {
					int temp = num2;
					num2 = num1;
					num1 = temp;
				}
				if (!((num1 > 0 && num2 > 0) && (num1 <= _size2 && num2 <= _size2) &&
					((num2 - num1 == _size) || (num2 - num1 == 1 && num1 % _size != 0))))  {
					std::cout << "Unallowed move, please re-enter: \n";
					continue;
				}
				if (_game[num1 - 1] == "X" || _game[num2 - 1] == "X") {
					std::cout << "The square is covered, please re-enter: \n";
					continue;
				}
				_game[num1 - 1] = "X";
				_game[num2 - 1] = "X";
				break;
			}
		}
		printboard();
		std::cout << "--------------------------------------\n";
		std::cout << "Player " << turn << " is the winner!!! Congrats!!! :D\n";

		std::cout << "Play again? \"y/n\": \n";
		_gamestate = std::cin.get();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

	}

}
