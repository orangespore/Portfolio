#include <iostream>
#include <queue>
#include <string>
#include <algorithm>

using namespace std;

// ~~~ heapify


class _heap {
public:
	int arr[101];
	int _size;
	_heap() {
		_size = 10;
	}
	~_heap() {

	}

	void heapify() {
		//for (int i = _size / 2; i >= 1; i--) {
		//	upstream(i);
		//}
		for (int i = _size; i > _size / 2; i--) {
			downstream(i);
		}
	}
	void upstream(int index) {
		
		int child = index;
		int parent = child / 2;

		while (child > 1) {
			if (arr[child] > arr[parent]) {
				swap(arr[child], arr[parent]);
				child = parent;
				parent = child / 2;
			}
			else {
				break;
			}
		}
	}
	void downstream(int index) {

		int parent = index;
		int child = parent * 2; // 왼쪽 자식으로 일단 초기화 

		while (child <= _size) {
			if (child + 1 <= _size && arr[child] < arr[child + 1]) {
				// 만약에 오른쪽 자식이 존재하면서
				// 왼쪽자식보다 값이 큰경우
				child = child + 1;
			}
			// parent 와 왼쪽과 오른쪽 중 더 큰 자식과 비교
			if (arr[parent] < arr[child]) {
				swap(arr[child], arr[parent]);
				parent = child;
				child = parent * 2;
			}
			else {
				break;
			}
		}
	}
	bool empty() {
		return (_size == 0);
	}
	void pop() {
		arr[1] = arr[_size];
		_size -= 1;

		int parent = 1;
		int child = parent * 2; // 왼쪽 자식으로 일단 초기화 

		while (child <= _size) {
			if (child + 1 <= _size && arr[child] < arr[child + 1]) {
				// 만약에 오른쪽 자식이 존재하면서
				// 왼쪽자식보다 값이 큰경우
				child = child + 1;
			}
			// parent 와 왼쪽과 오른쪽 중 더 큰 자식과 비교
			if (arr[parent] < arr[child]) {
				swap(arr[child], arr[parent]);
				parent = child;
				child = parent * 2;
			}
			else {
				break;
			}
		}
	}
	int top() {
		return arr[1];
	}
};

int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	_heap h;
	for (int i = 1; i <= 10; i++) {
		h.arr[i] = rand() % INT_MAX;
	}
	for (int i = 1; i <= 10; i++) {
		cout << h.arr[i] << " ";
	}
	cout << "\n";
	h.heapify();
	while (!h.empty()) {
		cout << h.top() << " ";
		h.pop();
	}

}

