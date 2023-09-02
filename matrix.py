import argparse
import ast
from copy import deepcopy
import error
import logging

logging.basicConfig(
    format='{name}: {asctime} {lineno} -> {msg}',
    style='{',
    filename=f'{__file__}.log',
    encoding='utf-8',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def log_deco(func):
    def wrapper(self, *args, **kwargs):
        try:
            reversed_args = args[::-1]
            result = func(self, *args, **kwargs)
            if result is None:
                logging.info(f'{func.__name__} {str(*reversed_args, **kwargs)} {self}')
            else:
                logging.info(f'{func.__name__} {str(*reversed_args, **kwargs)} {self}    Result = {result}')
        except error.UserException as e:
            logging.error(f'{type(e).__name__} {e}')
        return result

    return wrapper


class Matrix:
    """"Класс матрицы"""

    @log_deco
    def __init__(self, list_of_lists):
        """Создаёт объект класса Matrix принимая список списков, содержащих числа."""
        if not isinstance(list_of_lists, list):
            raise error.MatrixTypeError(1)
        for i in list_of_lists:
            if not isinstance(i, list):
                raise error.MatrixTypeError(1)
            if len(i) == len(list_of_lists[0]):
                if not all(isinstance(x, int | float) for x in i):
                    raise error.MatrixTypeError(2)
            else:
                raise error.SizeError(2)
        self.matrix = deepcopy(list_of_lists)
        self.rows = len(list_of_lists)
        self.columns = len(list_of_lists[0])

    def __str__(self):
        """Печать матрицы"""
        format_size = []
        for col in zip(*self.matrix):
            col_len = [len(str(x)) for x in col]
            format_size.append(max(col_len))
        res = '\n'
        for i in self.matrix:
            for n, e in enumerate(i):
                res += f'{e:>{format_size[n]}}  '
            res += '\n'
        return res

    def __repr__(self):
        """Печать матрицы"""
        format_size = []
        for col in zip(*self.matrix):
            col_len = [len(str(x)) for x in col]
            format_size.append(max(col_len))
        res = '\n'
        for i in self.matrix:
            for n, e in enumerate(i):
                res += f'{e:>{format_size[n]}}  '
            res += '\n'
        return res

    @log_deco
    def __eq__(self, other):
        """Сравнение матриц."""
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.columns == other.columns:
                return all([all([self.matrix[row][col] == other.matrix[row][col]
                                 for col in range(self.columns)]) for row in range(self.rows)])
            else:
                return False
        else:
            raise error.MatrixTypeError(3)

    @log_deco
    def __add__(self, other):
        """Сложение матриц. Для матриц одной размерности"""
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.columns == other.columns:
                return Matrix([list(map(sum, zip(*i))) for i in zip(self.matrix, other.matrix)])
            else:
                raise error.SizeError(1)
        else:
            raise error.MatrixTypeError(3)

    @log_deco
    def __mul__(self, other):
        """Умножение матриц. Для совместимых матриц."""
        if isinstance(other, Matrix):
            if self.rows == other.columns and self.columns == other.rows:
                return Matrix([[sum(a * b for a, b in zip(ra, cb)) for cb in zip(*other.matrix)] for ra in self.matrix])
            else:
                raise error.NotDefinedError('Матрицы не совместимы')
        elif isinstance(other, int | float):
            return Matrix([[self.matrix[row][col] * other for col in range(self.columns)] for row in range(self.rows)])
        else:
            raise error.MatrixTypeError(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Матрицы')
    parser.add_argument('-a', nargs='*', metavar='a', type=str, help='Введите матрицу '
                                                                     'в виде списка списков [[0,0],[0,0]]')
    parser.add_argument('-s', metavar='sign', type=str, help='Введите знак (+,=,*)', default=None)
    parser.add_argument('-b', metavar='b', type=str, default=None, help='Введите матрицу '
                                                                        'в виде списка списков [[0,0],[0,0]]')
    args = parser.parse_args()
    if args.b is not None:
        try:
            args.b = int(args.b)
        except:
            args.b = ast.literal_eval(args.b)
    args_list = [ast.literal_eval(args.a[0]), args.s, args.b]
    if args_list[2] is None:
        print(Matrix(args_list[0]))
    else:
        if isinstance(args.b, int):
            if args_list[1] == '*':
                print(Matrix(args_list[0]) * args.b)
            else:
                raise ValueError('знак должен быть *')
        else:
            match args_list[1]:
                case '=':
                    print(Matrix(args_list[0]) == Matrix(args.b))
                case '+':
                    print(Matrix(args_list[0]) + Matrix(args.b))
                case '*':
                    print(Matrix(args_list[0]) * Matrix(args.b))
                case _:
                    raise ValueError('знак должен быть =, + или *')

# python matrix.py -a [[1,2],[3,4]] -s + -b [[1,2],[3,4]]
