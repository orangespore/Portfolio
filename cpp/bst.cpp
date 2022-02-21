#include <iostream>
using namespace std;

class BST {
private:
	struct node {
		int key;
		node* left;
		node* right;
	};

	node* root;

public:

	BST() {
		root = nullptr;
	};
	~BST() {};

	node* insert_Helper(node* cur_node, int input) {
		if (cur_node == nullptr) {
			node* new_node = new node();
			new_node->key = input;
			new_node->left = nullptr/*fill your code*/;
			new_node->right = nullptr/*fill your code*/;
			return new_node;
		}

		if (cur_node->key > input/*fill your code*/) {
			cur_node->left = input/*fill your code*/;
		}
		else {
			cur_node->right = input/*fill your code*/;
		}
		return cur_node;
	}

	void insert(int input) {
		// root 부터 탐색을 진행하여, input이 들어갈 위치에 새로운 노드를 만들어서
		// 데이터를 저장하겠다.
		root = insert_Helper(/*fill your code*/, /*fill your code*/);
	}


	bool find_Helper(node* cur_node, int target) {
		if (cur_node == /*fill your code*/) {
			return false;
		}
		if (cur_node->key == /*fill your code*/) {
			return true;
		}

		if (cur_node->key > /*fill your code*/) {
			return /*fill your code*/;
		}
		else {
			return /*fill your code*/;
		}

	}

	bool find(int target) {
		return find_Helper(root, target);
	}


	void inorder_Helper(node* cur_node) {
		if (cur_node->left != nullptr) {
			inorder_Helper(cur_node->left);
		}
		cout << cur_node->key << " ";
		if (cur_node->right != nullptr) {
			inorder_Helper(cur_node->right);
		}
	}

	void inorder() {
		inorder_Helper(root);
	}



	node* remove_Helper(node* cur_node, node * parent, int target) {

		if (cur_node == nullptr) {
			return cur_node;
		}

		if (cur_node->key == target) {
			// 삭제~
			if (cur_node->left == nullptr && cur_node->right == nullptr) {
				free(cur_node);
				return nullptr;
			}
			else if(cur_node->left == nullptr){// 오른쪽 자식만 존재하는 경우
				node* right = cur_node->right;
				if (parent->left == cur_node) {
					parent->left = right;
				}
				else {
					parent->right = right;
				}
				free(cur_node);
				return right;
			}
			else if (cur_node->right == nullptr) { //왼쪽 자식만 존재하는 경우
				node* left = cur_node->left;
				if (parent->left == cur_node) {
					parent->left = left;
				}
				else {
					parent->right = left;
				}
				free(cur_node);
				return left;
			}
			else {
				// 양쪽 자식이 모두 존재하는 경우
				node* right_min = cur_node->right;
				while (right_min->left != nullptr) {
					right_min = right_min->left;
				}
				cur_node->key = right_min->key;
				cur_node->right = remove_Helper(cur_node->right, cur_node, right_min->key);
				return cur_node;
			}
			//node* left_max = cur_node->left;
			//node* right_min = cur_node->right;
		

			//if (left_max != nullptr) {
			//	while (left_max->right != nullptr) {
			//		left_max = left_max->right;
			//	}
			//	cur_node->key = left_max->key;
			//	cur_node->left = remove_Helper(cur_node->left, cur_node, left_max->key);
			//}
			//else if (right_min != nullptr) {
			//	while (right_min->left != nullptr) {
			//		right_min = right_min->left;
			//	}
			//	cur_node->key = right_min->key;
			//	cur_node->right = remove_Helper(cur_node->right, cur_node, right_min->key);
			//}
			//else { // 자식이 없는경우 
			//	free(cur_node);
			//	return nullptr;
			//}
			//return cur_node;
		}
		else if (cur_node->key > target) {
			cur_node->left = remove_Helper(cur_node->left, cur_node, target);
		}
		else {
			cur_node->right = remove_Helper(cur_node->right, cur_node, target);
		}
		return cur_node;
	}

	void remove(int target) {
		root = remove_Helper(root, nullptr, target);
	}

};

void search(BST tree, int value) {
	if (tree.find(value)) {
		cout << " 값 " << value <<" 가 존재함\n";
	}
	else {
		cout << " 값 " << value << " 가 존재하지 않음\n";
	}
}



int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(0); cout.tie(0);

	BST tree;
	tree.insert(6);
	tree.insert(1);
	tree.insert(4);
	tree.insert(7);
	tree.insert(10);
	tree.insert(8);
	tree.insert(9);
	tree.insert(5);
	tree.insert(-3);
	tree.insert(13);

	tree.inorder();
	cout << "\n";

	search(tree, 2);
	search(tree, 4);
	search(tree, 13);
	search(tree, 12);
	search(tree, -3);

	tree.remove(4);
	tree.remove(13);
	tree.remove(-3);

	cout << "\n";

	search(tree, 2);
	search(tree, 4);
	search(tree, 13);
	search(tree, 12);
	search(tree, -3);

	tree.inorder();
	cout << "\n";

}
