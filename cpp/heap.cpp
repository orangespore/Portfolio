#include <iostream>
#include <queue>
#include <string>

using namespace std;

class maxheap {

private:
	int arr[200001];
	int _size;

public:
	maxheap() {
		_size = 0;
	}
	~maxheap() {

	}
	void push(int input) {
		_size += 1;
		arr[_size] = input;

		int child = _size;
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
	int top() {
		return arr[1];
	}

	void pop() {
		arr[1] = arr[_size];
		_size -= 1;

		int parent = 1;
		int child = parent * 2; // 왼쪽 자식으로 일단 초기화 

		while (child <= _size) {
			if (child + 1 <= _size && arr[child] < arr[child+1]) { 
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
		if (_size == 0) {
			return true;
		}
		else {
			return false;
		}
	}
	
};

int main() {

	ios_base::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);

	maxheap mh;
	int n;
	cin >> n;
	for (int i = 0; i < n; i++) {
		int num;
		cin >> num;
		mh.push(-num);
	}

	while (!mh.empty()) {
		cout << -mh.top() << "\n";
		mh.pop();
	}

}

