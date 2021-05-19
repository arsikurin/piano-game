class __Deque:
    def __init__(self):
        self.items = []

    def is_empty(self) -> bool:
        return self.items == []

    def front(self):
        if not rightStack.is_empty():
            return rightStack.items[-1]
        else:
            return leftStack.items[0]

    def back(self):
        if not leftStack.items == []:
            return leftStack.items[-1]
        else:
            return rightStack.items[0]

    def pop_back(self):
        if not leftStack.is_empty():
            return self.items.pop()
        else:
            sizeRS = len(rightStack.items)
            localStack = []
            for i in range(sizeRS // 2):
                localStack.append(rightStack.items.pop())
            while not rightStack.is_empty():
                self.items.append(rightStack.items.pop())
            while not localStack == []:
                rightStack.items.append(localStack.pop())
            return self.items.pop()

    def pop_front(self):
        if not rightStack.is_empty():
            return self.items.pop()
        else:
            sizeLS = len(leftStack.items)
            localStack = []
            for i in range(sizeLS // 2):
                localStack.append(leftStack.items.pop())
            while not leftStack.is_empty():
                self.items.append(leftStack.items.pop())
            while not localStack == []:
                leftStack.items.append(localStack.pop())
            return self.items.pop()

    def push_back(self, item):
        self.items.append(item)

    def push_front(self, item):
        self.items.append(item)

    def clear(self):
        leftStack.items.clear()
        rightStack.items.clear()

    def size(self):
        return len(leftStack.items) + len(rightStack.items)


class __Queue:
    def __init__(self):
        self.items = []
        self.start = 0

    def is_empty(self):
        length = len(self.items) - Start
        return length == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        self.start += 1
        res = self.items[self.start]
        # if self.start >= len(self.items):
        #     self.items = self.items[self.start:]
        #     self.start = 0
        return res

    def front(self):
        return self.items[self.start]

    def size(self):
        return len(self.items) - self.start

    def clear(self):
        self.items.clear()
        self.start = 0


class __Stack:
    def __init__(self):
        self.items = []
        self.size = 0

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
        self.size += 1

    def pop(self):
        if not self.is_empty():
            self.size -= 1
            return self.items.pop()

    def back(self):
        if not self.is_empty():
            return self.items[-1]

    def size(self):
        return self.size

    def clear(self):
        self.items.clear()


class __Heap:
    def __init__(self):
        self.items = []

    def max_child(self, i):
        try:
            if self.items[(i - 1) * 2] < self.items[(i - 1) * 2 + 1]:
                return (i - 1) * 2 + 1
            else:
                return (i - 1) * 2
        except IndexError:
            return "break"

    def add(self, item):
        global maxHeapLen
        self.items.append(item)
        maxHeapLen += 1
        i = maxHeapLen - 1
        while True:
            if self.items[i] > self.items[i // 2]:
                tmp = self.items[i // 2]
                self.items[i // 2] = self.items[i]
                self.items[i] = tmp
            else:
                break
            i = i // 2

    def delete(self):
        global maxHeapLen
        maxi = self.items[0]
        if maxHeapLen < 2:
            maxHeapLen -= 1
            return maxi
        self.items[0] = self.items.pop()
        maxHeapLen -= 1
        i = 0
        while True:
            mc = self.max_child(i + 1)
            if mc == "break":
                break
            if self.items[i] < self.items[mc]:
                tmp = self.items[i]
                self.items[i] = self.items[mc]
                self.items[mc] = tmp
            else:
                break
            i = mc
        return maxi


leftStack = __Deque()
rightStack = __Deque()

maxHeapLen = 0
heap = __Heap()

queue = __Queue()
# Start = 0

stack = __Stack()
