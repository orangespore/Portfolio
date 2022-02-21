#include <iostream>
#include <string>
using namespace std;

template <typename T>

class queue {

private:

	struct node {
		T data;
		node* nxt;
	};
	node* q_front; // 저장된 데이터 (체인)의 맨앞 주소값을 저장
	node* q_back; // 저장된 데이터의 맨 뒤 주소값을 저장
	int q_size;

public:
	queue() {
		q_front = nullptr;
		q_back = nullptr;
		q_size = 0;
	}
	~queue() {
		while (!empty()) {
			pop();
		}
	}
	void push(T input) {
		node* new_node = new node();
		new_node->data = input;
		new_node->nxt = nullptr;
		if (q_size == 0) {
			q_front = q_back = new_node;
		}
		else {
			q_back->nxt = new_node;
			q_back = new_node;
		}
		q_size += 1;
	}
	void pop() {
		node* cur_front = q_front;
		q_front = q_front->nxt;
		free(cur_front);
		q_size -= 1;
	}
	int size() { // 현재 큐에 저장된데이터의 개수를 반환
		return q_size;
	}
	bool empty() {
		if (q_size == 0) { // if(front == nullptr)
			return true;
		}
		else {
			return false;
		}
		// return !q_size;
	}
	T front() {
		return q_front->data;
	}
	T back() {
		return q_back->data;
	}
};

int main() {

	queue<int> q;
	
	q.push(5);
	q.push(1);
	q.push(3);
	q.push(4);
	q.push(7);
	q.push(8);
	q.push(7);

	cout << q.size() << "\n";

	q.pop();
	q.pop();
	q.pop();
	q.pop();

	cout << q.size() << "\n";

	while (!q.empty()) {
		cout << q.front() << "\n";
		q.pop();
	}

}

/*

7
3
7
8
7

*/