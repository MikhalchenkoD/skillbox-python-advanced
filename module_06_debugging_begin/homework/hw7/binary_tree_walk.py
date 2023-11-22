"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    node_dict = {}

    with open(path_to_log_file, 'r') as log_file:
        for line in log_file:
            log_entry = line.strip().split(':')
            log_type = log_entry[0]
            log_message = log_entry[1]

            if log_type == "DEBUG" and "left" in log_message:
                node_info = log_message.split("<BinaryTreeNode[")[1].split("]>")[0]
                node_num = int(node_info.split(' ')[0])
                node = node_dict.get(node_num)

                if not node:
                    node = BinaryTreeNode(node_num)
                    node_dict[node_num] = node

            elif log_type == "DEBUG" and "right" in log_message:
                node_info = log_message.split("<BinaryTreeNode[")[1].split("]>")[0]
                node_num = int(node_info.split(' ')[0])
                node = node_dict.get(node_num)

                if not node:
                    node = BinaryTreeNode(node_num)
                    node_dict[node_num] = node

    for node_num, node in node_dict.items():
        left_child_num = 2 * node_num
        right_child_num = 2 * node_num + 1
        node.left = node_dict.get(left_child_num)
        node.right = node_dict.get(right_child_num)

    return node_dict[1]

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )
    root = get_tree(7)
    walk(root)
    print(restore_tree('walk_log_1.txt'))