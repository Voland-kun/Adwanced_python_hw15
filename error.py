class UserException(Exception):
    pass


class NotDefinedError(UserException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class SizeError(UserException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        match self.value:
            case 1:
                return 'Матрицы разного размера.'
            case 2:
                return 'Строки матрицы разной длины.'
            case _:
                return 'SizeError'


class MatrixTypeError(UserException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        match self.value:
            case 1:
                return 'Неверный тип данных. При создании матрицы необходим список списков.'
            case 2:
                return 'Неверный тип данных. Матрица должна содержать числовые значения.'
            case 3:
                return 'Неверный тип данных.'
            case _:
                return 'MatrixTypeError'
