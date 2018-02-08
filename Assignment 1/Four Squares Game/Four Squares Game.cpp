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
		else if ((i + _size) < _size2 && _game[i] != "X" && _game[i + _size] != "X") //vertical stick
			return true;
	}
	return false;
}

int* getvalidmove(char turn) {
	int* ans = new int[2];
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
		catch (...) {
			std::cout << "Invalid input, please re-enter in this format \"x,y\": \n";
			continue;
		}
		if (num1 > num2) {
			int temp = num2;
			num2 = num1;
			num1 = temp;
		}
		if (!((num1 > 0 && num2 > 0) && (num1 <= _size2 && num2 <= _size2) &&
			((num2 - num1 == _size) || (num2 - num1 == 1 && num1 % _size != 0)))) {
			std::cout << "Unallowed move, please re-enter: \n";
			continue;
		}
		if (_game[num1 - 1] == "X" || _game[num2 - 1] == "X") {
			std::cout << "The square is covered, please re-enter: \n";
			continue;
		}
		ans[0] = num1;
		ans[1] = num2;
		return ans;
	}
}

int* getAImove(int x, int y) {
	int* ans = new int[2];
	ans[0] = _size2 - x + 1;
	ans[1] = _size2 - y + 1;
	std::cout << "Hmm.... I will do " << ans[0] << ", " << ans[1] << "\n";
	return ans;
}

void coregame(bool human) {
	initializeboard();
	std::cout << "--------------------------------------\n";

	char turn = '0';
	int* ans ;
	while (checkpossible()) {
		printboard();
		if (turn == '1')
			turn = '2';
		else
			turn = '1';
		if (human == false && turn == '2')
			ans = getAImove(ans[0], ans[1]);
		else
			ans = getvalidmove(turn);

		_game[ans[0] - 1] = "X";
		_game[ans[1] - 1] = "X";
	}
	printboard();
	std::cout << "--------------------------------------\n";
	if (human == false && turn == '2')
		std::cout << "Hahaha! I win. Nobody can beat Mr. perfect AI :D\n";
	else
		std::cout << "Player " << turn << " is the winner!!! Congrats!!! :D\n";
}

int main() {
	std::cout << "Two squares game:\n\tThis game is played on a board of 4 x 4 squares. Two players take turns;\n";
	std::cout << "each of them takes turn to place a rectangle(that covers two squares) on the board, covering\n";
	std::cout << "any 2 squares. Only one rectangle can be on a square. A square cannot be covered twice. The\n";
	std::cout << "last player who can place a card on the board is the winner. By megadardery : D:\n\n";

	std::cout << "How many players are going to play ? \"1/2\" : \n";

	char gamestate;
	gamestate = std::cin.get();
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

	while (gamestate == '1' || gamestate == '2') {
		if (gamestate == '2')
			coregame(true);
		else
			coregame(false);

		std::cout << "Play again? How many players? \"1/2\": \n";
		gamestate = std::cin.get();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
	}
}
