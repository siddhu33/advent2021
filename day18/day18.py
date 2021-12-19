from ast import literal_eval
import copy
import itertools


class Node(object):
    def __init__(self, level=0, parent=None, direction=""):
        self.left = None
        self.right = None
        self.level = level
        self.parent = parent
        self.direction = direction

    @classmethod
    def init_from_pair(cls, pair, level=0, parent=None, direction=""):
        l, r = pair[0], pair[1]
        node = cls(level=level, parent=parent, direction=direction)
        node.left = (
            cls.init_from_pair(l, level + 1, parent=node, direction="left")
            if isinstance(l, list)
            else l
        )
        node.right = (
            cls.init_from_pair(r, level + 1, parent=node, direction="right")
            if isinstance(r, list)
            else r
        )
        return node

    def __str__(self):
        return f"Node({self.list_print()})"

    def __repr__(self):
        return self.__str__()

    def node_print(self, delim=" "):
        if self.level == 0:
            print(f"{delim*self.level}Node{self.level}:")
        if isinstance(self.left, int):
            print(f"{delim*self.level}{self.left}")
        else:
            self.left.node_print(delim)
        if isinstance(self.right, int):
            print(f"{delim*self.level}{self.right}")
        else:
            self.right.node_print(delim)

    def list_print(self):
        out = ["["]
        if self.level >= 4:
            out.insert(0, "E")
        if isinstance(self.left, int):
            out.append(str(self.left))
        else:
            out.append(self.left.list_print())
        out.append(",")
        if isinstance(self.right, int):
            out.append(str(self.right))
        else:
            out.append(self.right.list_print())
        out.append("]")
        return "".join(out)

    def magnitude(self):
        if isinstance(self.left, int):
            l = self.left
        else:
            l = self.left.magnitude()

        if isinstance(self.right, int):
            r = self.right
        else:
            r = self.right.magnitude()
        return 3 * l + 2 * r


def raise_level(node):
    node.level += 1
    if not isinstance(node.left, int):
        raise_level(node.left)
    if not isinstance(node.right, int):
        raise_level(node.right)


def join_nodes(a, b):
    new_parent = Node()
    new_parent.left = a
    a.direction = "left"
    new_parent.right = b
    b.direction = "right"
    a.parent = new_parent
    b.parent = new_parent
    raise_level(a)
    raise_level(b)
    return new_parent


def push_node(parent_node, tree, toPlace, value):
    # get next node in direction defined by 'toPlace'
    # then get opposite direction value to that in leaf
    # then add value to it.
    prev = tree
    direction_node = getattr(parent_node, toPlace)
    if isinstance(direction_node, int):
        setattr(parent_node, toPlace, getattr(parent_node, toPlace) + value)
        return
    else:
        while parent_node.level > 0 and direction_node == prev:
            prev = parent_node
            parent_node = parent_node.parent
            direction_node = getattr(parent_node, toPlace)

    if isinstance(direction_node, int):
        setattr(parent_node, toPlace, getattr(parent_node, toPlace) + value)
        return
    elif toPlace == "left" and direction_node != prev:
        while isinstance(direction_node.right, Node):
            direction_node = direction_node.right
        direction_node.right += value
    elif toPlace == "right" and direction_node != prev:
        while isinstance(direction_node.left, Node):
            direction_node = direction_node.left
        direction_node.left += value


def delete_node(parent_node, direction):
    setattr(parent_node, direction, 0)


def explode_nodes(tree, direction=""):
    if isinstance(tree, Node):
        if (
            tree.level == 4
            and isinstance(tree.left, int)
            and isinstance(tree.right, int)
        ):
            push_node(tree.parent, tree, "left", tree.left)
            push_node(tree.parent, tree, "right", tree.right)
            delete_node(tree.parent, direction)

        explode_nodes(
            tree.left,
            "left",
        )
        explode_nodes(
            tree.right,
            "right",
        )


def split_num(val):
    if val % 2 == 0:
        return val // 2, val // 2
    else:
        i = val // 2
        return i, i + 1


def split_nodes(tree):
    if isinstance(tree, Node):
        if isinstance(tree.left, int) and tree.left >= 10:
            lval, rval = split_num(tree.left)
            node = Node(level=tree.level + 1, parent=tree)
            node.left = lval
            node.right = rval
            tree.left = node
            tree.left.direction = "left"
            return True

        else:
            left = split_nodes(tree.left)
            if left:
                return left

        if isinstance(tree.right, int) and tree.right >= 10:
            lval, rval = split_num(tree.right)
            node = Node(level=tree.level + 1, parent=tree)
            node.left = lval
            node.right = rval
            tree.right = node
            tree.right.direction = "right"
            return True

        else:
            return split_nodes(tree.right)


def test_tree(tree, func):
    if isinstance(tree.left, int):
        left = func(tree, tree.left)
    else:
        left = test_tree(tree.left, func)

    if isinstance(tree.right, int):
        right = func(tree, tree.right)
    else:
        right = test_tree(tree.right, func)

    return left or right


def needs_reducing(tree):
    return test_tree(tree, lambda tree, val: tree.level > 3), test_tree(
        tree, lambda tree, val: val >= 10
    )


def reduce_nodes(tree: Node):
    explode, split = needs_reducing(tree)
    while explode or split:
        if explode:
            explode_nodes(tree)
        if split and not explode:
            split_nodes(tree)
        explode, split = needs_reducing(tree)


def part1(nums):
    start = copy.deepcopy(nums[0])
    for node in nums[1:]:
        start = join_nodes(start, copy.deepcopy(node))
        reduce_nodes(start)

    print(start.list_print())
    print(start.magnitude())


def part2(nums):
    max_mag = 0
    perms = list(itertools.permutations(nums, 2))
    for x, y in perms:
        z = join_nodes(copy.deepcopy(x), copy.deepcopy(y))
        reduce_nodes(z)
        max_mag = max(max_mag, z.magnitude())
    print(max_mag)


def main():
    nums = []
    with open("day18.txt", "r") as f:
        while l := f.readline():
            nums.append(Node.init_from_pair(literal_eval(l.strip("\n"))))

    part1(nums)
    part2(nums)


if __name__ == "__main__":
    main()
