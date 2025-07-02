class FlatIterator: 
    # Изменения с учетом рекоменлаций преподавателя.
    # Его замечание: "В текущей реализации первого задания создается копия всех списков, 
    # что значительно увеличивает потребление памяти, 
    # на больших данных это может приводить к проблемам."
  
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.iters_stack = [iter(self.list_of_list)]
        return self

    def __next__(self):
        while self.iters_stack:
            try:
                next_item = next(self.iters_stack[-1])
                #  пытаемся получить следующий элемент
            except StopIteration:
                self.iters_stack.pop()
                #  если не получилось, значит итератор пустой
                continue

            if isinstance(next_item, list):
                # если следующий элемент оказался списком, то
                # добавляем его итератор в стек
                self.iters_stack.append(iter(next_item))

            else:
                return next_item
        raise StopIteration


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
