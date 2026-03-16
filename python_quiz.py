#!/usr/bin/env python3
"""Python Quiz Flask application for 9th grade students."""

import json
import os
import re
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_DIR = "/var/www/quiz_data"
MATAN_DATA_DIR = "/var/www/matan_data"
TEACHER_KEY = "xR7kP2mQw9"
REPORT_KEY = "jN4vL8tH1s"

QUESTIONS = [
    # ── Типы данных и переменные ─────────────────────────────────────────────
    {
        "id": 1, "topic": "Типы данных",
        "text": "Что выведет <code>print(type(1 + 2.0))</code>?",
        "options": ["&lt;class 'int'&gt;", "&lt;class 'float'&gt;", "&lt;class 'complex'&gt;", "&lt;class 'number'&gt;"],
        "answer": "B"
    },
    {
        "id": 2, "topic": "Типы данных",
        "text": "Что выведет <code>print(bool(0), bool(''), bool([]))</code>?",
        "options": ["True True True", "False False False", "True False True", "False True False"],
        "answer": "B"
    },
    {
        "id": 3, "topic": "Типы данных",
        "text": "Что выведет <code>print(1 == True, 0 == False, 2 == True)</code>?",
        "options": ["True True True", "False False False", "True True False", "False True True"],
        "answer": "C"
    },
    {
        "id": 4, "topic": "Типы данных",
        "text": "Что произойдёт при выполнении <code>x = 5; x += '3'</code>?",
        "options": ["x станет '53'", "x станет 8", "Возникнет TypeError", "x станет 53"],
        "answer": "C"
    },
    {
        "id": 5, "topic": "Типы данных",
        "text": "Что выведет <code>print(int(3.9))</code>?",
        "options": ["4", "3", "3.9", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 6, "topic": "Типы данных",
        "text": "Какой тип у результата <code>10 / 2</code> в Python 3?",
        "options": ["int", "float", "double", "fraction"],
        "answer": "B"
    },
    {
        "id": 7, "topic": "Типы данных",
        "text": "Что выведет <code>print(type(None))</code>?",
        "options": ["&lt;class 'null'&gt;", "&lt;class 'void'&gt;", "&lt;class 'NoneType'&gt;", "&lt;class 'None'&gt;"],
        "answer": "C"
    },
    {
        "id": 8, "topic": "Типы данных",
        "text": "Чему равно <code>round(2.5)</code> в Python 3?",
        "options": ["3", "2", "2.5", "Ошибка"],
        "answer": "B"
    },
    {
        "id": 9, "topic": "Типы данных",
        "text": "Что выведет <code>print(0.1 + 0.2 == 0.3)</code>?",
        "options": ["True", "False", "None", "Error"],
        "answer": "B"
    },
    {
        "id": 10, "topic": "Типы данных",
        "text": "Что выведет <code>print(bool(-1))</code>?",
        "options": ["False", "True", "-1", "None"],
        "answer": "B"
    },
    # ── Операторы ────────────────────────────────────────────────────────────
    {
        "id": 11, "topic": "Операторы",
        "text": "Что выведет <code>print(7 // -2)</code>?",
        "options": ["-3", "-4", "3", "4"],
        "answer": "B"
    },
    {
        "id": 12, "topic": "Операторы",
        "text": "Что выведет <code>print(-7 % 3)</code>?",
        "options": ["-1", "2", "-2", "1"],
        "answer": "B"
    },
    {
        "id": 13, "topic": "Операторы",
        "text": "Что выведет <code>print(3 ** 2 ** 2)</code>?",
        "options": ["81", "36", "729", "12"],
        "answer": "A"
    },
    {
        "id": 14, "topic": "Операторы",
        "text": "Что выведет <code>print(not not True)</code>?",
        "options": ["False", "True", "None", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 15, "topic": "Операторы",
        "text": "Что выведет <code>print(5 &amp; 3)</code> (побитовое AND)?",
        "options": ["7", "1", "3", "5"],
        "answer": "B"
    },
    {
        "id": 16, "topic": "Операторы",
        "text": "Что выведет <code>print(5 | 3)</code> (побитовое OR)?",
        "options": ["7", "1", "3", "15"],
        "answer": "A"
    },
    {
        "id": 17, "topic": "Операторы",
        "text": "Что выведет <code>print(5 ^ 3)</code> (побитовое XOR)?",
        "options": ["7", "6", "1", "2"],
        "answer": "B"
    },
    {
        "id": 18, "topic": "Операторы",
        "text": "Что выведет <code>print(1 &lt;&lt; 3)</code>?",
        "options": ["3", "6", "8", "16"],
        "answer": "C"
    },
    {
        "id": 19, "topic": "Операторы",
        "text": "Что выведет <code>print(True + True + False)</code>?",
        "options": ["True", "2", "0", "False"],
        "answer": "B"
    },
    {
        "id": 20, "topic": "Операторы",
        "text": "Что выведет <code>print(10 and 20)</code>?",
        "options": ["True", "10", "20", "False"],
        "answer": "C"
    },
    {
        "id": 21, "topic": "Операторы",
        "text": "Что выведет <code>print(0 or '' or [] or 'hello')</code>?",
        "options": ["0", "''", "[]", "hello"],
        "answer": "D"
    },
    {
        "id": 22, "topic": "Операторы",
        "text": "Что выведет <code>x = 10; x //= 3; print(x)</code>?",
        "options": ["3.33", "3", "4", "0"],
        "answer": "B"
    },
    # ── Строки ───────────────────────────────────────────────────────────────
    {
        "id": 23, "topic": "Строки",
        "text": "Что выведет <code>print('python'[-3:])</code>?",
        "options": ["pyt", "hon", "tho", "on"],
        "answer": "B"
    },
    {
        "id": 24, "topic": "Строки",
        "text": "Что выведет <code>print('abcde'[::2])</code>?",
        "options": ["ace", "bdf", "abcde", "acd"],
        "answer": "A"
    },
    {
        "id": 25, "topic": "Строки",
        "text": "Что выведет <code>print('hello world'.split())</code>?",
        "options": ["('hello', 'world')", "['hello', 'world']", "{'hello', 'world'}", "hello world"],
        "answer": "B"
    },
    {
        "id": 26, "topic": "Строки",
        "text": "Что выведет <code>print('-'.join(['a', 'b', 'c']))</code>?",
        "options": ["a b c", "a-b-c", "['a','b','c']", "abc"],
        "answer": "B"
    },
    {
        "id": 27, "topic": "Строки",
        "text": "Что выведет <code>print('  hello  '.strip())</code>?",
        "options": ["'  hello  '", "'hello'", "hello", "'hello  '"],
        "answer": "C"
    },
    {
        "id": 28, "topic": "Строки",
        "text": "Что выведет <code>print('hello'.replace('l', 'r'))</code>?",
        "options": ["herro", "hero", "helo", "helro"],
        "answer": "A"
    },
    {
        "id": 29, "topic": "Строки",
        "text": "Что выведет <code>s = 'abc'; print(s * 2)</code>?",
        "options": ["abc abc", "abcabc", "6", "['abc','abc']"],
        "answer": "B"
    },
    {
        "id": 30, "topic": "Строки",
        "text": "Что выведет <code>print(f'{2 ** 10}')</code>?",
        "options": ["2 ** 10", "1024", "210", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 31, "topic": "Строки",
        "text": "Что выведет <code>print('abc'.find('d'))</code>?",
        "options": ["None", "False", "-1", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 32, "topic": "Строки",
        "text": "Что выведет <code>print(len('hello\\n'))</code>?",
        "options": ["5", "6", "7", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 33, "topic": "Строки",
        "text": "Что выведет <code>print('Hello World'.lower())</code>?",
        "options": ["Hello World", "HELLO WORLD", "hello world", "hELLO wORLD"],
        "answer": "C"
    },
    {
        "id": 34, "topic": "Строки",
        "text": "Что выведет <code>print('12abc'.isdigit())</code>?",
        "options": ["True", "False", "None", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 35, "topic": "Строки",
        "text": "Что выведет <code>print('hello'[1:4])</code>?",
        "options": ["hell", "ell", "ello", "hel"],
        "answer": "B"
    },
    # ── Списки ───────────────────────────────────────────────────────────────
    {
        "id": 36, "topic": "Списки",
        "text": "Что выведет следующий код?<br><pre>a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)</pre>",
        "options": ["[1, 2, 3]", "[1, 2, 3, 4]", "[4, 1, 2, 3]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 37, "topic": "Списки",
        "text": "Что выведет <code>print([1,2,3].pop(1))</code>?",
        "options": ["1", "2", "3", "[1,3]"],
        "answer": "B"
    },
    {
        "id": 38, "topic": "Списки",
        "text": "Что выведет <code>print(sorted([3,1,4,1,5], reverse=True))</code>?",
        "options": ["[1,1,3,4,5]", "[5,4,3,1,1]", "[5,4,1,3,1]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 39, "topic": "Списки",
        "text": "Что выведет следующий код?<br><pre>lst = [1, 2, 3, 4, 5]\nprint(lst[1::2])</pre>",
        "options": ["[1, 3, 5]", "[2, 4]", "[2, 3, 4]", "[1, 3]"],
        "answer": "B"
    },
    {
        "id": 40, "topic": "Списки",
        "text": "Что выведет <code>print([0] * 3 + [1] * 2)</code>?",
        "options": ["[0, 0, 0, 1, 1]", "[0, 1]", "[0, 0, 0, 0, 0]", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 41, "topic": "Списки",
        "text": "Как скопировать список <code>a</code> так, чтобы изменение копии не меняло оригинал?",
        "options": ["b = a", "b = a[:]", "b = list(a[:])", "b = a.copy(); оба варианта B и C верны"],
        "answer": "D"
    },
    {
        "id": 42, "topic": "Списки",
        "text": "Что выведет следующий код?<br><pre>a = [1, [2, 3]]\nb = a[:]\nb[1].append(4)\nprint(a)</pre>",
        "options": ["[1, [2, 3]]", "[1, [2, 3, 4]]", "[1, 2, 3, 4]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 43, "topic": "Списки",
        "text": "Что выведет <code>print(sum([1,2,3,4,5]))</code>?",
        "options": ["10", "15", "12345", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 44, "topic": "Списки",
        "text": "Что выведет следующий код?<br><pre>a = [3, 1, 4, 1, 5]\na.sort()\nprint(a[0], a[-1])</pre>",
        "options": ["3 5", "1 5", "3 4", "1 4"],
        "answer": "B"
    },
    {
        "id": 45, "topic": "Списки",
        "text": "Что выведет <code>print([x**2 for x in range(4)])</code>?",
        "options": ["[1, 4, 9, 16]", "[0, 1, 4, 9]", "[0, 1, 2, 3]", "[0, 2, 4, 6]"],
        "answer": "B"
    },
    # ── Кортежи и множества ───────────────────────────────────────────────────
    {
        "id": 46, "topic": "Кортежи",
        "text": "Что выведет <code>t = (1, 2, 3); t[0] = 10; print(t)</code>?",
        "options": ["(10, 2, 3)", "(1, 2, 3)", "Ошибку TypeError", "Ошибку IndexError"],
        "answer": "C"
    },
    {
        "id": 47, "topic": "Кортежи",
        "text": "Что выведет <code>print(type((1,)))</code>?",
        "options": ["&lt;class 'list'&gt;", "&lt;class 'int'&gt;", "&lt;class 'tuple'&gt;", "&lt;class 'set'&gt;"],
        "answer": "C"
    },
    {
        "id": 48, "topic": "Кортежи",
        "text": "Что выведет следующий код?<br><pre>a, *b, c = [1, 2, 3, 4, 5]\nprint(b)</pre>",
        "options": ["[2, 3, 4]", "[1, 2, 3, 4]", "(2, 3, 4)", "[2, 3]"],
        "answer": "A"
    },
    {
        "id": 49, "topic": "Множества",
        "text": "Что выведет <code>print(len({1, 2, 2, 3, 3, 3}))</code>?",
        "options": ["6", "3", "2", "1"],
        "answer": "B"
    },
    {
        "id": 50, "topic": "Множества",
        "text": "Что выведет <code>print({1,2,3} &amp; {2,3,4})</code>?",
        "options": ["{1,2,3,4}", "{2,3}", "{1,4}", "{2,3,4}"],
        "answer": "B"
    },
    {
        "id": 51, "topic": "Множества",
        "text": "Что выведет <code>print({1,2,3} - {2,3,4})</code>?",
        "options": ["{1}", "{4}", "{1,4}", "{}"],
        "answer": "A"
    },
    {
        "id": 52, "topic": "Множества",
        "text": "Является ли множество <code>set</code> упорядоченной коллекцией?",
        "options": ["Да, по значению", "Да, по порядку добавления", "Нет, порядок не гарантирован", "Да, по убыванию"],
        "answer": "C"
    },
    # ── Словари ───────────────────────────────────────────────────────────────
    {
        "id": 53, "topic": "Словари",
        "text": "Что выведет следующий код?<br><pre>d = {'a': 1, 'b': 2}\nprint(d.get('c', 0))</pre>",
        "options": ["None", "KeyError", "0", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 54, "topic": "Словари",
        "text": "Что выведет <code>print(list({'a':1,'b':2,'c':3}.keys()))</code>?",
        "options": ["['a','b','c']", "[1,2,3]", "[('a',1),('b',2),('c',3)]", "dict_keys"],
        "answer": "A"
    },
    {
        "id": 55, "topic": "Словари",
        "text": "Что выведет следующий код?<br><pre>d = {}\nd['x'] = d.get('x', 0) + 1\nd['x'] = d.get('x', 0) + 1\nprint(d['x'])</pre>",
        "options": ["0", "1", "2", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 56, "topic": "Словари",
        "text": "Что произойдёт при <code>d = {'a':1}; del d['b']</code>?",
        "options": ["Ничего", "d останется {'a':1}", "KeyError", "ValueError"],
        "answer": "C"
    },
    {
        "id": 57, "topic": "Словари",
        "text": "Что выведет <code>print({i: i**2 for i in range(4)})</code>?",
        "options": ["{0:0, 1:1, 2:4, 3:9}", "{1:1, 2:4, 3:9}", "{0:0, 1:2, 2:4, 3:6}", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 58, "topic": "Словари",
        "text": "Что выведет следующий код?<br><pre>d = {'a': 1, 'b': 2}\nd.update({'b': 3, 'c': 4})\nprint(d)</pre>",
        "options": ["{'a':1,'b':2}", "{'a':1,'b':3,'c':4}", "{'a':1,'b':2,'b':3,'c':4}", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 59, "topic": "Словари",
        "text": "Можно ли использовать список как ключ словаря?",
        "options": ["Да", "Нет, только строки", "Нет, список изменяемый — будет TypeError", "Да, но только пустой"],
        "answer": "C"
    },
    {
        "id": 60, "topic": "Словари",
        "text": "Что выведет <code>print(sorted({'b':2,'a':1,'c':3}.items()))</code>?",
        "options": ["[('a',1),('b',2),('c',3)]", "[('b',2),('a',1),('c',3)]", "[(1,'a'),(2,'b'),(3,'c')]", "Ошибку"],
        "answer": "A"
    },
    # ── Ветвление ─────────────────────────────────────────────────────────────
    {
        "id": 61, "topic": "Ветвление",
        "text": "Что выведет следующий код?<br><pre>x = 10\nif x > 5:\n    if x > 8:\n        print('A')\n    else:\n        print('B')\nelse:\n    print('C')</pre>",
        "options": ["A", "B", "C", "AB"],
        "answer": "A"
    },
    {
        "id": 62, "topic": "Ветвление",
        "text": "Что выведет <code>print('big' if 100 > 10 > 5 else 'small')</code>?",
        "options": ["big", "small", "True", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 63, "topic": "Ветвление",
        "text": "Что выведет следующий код?<br><pre>a = 5\nb = 10\nprint(a if a > b else b)</pre>",
        "options": ["5", "10", "True", "False"],
        "answer": "B"
    },
    {
        "id": 64, "topic": "Ветвление",
        "text": "Что выведет следующий код?<br><pre>x = None\nif x:\n    print('yes')\nelse:\n    print('no')</pre>",
        "options": ["yes", "no", "None", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 65, "topic": "Ветвление",
        "text": "Что выведет <code>print(1 if [] else 2 if {} else 3)</code>?",
        "options": ["1", "2", "3", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 66, "topic": "Ветвление",
        "text": "Что выведет следующий код?<br><pre>x = 7\nmatch x:\n    case 1:\n        print('one')\n    case 7:\n        print('seven')\n    case _:\n        print('other')</pre>",
        "options": ["one", "seven", "other", "Ошибку (match нет в Python)"],
        "answer": "B"
    },
    # ── Циклы ─────────────────────────────────────────────────────────────────
    {
        "id": 67, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>for i in range(10):\n    if i == 5:\n        break\nelse:\n    print('done')\nprint(i)</pre>",
        "options": ["done\\n5", "5", "done", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 68, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>for i in range(3):\n    pass\nelse:\n    print('ok')</pre>",
        "options": ["ok", "Ничего", "pass", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 69, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>total = 0\nfor x in [1, 2, 3]:\n    total += x\nprint(total)</pre>",
        "options": ["123", "0", "6", "[1,2,3]"],
        "answer": "C"
    },
    {
        "id": 70, "topic": "Циклы",
        "text": "Сколько итераций выполнит цикл <code>for i in range(2, 10, 3)</code>?",
        "options": ["3", "4", "8", "2"],
        "answer": "A"
    },
    {
        "id": 71, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>i = 0\nwhile True:\n    i += 1\n    if i == 3:\n        break\nprint(i)</pre>",
        "options": ["0", "1", "3", "Бесконечный цикл"],
        "answer": "C"
    },
    {
        "id": 72, "topic": "Циклы",
        "text": "Что выведет <code>print(list(enumerate(['a','b','c'])))</code>?",
        "options": ["[(0,'a'),(1,'b'),(2,'c')]", "[('a',0),('b',1),('c',2)]", "['a','b','c']", "[0,1,2]"],
        "answer": "A"
    },
    {
        "id": 73, "topic": "Циклы",
        "text": "Что выведет <code>print(list(zip([1,2,3],[4,5,6])))</code>?",
        "options": ["[(1,4),(2,5),(3,6)]", "[[1,4],[2,5],[3,6]]", "(1,4,2,5,3,6)", "[1,2,3,4,5,6]"],
        "answer": "A"
    },
    {
        "id": 74, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>result = []\nfor i in range(3):\n    for j in range(3):\n        if i == j:\n            result.append(i)\nprint(result)</pre>",
        "options": ["[0, 0, 1, 1, 2, 2]", "[0, 1, 2]", "[[0,0],[1,1],[2,2]]", "[]"],
        "answer": "B"
    },
    {
        "id": 75, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>nums = [1,2,3,4,5,6]\neven = [x for x in nums if x % 2 == 0]\nprint(even)</pre>",
        "options": ["[1,3,5]", "[2,4,6]", "[1,2,3,4,5,6]", "[0,0,1,0,1,0]"],
        "answer": "B"
    },
    # ── Функции ───────────────────────────────────────────────────────────────
    {
        "id": 76, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def f(a, b=2, c=3):\n    return a + b + c\nprint(f(1, c=10))</pre>",
        "options": ["6", "13", "Ошибку", "3"],
        "answer": "B"
    },
    {
        "id": 77, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def f(*args):\n    return sum(args)\nprint(f(1,2,3,4))</pre>",
        "options": ["[1,2,3,4]", "10", "(1,2,3,4)", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 78, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def f(**kwargs):\n    return kwargs.get('x', 0)\nprint(f(x=5, y=10))</pre>",
        "options": ["0", "5", "10", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 79, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>x = 10\ndef f():\n    x = 20\nf()\nprint(x)</pre>",
        "options": ["20", "10", "None", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 80, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>x = 10\ndef f():\n    global x\n    x = 20\nf()\nprint(x)</pre>",
        "options": ["10", "20", "None", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 81, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)\nprint(fib(6))</pre>",
        "options": ["8", "13", "5", "21"],
        "answer": "A"
    },
    {
        "id": 82, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def make_adder(n):\n    return lambda x: x + n\nadd5 = make_adder(5)\nprint(add5(3))</pre>",
        "options": ["3", "5", "8", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 83, "topic": "Функции",
        "text": "Что выведет <code>print(list(map(lambda x: x*2, [1,2,3])))</code>?",
        "options": ["[1,2,3]", "[2,4,6]", "[1,4,9]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 84, "topic": "Функции",
        "text": "Что выведет <code>print(list(filter(lambda x: x%2==0, [1,2,3,4,5])))</code>?",
        "options": ["[1,3,5]", "[2,4]", "[True,False,True,False,True]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 85, "topic": "Функции",
        "text": "Каков результат <code>sorted(['banana','apple','cherry'], key=len)</code>?",
        "options": ["['apple','banana','cherry']", "['apple','cherry','banana']", "['banana','apple','cherry']", "['cherry','apple','banana']"],
        "answer": "B"
    },
    {
        "id": 86, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def counter():\n    count = 0\n    def inc():\n        nonlocal count\n        count += 1\n        return count\n    return inc\nc = counter()\nprint(c(), c(), c())</pre>",
        "options": ["0 0 0", "1 1 1", "1 2 3", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 87, "topic": "Функции",
        "text": "Что происходит при изменении изменяемого аргумента по умолчанию?<br><pre>def f(lst=[]):\n    lst.append(1)\n    return lst\nprint(f(), f(), f())</pre>",
        "options": ["[1] [1] [1]", "[1] [1,1] [1,1,1]", "[1] [] []", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 88, "topic": "Функции",
        "text": "Что выведет <code>print((lambda x, y: x**y)(2, 8))</code>?",
        "options": ["16", "256", "10", "Ошибку"],
        "answer": "B"
    },
    # ── Генераторы и итераторы ────────────────────────────────────────────────
    {
        "id": 89, "topic": "Генераторы",
        "text": "Что выведет следующий код?<br><pre>def gen():\n    yield 1\n    yield 2\n    yield 3\ng = gen()\nprint(next(g), next(g))</pre>",
        "options": ["1 2", "1 1", "2 3", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 90, "topic": "Генераторы",
        "text": "Чем генераторное выражение отличается от list comprehension?",
        "options": ["Ничем, это синонимы", "Генератор ленивый, не хранит все элементы в памяти", "Генератор быстрее list comprehension", "Генератор возвращает кортеж"],
        "answer": "B"
    },
    {
        "id": 91, "topic": "Генераторы",
        "text": "Что выведет <code>print(sum(x*x for x in range(4)))</code>?",
        "options": ["14", "36", "0", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 92, "topic": "Генераторы",
        "text": "Что произойдёт при повторном вызове <code>next()</code> на исчерпанном генераторе?",
        "options": ["Вернёт None", "Вернёт 0", "Возникнет StopIteration", "Перезапустит генератор"],
        "answer": "C"
    },
    # ── ООП ───────────────────────────────────────────────────────────────────
    {
        "id": 93, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class A:\n    x = 10\na = A()\na.x = 20\nprint(A.x, a.x)</pre>",
        "options": ["20 20", "10 10", "10 20", "20 10"],
        "answer": "C"
    },
    {
        "id": 94, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class Animal:\n    def speak(self):\n        return 'sound'\nclass Dog(Animal):\n    def speak(self):\n        return 'woof'\nd = Dog()\nprint(d.speak())</pre>",
        "options": ["sound", "woof", "sound woof", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 95, "topic": "ООП",
        "text": "Что делает метод <code>__str__</code> в классе?",
        "options": ["Инициализирует объект", "Возвращает строковое представление объекта", "Сравнивает объекты", "Вызывается при удалении объекта"],
        "answer": "B"
    },
    {
        "id": 96, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1\na = Counter()\nb = Counter()\nprint(Counter.count)</pre>",
        "options": ["0", "1", "2", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 97, "topic": "ООП",
        "text": "Что такое инкапсуляция?",
        "options": ["Наследование свойств родителя", "Скрытие внутренних деталей объекта", "Создание множества объектов", "Переопределение методов"],
        "answer": "B"
    },
    {
        "id": 98, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class A:\n    def __init__(self):\n        self.__x = 5\na = A()\nprint(a.__x)</pre>",
        "options": ["5", "None", "Ошибку AttributeError", "0"],
        "answer": "C"
    },
    {
        "id": 99, "topic": "ООП",
        "text": "Что делает декоратор <code>@staticmethod</code>?",
        "options": ["Метод не может обращаться к self или cls", "Метод вызывается автоматически", "Метод является приватным", "Метод нельзя переопределить"],
        "answer": "A"
    },
    {
        "id": 100, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class A:\n    pass\nclass B(A):\n    pass\nprint(issubclass(B, A), isinstance(B(), A))</pre>",
        "options": ["False False", "True True", "True False", "False True"],
        "answer": "B"
    },
    # ── Исключения ────────────────────────────────────────────────────────────
    {
        "id": 101, "topic": "Исключения",
        "text": "Что выведет следующий код?<br><pre>try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print('zero')\nfinally:\n    print('done')</pre>",
        "options": ["zero", "done", "zero\\ndone", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 102, "topic": "Исключения",
        "text": "Что выведет следующий код?<br><pre>try:\n    print(1)\nexcept:\n    print(2)\nelse:\n    print(3)</pre>",
        "options": ["1", "1\\n3", "2", "1\\n2\\n3"],
        "answer": "B"
    },
    {
        "id": 103, "topic": "Исключения",
        "text": "Что произойдёт при выполнении <code>raise ValueError('bad')</code>?",
        "options": ["Программа напечатает 'bad' и продолжит", "Возникнет исключение ValueError с сообщением 'bad'", "Программа завершится без сообщения", "Переменная 'bad' будет создана"],
        "answer": "B"
    },
    {
        "id": 104, "topic": "Исключения",
        "text": "Какой блок выполняется всегда — даже если исключение не было?",
        "options": ["except", "else", "finally", "raise"],
        "answer": "C"
    },
    {
        "id": 105, "topic": "Исключения",
        "text": "Что выведет следующий код?<br><pre>try:\n    int('abc')\nexcept (ValueError, TypeError) as e:\n    print(type(e).__name__)</pre>",
        "options": ["TypeError", "ValueError", "Exception", "Ошибку"],
        "answer": "B"
    },
    # ── Работа с файлами ──────────────────────────────────────────────────────
    {
        "id": 106, "topic": "Файлы",
        "text": "Что делает конструкция <code>with open('f.txt') as f:</code>?",
        "options": ["Открывает файл и гарантирует его закрытие", "Открывает файл только для чтения навсегда", "Создаёт файл и сразу удаляет", "Читает файл в список"],
        "answer": "A"
    },
    {
        "id": 107, "topic": "Файлы",
        "text": "Какой режим открытия файла перезаписывает его содержимое?",
        "options": ["'r'", "'a'", "'w'", "'rb'"],
        "answer": "C"
    },
    {
        "id": 108, "topic": "Файлы",
        "text": "Что возвращает <code>f.readlines()</code>?",
        "options": ["Строку с содержимым", "Список строк", "Генератор строк", "Байты"],
        "answer": "B"
    },
    # ── Встроенные функции ────────────────────────────────────────────────────
    {
        "id": 109, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(max([3,1,4,1,5,9,2,6]))</code>?",
        "options": ["3", "6", "9", "5"],
        "answer": "C"
    },
    {
        "id": 110, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(min('python'))</code>?",
        "options": ["p", "h", "n", "o"],
        "answer": "B"
    },
    {
        "id": 111, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(abs(-7.5))</code>?",
        "options": ["-7.5", "7", "7.5", "8"],
        "answer": "C"
    },
    {
        "id": 112, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(list(reversed([1,2,3])))</code>?",
        "options": ["[1,2,3]", "[3,2,1]", "reversed object", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 113, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(all([1, 2, 0, 3]))</code>?",
        "options": ["True", "False", "0", "3"],
        "answer": "B"
    },
    {
        "id": 114, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(any([0, '', [], None]))</code>?",
        "options": ["True", "False", "None", "0"],
        "answer": "B"
    },
    {
        "id": 115, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(chr(65))</code>?",
        "options": ["a", "A", "65", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 116, "topic": "Встроенные функции",
        "text": "Что выведет <code>print(ord('z') - ord('a'))</code>?",
        "options": ["1", "25", "26", "0"],
        "answer": "B"
    },
    # ── Comprehensions ────────────────────────────────────────────────────────
    {
        "id": 117, "topic": "Comprehensions",
        "text": "Что выведет <code>print([x for x in range(10) if x % 3 == 0])</code>?",
        "options": ["[0, 3, 6, 9]", "[3, 6, 9]", "[0, 3, 6]", "[1, 4, 7]"],
        "answer": "A"
    },
    {
        "id": 118, "topic": "Comprehensions",
        "text": "Что выведет <code>print({x % 3 for x in range(9)})</code>?",
        "options": ["[0, 1, 2]", "{0, 1, 2}", "{0, 0, 0, 1, 1, 1, 2, 2, 2}", "set()"],
        "answer": "B"
    },
    {
        "id": 119, "topic": "Comprehensions",
        "text": "Что выведет следующий код?<br><pre>matrix = [[1,2],[3,4],[5,6]]\nflat = [x for row in matrix for x in row]\nprint(flat)</pre>",
        "options": ["[[1,2],[3,4],[5,6]]", "[1,3,5,2,4,6]", "[1,2,3,4,5,6]", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 120, "topic": "Comprehensions",
        "text": "Что выведет <code>print([x if x>0 else -x for x in [-3,1,-2,4]])</code>?",
        "options": ["[-3,1,-2,4]", "[3,1,2,4]", "[0,1,0,4]", "Ошибку"],
        "answer": "B"
    },
    # ── Модули ────────────────────────────────────────────────────────────────
    {
        "id": 121, "topic": "Модули",
        "text": "Что выведет следующий код?<br><pre>import math\nprint(math.ceil(4.1), math.floor(4.9))</pre>",
        "options": ["4 4", "5 4", "4 5", "5 5"],
        "answer": "B"
    },
    {
        "id": 122, "topic": "Модули",
        "text": "Что выведет <code>import math; print(math.sqrt(144))</code>?",
        "options": ["12", "12.0", "144.0", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 123, "topic": "Модули",
        "text": "Что выведет <code>from random import seed; seed(0); import random; print(random.randint(1,10))</code>?",
        "options": ["Непредсказуемо", "Всегда одно и то же число", "Всегда 0", "Ошибку"],
        "answer": "B"
    },
    # ── Алгоритмы и логика ────────────────────────────────────────────────────
    {
        "id": 124, "topic": "Алгоритмы",
        "text": "Что выведет следующий код (бинарный поиск)?<br><pre>def bs(arr, t):\n    l, r = 0, len(arr)-1\n    while l <= r:\n        m = (l+r)//2\n        if arr[m] == t: return m\n        elif arr[m] < t: l = m+1\n        else: r = m-1\n    return -1\nprint(bs([1,3,5,7,9,11], 7))</pre>",
        "options": ["3", "7", "2", "-1"],
        "answer": "A"
    },
    {
        "id": 125, "topic": "Алгоритмы",
        "text": "Какова сложность бинарного поиска в отсортированном массиве из n элементов?",
        "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
        "answer": "C"
    },
    {
        "id": 126, "topic": "Алгоритмы",
        "text": "Что выведет следующий код?<br><pre>def fact(n):\n    return 1 if n <= 1 else n * fact(n-1)\nprint(fact(5))</pre>",
        "options": ["15", "120", "24", "5"],
        "answer": "B"
    },
    {
        "id": 127, "topic": "Алгоритмы",
        "text": "Что выведет следующий код (пузырьковая сортировка, 1 проход)?<br><pre>a = [5, 3, 1, 4]\nfor i in range(len(a)-1):\n    if a[i] > a[i+1]:\n        a[i], a[i+1] = a[i+1], a[i]\nprint(a)</pre>",
        "options": ["[1, 3, 4, 5]", "[3, 1, 4, 5]", "[3, 5, 1, 4]", "[5, 3, 1, 4]"],
        "answer": "B"
    },
    {
        "id": 128, "topic": "Алгоритмы",
        "text": "Что выведет следующий код?<br><pre>def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True\nprint(sum(1 for x in range(100) if is_prime(x)))</pre>",
        "options": ["24", "25", "23", "26"],
        "answer": "B"
    },
    {
        "id": 129, "topic": "Алгоритмы",
        "text": "Что выведет следующий код?<br><pre>stack = []\nfor c in '([{]])':\n    if c in '([{':\n        stack.append(c)\n    elif stack:\n        stack.pop()\nprint(len(stack))</pre>",
        "options": ["0", "1", "2", "3"],
        "answer": "B"
    },
    {
        "id": 130, "topic": "Алгоритмы",
        "text": "Сколько раз выполнится тело функции (не считая финальный вызов)?<br><pre>def count(n):\n    if n == 0:\n        return 0\n    return 1 + count(n-1)\nprint(count(5))</pre>",
        "options": ["4", "5", "6", "Бесконечно"],
        "answer": "B"
    },
    # ── Сложные вопросы по синтаксису ─────────────────────────────────────────
    {
        "id": 131, "topic": "Синтаксис",
        "text": "Что выведет <code>print(*[1,2,3])</code>?",
        "options": ["[1, 2, 3]", "1 2 3", "(1, 2, 3)", "1\\n2\\n3"],
        "answer": "B"
    },
    {
        "id": 132, "topic": "Синтаксис",
        "text": "Что выведет <code>x = y = z = 0; x += 1; print(x, y, z)</code>?",
        "options": ["1 1 1", "1 0 0", "0 0 0", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 133, "topic": "Синтаксис",
        "text": "Что выведет <code>a, b = b, a = 1, 2; print(a, b)</code>?",
        "options": ["1 2", "2 1", "1 1", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 134, "topic": "Синтаксис",
        "text": "Что выведет <code>print(1_000_000 + 2_000)</code>?",
        "options": ["1_000_000 + 2_000", "Ошибку", "1002000", "1 2"],
        "answer": "C"
    },
    {
        "id": 135, "topic": "Синтаксис",
        "text": "Что выведет <code>print(f\"{'hi':>10}\")</code>?",
        "options": ["hi        ", "        hi", "hi", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 136, "topic": "Синтаксис",
        "text": "Что выведет <code>print(f\"{3.14159:.2f}\")</code>?",
        "options": ["3.14159", "3.14", "3.1", "3"],
        "answer": "B"
    },
    {
        "id": 137, "topic": "Синтаксис",
        "text": "Что выведет <code>print([i for i in range(5) if i != 3])</code>?",
        "options": ["[0,1,2,4]", "[0,1,2,3,4]", "[1,2,4]", "[0,1,2,3]"],
        "answer": "A"
    },
    {
        "id": 138, "topic": "Синтаксис",
        "text": "Что выведет следующий код?<br><pre>x = 5\nprint(x := x + 1)</pre>",
        "options": ["5", "6", "None", "Ошибку"],
        "answer": "B"
    },
    # ── Область видимости ─────────────────────────────────────────────────────
    {
        "id": 139, "topic": "Область видимости",
        "text": "В каком порядке Python ищет имена переменных (правило LEGB)?",
        "options": ["Global → Local → Enclosing → Built-in", "Local → Enclosing → Global → Built-in", "Built-in → Global → Local → Enclosing", "Local → Global → Enclosing → Built-in"],
        "answer": "B"
    },
    {
        "id": 140, "topic": "Область видимости",
        "text": "Что выведет следующий код?<br><pre>x = 'global'\ndef outer():\n    x = 'outer'\n    def inner():\n        print(x)\n    inner()\nouter()</pre>",
        "options": ["global", "outer", "None", "Ошибку"],
        "answer": "B"
    },
    # ── Декораторы ────────────────────────────────────────────────────────────
    {
        "id": 141, "topic": "Декораторы",
        "text": "Что выведет следующий код?<br><pre>def deco(f):\n    def wrapper():\n        print('before')\n        f()\n        print('after')\n    return wrapper\n@deco\ndef hello():\n    print('hello')\nhello()</pre>",
        "options": ["hello", "before\\nhello\\nafter", "after\\nhello\\nbefore", "before\\nafter"],
        "answer": "B"
    },
    {
        "id": 142, "topic": "Декораторы",
        "text": "Что делает <code>@property</code> в классе?",
        "options": ["Делает атрибут публичным", "Позволяет вызывать метод как атрибут без ()", "Создаёт статический метод", "Запрещает изменение атрибута"],
        "answer": "B"
    },
    # ── Работа со временем и числами ─────────────────────────────────────────
    {
        "id": 143, "topic": "Математика",
        "text": "Что выведет <code>import math; print(math.gcd(48, 18))</code>?",
        "options": ["3", "6", "9", "18"],
        "answer": "B"
    },
    {
        "id": 144, "topic": "Математика",
        "text": "Что выведет <code>print(divmod(17, 5))</code>?",
        "options": ["(3, 2)", "(2, 3)", "3", "3.4"],
        "answer": "A"
    },
    {
        "id": 145, "topic": "Математика",
        "text": "Что выведет <code>print(sum(range(1, 101)))</code>?",
        "options": ["100", "5000", "5050", "5100"],
        "answer": "C"
    },
    # ── Рекурсия ─────────────────────────────────────────────────────────────
    {
        "id": 146, "topic": "Рекурсия",
        "text": "Что произойдёт при бесконечной рекурсии без базового случая?",
        "options": ["Программа зависнет навсегда", "Возникнет RecursionError", "Python обнаружит петлю и остановит", "Программа завершится без ошибок"],
        "answer": "B"
    },
    {
        "id": 147, "topic": "Рекурсия",
        "text": "Что выведет следующий код?<br><pre>def power(base, exp):\n    if exp == 0:\n        return 1\n    return base * power(base, exp - 1)\nprint(power(3, 4))</pre>",
        "options": ["12", "81", "64", "27"],
        "answer": "B"
    },
    {
        "id": 148, "topic": "Рекурсия",
        "text": "Что выведет следующий код?<br><pre>def flatten(lst):\n    result = []\n    for x in lst:\n        if isinstance(x, list):\n            result.extend(flatten(x))\n        else:\n            result.append(x)\n    return result\nprint(flatten([1,[2,[3,4]],5]))</pre>",
        "options": ["[1,[2,[3,4]],5]", "[1,2,[3,4],5]", "[1,2,3,4,5]", "Ошибку"],
        "answer": "C"
    },
    # ── Ошибки и отладка ─────────────────────────────────────────────────────
    {
        "id": 149, "topic": "Ошибки",
        "text": "Какое исключение вызывает <code>[][0]</code>?",
        "options": ["ValueError", "KeyError", "IndexError", "TypeError"],
        "answer": "C"
    },
    {
        "id": 150, "topic": "Ошибки",
        "text": "Какое исключение вызывает <code>'5' + 5</code>?",
        "options": ["ValueError", "TypeError", "SyntaxError", "AttributeError"],
        "answer": "B"
    },
    {
        "id": 151, "topic": "Ошибки",
        "text": "Какое исключение вызывает <code>x</code>, если переменная <code>x</code> не определена?",
        "options": ["ValueError", "AttributeError", "NameError", "TypeError"],
        "answer": "C"
    },
    {
        "id": 152, "topic": "Ошибки",
        "text": "Что выведет следующий код?<br><pre>try:\n    raise Exception('oops')\nexcept Exception as e:\n    print(str(e))</pre>",
        "options": ["Exception: oops", "oops", "raise oops", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 153, "topic": "Ошибки",
        "text": "Какое исключение вызывает <code>int('3.5')</code>?",
        "options": ["TypeError", "FloatError", "ValueError", "ParseError"],
        "answer": "C"
    },
    # ── Продвинутые темы ─────────────────────────────────────────────────────
    {
        "id": 154, "topic": "Продвинутые темы",
        "text": "Что выведет <code>print(id(1) == id(1))</code>?",
        "options": ["Зависит от реализации", "Всегда False", "Всегда True (малые int кэшируются)", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 155, "topic": "Продвинутые темы",
        "text": "Что выведет <code>a = [1,2]; b = [1,2]; print(a == b, a is b)</code>?",
        "options": ["False False", "True True", "True False", "False True"],
        "answer": "C"
    },
    {
        "id": 156, "topic": "Продвинутые темы",
        "text": "Что делает <code>__slots__</code> в классе?",
        "options": ["Задаёт порядок методов", "Ограничивает атрибуты и экономит память", "Делает объект неизменяемым", "Указывает наследуемые методы"],
        "answer": "B"
    },
    {
        "id": 157, "topic": "Продвинутые темы",
        "text": "Что выведет следующий код?<br><pre>from functools import reduce\nprint(reduce(lambda a, b: a*b, [1,2,3,4,5]))</pre>",
        "options": ["15", "120", "5", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 158, "topic": "Продвинутые темы",
        "text": "Что выведет <code>print(list(range(5, 0, -1)))</code>?",
        "options": ["[0,1,2,3,4]", "[5,4,3,2,1]", "[1,2,3,4,5]", "[4,3,2,1,0]"],
        "answer": "B"
    },
    {
        "id": 159, "topic": "Продвинутые темы",
        "text": "Что выведет следующий код?<br><pre>d = {}\nfor i in range(5):\n    d[i % 3] = i\nprint(sorted(d.values()))</pre>",
        "options": ["[0,1,2,3,4]", "[2,3,4]", "[0,1,4]", "[2,4,3]"],
        "answer": "B"
    },
    {
        "id": 160, "topic": "Продвинутые темы",
        "text": "Что выведет следующий код?<br><pre>class Singleton:\n    _inst = None\n    def __new__(cls):\n        if cls._inst is None:\n            cls._inst = super().__new__(cls)\n        return cls._inst\na = Singleton()\nb = Singleton()\nprint(a is b)</pre>",
        "options": ["False", "True", "None", "Ошибку"],
        "answer": "B"
    },
    # ── Практические задачи ───────────────────────────────────────────────────
    {
        "id": 161, "topic": "Практика",
        "text": "Что выведет следующий код (подсчёт частот)?<br><pre>words = ['a','b','a','c','b','a']\nfreq = {}\nfor w in words:\n    freq[w] = freq.get(w, 0) + 1\nprint(freq['a'])</pre>",
        "options": ["1", "2", "3", "4"],
        "answer": "C"
    },
    {
        "id": 162, "topic": "Практика",
        "text": "Что выведет следующий код (анаграммы)?<br><pre>def is_anagram(a, b):\n    return sorted(a) == sorted(b)\nprint(is_anagram('listen','silent'), is_anagram('hello','world'))</pre>",
        "options": ["True False", "False True", "True True", "False False"],
        "answer": "A"
    },
    {
        "id": 163, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>s = 'abcba'\nprint(s == s[::-1])</pre>",
        "options": ["True (палиндром)", "False", "None", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 164, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>nums = [4, 7, 2, 9, 1]\nprint(sorted(nums, key=lambda x: -x)[0])</pre>",
        "options": ["1", "4", "9", "7"],
        "answer": "C"
    },
    {
        "id": 165, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>pairs = [(1,'b'),(3,'a'),(2,'c')]\nprint(sorted(pairs, key=lambda x: x[1]))</pre>",
        "options": ["[(1,'b'),(3,'a'),(2,'c')]", "[(3,'a'),(1,'b'),(2,'c')]", "[(2,'c'),(1,'b'),(3,'a')]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 166, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>text = 'hello world'\nprint(sum(1 for c in text if c.isalpha()))</pre>",
        "options": ["10", "11", "12", "9"],
        "answer": "A"
    },
    {
        "id": 167, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>data = [3,1,4,1,5,9,2,6,5]\nprint(len(set(data)))</pre>",
        "options": ["9", "7", "6", "8"],
        "answer": "B"
    },
    {
        "id": 168, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>matrix = [[1,2,3],[4,5,6],[7,8,9]]\nprint(matrix[1][2])</pre>",
        "options": ["4", "5", "6", "8"],
        "answer": "C"
    },
    {
        "id": 169, "topic": "Практика",
        "text": "Что выведет следующий код (транспонирование матрицы)?<br><pre>m = [[1,2],[3,4],[5,6]]\nt = list(zip(*m))\nprint(len(t), len(t[0]))</pre>",
        "options": ["3 2", "2 3", "2 2", "3 3"],
        "answer": "B"
    },
    {
        "id": 170, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>n = 153\nprint(sum(int(d)**3 for d in str(n)) == n)</pre>",
        "options": ["False", "True (число Армстронга)", "153", "Ошибку"],
        "answer": "B"
    },
    # ── Ещё вопросы ───────────────────────────────────────────────────────────
    {
        "id": 171, "topic": "Строки",
        "text": "Что выведет <code>print('py' in 'python')</code>?",
        "options": ["True", "False", "py", "2"],
        "answer": "A"
    },
    {
        "id": 172, "topic": "Строки",
        "text": "Что выведет <code>print('python'.count('o'))</code>?",
        "options": ["0", "1", "2", "3"],
        "answer": "B"
    },
    {
        "id": 173, "topic": "Строки",
        "text": "Что выведет <code>print('abc' * 0)</code>?",
        "options": ["abc", "0", "''", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 174, "topic": "Операторы",
        "text": "Что выведет <code>print(not 5 > 3)</code>?",
        "options": ["True", "False", "None", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 175, "topic": "Операторы",
        "text": "Что выведет <code>print(3 < 5 < 10)</code>?",
        "options": ["True", "False", "Error", "True True"],
        "answer": "A"
    },
    {
        "id": 176, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>result = 1\nfor i in range(1, 6):\n    result *= i\nprint(result)</pre>",
        "options": ["15", "120", "5", "6"],
        "answer": "B"
    },
    {
        "id": 177, "topic": "Циклы",
        "text": "Что выведет следующий код?<br><pre>i = 10\nwhile i > 0:\n    i //= 2\nprint(i)</pre>",
        "options": ["1", "0", "2", "Бесконечный цикл"],
        "answer": "B"
    },
    {
        "id": 178, "topic": "Списки",
        "text": "Что выведет <code>print([1,2,3,4,5][2:4])</code>?",
        "options": ["[2,3]", "[3,4]", "[2,3,4]", "[3,4,5]"],
        "answer": "B"
    },
    {
        "id": 179, "topic": "Списки",
        "text": "Что выведет следующий код?<br><pre>a = [1,2,3]\na.insert(1, 99)\nprint(a)</pre>",
        "options": ["[1,2,3,99]", "[99,1,2,3]", "[1,99,2,3]", "[1,2,99,3]"],
        "answer": "C"
    },
    {
        "id": 180, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def f(n):\n    return [i*i for i in range(n)]\nprint(f(5)[3])</pre>",
        "options": ["9", "16", "25", "4"],
        "answer": "A"
    },
    {
        "id": 181, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class A:\n    def __init__(self, x):\n        self.x = x\n    def __add__(self, other):\n        return A(self.x + other.x)\na = A(3) + A(4)\nprint(a.x)</pre>",
        "options": ["3", "4", "7", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 182, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class A:\n    def method(self):\n        return 'A'\nclass B(A):\n    def method(self):\n        return super().method() + 'B'\nprint(B().method())</pre>",
        "options": ["A", "B", "AB", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 183, "topic": "Словари",
        "text": "Что выведет следующий код?<br><pre>d = {'a':1,'b':2,'c':3}\nprint({v:k for k,v in d.items()})</pre>",
        "options": ["{'a':1,'b':2,'c':3}", "{1:'a',2:'b',3:'c'}", "Ошибку", "{1,2,3}"],
        "answer": "B"
    },
    {
        "id": 184, "topic": "Генераторы",
        "text": "Что выведет следующий код?<br><pre>def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\nprint(list(countdown(4)))</pre>",
        "options": ["[1,2,3,4]", "[4,3,2,1]", "[0,1,2,3]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 185, "topic": "Исключения",
        "text": "Что выведет следующий код?<br><pre>def safe_div(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\nprint(safe_div(10, 0))</pre>",
        "options": ["0", "10", "None", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 186, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>s = 'hello world'\nwords = s.split()\nprint(' '.join(w.capitalize() for w in words))</pre>",
        "options": ["hello world", "Hello World", "HELLO WORLD", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 187, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>from collections import Counter\nc = Counter('abracadabra')\nprint(c.most_common(1))</pre>",
        "options": ["[('a', 5)]", "[('b', 2)]", "[('r', 2)]", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 188, "topic": "Типы данных",
        "text": "Что выведет <code>print(complex(3, 4))</code>?",
        "options": ["(3+4j)", "3+4j", "7", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 189, "topic": "Синтаксис",
        "text": "Что выведет <code>print(\"\\\\n\")</code>?",
        "options": ["Новая строка", "\\n", "\\\\n", "n"],
        "answer": "B"
    },
    {
        "id": 190, "topic": "Синтаксис",
        "text": "Что выведет <code>print(r\"\\n\")</code>?",
        "options": ["Новая строка", "\\n", "n", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 191, "topic": "Алгоритмы",
        "text": "Что выведет следующий код?<br><pre>def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\nprint(gcd(56, 98))</pre>",
        "options": ["7", "14", "28", "56"],
        "answer": "B"
    },
    {
        "id": 192, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>n = 12345\ndigit_sum = sum(int(d) for d in str(n))\nprint(digit_sum)</pre>",
        "options": ["12345", "15", "5", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 193, "topic": "Практика",
        "text": "Что выведет следующий код?<br><pre>data = [5, 2, 8, 1, 9, 3]\ndata.sort()\nprint(data[len(data)//2])</pre>",
        "options": ["5", "4", "5 или 8", "Ошибку"],
        "answer": "A"
    },
    {
        "id": 194, "topic": "Функции",
        "text": "Что выведет следующий код?<br><pre>def apply(func, lst):\n    return [func(x) for x in lst]\nprint(apply(abs, [-3, 1, -2, 4]))</pre>",
        "options": ["[-3,1,-2,4]", "[3,1,2,4]", "Ошибку", "[3,-1,2,-4]"],
        "answer": "B"
    },
    {
        "id": 195, "topic": "Рекурсия",
        "text": "Что выведет следующий код?<br><pre>def digits(n):\n    if n < 10:\n        return [n]\n    return digits(n // 10) + [n % 10]\nprint(digits(357))</pre>",
        "options": ["[7,5,3]", "[3,5,7]", "[3,57]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 196, "topic": "Comprehensions",
        "text": "Что выведет следующий код?<br><pre>words = ['ant','bear','cat','deer']\nprint([w.upper() for w in words if len(w) > 3])</pre>",
        "options": ["['ANT','BEAR','CAT','DEER']", "['BEAR','DEER']", "['BEAR','CAT','DEER']", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 197, "topic": "ООП",
        "text": "Что выведет следующий код?<br><pre>class Temp:\n    def __init__(self, c):\n        self.c = c\n    @property\n    def fahrenheit(self):\n        return self.c * 9/5 + 32\nt = Temp(100)\nprint(t.fahrenheit)</pre>",
        "options": ["100", "212.0", "37.0", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 198, "topic": "Декораторы",
        "text": "Что выведет следующий код?<br><pre>calls = []\ndef log(f):\n    def w(*a):\n        calls.append(f.__name__)\n        return f(*a)\n    return w\n@log\ndef add(x,y): return x+y\nadd(1,2); add(3,4)\nprint(len(calls))</pre>",
        "options": ["0", "1", "2", "Ошибку"],
        "answer": "C"
    },
    {
        "id": 199, "topic": "Продвинутые темы",
        "text": "Что выведет следующий код?<br><pre>from itertools import chain\nprint(list(chain([1,2],[3,4],[5])))</pre>",
        "options": ["[[1,2],[3,4],[5]]", "[1,2,3,4,5]", "[(1,2),(3,4),(5,)]", "Ошибку"],
        "answer": "B"
    },
    {
        "id": 200, "topic": "Продвинутые темы",
        "text": "Что выведет следующий код?<br><pre>from collections import defaultdict\nd = defaultdict(list)\nfor k, v in [('a',1),('b',2),('a',3)]:\n    d[k].append(v)\nprint(dict(d))</pre>",
        "options": ["{'a':3,'b':2}", "{'a':[1,3],'b':[2]}", "{'a':[1],'b':[2],'a':[3]}", "Ошибку"],
        "answer": "B"
    },
]

OPTION_LABELS = ["A", "B", "C", "D"]

# ─── HTML ────────────────────────────────────────────────────────────────────

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Python Quiz — 9 класс</title>
<style>
  :root {
    --bg: #0f172a; --card: #1e293b; --border: #334155;
    --accent: #3b82f6; --green: #22c55e; --red: #ef4444;
    --text: #f1f5f9; --muted: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; min-height: 100vh; }
  .container { max-width: 800px; margin: 0 auto; padding: 24px 16px; }
  h1 { font-size: 1.6rem; margin-bottom: 8px; }
  .subtitle { color: var(--muted); margin-bottom: 24px; }

  #name-screen { text-align: center; padding-top: 80px; }
  #name-screen input { width: 100%; max-width: 360px; padding: 12px 16px; border-radius: 8px;
    border: 1px solid var(--border); background: var(--card); color: var(--text);
    font-size: 1rem; margin-bottom: 16px; display: block; margin: 0 auto 16px; }
  button { background: var(--accent); color: #fff; border: none; padding: 12px 28px;
    border-radius: 8px; font-size: 1rem; cursor: pointer; transition: opacity .15s; }
  button:hover { opacity: .85; }
  button:disabled { opacity: .4; cursor: default; }

  .progress-bar { height: 6px; background: var(--border); border-radius: 3px; margin-bottom: 24px; }
  .progress-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width .3s; }
  .progress-text { color: var(--muted); font-size: .85rem; margin-bottom: 8px; }

  .question-card { background: var(--card); border-radius: 12px; padding: 24px; margin-bottom: 20px; }
  .question-num { color: var(--muted); font-size: .8rem; margin-bottom: 8px; }
  .question-text { font-size: 1.05rem; line-height: 1.6; margin-bottom: 20px; }
  .question-text pre { background: #0f172a; padding: 12px; border-radius: 6px; margin-top: 8px;
    font-size: .88rem; overflow-x: auto; white-space: pre-wrap; }
  .options { display: grid; gap: 10px; }
  .option { display: flex; align-items: flex-start; gap: 12px; padding: 12px 16px;
    border: 1px solid var(--border); border-radius: 8px; cursor: pointer; transition: all .15s; }
  .option:hover { border-color: var(--accent); background: rgba(59,130,246,.08); }
  .option.selected { border-color: var(--accent); background: rgba(59,130,246,.15); }
  .option.correct { border-color: var(--green); background: rgba(34,197,94,.15); }
  .option.wrong { border-color: var(--red); background: rgba(239,68,68,.15); }
  .option-label { width: 28px; height: 28px; border-radius: 50%; border: 2px solid var(--border);
    display: flex; align-items: center; justify-content: center; font-weight: 600;
    font-size: .85rem; flex-shrink: 0; margin-top: 1px; }
  .option.selected .option-label { border-color: var(--accent); color: var(--accent); }
  .option.correct .option-label { border-color: var(--green); color: var(--green); }
  .option.wrong   .option-label { border-color: var(--red);   color: var(--red); }

  .nav-buttons { display: flex; gap: 12px; flex-wrap: wrap; }
  .btn-secondary { background: var(--card); border: 1px solid var(--border); color: var(--text); }
  .btn-secondary:hover { opacity: 1; border-color: var(--accent); }
  .btn-finish { background: var(--green); }

  .result-card { background: var(--card); border-radius: 12px; padding: 32px; text-align: center; margin-bottom: 24px; }
  .score-big { font-size: 3rem; font-weight: 700; margin: 16px 0; }
  .score-label { color: var(--muted); }

  table { width: 100%; border-collapse: collapse; margin-top: 16px; }
  th, td { text-align: left; padding: 10px 14px; border-bottom: 1px solid var(--border); }
  th { color: var(--muted); font-size: .85rem; font-weight: 500; }
  .badge { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: .8rem; font-weight: 600; }
  .badge-green { background: rgba(34,197,94,.2); color: var(--green); }
  .badge-yellow { background: rgba(234,179,8,.2); color: #eab308; }
  .badge-red { background: rgba(239,68,68,.2); color: var(--red); }
  .btn-sm { padding: 6px 14px; font-size: .82rem; margin-right: 4px; }
  .btn-outline { background: transparent; border: 1px solid var(--accent); color: var(--accent); }
  .stat-row { display: flex; gap: 24px; flex-wrap: wrap; margin: 16px 0; }
  .stat-box { background: var(--card); border-radius: 10px; padding: 16px 24px; flex: 1; min-width: 140px; }
  .stat-val { font-size: 1.8rem; font-weight: 700; }
  .stat-lbl { color: var(--muted); font-size: .82rem; }

  .answer-card { background: var(--card); border-radius: 10px; padding: 20px; margin-bottom: 14px; }
  .answer-status { font-size: .82rem; font-weight: 600; margin-bottom: 8px; }
  .answer-status.ok { color: var(--green); }
  .answer-status.fail { color: var(--red); }
  .answer-status.skip { color: var(--muted); }
  .given-answer { margin-top: 6px; font-size: .9rem; }
  .correct-answer { margin-top: 4px; font-size: .9rem; color: var(--green); }

  /* Jump grid */
  .jump-grid { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; }
  .jump-btn { width: 34px; height: 34px; border-radius: 6px; font-size: .78rem; padding: 0;
    background: var(--card); border: 1px solid var(--border); color: var(--muted); }
  .jump-btn.answered { background: rgba(59,130,246,.25); border-color: var(--accent); color: var(--text); }
  .jump-btn.current { border-color: var(--accent); color: var(--accent); font-weight: 700; }
</style>
</head>
<body>
<div class="container">

<div id="name-screen">
  <h1>🐍 Python Quiz</h1>
  <p class="subtitle">200 вопросов · 9 класс · Удачи!</p>
  <input type="text" id="student-name" placeholder="Введи своё имя и фамилию" maxlength="60">
  <br>
  <button id="btn-start" onclick="startQuiz()">Начать тест</button>
</div>

<div id="quiz-screen" style="display:none">
  <h1>🐍 Python Quiz</h1>
  <p class="subtitle" id="quiz-student-name"></p>
  <p class="progress-text" id="progress-text"></p>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  <div class="jump-grid" id="jump-grid"></div>
  <div id="question-container"></div>
  <div class="nav-buttons" style="margin-top:12px">
    <button class="btn-secondary" onclick="prevQ()">← Назад</button>
    <button class="btn-secondary" onclick="nextQ()">Вперёд →</button>
    <button class="btn-finish" onclick="finishQuiz()">Завершить тест</button>
  </div>
</div>

<div id="result-screen" style="display:none">
  <div class="result-card">
    <h1>Результат</h1>
    <div class="score-big" id="result-score"></div>
    <div class="score-label">правильных ответов из 200</div>
    <p style="margin-top:16px;color:var(--muted)" id="result-msg"></p>
  </div>
  <button onclick="viewMyAnswers()">Посмотреть мои ответы</button>
</div>

<div id="view-screen" style="display:none">
  <div id="view-content"><p style="color:var(--muted)">Загрузка…</p></div>
</div>

<div id="teacher-screen" style="display:none">
  <div id="teacher-content"><p style="color:var(--muted)">Загрузка…</p></div>
</div>

</div>

<script>
const QUESTIONS = __QUESTIONS_JSON__;
const TEACHER_MODE = __TEACHER_MODE__;
const REPORT_MODE = __REPORT_MODE__;
const VIEW_STUDENT = __VIEW_STUDENT__;
const TEACHER_KEY_VAL = __TEACHER_KEY__;

let currentQ = 0;
let answers = {};
let studentName = '';
let startedAt = '';

window.onload = function() {
  if (REPORT_MODE) { fetchReport(); return; }
  if (TEACHER_MODE) { showTeacherList(); return; }
  if (VIEW_STUDENT) { showViewScreen(VIEW_STUDENT, false); return; }
  document.getElementById('name-screen').style.display = 'block';
  document.getElementById('student-name').addEventListener('keydown', e => {
    if (e.key === 'Enter') startQuiz();
  });
};

function startQuiz() {
  const n = document.getElementById('student-name').value.trim();
  if (!n) { alert('Введи имя!'); return; }
  studentName = n;
  startedAt = new Date().toISOString();
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('quiz-screen').style.display = 'block';
  document.getElementById('quiz-student-name').textContent = n;
  renderJumpGrid();
  renderQuestion();
}

function renderJumpGrid() {
  const grid = document.getElementById('jump-grid');
  grid.innerHTML = QUESTIONS.map((q,i) => {
    const ans = answers[q.id];
    const cls = i === currentQ ? 'jump-btn current' : ans ? 'jump-btn answered' : 'jump-btn';
    return `<button class="${cls}" onclick="goToQ(${i})">${q.id}</button>`;
  }).join('');
}

function goToQ(i) { currentQ = i; renderQuestion(); renderJumpGrid(); }

function renderQuestion() {
  const q = QUESTIONS[currentQ];
  const total = QUESTIONS.length;
  document.getElementById('progress-text').textContent =
    `Вопрос ${currentQ+1} из ${total}  ·  Отвечено: ${Object.keys(answers).length}`;
  document.getElementById('progress-fill').style.width = `${((currentQ+1)/total)*100}%`;

  let html = `<div class="question-card">
    <div class="question-num">Вопрос ${q.id} · ${q.topic}</div>
    <div class="question-text">${q.text}</div>
    <div class="options">`;
  q.options.forEach((opt, i) => {
    const label = ['A','B','C','D'][i];
    const sel = answers[q.id] === label ? ' selected' : '';
    html += `<div class="option${sel}" onclick="selectAnswer(${q.id},'${label}',this)">
      <span class="option-label">${label}</span>
      <span>${opt}</span></div>`;
  });
  html += `</div></div>`;
  document.getElementById('question-container').innerHTML = html;
}

function selectAnswer(qid, label, el) {
  answers[qid] = label;
  document.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('progress-text').textContent =
    `Вопрос ${currentQ+1} из ${QUESTIONS.length}  ·  Отвечено: ${Object.keys(answers).length}`;
  renderJumpGrid();
}

function prevQ() { if (currentQ > 0) { currentQ--; renderQuestion(); renderJumpGrid(); } }
function nextQ() { if (currentQ < QUESTIONS.length-1) { currentQ++; renderQuestion(); renderJumpGrid(); } }

function finishQuiz() {
  const unanswered = QUESTIONS.length - Object.keys(answers).length;
  if (unanswered > 0) {
    if (!confirm(`Пропущено вопросов: ${unanswered}. Завершить?`)) return;
  }
  const score = QUESTIONS.filter(q => answers[q.id] === q.answer).length;
  const payload = {
    name: studentName,
    started_at: startedAt,
    finished_at: new Date().toISOString(),
    answers: answers,
    score: score,
    total: QUESTIONS.length
  };
  fetch('/python_check/save', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  }).then(r => r.json()).then(d => {
    if (d.ok) {
      document.getElementById('quiz-screen').style.display = 'none';
      document.getElementById('result-screen').style.display = 'block';
      document.getElementById('result-score').textContent = d.score;
      const pct = Math.round(d.score/QUESTIONS.length*100);
      document.getElementById('result-msg').textContent =
        pct >= 85 ? '🎉 Отлично!' : pct >= 70 ? '👍 Хорошо!' : pct >= 50 ? '📖 Неплохо, но есть куда расти' : '📚 Нужно повторить материал';
      window._savedName = studentName;
    } else { alert('Ошибка сохранения: ' + (d.error||'?')); }
  }).catch(() => alert('Ошибка сети'));
}

function viewMyAnswers() {
  document.getElementById('result-screen').style.display = 'none';
  showViewScreen(window._savedName, false);
}

function showViewScreen(name, withAnswers) {
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('view-screen').style.display = 'block';
  fetch('/python_check/student?name=' + encodeURIComponent(name))
    .then(r => r.json()).then(data => {
      if (data.error) { document.getElementById('view-content').innerHTML = '<p>Ученик не найден</p>'; return; }
      renderViewContent(data, withAnswers);
    });
}

function renderViewContent(data, withAnswers) {
  const pct = Math.round(data.score/data.total*100);
  let html = `<h1 style="margin-bottom:8px">${data.name}</h1>`;
  html += `<p class="subtitle">Результат: <b>${data.score}/${data.total}</b> (${pct}%)`;
  if (data.finished_at) html += ` &nbsp;·&nbsp; ${new Date(data.finished_at).toLocaleString('ru')}`;
  html += `</p>`;
  QUESTIONS.forEach(q => {
    const given = data.answers[String(q.id)];
    const isCorrect = given === q.answer;
    const statusClass = given ? (isCorrect ? 'ok' : 'fail') : 'skip';
    const statusText = given ? (isCorrect ? '✓ Верно' : '✗ Неверно') : '— Пропущено';
    html += `<div class="answer-card">
      <div class="answer-status ${statusClass}">${statusText}</div>
      <div class="question-num">Вопрос ${q.id} · ${q.topic}</div>
      <div class="question-text" style="margin:6px 0">${q.text}</div>`;
    if (given) {
      const givenIdx = ['A','B','C','D'].indexOf(given);
      html += `<div class="given-answer">Ответ: <b>${given})</b> ${q.options[givenIdx]||''}</div>`;
    }
    if (withAnswers && !isCorrect) {
      const corrIdx = ['A','B','C','D'].indexOf(q.answer);
      html += `<div class="correct-answer">Правильно: <b>${q.answer})</b> ${q.options[corrIdx]||''}</div>`;
    }
    html += `</div>`;
  });
  document.getElementById('view-content').innerHTML = html;
}

function showTeacherList() {
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('teacher-screen').style.display = 'block';
  const params = new URLSearchParams(location.search);
  const studentParam = params.get('student');
  if (studentParam) {
    document.getElementById('teacher-screen').style.display = 'none';
    document.getElementById('view-screen').style.display = 'block';
    fetch('/python_check/student?name=' + encodeURIComponent(studentParam))
      .then(r => r.json()).then(data => {
        if (data.error) { document.getElementById('view-content').innerHTML = '<p>Ученик не найден</p>'; return; }
        renderViewContent(data, true);
      });
    return;
  }
  fetch('/python_check/list').then(r => r.json()).then(renderTeacherList);
}

function renderTeacherList(students) {
  const tkey = new URLSearchParams(location.search).get('teacher');
  if (!students.length) {
    document.getElementById('teacher-content').innerHTML = '<h1>Учитель</h1><p style="color:var(--muted);margin-top:16px">Нет данных.</p>';
    return;
  }
  const scores = students.map(s => s.score);
  const avg = Math.round(scores.reduce((a,b)=>a+b,0)/scores.length);
  let html = `<h1>Панель учителя</h1>
  <div class="stat-row">
    <div class="stat-box"><div class="stat-val">${students.length}</div><div class="stat-lbl">Учеников</div></div>
    <div class="stat-box"><div class="stat-val">${avg}</div><div class="stat-lbl">Средний балл</div></div>
    <div class="stat-box"><div class="stat-val">${Math.min(...scores)}–${Math.max(...scores)}</div><div class="stat-lbl">Диапазон</div></div>
  </div>
  <table><thead><tr><th>Имя</th><th>Дата</th><th>Баллы</th><th>Действия</th></tr></thead><tbody>`;
  students.sort((a,b) => b.score - a.score).forEach(s => {
    const pct = Math.round(s.score/s.total*100);
    const bc = pct >= 85 ? 'badge-green' : pct >= 60 ? 'badge-yellow' : 'badge-red';
    const date = s.finished_at ? new Date(s.finished_at).toLocaleString('ru') : '—';
    html += `<tr>
      <td>${s.name}</td>
      <td style="color:var(--muted);font-size:.85rem">${date}</td>
      <td><span class="badge ${bc}">${s.score}/${s.total} (${pct}%)</span></td>
      <td>
        <button class="btn-sm btn-outline" onclick="teacherView('${encodeURIComponent(s.name)}','${tkey}',false)">Просмотр</button>
        <button class="btn-sm" onclick="teacherView('${encodeURIComponent(s.name)}','${tkey}',true)">С ответами</button>
      </td>
    </tr>`;
  });
  html += `</tbody></table>`;
  document.getElementById('teacher-content').innerHTML = html;
}

function teacherView(enc, tkey, withAnswers) {
  const name = decodeURIComponent(enc);
  document.getElementById('teacher-screen').style.display = 'none';
  document.getElementById('view-screen').style.display = 'block';
  const back = `<button class="btn-secondary" style="margin-bottom:16px" onclick="location.href='/python_check?teacher=${tkey}'">← Назад к списку</button>`;
  fetch('/python_check/student?name=' + encodeURIComponent(name))
    .then(r => r.json()).then(data => {
      if (data.error) { document.getElementById('view-content').innerHTML = back + '<p>Ученик не найден</p>'; return; }
      renderViewContent(data, withAnswers);
      document.getElementById('view-content').insertAdjacentHTML('afterbegin', back);
    });
}

function fetchReport() {
  fetch('/python_check/list').then(r => r.json()).then(d => {
    document.getElementById('name-screen').style.display = 'none';
    document.body.innerHTML = '<pre style="padding:24px;color:#f1f5f9;background:#0f172a;min-height:100vh">' +
      JSON.stringify(d, null, 2) + '</pre>';
  });
}
</script>
</body>
</html>
"""

# ─── Helper ──────────────────────────────────────────────────────────────────

ENGLISH_DATA_DIR = "/var/www/english_data"
ENGLISH_TEACHER_KEY = "eNg7LkQ2w5"

ENGLISH_QUESTIONS = [
    # ── Grammar: Tenses ──────────────────────────────────────────────────────
    {"id":1,"topic":"Tenses","text":"I ___ (work) here since 2019.","options":["work","am working","have worked","had worked"],"answer":"C"},
    {"id":2,"topic":"Tenses","text":"By the time we arrived, the film ___.","options":["already started","has already started","had already started","already starts"],"answer":"C"},
    {"id":3,"topic":"Tenses","text":"She ___ to Paris three times so far.","options":["has been","was","had been","is"],"answer":"A"},
    {"id":4,"topic":"Tenses","text":"This time tomorrow I ___ on the beach.","options":["will lie","will be lying","am lying","lie"],"answer":"B"},
    {"id":5,"topic":"Tenses","text":"He ___ the report before the meeting started.","options":["finished","has finished","had finished","was finishing"],"answer":"C"},
    {"id":6,"topic":"Tenses","text":"We ___ each other for ten years next month.","options":["will know","will have known","are knowing","have known"],"answer":"B"},
    {"id":7,"topic":"Tenses","text":"I ___ about calling you when you rang.","options":["just thought","was just thinking","have just thought","had just thought"],"answer":"B"},
    {"id":8,"topic":"Tenses","text":"She ___ three cups of coffee today.","options":["drank","has drunk","drinks","is drinking"],"answer":"B"},
    {"id":9,"topic":"Tenses","text":"By 2030 they ___ the new bridge.","options":["will build","will have built","are building","build"],"answer":"B"},
    {"id":10,"topic":"Tenses","text":"I ___ my keys — can you help me find them?","options":["lost","have lost","lose","was losing"],"answer":"B"},

    # ── Grammar: Conditionals ────────────────────────────────────────────────
    {"id":11,"topic":"Conditionals","text":"If I ___ you, I would accept the offer.","options":["am","was","were","be"],"answer":"C"},
    {"id":12,"topic":"Conditionals","text":"If she had studied harder, she ___ the exam.","options":["would pass","would have passed","will pass","passes"],"answer":"B"},
    {"id":13,"topic":"Conditionals","text":"Unless you ___, you'll miss the train.","options":["hurry","won't hurry","don't hurry","hurried"],"answer":"A"},
    {"id":14,"topic":"Conditionals","text":"If it rains tomorrow, we ___ at home.","options":["stay","will stay","would stay","stayed"],"answer":"B"},
    {"id":15,"topic":"Conditionals","text":"I wish I ___ more time for hobbies.","options":["have","had","would have","will have"],"answer":"B"},
    {"id":16,"topic":"Conditionals","text":"If only she ___ me about the party!","options":["tells","told","had told","would tell"],"answer":"C"},
    {"id":17,"topic":"Conditionals","text":"Provided that you ___ hard, you'll succeed.","options":["work","will work","worked","would work"],"answer":"A"},
    {"id":18,"topic":"Conditionals","text":"Were I ___ the answer, I would tell you.","options":["know","to know","knowing","knew"],"answer":"B"},
    {"id":19,"topic":"Conditionals","text":"If I hadn't been so tired, I ___ to the party.","options":["will go","would go","would have gone","went"],"answer":"C"},
    {"id":20,"topic":"Conditionals","text":"Suppose you ___ a million dollars, what would you do?","options":["win","won","had won","will win"],"answer":"B"},

    # ── Grammar: Passive Voice ───────────────────────────────────────────────
    {"id":21,"topic":"Passive Voice","text":"The cake ___ by my grandmother yesterday.","options":["was baked","baked","is baked","has baked"],"answer":"A"},
    {"id":22,"topic":"Passive Voice","text":"A new hospital ___ in our city now.","options":["is built","is being built","was built","has been built"],"answer":"B"},
    {"id":23,"topic":"Passive Voice","text":"The letter ___ yet.","options":["hasn't been sent","wasn't sent","isn't sent","didn't send"],"answer":"A"},
    {"id":24,"topic":"Passive Voice","text":"The window ___ by the children playing football.","options":["broke","was broken","has broken","is breaking"],"answer":"B"},
    {"id":25,"topic":"Passive Voice","text":"English ___ all over the world.","options":["speaks","is spoken","is speaking","has spoken"],"answer":"B"},

    # ── Grammar: Modal Verbs ─────────────────────────────────────────────────
    {"id":26,"topic":"Modal Verbs","text":"You ___ be tired after such a long flight.","options":["must","can","should","would"],"answer":"A"},
    {"id":27,"topic":"Modal Verbs","text":"She ___ have left already — her car is gone.","options":["must","can","should","would"],"answer":"A"},
    {"id":28,"topic":"Modal Verbs","text":"You ___ have told me earlier!","options":["must","should","can","would"],"answer":"B"},
    {"id":29,"topic":"Modal Verbs","text":"___ I borrow your pen, please?","options":["May","Must","Should","Would"],"answer":"A"},
    {"id":30,"topic":"Modal Verbs","text":"He ___ swim when he was five.","options":["can","could","may","must"],"answer":"B"},
    {"id":31,"topic":"Modal Verbs","text":"You ___ park here — it's a no-parking zone.","options":["mustn't","don't have to","shouldn't","needn't"],"answer":"A"},
    {"id":32,"topic":"Modal Verbs","text":"You ___ finish the report today; tomorrow is fine.","options":["mustn't","don't have to","can't","shouldn't"],"answer":"B"},
    {"id":33,"topic":"Modal Verbs","text":"She ___ be at home — I just saw her at the shop.","options":["can't","mustn't","shouldn't","needn't"],"answer":"A"},
    {"id":34,"topic":"Modal Verbs","text":"We ___ to wear a uniform at school.","options":["must","have","should","ought"],"answer":"B"},
    {"id":35,"topic":"Modal Verbs","text":"You ___ to apologise — it wasn't your fault.","options":["needn't","mustn't","don't need","shouldn't"],"answer":"C"},

    # ── Grammar: Reported Speech ─────────────────────────────────────────────
    {"id":36,"topic":"Reported Speech","text":"She said she ___ the film the day before.","options":["has seen","saw","had seen","sees"],"answer":"C"},
    {"id":37,"topic":"Reported Speech","text":"He told me he ___ help me the next day.","options":["will","would","can","shall"],"answer":"B"},
    {"id":38,"topic":"Reported Speech","text":"'I'm leaving tomorrow,' she said. → She said she ___ leaving ___.","options":["was / the next day","is / tomorrow","was / tomorrow","is / the next day"],"answer":"A"},
    {"id":39,"topic":"Reported Speech","text":"He asked me where I ___.","options":["live","lived","am living","do live"],"answer":"B"},
    {"id":40,"topic":"Reported Speech","text":"She asked if I ___ come to her party.","options":["can","could","will","may"],"answer":"B"},

    # ── Grammar: Relative Clauses ────────────────────────────────────────────
    {"id":41,"topic":"Relative Clauses","text":"The man ___ lives next door is a doctor.","options":["who","which","whom","whose"],"answer":"A"},
    {"id":42,"topic":"Relative Clauses","text":"The book ___ I bought yesterday is amazing.","options":["who","which","whose","whom"],"answer":"B"},
    {"id":43,"topic":"Relative Clauses","text":"That's the woman ___ son won the competition.","options":["who","which","whose","whom"],"answer":"C"},
    {"id":44,"topic":"Relative Clauses","text":"The restaurant ___ we had dinner was excellent.","options":["which","where","that","whose"],"answer":"B"},
    {"id":45,"topic":"Relative Clauses","text":"Is that the reason ___ you left early?","options":["which","where","why","when"],"answer":"C"},

    # ── Grammar: Articles ────────────────────────────────────────────────────
    {"id":46,"topic":"Articles","text":"I'd like ___ apple, please.","options":["a","an","the","—"],"answer":"B"},
    {"id":47,"topic":"Articles","text":"___ Nile is the longest river in Africa.","options":["A","An","The","—"],"answer":"C"},
    {"id":48,"topic":"Articles","text":"She plays ___ piano beautifully.","options":["a","an","the","—"],"answer":"C"},
    {"id":49,"topic":"Articles","text":"___ life is beautiful.","options":["A","The","An","—"],"answer":"D"},
    {"id":50,"topic":"Articles","text":"He is ___ honest person.","options":["a","an","the","—"],"answer":"B"},

    # ── Vocabulary: Phrasal Verbs ────────────────────────────────────────────
    {"id":51,"topic":"Phrasal Verbs","text":"Can you <b>turn down</b> the music? It means:","options":["Make louder","Make quieter","Turn off","Change"],"answer":"B"},
    {"id":52,"topic":"Phrasal Verbs","text":"I need to <b>look into</b> this problem. It means:","options":["Ignore","Investigate","Watch","Create"],"answer":"B"},
    {"id":53,"topic":"Phrasal Verbs","text":"She <b>gave up</b> smoking last year. It means:","options":["Started","Continued","Stopped","Enjoyed"],"answer":"C"},
    {"id":54,"topic":"Phrasal Verbs","text":"We had to <b>put off</b> the meeting. It means:","options":["Cancel","Postpone","Attend","Organise"],"answer":"B"},
    {"id":55,"topic":"Phrasal Verbs","text":"I can't <b>make out</b> what he's saying. It means:","options":["Hear clearly","Understand","See","Write"],"answer":"B"},
    {"id":56,"topic":"Phrasal Verbs","text":"Please <b>fill in</b> the form. It means:","options":["Throw away","Complete","Read","Sign"],"answer":"B"},
    {"id":57,"topic":"Phrasal Verbs","text":"The plane <b>took off</b> on time. It means:","options":["Landed","Departed","Crashed","Arrived"],"answer":"B"},
    {"id":58,"topic":"Phrasal Verbs","text":"I <b>came across</b> an old photo. It means:","options":["Lost","Found by chance","Threw away","Bought"],"answer":"B"},
    {"id":59,"topic":"Phrasal Verbs","text":"She <b>broke down</b> in tears. It means:","options":["Laughed","Smiled","Started crying","Fell asleep"],"answer":"C"},
    {"id":60,"topic":"Phrasal Verbs","text":"He <b>turned out</b> to be right. It means:","options":["Proved to be","Decided","Refused","Pretended"],"answer":"A"},

    # ── Vocabulary: Word Formation ───────────────────────────────────────────
    {"id":61,"topic":"Word Formation","text":"The opposite of 'possible' is:","options":["unpossible","impossible","dispossible","inpossible"],"answer":"B"},
    {"id":62,"topic":"Word Formation","text":"The noun form of 'decide' is:","options":["decidement","decidion","decision","deciding"],"answer":"C"},
    {"id":63,"topic":"Word Formation","text":"The adjective form of 'beauty' is:","options":["beautious","beautyful","beautiful","beautied"],"answer":"C"},
    {"id":64,"topic":"Word Formation","text":"The noun form of 'achieve' is:","options":["achieval","achievement","achieveness","achieving"],"answer":"B"},
    {"id":65,"topic":"Word Formation","text":"'Care' + suffix = full of care:","options":["careless","careful","caring","cared"],"answer":"B"},

    # ── Vocabulary: Collocations ─────────────────────────────────────────────
    {"id":66,"topic":"Collocations","text":"We need to ___ a decision quickly.","options":["do","make","take","get"],"answer":"B"},
    {"id":67,"topic":"Collocations","text":"She ___ a mistake on the test.","options":["did","made","had","took"],"answer":"B"},
    {"id":68,"topic":"Collocations","text":"Can you ___ me a favour?","options":["make","give","do","take"],"answer":"C"},
    {"id":69,"topic":"Collocations","text":"He ___ his best to help us.","options":["made","did","got","took"],"answer":"B"},
    {"id":70,"topic":"Collocations","text":"I'd like to ___ a complaint.","options":["do","make","give","put"],"answer":"B"},

    # ── Grammar: Prepositions ────────────────────────────────────────────────
    {"id":71,"topic":"Prepositions","text":"I'm interested ___ learning Japanese.","options":["at","on","in","for"],"answer":"C"},
    {"id":72,"topic":"Prepositions","text":"She's been waiting ___ the bus for 20 minutes.","options":["to","for","on","at"],"answer":"B"},
    {"id":73,"topic":"Prepositions","text":"He apologised ___ being late.","options":["about","for","of","to"],"answer":"B"},
    {"id":74,"topic":"Prepositions","text":"I'm not used ___ getting up early.","options":["for","to","at","with"],"answer":"B"},
    {"id":75,"topic":"Prepositions","text":"She depends ___ her parents financially.","options":["from","of","on","at"],"answer":"C"},

    # ── Grammar: Gerund vs Infinitive ────────────────────────────────────────
    {"id":76,"topic":"Gerund / Infinitive","text":"I enjoy ___ in the rain.","options":["walk","to walk","walking","walked"],"answer":"C"},
    {"id":77,"topic":"Gerund / Infinitive","text":"She decided ___ a new car.","options":["buying","to buy","buy","bought"],"answer":"B"},
    {"id":78,"topic":"Gerund / Infinitive","text":"He avoided ___ the question.","options":["to answer","answering","answer","answered"],"answer":"B"},
    {"id":79,"topic":"Gerund / Infinitive","text":"I can't afford ___ a new house.","options":["buying","to buy","buy","bought"],"answer":"B"},
    {"id":80,"topic":"Gerund / Infinitive","text":"She suggested ___ to the cinema.","options":["to go","going","go","went"],"answer":"B"},

    # ── Grammar: Comparatives & Superlatives ─────────────────────────────────
    {"id":81,"topic":"Comparatives","text":"This book is ___ than the last one.","options":["more interesting","interestinger","most interesting","the interesting"],"answer":"A"},
    {"id":82,"topic":"Comparatives","text":"She is the ___ student in the class.","options":["most clever","cleverest","more clever","clever"],"answer":"B"},
    {"id":83,"topic":"Comparatives","text":"The ___ you study, the ___ you'll get.","options":["harder / better","more hard / more good","hardest / best","most hard / most good"],"answer":"A"},
    {"id":84,"topic":"Comparatives","text":"This is ___ film I've ever seen.","options":["the worst","the worse","worse","bad"],"answer":"A"},
    {"id":85,"topic":"Comparatives","text":"My car is not as ___ as yours.","options":["fast","faster","fastest","more fast"],"answer":"A"},

    # ── Reading: Linking Words ───────────────────────────────────────────────
    {"id":86,"topic":"Linking Words","text":"___ the rain, we went for a walk.","options":["Despite","Although","Because","However"],"answer":"A"},
    {"id":87,"topic":"Linking Words","text":"He failed the exam ___ he didn't study enough.","options":["although","because","despite","however"],"answer":"B"},
    {"id":88,"topic":"Linking Words","text":"She's very talented. ___, she's also hardworking.","options":["Moreover","However","Although","Despite"],"answer":"A"},
    {"id":89,"topic":"Linking Words","text":"I was tired. ___, I finished the project.","options":["Moreover","Therefore","Nevertheless","Because"],"answer":"C"},
    {"id":90,"topic":"Linking Words","text":"___ having a headache, she went to work.","options":["Although","Despite","However","Because"],"answer":"B"},

    # ── Grammar: Used to / Would ─────────────────────────────────────────────
    {"id":91,"topic":"Used to / Would","text":"I ___ live in London when I was a child.","options":["used to","would","use to","was used to"],"answer":"A"},
    {"id":92,"topic":"Used to / Would","text":"She ___ play tennis every weekend. (repeated action)","options":["used to","would","use to","is used to"],"answer":"B"},
    {"id":93,"topic":"Used to / Would","text":"I'm ___ waking up early now.","options":["used to","use to","would","got used to"],"answer":"A"},
    {"id":94,"topic":"Used to / Would","text":"He didn't ___ like vegetables.","options":["used to","use to","would","get used to"],"answer":"B"},
    {"id":95,"topic":"Used to / Would","text":"It took me a while to ___ the cold weather.","options":["used to","use to","get used to","would"],"answer":"C"},

    # ── Vocabulary: Confusing Words ──────────────────────────────────────────
    {"id":96,"topic":"Confusing Words","text":"The news ___ very surprising.","options":["was","were","are","have been"],"answer":"A"},
    {"id":97,"topic":"Confusing Words","text":"I need some ___ about the course.","options":["informations","information","an information","the informations"],"answer":"B"},
    {"id":98,"topic":"Confusing Words","text":"She gave me a good piece of ___.","options":["advise","advice","advices","advises"],"answer":"B"},
    {"id":99,"topic":"Confusing Words","text":"There are ___ people in the park.","options":["few","a few","little","a little"],"answer":"B"},
    {"id":100,"topic":"Confusing Words","text":"I have ___ money left.","options":["few","a few","little","a little"],"answer":"D"},
]

def english_student_path(name):
    return os.path.join(ENGLISH_DATA_DIR, safe_filename(name) + ".json")


def load_all_english_students():
    students = []
    if not os.path.isdir(ENGLISH_DATA_DIR):
        return students
    for fname in os.listdir(ENGLISH_DATA_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(ENGLISH_DATA_DIR, fname), "r", encoding="utf-8") as f:
                    students.append(json.load(f))
            except Exception:
                pass
    return students


def safe_filename(name: str) -> str:
    name = name.strip()[:60]
    name = re.sub(r'[^\w\s\-]', '', name, flags=re.UNICODE)
    name = re.sub(r'\s+', '_', name)
    return name


def student_path(name: str) -> str:
    return os.path.join(DATA_DIR, safe_filename(name) + ".json")


def matan_path(name: str) -> str:
    return os.path.join(MATAN_DATA_DIR, safe_filename(name) + ".json")


def load_all_students():
    students = []
    if not os.path.isdir(DATA_DIR):
        return students
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
                    students.append(json.load(f))
            except Exception:
                pass
    return students


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/python_check")
@app.route("/python_check/")
def index():
    teacher_param = request.args.get("teacher", "")
    report_param = request.args.get("report", "")
    view_student = request.args.get("view", "")

    teacher_mode = "true" if teacher_param == TEACHER_KEY else "false"
    report_mode = "true" if report_param == REPORT_KEY else "false"
    view_student_js = json.dumps(view_student if view_student else "")
    teacher_key_js = json.dumps(TEACHER_KEY if teacher_param == TEACHER_KEY else "")

    questions_js = json.dumps([
        {"id": q["id"], "topic": q["topic"], "text": q["text"], "options": q["options"]}
        for q in QUESTIONS
    ], ensure_ascii=False)

    html = HTML_PAGE
    html = html.replace("__QUESTIONS_JSON__", questions_js)
    html = html.replace("__TEACHER_MODE__", teacher_mode)
    html = html.replace("__REPORT_MODE__", report_mode)
    html = html.replace("__VIEW_STUDENT__", view_student_js)
    html = html.replace("__TEACHER_KEY__", teacher_key_js)
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/python_check/save", methods=["POST"])
def save():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "no data"}), 400
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"ok": False, "error": "name required"}), 400

    answers = data.get("answers", {})
    score = sum(1 for q in QUESTIONS if str(answers.get(str(q["id"]), "")) == q["answer"])

    record = {
        "name": name,
        "started_at": data.get("started_at", ""),
        "finished_at": data.get("finished_at", datetime.now().isoformat()),
        "answers": {str(k): str(v) for k, v in answers.items()},
        "score": score,
        "total": len(QUESTIONS),
    }

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(student_path(name), "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    return jsonify({"ok": True, "score": score})


@app.route("/python_check/student")
def student():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    path = student_path(name)
    if not os.path.exists(path):
        return jsonify({"error": "not found"}), 404
    with open(path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/python_check/list")
def list_students():
    return jsonify(load_all_students())


# ─── Matan topics (save/load selection on server) ─────────────────────────────

@app.route("/matan_topics/load")
def matan_load():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    path = matan_path(name)
    if not os.path.exists(path):
        return jsonify({"sections": {}})
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception:
        return jsonify({"sections": {}})


@app.route("/matan_topics/save", methods=["POST"])
def matan_save():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "no data"}), 400
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"ok": False, "error": "name required"}), 400
    os.makedirs(MATAN_DATA_DIR, exist_ok=True)
    os.makedirs(ENGLISH_DATA_DIR, exist_ok=True)
    path = matan_path(name)

    if "sections" in data and isinstance(data["sections"], dict):
        sections = {}
        for section_title, indices in data["sections"].items():
            if not isinstance(indices, list):
                continue
            sections[str(section_title)] = [int(x) for x in indices if isinstance(x, (int, float)) and int(x) >= 0]
        payload = {"name": name, "sections": sections}
    else:
        selected = data.get("selected", [])
        if not isinstance(selected, list):
            selected = []
        selected = [int(x) for x in selected if isinstance(x, (int, float)) and 0 <= int(x) < 500]
        payload = {"name": name, "selected": selected}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return jsonify({"ok": True})



@app.route('/matan_topics/theory')
def matan_theory():
    try:
        idx = int(request.args.get('idx', ''))
    except (ValueError, TypeError):
        return jsonify({'error': 'invalid idx'}), 400
    theory_path = os.path.join(MATAN_DATA_DIR, 'theory.json')
    if not os.path.exists(theory_path):
        return jsonify({'paragraphs': []})
    try:
        with open(theory_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        paragraphs = data.get(str(idx), [])
        return jsonify({'paragraphs': paragraphs[:5]})
    except Exception:
        return jsonify({'paragraphs': []})




# ─── English Quiz Routes ─────────────────────────────────────────────────────

ENGLISH_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>English B1-B2 Quiz</title>
<style>
  :root { --bg:#0f1419; --card:#1a2332; --border:#2d3a4f; --accent:#58a6ff;
    --accent-dim:rgba(88,166,255,.15); --green:#3fb950; --red:#f85149;
    --text:#e6edf3; --muted:#8b949e; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif;
    min-height:100vh; line-height:1.5; }
  .container { max-width:640px; margin:0 auto; padding:32px 20px; }
  h1 { font-size:1.5rem; font-weight:600; margin-bottom:6px; }
  .subtitle { color:var(--muted); font-size:.9rem; margin-bottom:24px; }
  input[type=text] { width:100%; padding:12px 16px; border-radius:8px; border:1px solid var(--border);
    background:var(--card); color:var(--text); font-size:1rem; margin-bottom:16px; outline:none; }
  input:focus { border-color:var(--accent); }
  button { padding:12px 24px; border-radius:8px; border:none; font-size:.95rem;
    cursor:pointer; background:var(--accent); color:#fff; font-weight:600;
    transition:opacity .15s; }
  button:hover { opacity:.85; }
  .progress-text { color:var(--muted); font-size:.85rem; margin-bottom:8px; }
  .progress-bar { height:4px; background:var(--border); border-radius:2px; margin-bottom:16px; }
  .progress-fill { height:100%; background:var(--accent); border-radius:2px; transition:width .2s; }
  .question-card { background:var(--card); border-radius:12px; padding:24px; }
  .question-num { color:var(--muted); font-size:.8rem; margin-bottom:8px; }
  .question-text { font-size:1.05rem; margin-bottom:16px; line-height:1.6; }
  .options { display:flex; flex-direction:column; gap:8px; }
  .option { display:flex; align-items:center; gap:12px; padding:12px 16px; border-radius:8px;
    border:1px solid var(--border); cursor:pointer; transition:background .15s,border-color .15s; }
  .option:hover { background:var(--accent-dim); border-color:var(--accent); }
  .option.selected { background:var(--accent-dim); border-color:var(--accent); }
  .option-label { display:flex; align-items:center; justify-content:center; width:28px; height:28px;
    border-radius:6px; background:var(--border); font-weight:600; font-size:.85rem; flex-shrink:0; }
  .option.selected .option-label { background:var(--accent); color:#fff; }
  .nav-buttons { display:flex; gap:12px; flex-wrap:wrap; }
  .btn-secondary { background:var(--card); border:1px solid var(--border); color:var(--text); }
  .btn-secondary:hover { opacity:1; border-color:var(--accent); }
  .btn-finish { background:var(--green); }
  .result-card { background:var(--card); border-radius:12px; padding:32px; text-align:center; margin-bottom:24px; }
  .score-big { font-size:3rem; font-weight:700; margin:16px 0; }
  .score-label { color:var(--muted); }
  table { width:100%; border-collapse:collapse; margin-top:16px; }
  th,td { text-align:left; padding:10px 14px; border-bottom:1px solid var(--border); }
  th { color:var(--muted); font-size:.85rem; font-weight:500; }
  .badge { display:inline-block; padding:3px 10px; border-radius:99px; font-size:.8rem; font-weight:600; }
  .badge-green { background:rgba(34,197,94,.2); color:var(--green); }
  .badge-yellow { background:rgba(234,179,8,.2); color:#eab308; }
  .badge-red { background:rgba(239,68,68,.2); color:var(--red); }
  .btn-sm { padding:6px 14px; font-size:.82rem; margin-right:4px; }
  .btn-outline { background:transparent; border:1px solid var(--accent); color:var(--accent); }
  .stat-row { display:flex; gap:24px; flex-wrap:wrap; margin:16px 0; }
  .stat-box { background:var(--card); border-radius:10px; padding:16px 24px; flex:1; min-width:140px; }
  .stat-val { font-size:1.8rem; font-weight:700; }
  .stat-lbl { color:var(--muted); font-size:.82rem; }
  .answer-card { background:var(--card); border-radius:10px; padding:20px; margin-bottom:14px; }
  .answer-status { font-size:.82rem; font-weight:600; margin-bottom:8px; }
  .answer-status.ok { color:var(--green); }
  .answer-status.fail { color:var(--red); }
  .answer-status.skip { color:var(--muted); }
  .given-answer { margin-top:6px; font-size:.9rem; }
  .correct-answer { margin-top:4px; font-size:.9rem; color:var(--green); }
  .jump-grid { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:20px; }
  .jump-btn { width:34px; height:34px; border-radius:6px; font-size:.78rem; padding:0;
    background:var(--card); border:1px solid var(--border); color:var(--muted); }
  .jump-btn.answered { background:rgba(59,130,246,.25); border-color:var(--accent); color:var(--text); }
  .jump-btn.current { border-color:var(--accent); color:var(--accent); font-weight:700; }
</style>
</head>
<body>
<div class="container">

<div id="name-screen">
  <h1>🇬🇧 English B1-B2 Quiz</h1>
  <p class="subtitle">100 questions · Grammar & Vocabulary · Good luck!</p>
  <input type="text" id="student-name" placeholder="Enter your first and last name" maxlength="60">
  <br>
  <button id="btn-start" onclick="startQuiz()">Start Quiz</button>
</div>

<div id="quiz-screen" style="display:none">
  <h1>🇬🇧 English B1-B2 Quiz</h1>
  <p class="subtitle" id="quiz-student-name"></p>
  <p class="progress-text" id="progress-text"></p>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  <div class="jump-grid" id="jump-grid"></div>
  <div id="question-container"></div>
  <div class="nav-buttons" style="margin-top:12px">
    <button class="btn-secondary" onclick="prevQ()">← Back</button>
    <button class="btn-secondary" onclick="nextQ()">Next →</button>
    <button class="btn-finish" onclick="finishQuiz()">Finish Quiz</button>
  </div>
</div>

<div id="result-screen" style="display:none">
  <div class="result-card">
    <h1>Result</h1>
    <div class="score-big" id="result-score"></div>
    <div class="score-label">correct answers out of 100</div>
    <p style="margin-top:16px;color:var(--muted)" id="result-msg"></p>
  </div>
  <button onclick="viewMyAnswers()">View my answers</button>
</div>

<div id="view-screen" style="display:none">
  <div id="view-content"><p style="color:var(--muted)">Loading…</p></div>
</div>

<div id="teacher-screen" style="display:none">
  <div id="teacher-content"><p style="color:var(--muted)">Loading…</p></div>
</div>

</div>

<script>
const QUESTIONS = __QUESTIONS_JSON__;
const TEACHER_MODE = __TEACHER_MODE__;
const VIEW_STUDENT = __VIEW_STUDENT__;
const TEACHER_KEY_VAL = __TEACHER_KEY__;

let currentQ = 0;
let answers = {};
let studentName = '';
let startedAt = '';

window.onload = function() {
  if (TEACHER_MODE) { showTeacherList(); return; }
  if (VIEW_STUDENT) { showViewScreen(VIEW_STUDENT, false); return; }
  document.getElementById('name-screen').style.display = 'block';
  document.getElementById('student-name').addEventListener('keydown', e => {
    if (e.key === 'Enter') startQuiz();
  });
};

function startQuiz() {
  const n = document.getElementById('student-name').value.trim();
  if (!n) { alert('Please enter your name!'); return; }
  studentName = n;
  startedAt = new Date().toISOString();
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('quiz-screen').style.display = 'block';
  document.getElementById('quiz-student-name').textContent = n;
  renderJumpGrid();
  renderQuestion();
}

function renderJumpGrid() {
  const grid = document.getElementById('jump-grid');
  grid.innerHTML = QUESTIONS.map((q,i) => {
    const ans = answers[q.id];
    const cls = i === currentQ ? 'jump-btn current' : ans ? 'jump-btn answered' : 'jump-btn';
    return '<button class="'+cls+'" onclick="goToQ('+i+')">'+q.id+'</button>';
  }).join('');
}

function goToQ(i) { currentQ = i; renderQuestion(); renderJumpGrid(); }

function renderQuestion() {
  const q = QUESTIONS[currentQ];
  const total = QUESTIONS.length;
  document.getElementById('progress-text').textContent =
    'Question '+(currentQ+1)+' of '+total+'  ·  Answered: '+Object.keys(answers).length;
  document.getElementById('progress-fill').style.width = ((currentQ+1)/total*100)+'%';

  let html = '<div class="question-card"><div class="question-num">Question '+q.id+' · '+q.topic+'</div><div class="question-text">'+q.text+'</div><div class="options">';
  q.options.forEach((opt, i) => {
    const label = ['A','B','C','D'][i];
    const sel = answers[q.id] === label ? ' selected' : '';
    html += '<div class="option'+sel+'" onclick="selectAnswer('+q.id+',&#39;'+label+'&#39;,this)">';
      + '<span class="option-label">'+label+'</span><span>'+opt+'</span></div>';
  });
  html += '</div></div>';
  document.getElementById('question-container').innerHTML = html;
}

function selectAnswer(qid, label, el) {
  answers[qid] = label;
  document.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  document.getElementById('progress-text').textContent =
    'Question '+(currentQ+1)+' of '+QUESTIONS.length+'  ·  Answered: '+Object.keys(answers).length;
  renderJumpGrid();
}

function prevQ() { if (currentQ > 0) { currentQ--; renderQuestion(); renderJumpGrid(); } }
function nextQ() { if (currentQ < QUESTIONS.length-1) { currentQ++; renderQuestion(); renderJumpGrid(); } }

function finishQuiz() {
  const unanswered = QUESTIONS.length - Object.keys(answers).length;
  if (unanswered > 0) {
    if (!confirm('Unanswered: '+unanswered+'. Finish anyway?')) return;
  }
  const score = QUESTIONS.filter(q => answers[q.id] === q.answer).length;
  const payload = {
    name: studentName, started_at: startedAt,
    finished_at: new Date().toISOString(),
    answers: answers, score: score, total: QUESTIONS.length
  };
  fetch('/english_check/save', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  }).then(r => r.json()).then(d => {
    if (d.ok) {
      document.getElementById('quiz-screen').style.display = 'none';
      document.getElementById('result-screen').style.display = 'block';
      document.getElementById('result-score').textContent = d.score;
      const pct = Math.round(d.score/QUESTIONS.length*100);
      document.getElementById('result-msg').textContent =
        pct >= 85 ? 'Excellent!' : pct >= 70 ? 'Good job!' : pct >= 50 ? 'Not bad, keep practising!' : 'You need more practice!';
      window._savedName = studentName;
    } else { alert('Save error: '+(d.error||'?')); }
  }).catch(() => alert('Network error'));
}

function viewMyAnswers() {
  document.getElementById('result-screen').style.display = 'none';
  showViewScreen(window._savedName, false);
}

function showViewScreen(name, withAnswers) {
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('view-screen').style.display = 'block';
  fetch('/english_check/student?name='+encodeURIComponent(name))
    .then(r => r.json()).then(data => {
      if (data.error) { document.getElementById('view-content').innerHTML = '<p>Student not found</p>'; return; }
      renderViewContent(data, withAnswers);
    });
}

function renderViewContent(data, withAnswers) {
  const pct = Math.round(data.score/data.total*100);
  let html = '<h1 style="margin-bottom:8px">'+data.name+'</h1>';
  html += '<p class="subtitle">Result: <b>'+data.score+'/'+data.total+'</b> ('+pct+'%)';
  if (data.finished_at) html += ' &nbsp;·&nbsp; '+new Date(data.finished_at).toLocaleString('en');
  html += '</p>';
  QUESTIONS.forEach(q => {
    const given = data.answers[String(q.id)];
    const isCorrect = given === q.answer;
    const statusClass = given ? (isCorrect ? 'ok' : 'fail') : 'skip';
    const statusText = given ? (isCorrect ? '✓ Correct' : '✗ Wrong') : '— Skipped';
    html += '<div class="answer-card"><div class="answer-status '+statusClass+'">'+statusText+'</div>'
      + '<div class="question-num">Q'+q.id+' · '+q.topic+'</div>'
      + '<div class="question-text" style="margin:6px 0">'+q.text+'</div>';
    if (given) {
      const gi = ['A','B','C','D'].indexOf(given);
      html += '<div class="given-answer">Your answer: <b>'+given+')</b> '+(q.options[gi]||'')+'</div>';
    }
    if (withAnswers && !isCorrect) {
      const ci = ['A','B','C','D'].indexOf(q.answer);
      html += '<div class="correct-answer">Correct: <b>'+q.answer+')</b> '+(q.options[ci]||'')+'</div>';
    }
    html += '</div>';
  });
  document.getElementById('view-content').innerHTML = html;
}

function showTeacherList() {
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('teacher-screen').style.display = 'block';
  const params = new URLSearchParams(location.search);
  const sp = params.get('student');
  if (sp) {
    document.getElementById('teacher-screen').style.display = 'none';
    document.getElementById('view-screen').style.display = 'block';
    fetch('/english_check/student?name='+encodeURIComponent(sp))
      .then(r => r.json()).then(data => {
        if (data.error) { document.getElementById('view-content').innerHTML = '<p>Student not found</p>'; return; }
        renderViewContent(data, true);
      });
    return;
  }
  fetch('/english_check/list').then(r => r.json()).then(renderTeacherList);
}

function renderTeacherList(students) {
  const tkey = new URLSearchParams(location.search).get('teacher');
  if (!students.length) {
    document.getElementById('teacher-content').innerHTML = '<h1>Teacher Panel</h1><p style="color:var(--muted);margin-top:16px">No data.</p>';
    return;
  }
  const scores = students.map(s => s.score);
  const avg = Math.round(scores.reduce((a,b)=>a+b,0)/scores.length);
  let html = '<h1>Teacher Panel — English B1-B2</h1>'
    + '<div class="stat-row">'
    + '<div class="stat-box"><div class="stat-val">'+students.length+'</div><div class="stat-lbl">Students</div></div>'
    + '<div class="stat-box"><div class="stat-val">'+avg+'</div><div class="stat-lbl">Average</div></div>'
    + '<div class="stat-box"><div class="stat-val">'+Math.min(...scores)+'–'+Math.max(...scores)+'</div><div class="stat-lbl">Range</div></div>'
    + '</div>'
    + '<table><thead><tr><th>Name</th><th>Date</th><th>Score</th><th>Actions</th></tr></thead><tbody>';
  students.sort((a,b) => b.score - a.score).forEach(s => {
    const pct = Math.round(s.score/s.total*100);
    const bc = pct >= 85 ? 'badge-green' : pct >= 60 ? 'badge-yellow' : 'badge-red';
    const dt = s.finished_at ? new Date(s.finished_at).toLocaleString('en') : '—';
    html += '<tr><td>'+s.name+'</td><td style="color:var(--muted);font-size:.85rem">'+dt+'</td>'
      + '<td><span class="badge '+bc+'">'+s.score+'/'+s.total+' ('+pct+'%)</span></td>'
      + '<td><button class="btn-sm btn-outline" onclick="teacherView(&#39;'+encodeURIComponent(s.name)+'&#39;,&#39;'+tkey+'&#39;,false)">View</button>'
      + '<button class="btn-sm" onclick="teacherView(&#39;'+encodeURIComponent(s.name)+'&#39;,&#39;'+tkey+'&#39;,true)">With answers</button></td></tr>';
  });
  html += '</tbody></table>';
  document.getElementById('teacher-content').innerHTML = html;
}

function teacherView(enc, tkey, withAnswers) {
  const name = decodeURIComponent(enc);
  document.getElementById('teacher-screen').style.display = 'none';
  document.getElementById('view-screen').style.display = 'block';
  const back = '<button class="btn-secondary" style="margin-bottom:16px" onclick="location.href=&#39;/english_check?teacher='+tkey+'&#39;">← Back to list</button>';
  fetch('/english_check/student?name='+encodeURIComponent(name))
    .then(r => r.json()).then(data => {
      if (data.error) { document.getElementById('view-content').innerHTML = back+'<p>Student not found</p>'; return; }
      renderViewContent(data, withAnswers);
      document.getElementById('view-content').insertAdjacentHTML('afterbegin', back);
    });
}
</script>
</body>
</html>
"""


@app.route("/english_check")
@app.route("/english_check/")
def english_index():
    teacher_param = request.args.get("teacher", "")
    view_param = request.args.get("view", "")
    is_teacher = (teacher_param == ENGLISH_TEACHER_KEY)
    safe_q = json.dumps([{k: v for k, v in q.items() if k != "answer"} for q in ENGLISH_QUESTIONS], ensure_ascii=False)
    full_q = json.dumps(ENGLISH_QUESTIONS, ensure_ascii=False) if is_teacher else safe_q
    html = ENGLISH_HTML
    html = html.replace("__QUESTIONS_JSON__", full_q)
    html = html.replace("__TEACHER_MODE__", "true" if is_teacher else "false")
    html = html.replace("__VIEW_STUDENT__", json.dumps(view_param) if view_param else "null")
    html = html.replace("__TEACHER_KEY__", json.dumps(teacher_param))
    return html


@app.route("/english_check/save", methods=["POST"])
def english_save():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "no data"}), 400
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"ok": False, "error": "name required"}), 400
    os.makedirs(ENGLISH_DATA_DIR, exist_ok=True)
    answers = data.get("answers", {})
    score = sum(1 for q in ENGLISH_QUESTIONS if answers.get(str(q["id"])) == q["answer"])
    payload = {
        "name": name,
        "started_at": data.get("started_at", ""),
        "finished_at": data.get("finished_at", ""),
        "answers": answers,
        "score": score,
        "total": len(ENGLISH_QUESTIONS),
    }
    path = english_student_path(name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return jsonify({"ok": True, "score": score})


@app.route("/english_check/student")
def english_student():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    path = english_student_path(name)
    if not os.path.exists(path):
        return jsonify({"error": "not found"}), 404
    with open(path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/english_check/list")
def english_list():
    return jsonify(load_all_english_students())


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MATAN_DATA_DIR, exist_ok=True)
    os.makedirs(ENGLISH_DATA_DIR, exist_ok=True)
    app.run(host="127.0.0.1", port=5001, debug=False)
