class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.flat_list = []
        self.get_flat_list(self.list_of_list)
        self.index = -1

    def get_flat_list(self, list_of_list):
        for item in list_of_list:
            if isinstance(item, list):
                self.get_flat_list(item)
            else:
                self.flat_list.append(item)

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.flat_list):
            raise StopIteration
        return self.flat_list[self.index]


def test():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    try:
        test()
        print('Successfully!')
    except AssertionError:
        print(f'Error!')
