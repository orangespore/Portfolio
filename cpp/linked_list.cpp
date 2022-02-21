#include <iostream>

using namespace std;


// vector<int>
// vector<string> 
template <typename T>

class Linked_list {

private:
	// 클래스 내부에서 접근 가능한 함수 또는 변수
	struct node {
		T data;
		node* nxt;
	};

	node* head;
	node* tail;

public:
	// 클래스 외부에서 접근 가능한 함수 또는 변수 
	Linked_list() { // 생성자 
		// 자동으로 실행되는 부분
		tail = nullptr;
		head = nullptr;
	}
	~Linked_list() { // 소멸자
		node* cur = head;
		while (cur != nullptr) {
			node* remove = cur;
			cur = cur->nxt;
			free(remove);
		}
		head = tail = nullptr;
	}
	void push_back(T input) {
		node* new_node = new node();
		new_node->data = input;
		new_node->nxt = nullptr;

		if (tail == nullptr) { // 처음 데이터가 들어가는 부분
			head = new_node;
			tail = new_node;
		}
		else {
			tail->nxt = new_node;
			tail = new_node;
		}
	}

	void print() {
		node* cur_node = head;
		while (cur_node != nullptr) {
			cout << cur_node->data << " ";
			cur_node = cur_node->nxt;
		}
	}

	void pop_back() { // 맨 뒤 (tail)의 노드를 삭제한다
		if (tail != nullptr) {
			node* pre = nullptr; // 내가 찾은 노드의 이전 노드
			node* cur = head; // 내가 찾은 노드
			while (cur->nxt != nullptr) {
				pre = cur;
				cur = cur->nxt;
			}
			// cur 가 tail 노드, pre은 tail 이전 노드가 된다.
			
			free(cur);
			if (pre == nullptr) {
				head = tail = nullptr;
			}
			else {
				pre->nxt = nullptr;
				tail = pre;
			}
		}
	}
};

int main() {
	{
		Linked_list<int> a;
		a.push_back(3);
		a.push_back(5);
		a.push_back(8);
		a.push_back(1);
		a.push_back(2);
		a.push_back(10);
		a.push_back(23);
		a.pop_back();
		a.pop_back();
		a.pop_back();
		a.print();
	}
	// 
}