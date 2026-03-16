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
  .jump-btn.correct { background:rgba(34,197,94,.3); border-color:var(--green); color:var(--green); }
  .jump-btn.incorrect { background:rgba(248,81,73,.25); border-color:var(--red); color:var(--red); }
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
    {"id": 1, "topic": "B1: Present Tenses", "text": "She ___ to school every day.", "options": ["go", "goes", "going", "is go"], "answer": "B"},
    {"id": 2, "topic": "B1: Present Tenses", "text": "I ___ my homework right now.", "options": ["do", "does", "am doing", "doing"], "answer": "C"},
    {"id": 3, "topic": "B1: Present Tenses", "text": "They ___ football on Sundays.", "options": ["play", "plays", "are playing", "is playing"], "answer": "A"},
    {"id": 4, "topic": "B1: Present Tenses", "text": "He ___ English very well.", "options": ["speak", "speaks", "is speaking", "speaking"], "answer": "B"},
    {"id": 5, "topic": "B1: Present Tenses", "text": "Look! It ___ outside.", "options": ["rains", "rain", "is raining", "raining"], "answer": "C"},
    {"id": 6, "topic": "B1: Present Tenses", "text": "We ___ lunch at 1 p.m. every day.", "options": ["have", "has", "are having", "having"], "answer": "A"},
    {"id": 7, "topic": "B1: Present Tenses", "text": "She ___ TV at the moment.", "options": ["watches", "watch", "is watching", "watching"], "answer": "C"},
    {"id": 8, "topic": "B1: Present Tenses", "text": "The Sun ___ in the east.", "options": ["rise", "rises", "is rising", "rising"], "answer": "B"},
    {"id": 9, "topic": "B1: Present Tenses", "text": "I ___ coffee. I prefer tea.", "options": ["don't like", "doesn't like", "am not liking", "not like"], "answer": "A"},
    {"id": 10, "topic": "B1: Present Tenses", "text": "What ___ you doing right now?", "options": ["do", "are", "is", "does"], "answer": "B"},
    {"id": 11, "topic": "B1: Present Tenses", "text": "___ she work in an office?", "options": ["Do", "Does", "Is", "Are"], "answer": "B"},
    {"id": 12, "topic": "B1: Present Tenses", "text": "He never ___ breakfast.", "options": ["eat", "eats", "is eating", "eating"], "answer": "B"},
    {"id": 13, "topic": "B1: Present Tenses", "text": "They ___ always late for class.", "options": ["is", "are", "be", "being"], "answer": "B"},
    {"id": 14, "topic": "B1: Present Tenses", "text": "I ___ to music while I study.", "options": ["listen", "listens", "am listening", "listening"], "answer": "C"},
    {"id": 15, "topic": "B1: Present Tenses", "text": "Water ___ at 100 degrees Celsius.", "options": ["boil", "boils", "is boiling", "boiling"], "answer": "B"},
    {"id": 16, "topic": "B1: Present Tenses", "text": "My mother ___ dinner now. Can I call back?", "options": ["cook", "cooks", "is cooking", "cooking"], "answer": "C"},
    {"id": 17, "topic": "B1: Present Tenses", "text": "He ___ three languages fluently.", "options": ["speak", "speaks", "is speaking", "speaking"], "answer": "B"},
    {"id": 18, "topic": "B1: Present Tenses", "text": "The children ___ in the garden right now.", "options": ["play", "plays", "are playing", "played"], "answer": "C"},
    {"id": 19, "topic": "B1: Present Tenses", "text": "I ___ this exercise is easy.", "options": ["think", "am thinking", "thinks", "thinking"], "answer": "A"},
    {"id": 20, "topic": "B1: Present Tenses", "text": "She ___ yoga every morning.", "options": ["practise", "practises", "is practising", "practised"], "answer": "B"},
    {"id": 21, "topic": "B1: Present Tenses", "text": "We ___ a great time at the party right now.", "options": ["have", "has", "are having", "having"], "answer": "C"},
    {"id": 22, "topic": "B1: Present Tenses", "text": "___ you understand this question?", "options": ["Do", "Are", "Is", "Does"], "answer": "A"},
    {"id": 23, "topic": "B1: Present Tenses", "text": "He ___ to work by bus.", "options": ["usually goes", "usually go", "is usually going", "goes usually"], "answer": "A"},
    {"id": 24, "topic": "B1: Present Tenses", "text": "Right now, I ___ for the exam.", "options": ["study", "studies", "am studying", "studying"], "answer": "C"},
    {"id": 25, "topic": "B1: Present Tenses", "text": "She ___ to the gym three times a week.", "options": ["go", "goes", "is going", "going"], "answer": "B"},
    {"id": 26, "topic": "B1: Past Tenses", "text": "I ___ to Paris last summer.", "options": ["go", "went", "have gone", "going"], "answer": "B"},
    {"id": 27, "topic": "B1: Past Tenses", "text": "She ___ a book when I called.", "options": ["read", "reads", "was reading", "is reading"], "answer": "C"},
    {"id": 28, "topic": "B1: Past Tenses", "text": "They ___ the match yesterday.", "options": ["win", "won", "have won", "winning"], "answer": "B"},
    {"id": 29, "topic": "B1: Past Tenses", "text": "We ___ dinner when the lights went out.", "options": ["have", "had", "were having", "having"], "answer": "C"},
    {"id": 30, "topic": "B1: Past Tenses", "text": "He ___ born in 1990.", "options": ["is", "was", "were", "been"], "answer": "B"},
    {"id": 31, "topic": "B1: Past Tenses", "text": "I ___ see the film last night.", "options": ["don't", "didn't", "wasn't", "haven't"], "answer": "B"},
    {"id": 32, "topic": "B1: Past Tenses", "text": "What ___ you do yesterday?", "options": ["do", "did", "were", "have"], "answer": "B"},
    {"id": 33, "topic": "B1: Past Tenses", "text": "She ___ while he was cooking.", "options": ["cleaned", "was cleaning", "cleans", "is cleaning"], "answer": "B"},
    {"id": 34, "topic": "B1: Past Tenses", "text": "They ___ to the beach every summer when they were children.", "options": ["go", "went", "were going", "have gone"], "answer": "B"},
    {"id": 35, "topic": "B1: Past Tenses", "text": "I ___ my keys yesterday. I couldn't find them.", "options": ["lose", "lost", "was losing", "have lost"], "answer": "B"},
    {"id": 36, "topic": "B1: Past Tenses", "text": "He ___ TV when the phone rang.", "options": ["watched", "was watching", "watches", "is watching"], "answer": "B"},
    {"id": 37, "topic": "B1: Past Tenses", "text": "We ___ football at 5 p.m. yesterday.", "options": ["play", "played", "were playing", "are playing"], "answer": "C"},
    {"id": 38, "topic": "B1: Past Tenses", "text": "___ she go to the party?", "options": ["Do", "Did", "Was", "Has"], "answer": "B"},
    {"id": 39, "topic": "B1: Past Tenses", "text": "I ___ my homework before I went out.", "options": ["finish", "finished", "was finishing", "have finished"], "answer": "B"},
    {"id": 40, "topic": "B1: Past Tenses", "text": "It ___ heavily when I left the house.", "options": ["rained", "was raining", "rains", "is raining"], "answer": "B"},
    {"id": 41, "topic": "B1: Past Tenses", "text": "She ___ him at a party in 2020.", "options": ["meet", "met", "was meeting", "has met"], "answer": "B"},
    {"id": 42, "topic": "B1: Past Tenses", "text": "They ___ in London for five years. Then they moved.", "options": ["live", "lived", "were living", "have lived"], "answer": "B"},
    {"id": 43, "topic": "B1: Past Tenses", "text": "While I ___ to work, I saw an accident.", "options": ["drive", "drove", "was driving", "am driving"], "answer": "C"},
    {"id": 44, "topic": "B1: Past Tenses", "text": "He ___ to swim when he was seven.", "options": ["learn", "learnt", "was learning", "has learnt"], "answer": "B"},
    {"id": 45, "topic": "B1: Past Tenses", "text": "The film ___ at 8 and finished at 10.", "options": ["start", "started", "was starting", "has started"], "answer": "B"},
    {"id": 46, "topic": "B1: Past Tenses", "text": "I ___ very tired after the long walk.", "options": ["am", "was", "were", "been"], "answer": "B"},
    {"id": 47, "topic": "B1: Past Tenses", "text": "We ___ a wonderful holiday last year.", "options": ["have", "had", "were having", "has"], "answer": "B"},
    {"id": 48, "topic": "B1: Past Tenses", "text": "She ___ her arm while she was skiing.", "options": ["break", "broke", "was breaking", "has broken"], "answer": "B"},
    {"id": 49, "topic": "B1: Past Tenses", "text": "At 9 p.m. last night, I ___ a book.", "options": ["read", "was reading", "am reading", "have read"], "answer": "B"},
    {"id": 50, "topic": "B1: Past Tenses", "text": "He ___ to the USA twice before he turned 20.", "options": ["travel", "travelled", "was travelling", "has travelled"], "answer": "B"},
    {"id": 51, "topic": "B1: Future", "text": "I ___ visit my grandmother tomorrow.", "options": ["will", "am going", "going", "shall to"], "answer": "A"},
    {"id": 52, "topic": "B1: Future", "text": "Look at those clouds! It ___ rain.", "options": ["will", "is going to", "going", "shall"], "answer": "B"},
    {"id": 53, "topic": "B1: Future", "text": "She ___ 18 next month.", "options": ["will be", "is going to be", "is being", "will being"], "answer": "A"},
    {"id": 54, "topic": "B1: Future", "text": "We ___ have a test next Friday.", "options": ["are going to", "will to", "going", "shall to"], "answer": "A"},
    {"id": 55, "topic": "B1: Future", "text": "I think it ___ be sunny tomorrow.", "options": ["will", "is going to", "going to", "is"], "answer": "A"},
    {"id": 56, "topic": "B1: Future", "text": "They ___ married in June.", "options": ["are getting", "will getting", "get", "getting"], "answer": "A"},
    {"id": 57, "topic": "B1: Future", "text": "I ___ help you with your homework.", "options": ["will", "am going", "going", "going to"], "answer": "A"},
    {"id": 58, "topic": "B1: Future", "text": "What ___ you going to do this weekend?", "options": ["do", "are", "will", "is"], "answer": "B"},
    {"id": 59, "topic": "B1: Future", "text": "The train ___ at 6:30 tomorrow morning.", "options": ["leaves", "will leave", "is going to leave", "leaving"], "answer": "A"},
    {"id": 60, "topic": "B1: Future", "text": "Don't worry, I ___ forget your birthday.", "options": ["won't", "am not going to", "don't", "not will"], "answer": "A"},
    {"id": 61, "topic": "B1: Future", "text": "She ___ study medicine at university.", "options": ["is going to", "will to", "going", "shall"], "answer": "A"},
    {"id": 62, "topic": "B1: Future", "text": "We ___ a party next Saturday. Would you like to come?", "options": ["are having", "will have", "have", "having"], "answer": "A"},
    {"id": 63, "topic": "B1: Future", "text": "I promise I ___ be late again.", "options": ["won't", "am not going to", "don't", "not"], "answer": "A"},
    {"id": 64, "topic": "B1: Future", "text": "He ___ probably call you later.", "options": ["will", "is going to", "going", "shall"], "answer": "A"},
    {"id": 65, "topic": "B1: Future", "text": "Be careful! You ___ fall!", "options": ["will", "are going to", "going", "shall"], "answer": "B"},
    {"id": 66, "topic": "B1: Future", "text": "The concert ___ at 8 p.m. (schedule)", "options": ["starts", "will start", "is going to start", "starting"], "answer": "A"},
    {"id": 67, "topic": "B1: Future", "text": "I ___ buy a new laptop next week.", "options": ["am going to", "will to", "going", "shall to"], "answer": "A"},
    {"id": 68, "topic": "B1: Future", "text": "What time ___ the meeting start?", "options": ["does", "will", "is", "going to"], "answer": "A"},
    {"id": 69, "topic": "B1: Future", "text": "She ___ visit us tonight. She already has plans.", "options": ["isn't going to", "won't to", "don't", "not going"], "answer": "A"},
    {"id": 70, "topic": "B1: Future", "text": "I ___ you when I arrive.", "options": ["will call", "am going to call", "call", "calling"], "answer": "A"},
    {"id": 71, "topic": "B1: Future", "text": "They ___ fly to Rome this summer. They booked the tickets.", "options": ["are going to", "will", "shall", "going"], "answer": "A"},
    {"id": 72, "topic": "B1: Future", "text": "Maybe I ___ go to the cinema tonight.", "options": ["will", "am going to", "going", "shall"], "answer": "A"},
    {"id": 73, "topic": "B1: Future", "text": "Hurry up! The bus ___ in five minutes.", "options": ["leaves", "will leave", "is going to leave", "leaving"], "answer": "A"},
    {"id": 74, "topic": "B1: Future", "text": "I think she ___ like the present.", "options": ["will", "is going to", "going to", "is"], "answer": "A"},
    {"id": 75, "topic": "B1: Future", "text": "We ___ move to a bigger flat soon.", "options": ["are going to", "will to", "going", "shall to"], "answer": "A"},
    {"id": 76, "topic": "B1: Present Perfect", "text": "I ___ never been to Japan.", "options": ["have", "has", "am", "was"], "answer": "A"},
    {"id": 77, "topic": "B1: Present Perfect", "text": "She ___ already finished her homework.", "options": ["have", "has", "is", "was"], "answer": "B"},
    {"id": 78, "topic": "B1: Present Perfect", "text": "Have you ever ___ sushi?", "options": ["eat", "ate", "eaten", "eating"], "answer": "C"},
    {"id": 79, "topic": "B1: Present Perfect", "text": "They ___ lived here since 2010.", "options": ["have", "has", "are", "were"], "answer": "A"},
    {"id": 80, "topic": "B1: Present Perfect", "text": "He ___ just arrived.", "options": ["have", "has", "is", "was"], "answer": "B"},
    {"id": 81, "topic": "B1: Present Perfect", "text": "I ___ seen that film three times.", "options": ["have", "has", "am", "was"], "answer": "A"},
    {"id": 82, "topic": "B1: Present Perfect", "text": "She ___ been to London twice.", "options": ["have", "has", "is", "was"], "answer": "B"},
    {"id": 83, "topic": "B1: Present Perfect", "text": "We ___ known each other for years.", "options": ["have", "has", "are", "were"], "answer": "A"},
    {"id": 84, "topic": "B1: Present Perfect", "text": "___ you ever met a famous person?", "options": ["Have", "Has", "Did", "Do"], "answer": "A"},
    {"id": 85, "topic": "B1: Present Perfect", "text": "He hasn't ___ me back yet.", "options": ["call", "called", "calling", "calls"], "answer": "B"},
    {"id": 86, "topic": "B1: Present Perfect", "text": "I've ___ my passport. Can you help me?", "options": ["lose", "lost", "losing", "loses"], "answer": "B"},
    {"id": 87, "topic": "B1: Present Perfect", "text": "How long ___ you known her?", "options": ["have", "has", "do", "did"], "answer": "A"},
    {"id": 88, "topic": "B1: Present Perfect", "text": "She ___ worked here since January.", "options": ["have", "has", "is", "was"], "answer": "B"},
    {"id": 89, "topic": "B1: Present Perfect", "text": "We've ___ to that restaurant many times.", "options": ["be", "been", "being", "was"], "answer": "B"},
    {"id": 90, "topic": "B1: Present Perfect", "text": "I haven't seen him ___ last Monday.", "options": ["for", "since", "from", "ago"], "answer": "B"},
    {"id": 91, "topic": "B1: Present Perfect", "text": "They have lived here ___ ten years.", "options": ["for", "since", "from", "ago"], "answer": "A"},
    {"id": 92, "topic": "B1: Present Perfect", "text": "He has ___ gone home.", "options": ["already", "yet", "still", "ago"], "answer": "A"},
    {"id": 93, "topic": "B1: Present Perfect", "text": "I haven't finished ___.", "options": ["already", "yet", "still", "just"], "answer": "B"},
    {"id": 94, "topic": "B1: Present Perfect", "text": "She's ___ bought a new car.", "options": ["just", "yet", "already", "still"], "answer": "A"},
    {"id": 95, "topic": "B1: Present Perfect", "text": "Have you ___ been to Australia?", "options": ["ever", "never", "already", "just"], "answer": "A"},
    {"id": 96, "topic": "B1: Present Perfect", "text": "He ___ broken his leg.", "options": ["have", "has", "is", "did"], "answer": "B"},
    {"id": 97, "topic": "B1: Present Perfect", "text": "I ___ not decided yet.", "options": ["have", "has", "am", "did"], "answer": "A"},
    {"id": 98, "topic": "B1: Present Perfect", "text": "She ___ studied French since school.", "options": ["have", "has", "is", "was"], "answer": "B"},
    {"id": 99, "topic": "B1: Present Perfect", "text": "We ___ already packed our bags.", "options": ["have", "has", "are", "were"], "answer": "A"},
    {"id": 100, "topic": "B1: Present Perfect", "text": "How many books ___ you read this year?", "options": ["have", "has", "did", "do"], "answer": "A"},
    {"id": 101, "topic": "B1: Modal Verbs", "text": "You ___ wear a uniform at school.", "options": ["must", "can", "should to", "would"], "answer": "A"},
    {"id": 102, "topic": "B1: Modal Verbs", "text": "___ I open the window?", "options": ["Can", "Must", "Should", "Would to"], "answer": "A"},
    {"id": 103, "topic": "B1: Modal Verbs", "text": "You ___ drive without a licence.", "options": ["mustn't", "don't have to", "shouldn't to", "can to"], "answer": "A"},
    {"id": 104, "topic": "B1: Modal Verbs", "text": "She ___ speak three languages.", "options": ["can", "must", "should", "would"], "answer": "A"},
    {"id": 105, "topic": "B1: Modal Verbs", "text": "You ___ see a doctor. You look ill.", "options": ["should", "must to", "can to", "would"], "answer": "A"},
    {"id": 106, "topic": "B1: Modal Verbs", "text": "I ___ swim when I was five.", "options": ["can", "could", "may", "must"], "answer": "B"},
    {"id": 107, "topic": "B1: Modal Verbs", "text": "You ___ eat in the library.", "options": ["mustn't", "don't have to", "can't to", "shouldn't to"], "answer": "A"},
    {"id": 108, "topic": "B1: Modal Verbs", "text": "You ___ come if you don't want to.", "options": ["don't have to", "mustn't", "can't", "shouldn't to"], "answer": "A"},
    {"id": 109, "topic": "B1: Modal Verbs", "text": "___ you help me, please?", "options": ["Could", "Must", "Should to", "Would to"], "answer": "A"},
    {"id": 110, "topic": "B1: Modal Verbs", "text": "Students ___ be quiet during the exam.", "options": ["must", "can", "should to", "would"], "answer": "A"},
    {"id": 111, "topic": "B1: Modal Verbs", "text": "He ___ to leave early yesterday.", "options": ["have", "had", "must", "should"], "answer": "B"},
    {"id": 112, "topic": "B1: Modal Verbs", "text": "I ___ go now. It's getting late.", "options": ["must", "can to", "should to", "will to"], "answer": "A"},
    {"id": 113, "topic": "B1: Modal Verbs", "text": "You ___ eat so much sugar. It's unhealthy.", "options": ["shouldn't", "mustn't to", "can't to", "don't should"], "answer": "A"},
    {"id": 114, "topic": "B1: Modal Verbs", "text": "She ___ play the piano very well.", "options": ["can", "must", "should to", "have to"], "answer": "A"},
    {"id": 115, "topic": "B1: Modal Verbs", "text": "We ___ to get up early tomorrow.", "options": ["have", "must to", "should to", "can to"], "answer": "A"},
    {"id": 116, "topic": "B1: Modal Verbs", "text": "___ you like some tea?", "options": ["Would", "Could", "Should", "Must"], "answer": "A"},
    {"id": 117, "topic": "B1: Modal Verbs", "text": "You ___ touch that! It's dangerous.", "options": ["mustn't", "don't have to", "shouldn't to", "can't to"], "answer": "A"},
    {"id": 118, "topic": "B1: Modal Verbs", "text": "I ___ understand this word. What does it mean?", "options": ["can't", "mustn't", "shouldn't", "don't have to"], "answer": "A"},
    {"id": 119, "topic": "B1: Modal Verbs", "text": "He ___ be at home. I saw him at the shop.", "options": ["can't", "mustn't", "shouldn't", "doesn't have to"], "answer": "A"},
    {"id": 120, "topic": "B1: Modal Verbs", "text": "You ___ try this cake. It's delicious!", "options": ["should", "must to", "can to", "would to"], "answer": "A"},
    {"id": 121, "topic": "B1: Modal Verbs", "text": "___ I use your phone?", "options": ["May", "Must", "Should to", "Would to"], "answer": "A"},
    {"id": 122, "topic": "B1: Modal Verbs", "text": "We ___ leave now or we'll miss the bus.", "options": ["had better", "better to", "should to", "must to"], "answer": "A"},
    {"id": 123, "topic": "B1: Modal Verbs", "text": "She ___ to work on Saturdays.", "options": ["doesn't have", "mustn't", "can't to", "shouldn't to"], "answer": "A"},
    {"id": 124, "topic": "B1: Modal Verbs", "text": "I think you ___ apologise to her.", "options": ["should", "must to", "can to", "would to"], "answer": "A"},
    {"id": 125, "topic": "B1: Modal Verbs", "text": "He ___ run very fast when he was young.", "options": ["could", "can", "may", "must"], "answer": "A"},
    {"id": 126, "topic": "B1: Comparatives", "text": "She is ___ than her sister.", "options": ["tall", "taller", "tallest", "more tall"], "answer": "B"},
    {"id": 127, "topic": "B1: Comparatives", "text": "This is the ___ film I've ever seen.", "options": ["good", "better", "best", "most good"], "answer": "C"},
    {"id": 128, "topic": "B1: Comparatives", "text": "My bag is ___ than yours.", "options": ["heavy", "heavier", "heaviest", "more heavy"], "answer": "B"},
    {"id": 129, "topic": "B1: Comparatives", "text": "He is the ___ student in the class.", "options": ["smart", "smarter", "smartest", "most smart"], "answer": "C"},
    {"id": 130, "topic": "B1: Comparatives", "text": "English is ___ than Maths for me.", "options": ["easy", "easier", "easiest", "more easy"], "answer": "B"},
    {"id": 131, "topic": "B1: Comparatives", "text": "This is the ___ expensive restaurant in town.", "options": ["more", "most", "much", "very"], "answer": "B"},
    {"id": 132, "topic": "B1: Comparatives", "text": "She runs ___ than me.", "options": ["fast", "faster", "fastest", "more fast"], "answer": "B"},
    {"id": 133, "topic": "B1: Comparatives", "text": "This book is ___ interesting than that one.", "options": ["more", "most", "much", "very"], "answer": "A"},
    {"id": 134, "topic": "B1: Comparatives", "text": "Today is the ___ day of the year.", "options": ["hot", "hotter", "hottest", "most hot"], "answer": "C"},
    {"id": 135, "topic": "B1: Comparatives", "text": "He is as ___ as his father.", "options": ["tall", "taller", "tallest", "more tall"], "answer": "A"},
    {"id": 136, "topic": "B1: Comparatives", "text": "That was the ___ meal I've ever had.", "options": ["bad", "worse", "worst", "most bad"], "answer": "C"},
    {"id": 137, "topic": "B1: Comparatives", "text": "My car is not as ___ as yours.", "options": ["fast", "faster", "fastest", "more fast"], "answer": "A"},
    {"id": 138, "topic": "B1: Comparatives", "text": "She is much ___ than she was last year.", "options": ["happy", "happier", "happiest", "more happy"], "answer": "B"},
    {"id": 139, "topic": "B1: Comparatives", "text": "This test is ___ difficult than the last one.", "options": ["less", "least", "fewer", "little"], "answer": "A"},
    {"id": 140, "topic": "B1: Comparatives", "text": "The ___ you study, the better your grades.", "options": ["more", "most", "much", "many"], "answer": "A"},
    {"id": 141, "topic": "B1: Comparatives", "text": "He is the ___ person I know.", "options": ["funny", "funnier", "funniest", "most funny"], "answer": "C"},
    {"id": 142, "topic": "B1: Comparatives", "text": "Living in a city is ___ expensive than in a village.", "options": ["more", "most", "much", "many"], "answer": "A"},
    {"id": 143, "topic": "B1: Comparatives", "text": "This exercise is ___ easier than the last one.", "options": ["much", "more", "very", "most"], "answer": "A"},
    {"id": 144, "topic": "B1: Comparatives", "text": "She is ___ older than me. Just one year.", "options": ["a little", "much", "a lot", "very"], "answer": "A"},
    {"id": 145, "topic": "B1: Comparatives", "text": "That was the ___ interesting book I've read.", "options": ["more", "most", "much", "very"], "answer": "B"},
    {"id": 146, "topic": "B1: Prepositions", "text": "I was born ___ March.", "options": ["in", "on", "at", "to"], "answer": "A"},
    {"id": 147, "topic": "B1: Prepositions", "text": "She arrived ___ Monday morning.", "options": ["in", "on", "at", "to"], "answer": "B"},
    {"id": 148, "topic": "B1: Prepositions", "text": "We have a meeting ___ 3 o'clock.", "options": ["in", "on", "at", "to"], "answer": "C"},
    {"id": 149, "topic": "B1: Prepositions", "text": "He lives ___ London.", "options": ["in", "on", "at", "to"], "answer": "A"},
    {"id": 150, "topic": "B1: Prepositions", "text": "I'm good ___ maths.", "options": ["in", "on", "at", "to"], "answer": "C"},
    {"id": 151, "topic": "B1: Prepositions", "text": "She's afraid ___ spiders.", "options": ["from", "of", "about", "for"], "answer": "B"},
    {"id": 152, "topic": "B1: Prepositions", "text": "He's interested ___ history.", "options": ["on", "in", "at", "for"], "answer": "B"},
    {"id": 153, "topic": "B1: Prepositions", "text": "I'm waiting ___ the bus.", "options": ["to", "for", "on", "at"], "answer": "B"},
    {"id": 154, "topic": "B1: Prepositions", "text": "She depends ___ her parents.", "options": ["from", "of", "on", "at"], "answer": "C"},
    {"id": 155, "topic": "B1: Prepositions", "text": "The book is ___ the table.", "options": ["in", "on", "at", "to"], "answer": "B"},
    {"id": 156, "topic": "B1: Prepositions", "text": "He apologised ___ being late.", "options": ["about", "for", "of", "to"], "answer": "B"},
    {"id": 157, "topic": "B1: Prepositions", "text": "I'm tired ___ waiting.", "options": ["from", "of", "about", "for"], "answer": "B"},
    {"id": 158, "topic": "B1: Prepositions", "text": "She's married ___ a doctor.", "options": ["with", "to", "for", "by"], "answer": "B"},
    {"id": 159, "topic": "B1: Prepositions", "text": "We arrived ___ the airport early.", "options": ["in", "on", "at", "to"], "answer": "C"},
    {"id": 160, "topic": "B1: Prepositions", "text": "I agree ___ you completely.", "options": ["to", "with", "for", "on"], "answer": "B"},
    {"id": 161, "topic": "B1: Prepositions", "text": "He suffers ___ headaches.", "options": ["of", "from", "with", "by"], "answer": "B"},
    {"id": 162, "topic": "B1: Prepositions", "text": "She's keen ___ photography.", "options": ["in", "on", "at", "for"], "answer": "B"},
    {"id": 163, "topic": "B1: Prepositions", "text": "I'm proud ___ my children.", "options": ["about", "for", "of", "with"], "answer": "C"},
    {"id": 164, "topic": "B1: Prepositions", "text": "He complained ___ the noise.", "options": ["about", "for", "of", "with"], "answer": "A"},
    {"id": 165, "topic": "B1: Prepositions", "text": "The film is based ___ a true story.", "options": ["in", "on", "at", "for"], "answer": "B"},
    {"id": 166, "topic": "B1: Passive Voice", "text": "English ___ spoken all over the world.", "options": ["is", "are", "was", "be"], "answer": "A"},
    {"id": 167, "topic": "B1: Passive Voice", "text": "The car ___ repaired yesterday.", "options": ["is", "was", "has", "were"], "answer": "B"},
    {"id": 168, "topic": "B1: Passive Voice", "text": "These books ___ written by Tolkien.", "options": ["is", "was", "were", "has"], "answer": "C"},
    {"id": 169, "topic": "B1: Passive Voice", "text": "The letter ___ sent tomorrow.", "options": ["will be", "is", "was", "has been"], "answer": "A"},
    {"id": 170, "topic": "B1: Passive Voice", "text": "Rice ___ grown in Asia.", "options": ["is", "are", "was", "were"], "answer": "A"},
    {"id": 171, "topic": "B1: Passive Voice", "text": "The window ___ broken by the children.", "options": ["is", "was", "has", "were"], "answer": "B"},
    {"id": 172, "topic": "B1: Passive Voice", "text": "The cake ___ made by my grandmother.", "options": ["is", "was", "has", "were"], "answer": "B"},
    {"id": 173, "topic": "B1: Passive Voice", "text": "A new hospital ___ being built here.", "options": ["is", "are", "was", "were"], "answer": "A"},
    {"id": 174, "topic": "B1: Passive Voice", "text": "The homework ___ done yet.", "options": ["hasn't been", "wasn't", "isn't", "didn't"], "answer": "A"},
    {"id": 175, "topic": "B1: Passive Voice", "text": "Spanish ___ spoken in many countries.", "options": ["is", "are", "was", "were"], "answer": "A"},
    {"id": 176, "topic": "B1: Passive Voice", "text": "The thief ___ caught by the police.", "options": ["is", "was", "has", "were"], "answer": "B"},
    {"id": 177, "topic": "B1: Passive Voice", "text": "This bridge ___ built in 1920.", "options": ["is", "was", "has", "were"], "answer": "B"},
    {"id": 178, "topic": "B1: Passive Voice", "text": "Football ___ played in almost every country.", "options": ["is", "are", "was", "were"], "answer": "A"},
    {"id": 179, "topic": "B1: Passive Voice", "text": "The meeting ___ cancelled.", "options": ["has been", "have been", "is being", "was being"], "answer": "A"},
    {"id": 180, "topic": "B1: Passive Voice", "text": "Many trees ___ cut down every year.", "options": ["is", "are", "was", "were"], "answer": "B"},
    {"id": 181, "topic": "B1: Conditionals", "text": "If it rains, I ___ stay at home.", "options": ["will", "would", "am", "do"], "answer": "A"},
    {"id": 182, "topic": "B1: Conditionals", "text": "If you heat water to 100°C, it ___.", "options": ["boils", "will boil", "would boil", "boil"], "answer": "A"},
    {"id": 183, "topic": "B1: Conditionals", "text": "If she ___ harder, she will pass.", "options": ["studies", "study", "will study", "studied"], "answer": "A"},
    {"id": 184, "topic": "B1: Conditionals", "text": "I'll call you if I ___ time.", "options": ["have", "will have", "had", "would have"], "answer": "A"},
    {"id": 185, "topic": "B1: Conditionals", "text": "If I were rich, I ___ travel the world.", "options": ["will", "would", "do", "am"], "answer": "B"},
    {"id": 186, "topic": "B1: Conditionals", "text": "If I ___ you, I would accept the offer.", "options": ["am", "was", "were", "be"], "answer": "C"},
    {"id": 187, "topic": "B1: Conditionals", "text": "Unless you hurry, you ___ miss the bus.", "options": ["will", "would", "do", "are"], "answer": "A"},
    {"id": 188, "topic": "B1: Conditionals", "text": "If I had more time, I ___ learn guitar.", "options": ["will", "would", "do", "am"], "answer": "B"},
    {"id": 189, "topic": "B1: Conditionals", "text": "What ___ you do if you won the lottery?", "options": ["will", "would", "do", "are"], "answer": "B"},
    {"id": 190, "topic": "B1: Conditionals", "text": "If he ___ English, he would get a better job.", "options": ["speaks", "spoke", "speak", "speaking"], "answer": "B"},
    {"id": 191, "topic": "B1: Conditionals", "text": "If it ___ sunny, we'll go to the beach.", "options": ["is", "will be", "was", "were"], "answer": "A"},
    {"id": 192, "topic": "B1: Conditionals", "text": "She wouldn't be late if she ___ up earlier.", "options": ["get", "gets", "got", "getting"], "answer": "C"},
    {"id": 193, "topic": "B1: Conditionals", "text": "If you mix red and blue, you ___ purple.", "options": ["get", "will get", "would get", "got"], "answer": "A"},
    {"id": 194, "topic": "B1: Conditionals", "text": "I would buy a house if I ___ enough money.", "options": ["have", "has", "had", "having"], "answer": "C"},
    {"id": 195, "topic": "B1: Conditionals", "text": "If I see her, I ___ tell her the news.", "options": ["will", "would", "do", "am"], "answer": "A"},
    {"id": 196, "topic": "B1: Articles", "text": "I need ___ umbrella.", "options": ["a", "an", "the", "—"], "answer": "B"},
    {"id": 197, "topic": "B1: Articles", "text": "___ moon goes around ___ earth.", "options": ["A/an", "The/the", "A/the", "—/the"], "answer": "B"},
    {"id": 198, "topic": "B1: Articles", "text": "She is ___ teacher.", "options": ["a", "an", "the", "—"], "answer": "A"},
    {"id": 199, "topic": "B1: Articles", "text": "I love ___ music.", "options": ["a", "an", "the", "—"], "answer": "D"},
    {"id": 200, "topic": "B1: Articles", "text": "He plays ___ guitar.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 201, "topic": "B1: Articles", "text": "I had ___ breakfast at 8.", "options": ["a", "an", "the", "—"], "answer": "D"},
    {"id": 202, "topic": "B1: Articles", "text": "She is ___ honest person.", "options": ["a", "an", "the", "—"], "answer": "B"},
    {"id": 203, "topic": "B1: Articles", "text": "We live in ___ UK.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 204, "topic": "B1: Articles", "text": "___ dogs are loyal animals.", "options": ["A", "The", "An", "—"], "answer": "D"},
    {"id": 205, "topic": "B1: Articles", "text": "I bought ___ new dress yesterday.", "options": ["a", "an", "the", "—"], "answer": "A"},
    {"id": 206, "topic": "B1: Articles", "text": "Can you pass me ___ salt, please?", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 207, "topic": "B1: Articles", "text": "He is ___ best player on the team.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 208, "topic": "B1: Articles", "text": "I want to be ___ engineer.", "options": ["a", "an", "the", "—"], "answer": "B"},
    {"id": 209, "topic": "B1: Articles", "text": "___ life is short.", "options": ["A", "The", "An", "—"], "answer": "D"},
    {"id": 210, "topic": "B1: Articles", "text": "She works in ___ hospital.", "options": ["a", "an", "the", "—"], "answer": "A"},
    {"id": 211, "topic": "B1: Relative Clauses", "text": "The girl ___ sits next to me is very kind.", "options": ["who", "which", "whose", "whom"], "answer": "A"},
    {"id": 212, "topic": "B1: Relative Clauses", "text": "The book ___ I'm reading is exciting.", "options": ["who", "which", "whose", "whom"], "answer": "B"},
    {"id": 213, "topic": "B1: Relative Clauses", "text": "The man ___ car was stolen called the police.", "options": ["who", "which", "whose", "whom"], "answer": "C"},
    {"id": 214, "topic": "B1: Relative Clauses", "text": "The hotel ___ we stayed was lovely.", "options": ["who", "where", "which", "whose"], "answer": "B"},
    {"id": 215, "topic": "B1: Relative Clauses", "text": "The woman ___ lives next door is a nurse.", "options": ["who", "which", "whose", "whom"], "answer": "A"},
    {"id": 216, "topic": "B1: Relative Clauses", "text": "That's the restaurant ___ serves great pizza.", "options": ["who", "which", "where", "whose"], "answer": "B"},
    {"id": 217, "topic": "B1: Relative Clauses", "text": "The reason ___ I called is important.", "options": ["who", "which", "why", "where"], "answer": "C"},
    {"id": 218, "topic": "B1: Relative Clauses", "text": "The day ___ we met was special.", "options": ["who", "which", "when", "where"], "answer": "C"},
    {"id": 219, "topic": "B1: Relative Clauses", "text": "The teacher ___ taught us was very patient.", "options": ["who", "which", "whose", "whom"], "answer": "A"},
    {"id": 220, "topic": "B1: Relative Clauses", "text": "Is this the bag ___ you lost?", "options": ["who", "which", "whose", "whom"], "answer": "B"},
    {"id": 221, "topic": "B1: Vocabulary", "text": "The opposite of 'cheap' is:", "options": ["expensive", "difficult", "dangerous", "lazy"], "answer": "A"},
    {"id": 222, "topic": "B1: Vocabulary", "text": "A person who fixes cars is a:", "options": ["chef", "mechanic", "pilot", "surgeon"], "answer": "B"},
    {"id": 223, "topic": "B1: Vocabulary", "text": "'Huge' means:", "options": ["very small", "very big", "very fast", "very old"], "answer": "B"},
    {"id": 224, "topic": "B1: Vocabulary", "text": "If you are 'exhausted', you are very:", "options": ["happy", "tired", "hungry", "angry"], "answer": "B"},
    {"id": 225, "topic": "B1: Vocabulary", "text": "To 'postpone' means to:", "options": ["cancel", "delay", "start", "finish"], "answer": "B"},
    {"id": 226, "topic": "B1: Vocabulary", "text": "A 'colleague' is someone you:", "options": ["live with", "work with", "study with", "travel with"], "answer": "B"},
    {"id": 227, "topic": "B1: Vocabulary", "text": "'Eventually' means:", "options": ["never", "at the end", "maybe", "recently"], "answer": "B"},
    {"id": 228, "topic": "B1: Vocabulary", "text": "A 'receipt' is given after you:", "options": ["cook", "pay", "sleep", "drive"], "answer": "B"},
    {"id": 229, "topic": "B1: Vocabulary", "text": "If something is 'compulsory', it is:", "options": ["optional", "forbidden", "required", "free"], "answer": "C"},
    {"id": 230, "topic": "B1: Vocabulary", "text": "'Reliable' means you can ___ someone.", "options": ["trust", "ignore", "avoid", "fear"], "answer": "A"},
    {"id": 231, "topic": "B1: Vocabulary", "text": "The opposite of 'ancient' is:", "options": ["modern", "huge", "deep", "heavy"], "answer": "A"},
    {"id": 232, "topic": "B1: Vocabulary", "text": "A 'decade' is ___ years.", "options": ["5", "10", "20", "100"], "answer": "B"},
    {"id": 233, "topic": "B1: Vocabulary", "text": "To 'recommend' means to:", "options": ["suggest", "refuse", "forget", "demand"], "answer": "A"},
    {"id": 234, "topic": "B1: Vocabulary", "text": "'Generous' means willing to ___ things.", "options": ["take", "break", "give", "hide"], "answer": "C"},
    {"id": 235, "topic": "B1: Vocabulary", "text": "A 'pedestrian' is a person who:", "options": ["drives", "walks", "flies", "swims"], "answer": "B"},
    {"id": 236, "topic": "B1: Vocabulary", "text": "To 'prohibit' means to:", "options": ["allow", "forbid", "encourage", "ignore"], "answer": "B"},
    {"id": 237, "topic": "B1: Vocabulary", "text": "'Frequent' means happening ___.", "options": ["rarely", "often", "never", "once"], "answer": "B"},
    {"id": 238, "topic": "B1: Vocabulary", "text": "A 'bargain' is something ___ cheap.", "options": ["surprisingly", "sadly", "angrily", "tiredly"], "answer": "A"},
    {"id": 239, "topic": "B1: Vocabulary", "text": "'Gradually' means:", "options": ["suddenly", "slowly", "quickly", "loudly"], "answer": "B"},
    {"id": 240, "topic": "B1: Vocabulary", "text": "A 'symptom' is a sign of:", "options": ["success", "illness", "happiness", "wealth"], "answer": "B"},
    {"id": 241, "topic": "B1: Vocabulary", "text": "To 'estimate' means to:", "options": ["calculate roughly", "know exactly", "forget completely", "ignore"], "answer": "A"},
    {"id": 242, "topic": "B1: Vocabulary", "text": "'Brief' means:", "options": ["long", "short", "wide", "deep"], "answer": "B"},
    {"id": 243, "topic": "B1: Vocabulary", "text": "A 'currency' is a type of:", "options": ["food", "money", "sport", "language"], "answer": "B"},
    {"id": 244, "topic": "B1: Vocabulary", "text": "'Annoyed' means slightly:", "options": ["happy", "angry", "scared", "bored"], "answer": "B"},
    {"id": 245, "topic": "B1: Vocabulary", "text": "To 'delete' means to:", "options": ["create", "copy", "remove", "save"], "answer": "C"},
    {"id": 246, "topic": "B1: Phrasal Verbs", "text": "Please ___ your shoes before entering.", "options": ["take off", "take on", "take up", "take in"], "answer": "A"},
    {"id": 247, "topic": "B1: Phrasal Verbs", "text": "I need to ___ early tomorrow.", "options": ["get up", "get on", "get over", "get in"], "answer": "A"},
    {"id": 248, "topic": "B1: Phrasal Verbs", "text": "Can you ___ the music? It's too loud.", "options": ["turn down", "turn up", "turn on", "turn over"], "answer": "A"},
    {"id": 249, "topic": "B1: Phrasal Verbs", "text": "She ___ the invitation because she was busy.", "options": ["turned down", "turned up", "turned on", "turned over"], "answer": "A"},
    {"id": 250, "topic": "B1: Phrasal Verbs", "text": "He ___ smoking last year.", "options": ["gave up", "gave in", "gave out", "gave away"], "answer": "A"},
    {"id": 251, "topic": "B1: Phrasal Verbs", "text": "I ___ my old friend in the street.", "options": ["ran into", "ran out", "ran up", "ran over"], "answer": "A"},
    {"id": 252, "topic": "B1: Phrasal Verbs", "text": "Please ___ the form with your details.", "options": ["fill in", "fill up", "fill out", "fill on"], "answer": "A"},
    {"id": 253, "topic": "B1: Phrasal Verbs", "text": "The meeting was ___ until next week.", "options": ["put off", "put on", "put up", "put in"], "answer": "A"},
    {"id": 254, "topic": "B1: Phrasal Verbs", "text": "I need to ___ my English for the exam.", "options": ["brush up on", "brush off", "brush out", "brush away"], "answer": "A"},
    {"id": 255, "topic": "B1: Phrasal Verbs", "text": "She ___ the children while I was out.", "options": ["looked after", "looked for", "looked up", "looked into"], "answer": "A"},
    {"id": 256, "topic": "B1: Phrasal Verbs", "text": "Can you ___ this word in the dictionary?", "options": ["look up", "look after", "look for", "look into"], "answer": "A"},
    {"id": 257, "topic": "B1: Phrasal Verbs", "text": "We need to ___ a solution to this problem.", "options": ["come up with", "come across", "come down", "come over"], "answer": "A"},
    {"id": 258, "topic": "B1: Phrasal Verbs", "text": "The plane ___ at 6 a.m.", "options": ["took off", "took on", "took up", "took in"], "answer": "A"},
    {"id": 259, "topic": "B1: Phrasal Verbs", "text": "He ___ well with his colleagues.", "options": ["gets on", "gets up", "gets over", "gets in"], "answer": "A"},
    {"id": 260, "topic": "B1: Phrasal Verbs", "text": "I ___ the mess after the party.", "options": ["cleared up", "cleared out", "cleared off", "cleared away"], "answer": "A"},
    {"id": 261, "topic": "B1: Linking Words", "text": "I like tea ___ I don't like coffee.", "options": ["but", "and", "so", "because"], "answer": "A"},
    {"id": 262, "topic": "B1: Linking Words", "text": "She was tired ___ she went to bed early.", "options": ["but", "and", "so", "because"], "answer": "C"},
    {"id": 263, "topic": "B1: Linking Words", "text": "I stayed home ___ it was raining.", "options": ["but", "although", "because", "so"], "answer": "C"},
    {"id": 264, "topic": "B1: Linking Words", "text": "___ it was cold, she didn't wear a coat.", "options": ["Although", "Because", "So", "But"], "answer": "A"},
    {"id": 265, "topic": "B1: Linking Words", "text": "He studied hard. ___, he failed the exam.", "options": ["Moreover", "However", "Therefore", "Because"], "answer": "B"},
    {"id": 266, "topic": "B1: Linking Words", "text": "I'll go ___ you come with me.", "options": ["unless", "if", "although", "however"], "answer": "B"},
    {"id": 267, "topic": "B1: Linking Words", "text": "She likes both swimming ___ running.", "options": ["or", "and", "but", "so"], "answer": "B"},
    {"id": 268, "topic": "B1: Linking Words", "text": "I was hungry, ___ I made a sandwich.", "options": ["but", "although", "so", "because"], "answer": "C"},
    {"id": 269, "topic": "B1: Linking Words", "text": "He was late ___ the traffic.", "options": ["because", "because of", "although", "despite"], "answer": "B"},
    {"id": 270, "topic": "B1: Linking Words", "text": "___ studying hard, he didn't pass.", "options": ["Although", "Despite", "Because", "However"], "answer": "B"},
    {"id": 271, "topic": "B1: Gerund/Infinitive", "text": "I enjoy ___ books.", "options": ["read", "to read", "reading", "reads"], "answer": "C"},
    {"id": 272, "topic": "B1: Gerund/Infinitive", "text": "She decided ___ abroad.", "options": ["study", "to study", "studying", "studies"], "answer": "B"},
    {"id": 273, "topic": "B1: Gerund/Infinitive", "text": "He avoids ___ fast food.", "options": ["eat", "to eat", "eating", "eats"], "answer": "C"},
    {"id": 274, "topic": "B1: Gerund/Infinitive", "text": "I want ___ a doctor.", "options": ["be", "to be", "being", "been"], "answer": "B"},
    {"id": 275, "topic": "B1: Gerund/Infinitive", "text": "She suggested ___ to the park.", "options": ["go", "to go", "going", "goes"], "answer": "C"},
    {"id": 276, "topic": "B1: Gerund/Infinitive", "text": "I can't stand ___ in queues.", "options": ["wait", "to wait", "waiting", "waits"], "answer": "C"},
    {"id": 277, "topic": "B1: Gerund/Infinitive", "text": "He agreed ___ me.", "options": ["help", "to help", "helping", "helps"], "answer": "B"},
    {"id": 278, "topic": "B1: Gerund/Infinitive", "text": "She keeps ___ the same mistake.", "options": ["make", "to make", "making", "makes"], "answer": "C"},
    {"id": 279, "topic": "B1: Gerund/Infinitive", "text": "I hope ___ you soon.", "options": ["see", "to see", "seeing", "sees"], "answer": "B"},
    {"id": 280, "topic": "B1: Gerund/Infinitive", "text": "He denied ___ the vase.", "options": ["break", "to break", "breaking", "breaks"], "answer": "C"},
    {"id": 281, "topic": "B1: Gerund/Infinitive", "text": "I refuse ___ that.", "options": ["believe", "to believe", "believing", "believes"], "answer": "B"},
    {"id": 282, "topic": "B1: Gerund/Infinitive", "text": "She doesn't mind ___ overtime.", "options": ["work", "to work", "working", "works"], "answer": "C"},
    {"id": 283, "topic": "B1: Gerund/Infinitive", "text": "He promised ___ on time.", "options": ["arrive", "to arrive", "arriving", "arrives"], "answer": "B"},
    {"id": 284, "topic": "B1: Gerund/Infinitive", "text": "I finished ___ the report.", "options": ["write", "to write", "writing", "writes"], "answer": "C"},
    {"id": 285, "topic": "B1: Gerund/Infinitive", "text": "She offered ___ me.", "options": ["help", "to help", "helping", "helps"], "answer": "B"},
    {"id": 286, "topic": "B2: Perfect Tenses", "text": "By the time we arrived, the concert ___.", "options": ["started", "has started", "had started", "was starting"], "answer": "C"},
    {"id": 287, "topic": "B2: Perfect Tenses", "text": "I ___ (work) here for five years by next June.", "options": ["will work", "will have worked", "will be working", "am working"], "answer": "B"},
    {"id": 288, "topic": "B2: Perfect Tenses", "text": "She ___ (never/try) sushi before she went to Japan.", "options": ["never tried", "has never tried", "had never tried", "was never trying"], "answer": "C"},
    {"id": 289, "topic": "B2: Perfect Tenses", "text": "They ___ (live) in Paris for a decade when they decided to move.", "options": ["lived", "have lived", "had been living", "were living"], "answer": "C"},
    {"id": 290, "topic": "B2: Perfect Tenses", "text": "By this time tomorrow, I ___ the report.", "options": ["finish", "will finish", "will have finished", "am finishing"], "answer": "C"},
    {"id": 291, "topic": "B2: Perfect Tenses", "text": "He ___ three novels by the age of 25.", "options": ["wrote", "has written", "had written", "was writing"], "answer": "C"},
    {"id": 292, "topic": "B2: Perfect Tenses", "text": "I ___ about calling you when you rang.", "options": ["just thought", "was just thinking", "have just thought", "had just been thinking"], "answer": "D"},
    {"id": 293, "topic": "B2: Perfect Tenses", "text": "By 2030, scientists ___ a cure for cancer, hopefully.", "options": ["find", "will find", "will have found", "are finding"], "answer": "C"},
    {"id": 294, "topic": "B2: Perfect Tenses", "text": "She looked tired because she ___ all night.", "options": ["studied", "has studied", "had been studying", "was studying"], "answer": "C"},
    {"id": 295, "topic": "B2: Perfect Tenses", "text": "We ___ each other for years before we started dating.", "options": ["know", "knew", "had known", "have known"], "answer": "C"},
    {"id": 296, "topic": "B2: Perfect Tenses", "text": "He ___ the whole cake by the time we got home.", "options": ["ate", "has eaten", "had eaten", "was eating"], "answer": "C"},
    {"id": 297, "topic": "B2: Perfect Tenses", "text": "I ___ waiting for an hour when the bus finally came.", "options": ["was", "have been", "had been", "am"], "answer": "C"},
    {"id": 298, "topic": "B2: Perfect Tenses", "text": "By next week, they ___ here for a month.", "options": ["will live", "will have lived", "will be living", "are living"], "answer": "B"},
    {"id": 299, "topic": "B2: Perfect Tenses", "text": "She ___ (just/finish) her speech when the alarm went off.", "options": ["just finished", "has just finished", "had just finished", "was just finishing"], "answer": "C"},
    {"id": 300, "topic": "B2: Perfect Tenses", "text": "I realised I ___ my wallet at home.", "options": ["leave", "left", "had left", "have left"], "answer": "C"},
    {"id": 301, "topic": "B2: Perfect Tenses", "text": "By the end of this year, I ___ five countries.", "options": ["visit", "will visit", "will have visited", "am visiting"], "answer": "C"},
    {"id": 302, "topic": "B2: Perfect Tenses", "text": "He was exhausted. He ___ for twelve hours straight.", "options": ["worked", "has worked", "had been working", "was working"], "answer": "C"},
    {"id": 303, "topic": "B2: Perfect Tenses", "text": "No sooner ___ I sat down than the phone rang.", "options": ["—", "had", "have", "did"], "answer": "B"},
    {"id": 304, "topic": "B2: Perfect Tenses", "text": "They ___ married for 20 years next April.", "options": ["are", "will be", "will have been", "have been"], "answer": "C"},
    {"id": 305, "topic": "B2: Perfect Tenses", "text": "The road was wet. It ___ earlier.", "options": ["rained", "has rained", "had rained", "was raining"], "answer": "C"},
    {"id": 306, "topic": "B2: Perfect Tenses", "text": "I ___ the book three times. It's that good.", "options": ["read", "have read", "had read", "am reading"], "answer": "B"},
    {"id": 307, "topic": "B2: Perfect Tenses", "text": "By midnight, we ___ for 8 hours.", "options": ["drive", "will drive", "will have been driving", "are driving"], "answer": "C"},
    {"id": 308, "topic": "B2: Perfect Tenses", "text": "She ___ (already/leave) when I arrived.", "options": ["already left", "has already left", "had already left", "was already leaving"], "answer": "C"},
    {"id": 309, "topic": "B2: Perfect Tenses", "text": "This is the third time you ___ late this week.", "options": ["are", "were", "have been", "had been"], "answer": "C"},
    {"id": 310, "topic": "B2: Perfect Tenses", "text": "I wish I ___ harder at school.", "options": ["study", "studied", "had studied", "have studied"], "answer": "C"},
    {"id": 311, "topic": "B2: Conditionals", "text": "If she had studied harder, she ___ the exam.", "options": ["would pass", "would have passed", "will pass", "passes"], "answer": "B"},
    {"id": 312, "topic": "B2: Conditionals", "text": "Had I known about the problem, I ___ helped.", "options": ["will have", "would have", "had", "could"], "answer": "B"},
    {"id": 313, "topic": "B2: Conditionals", "text": "If only I ___ more time!", "options": ["have", "had", "would have", "will have"], "answer": "B"},
    {"id": 314, "topic": "B2: Conditionals", "text": "I wish I ___ what to say.", "options": ["know", "knew", "had known", "would know"], "answer": "B"},
    {"id": 315, "topic": "B2: Conditionals", "text": "Were I ___ the answer, I would tell you.", "options": ["know", "to know", "knowing", "knew"], "answer": "B"},
    {"id": 316, "topic": "B2: Conditionals", "text": "If I hadn't missed the bus, I ___ late.", "options": ["wouldn't be", "wouldn't have been", "won't be", "am not"], "answer": "B"},
    {"id": 317, "topic": "B2: Conditionals", "text": "Suppose you ___ the lottery, what would you buy?", "options": ["win", "won", "had won", "will win"], "answer": "B"},
    {"id": 318, "topic": "B2: Conditionals", "text": "But for your help, I ___ have succeeded.", "options": ["would", "wouldn't", "could", "couldn't"], "answer": "B"},
    {"id": 319, "topic": "B2: Conditionals", "text": "Provided that everyone ___, we can start.", "options": ["agree", "agrees", "agreed", "will agree"], "answer": "B"},
    {"id": 320, "topic": "B2: Conditionals", "text": "If she hadn't warned us, we ___ into trouble.", "options": ["would get", "would have got", "will get", "got"], "answer": "B"},
    {"id": 321, "topic": "B2: Conditionals", "text": "It's time we ___ home.", "options": ["go", "went", "will go", "going"], "answer": "B"},
    {"id": 322, "topic": "B2: Conditionals", "text": "I'd rather you ___ me the truth.", "options": ["tell", "told", "will tell", "telling"], "answer": "B"},
    {"id": 323, "topic": "B2: Conditionals", "text": "If it weren't for the rain, we ___ outside.", "options": ["would eat", "would have eaten", "will eat", "eat"], "answer": "A"},
    {"id": 324, "topic": "B2: Conditionals", "text": "He acts as if he ___ everything.", "options": ["knows", "knew", "had known", "will know"], "answer": "B"},
    {"id": 325, "topic": "B2: Conditionals", "text": "If I ___ earlier, I would have caught the train.", "options": ["leave", "left", "had left", "would leave"], "answer": "C"},
    {"id": 326, "topic": "B2: Conditionals", "text": "She wishes she ___ to the party last night.", "options": ["goes", "went", "had gone", "would go"], "answer": "C"},
    {"id": 327, "topic": "B2: Conditionals", "text": "Assuming you ___ the job, when could you start?", "options": ["get", "got", "had got", "will get"], "answer": "B"},
    {"id": 328, "topic": "B2: Conditionals", "text": "If need be, I ___ work overtime.", "options": ["will", "would", "had", "should"], "answer": "A"},
    {"id": 329, "topic": "B2: Conditionals", "text": "Had she been more careful, the accident ___.", "options": ["won't happen", "wouldn't happen", "wouldn't have happened", "didn't happen"], "answer": "C"},
    {"id": 330, "topic": "B2: Conditionals", "text": "If you ___ to see him, give him my regards.", "options": ["happen", "happened", "had happened", "will happen"], "answer": "A"},
    {"id": 331, "topic": "B2: Conditionals", "text": "What if we ___ the deadline?", "options": ["miss", "missed", "had missed", "will miss"], "answer": "A"},
    {"id": 332, "topic": "B2: Conditionals", "text": "She speaks as though she ___ a native.", "options": ["is", "were", "has been", "will be"], "answer": "B"},
    {"id": 333, "topic": "B2: Conditionals", "text": "On condition that you ___, I'll lend you the money.", "options": ["pay back", "will pay back", "paid back", "paying back"], "answer": "A"},
    {"id": 334, "topic": "B2: Conditionals", "text": "If only the weather ___ better!", "options": ["is", "were", "had been", "will be"], "answer": "B"},
    {"id": 335, "topic": "B2: Conditionals", "text": "I wouldn't have agreed ___ I known the full story.", "options": ["if", "had", "unless", "whether"], "answer": "B"},
    {"id": 336, "topic": "B2: Modal Verbs", "text": "She ___ have left already — her car is gone.", "options": ["must", "can", "should", "would"], "answer": "A"},
    {"id": 337, "topic": "B2: Modal Verbs", "text": "You ___ have told me earlier!", "options": ["must", "should", "can", "would"], "answer": "B"},
    {"id": 338, "topic": "B2: Modal Verbs", "text": "He ___ be at home. I just saw him at the gym.", "options": ["can't", "mustn't", "shouldn't", "needn't"], "answer": "A"},
    {"id": 339, "topic": "B2: Modal Verbs", "text": "You ___ have seen a ghost — they don't exist!", "options": ["can't", "mustn't", "shouldn't", "needn't"], "answer": "A"},
    {"id": 340, "topic": "B2: Modal Verbs", "text": "She ___ have taken the wrong bus.", "options": ["might", "must to", "should to", "would to"], "answer": "A"},
    {"id": 341, "topic": "B2: Modal Verbs", "text": "You needn't ___ worried — everything was fine.", "options": ["have", "be", "to have", "having"], "answer": "A"},
    {"id": 342, "topic": "B2: Modal Verbs", "text": "He ___ to have been a great athlete in his youth.", "options": ["is said", "says", "is saying", "said"], "answer": "A"},
    {"id": 343, "topic": "B2: Modal Verbs", "text": "You ___ have parked here — it's a private area.", "options": ["shouldn't", "mustn't", "couldn't", "needn't"], "answer": "A"},
    {"id": 344, "topic": "B2: Modal Verbs", "text": "I ___ as well go home — there's nothing to do.", "options": ["may", "must", "should", "would"], "answer": "A"},
    {"id": 345, "topic": "B2: Modal Verbs", "text": "She ___ have arrived by now. The flight was at 10.", "options": ["should", "must to", "can to", "would"], "answer": "A"},
    {"id": 346, "topic": "B2: Modal Verbs", "text": "He couldn't ___ known about it — it was a secret.", "options": ["have", "be", "to have", "having"], "answer": "A"},
    {"id": 347, "topic": "B2: Modal Verbs", "text": "You ___ have called before coming.", "options": ["could", "must to", "would to", "should to"], "answer": "A"},
    {"id": 348, "topic": "B2: Modal Verbs", "text": "She ___ not have received my message.", "options": ["may", "must to", "can to", "would to"], "answer": "A"},
    {"id": 349, "topic": "B2: Modal Verbs", "text": "The fire ___ have been caused by an electrical fault.", "options": ["could", "must to", "should to", "would to"], "answer": "A"},
    {"id": 350, "topic": "B2: Modal Verbs", "text": "We ___ have booked earlier — all tickets are sold out.", "options": ["should", "must to", "can to", "would to"], "answer": "A"},
    {"id": 351, "topic": "B2: Modal Verbs", "text": "He ___ be very rich — he drives a Rolls-Royce.", "options": ["must", "should to", "can to", "would to"], "answer": "A"},
    {"id": 352, "topic": "B2: Modal Verbs", "text": "You ___ have lied to her. That was wrong.", "options": ["shouldn't", "mustn't to", "couldn't to", "needn't to"], "answer": "A"},
    {"id": 353, "topic": "B2: Modal Verbs", "text": "They ___ have got lost — they have a GPS.", "options": ["can't", "mustn't", "shouldn't", "won't"], "answer": "A"},
    {"id": 354, "topic": "B2: Modal Verbs", "text": "I ___ have sworn I locked the door.", "options": ["could", "must to", "would to", "should to"], "answer": "A"},
    {"id": 355, "topic": "B2: Modal Verbs", "text": "She ___ be working late — the office lights are on.", "options": ["must", "should to", "can to", "would to"], "answer": "A"},
    {"id": 356, "topic": "B2: Modal Verbs", "text": "You ___ apply for this job — you have the right skills.", "options": ["ought to", "must to", "can to", "would to"], "answer": "A"},
    {"id": 357, "topic": "B2: Modal Verbs", "text": "It ___ rain later — take an umbrella just in case.", "options": ["might", "must to", "should to", "would to"], "answer": "A"},
    {"id": 358, "topic": "B2: Modal Verbs", "text": "We ___ to have informed you sooner.", "options": ["ought", "must", "can", "would"], "answer": "A"},
    {"id": 359, "topic": "B2: Modal Verbs", "text": "He ___ have been more polite to the guests.", "options": ["could", "must to", "would to", "should to"], "answer": "A"},
    {"id": 360, "topic": "B2: Modal Verbs", "text": "She ___ well become the next CEO.", "options": ["may", "must to", "should to", "would to"], "answer": "A"},
    {"id": 361, "topic": "B2: Reported Speech", "text": "She said she ___ the film the day before.", "options": ["has seen", "saw", "had seen", "sees"], "answer": "C"},
    {"id": 362, "topic": "B2: Reported Speech", "text": "He told me he ___ help me the next day.", "options": ["will", "would", "can", "shall"], "answer": "B"},
    {"id": 363, "topic": "B2: Reported Speech", "text": "She asked if I ___ come to her party.", "options": ["can", "could", "will", "may"], "answer": "B"},
    {"id": 364, "topic": "B2: Reported Speech", "text": "He asked me where I ___.", "options": ["live", "lived", "am living", "do live"], "answer": "B"},
    {"id": 365, "topic": "B2: Reported Speech", "text": "She told me ___ late.", "options": ["don't be", "not to be", "not be", "to not be"], "answer": "B"},
    {"id": 366, "topic": "B2: Reported Speech", "text": "He wondered whether I ___ free that evening.", "options": ["am", "was", "will be", "is"], "answer": "B"},
    {"id": 367, "topic": "B2: Reported Speech", "text": "She denied ___ the money.", "options": ["to take", "taking", "take", "took"], "answer": "B"},
    {"id": 368, "topic": "B2: Reported Speech", "text": "He reminded me ___ the door.", "options": ["lock", "to lock", "locking", "locked"], "answer": "B"},
    {"id": 369, "topic": "B2: Reported Speech", "text": "She admitted ___ a mistake.", "options": ["to make", "making", "make", "made"], "answer": "B"},
    {"id": 370, "topic": "B2: Reported Speech", "text": "He promised he ___ be there on time.", "options": ["will", "would", "can", "may"], "answer": "B"},
    {"id": 371, "topic": "B2: Reported Speech", "text": "She suggested ___ to the cinema.", "options": ["go", "to go", "going", "went"], "answer": "C"},
    {"id": 372, "topic": "B2: Reported Speech", "text": "He warned me ___ the dog.", "options": ["not touch", "not to touch", "don't touch", "touching"], "answer": "B"},
    {"id": 373, "topic": "B2: Reported Speech", "text": "She complained that the food ___ cold.", "options": ["is", "was", "has been", "be"], "answer": "B"},
    {"id": 374, "topic": "B2: Reported Speech", "text": "He explained that he ___ stuck in traffic.", "options": ["is", "was", "has been", "had been"], "answer": "D"},
    {"id": 375, "topic": "B2: Reported Speech", "text": "She begged me ___ her secret.", "options": ["not tell", "not to tell", "don't tell", "telling"], "answer": "B"},
    {"id": 376, "topic": "B2: Reported Speech", "text": "He insisted ___ paying for dinner.", "options": ["on", "to", "for", "about"], "answer": "A"},
    {"id": 377, "topic": "B2: Reported Speech", "text": "She accused me ___ lying.", "options": ["for", "of", "about", "to"], "answer": "B"},
    {"id": 378, "topic": "B2: Reported Speech", "text": "He congratulated me ___ passing the exam.", "options": ["for", "on", "about", "to"], "answer": "B"},
    {"id": 379, "topic": "B2: Reported Speech", "text": "'I'll do it tomorrow,' he said. → He said he ___ do it ___.", "options": ["will/tomorrow", "would/the next day", "would/tomorrow", "will/the next day"], "answer": "B"},
    {"id": 380, "topic": "B2: Reported Speech", "text": "'I was working,' she said. → She said she ___.", "options": ["was working", "had been working", "is working", "has been working"], "answer": "B"},
    {"id": 381, "topic": "B2: Passive Voice", "text": "The suspect is believed ___ the country.", "options": ["to leave", "to have left", "leaving", "left"], "answer": "B"},
    {"id": 382, "topic": "B2: Passive Voice", "text": "She is said ___ very talented.", "options": ["to be", "being", "be", "been"], "answer": "A"},
    {"id": 383, "topic": "B2: Passive Voice", "text": "The building ___ demolished next month.", "options": ["is being", "is to be", "has to", "will being"], "answer": "B"},
    {"id": 384, "topic": "B2: Passive Voice", "text": "I don't like ___ told what to do.", "options": ["be", "being", "been", "to be"], "answer": "B"},
    {"id": 385, "topic": "B2: Passive Voice", "text": "The car needs ___.", "options": ["to repair", "repairing", "repaired", "repair"], "answer": "B"},
    {"id": 386, "topic": "B2: Passive Voice", "text": "She had her hair ___.", "options": ["cut", "cutting", "to cut", "cuts"], "answer": "A"},
    {"id": 387, "topic": "B2: Passive Voice", "text": "He got his wallet ___.", "options": ["steal", "stolen", "stealing", "to steal"], "answer": "B"},
    {"id": 388, "topic": "B2: Passive Voice", "text": "The report is expected ___ ready by Friday.", "options": ["to be", "being", "be", "been"], "answer": "A"},
    {"id": 389, "topic": "B2: Passive Voice", "text": "The project ___ completed ahead of schedule.", "options": ["has been", "has being", "has be", "have been"], "answer": "A"},
    {"id": 390, "topic": "B2: Passive Voice", "text": "It ___ that the company will merge.", "options": ["is rumoured", "rumoured", "is rumouring", "rumours"], "answer": "A"},
    {"id": 391, "topic": "B2: Passive Voice", "text": "The package should ___ delivered by now.", "options": ["have been", "be", "being", "have being"], "answer": "A"},
    {"id": 392, "topic": "B2: Passive Voice", "text": "I had my computer ___ last week.", "options": ["fix", "fixed", "fixing", "to fix"], "answer": "B"},
    {"id": 393, "topic": "B2: Passive Voice", "text": "The bridge ___ being repaired when we drove past.", "options": ["is", "was", "has", "had"], "answer": "B"},
    {"id": 394, "topic": "B2: Passive Voice", "text": "She is thought ___ the best candidate.", "options": ["to be", "being", "be", "been"], "answer": "A"},
    {"id": 395, "topic": "B2: Passive Voice", "text": "The issue ___ dealt with immediately.", "options": ["must be", "must being", "must to be", "must been"], "answer": "A"},
    {"id": 396, "topic": "B2: Inversion", "text": "Never ___ I seen such a beautiful sunset.", "options": ["had", "have", "did", "was"], "answer": "B"},
    {"id": 397, "topic": "B2: Inversion", "text": "Not only ___ she smart, but she is also kind.", "options": ["is", "was", "does", "did"], "answer": "A"},
    {"id": 398, "topic": "B2: Inversion", "text": "Rarely ___ he make mistakes.", "options": ["do", "does", "is", "has"], "answer": "B"},
    {"id": 399, "topic": "B2: Inversion", "text": "Hardly ___ I sat down when the phone rang.", "options": ["have", "had", "did", "do"], "answer": "B"},
    {"id": 400, "topic": "B2: Inversion", "text": "No sooner ___ we arrived than it started raining.", "options": ["have", "had", "did", "do"], "answer": "B"},
    {"id": 401, "topic": "B2: Inversion", "text": "Little ___ she know what was about to happen.", "options": ["do", "did", "has", "was"], "answer": "B"},
    {"id": 402, "topic": "B2: Inversion", "text": "Only after finishing ___ I realise my mistake.", "options": ["do", "did", "have", "was"], "answer": "B"},
    {"id": 403, "topic": "B2: Inversion", "text": "Under no circumstances ___ you tell anyone.", "options": ["must", "do", "can to", "should to"], "answer": "A"},
    {"id": 404, "topic": "B2: Inversion", "text": "Not until I got home ___ I notice the stain.", "options": ["do", "did", "have", "was"], "answer": "B"},
    {"id": 405, "topic": "B2: Inversion", "text": "It ___ my brother who broke the window.", "options": ["is", "was", "were", "has"], "answer": "B"},
    {"id": 406, "topic": "B2: Inversion", "text": "What I ___ is a good night's sleep.", "options": ["need", "needs", "needed", "needing"], "answer": "A"},
    {"id": 407, "topic": "B2: Inversion", "text": "It was in Paris ___ they first met.", "options": ["that", "which", "who", "where"], "answer": "A"},
    {"id": 408, "topic": "B2: Inversion", "text": "So tired ___ she that she fell asleep instantly.", "options": ["is", "was", "did", "had"], "answer": "B"},
    {"id": 409, "topic": "B2: Inversion", "text": "At no point ___ I agree to this.", "options": ["do", "did", "have", "was"], "answer": "B"},
    {"id": 410, "topic": "B2: Inversion", "text": "Seldom ___ we have such good weather.", "options": ["do", "does", "is", "has"], "answer": "A"},
    {"id": 411, "topic": "B2: Phrasal Verbs", "text": "I need to <b>look into</b> this matter. Means:", "options": ["ignore", "investigate", "create", "enjoy"], "answer": "B"},
    {"id": 412, "topic": "B2: Phrasal Verbs", "text": "She <b>came across</b> an old letter. Means:", "options": ["wrote", "found by chance", "destroyed", "sent"], "answer": "B"},
    {"id": 413, "topic": "B2: Phrasal Verbs", "text": "He <b>turned out</b> to be a fraud. Means:", "options": ["appeared", "proved", "decided", "wanted"], "answer": "B"},
    {"id": 414, "topic": "B2: Phrasal Verbs", "text": "We need to <b>cut down on</b> expenses. Means:", "options": ["increase", "reduce", "enjoy", "calculate"], "answer": "B"},
    {"id": 415, "topic": "B2: Phrasal Verbs", "text": "The meeting was <b>called off</b>. Means:", "options": ["postponed", "cancelled", "started", "extended"], "answer": "B"},
    {"id": 416, "topic": "B2: Phrasal Verbs", "text": "I can't <b>put up with</b> this noise. Means:", "options": ["enjoy", "tolerate", "create", "hear"], "answer": "B"},
    {"id": 417, "topic": "B2: Phrasal Verbs", "text": "She <b>brought up</b> an interesting point. Means:", "options": ["raised", "forgot", "dismissed", "copied"], "answer": "A"},
    {"id": 418, "topic": "B2: Phrasal Verbs", "text": "He <b>broke down</b> during the speech. Means:", "options": ["laughed", "collapsed emotionally", "succeeded", "improved"], "answer": "B"},
    {"id": 419, "topic": "B2: Phrasal Verbs", "text": "They <b>carried out</b> the experiment successfully. Means:", "options": ["cancelled", "performed", "planned", "delayed"], "answer": "B"},
    {"id": 420, "topic": "B2: Phrasal Verbs", "text": "She <b>stood up for</b> her rights. Means:", "options": ["abandoned", "defended", "ignored", "questioned"], "answer": "B"},
    {"id": 421, "topic": "B2: Phrasal Verbs", "text": "The problem <b>came up</b> during the meeting. Means:", "options": ["disappeared", "arose", "was solved", "was ignored"], "answer": "B"},
    {"id": 422, "topic": "B2: Phrasal Verbs", "text": "I need to <b>catch up with</b> my studies. Means:", "options": ["abandon", "reach the same level", "forget", "delay"], "answer": "B"},
    {"id": 423, "topic": "B2: Phrasal Verbs", "text": "He <b>let me down</b>. Means:", "options": ["helped me", "disappointed me", "surprised me", "called me"], "answer": "B"},
    {"id": 424, "topic": "B2: Phrasal Verbs", "text": "She <b>took after</b> her mother. Means:", "options": ["avoided", "resembled", "followed", "called"], "answer": "B"},
    {"id": 425, "topic": "B2: Phrasal Verbs", "text": "We need to <b>figure out</b> a solution. Means:", "options": ["forget", "solve/understand", "ignore", "delay"], "answer": "B"},
    {"id": 426, "topic": "B2: Phrasal Verbs", "text": "The company <b>went through</b> a difficult period. Means:", "options": ["avoided", "experienced", "created", "ended"], "answer": "B"},
    {"id": 427, "topic": "B2: Phrasal Verbs", "text": "I <b>came up with</b> a great idea. Means:", "options": ["rejected", "thought of", "forgot", "delayed"], "answer": "B"},
    {"id": 428, "topic": "B2: Phrasal Verbs", "text": "She <b>backed out</b> of the deal. Means:", "options": ["agreed", "withdrew", "improved", "started"], "answer": "B"},
    {"id": 429, "topic": "B2: Phrasal Verbs", "text": "He <b>held back</b> his tears. Means:", "options": ["released", "restrained", "enjoyed", "forgot"], "answer": "B"},
    {"id": 430, "topic": "B2: Phrasal Verbs", "text": "They <b>set up</b> a new business. Means:", "options": ["closed", "established", "delayed", "bought"], "answer": "B"},
    {"id": 431, "topic": "B2: Phrasal Verbs", "text": "The argument <b>blew over</b> quickly. Means:", "options": ["got worse", "calmed down", "started", "continued"], "answer": "B"},
    {"id": 432, "topic": "B2: Phrasal Verbs", "text": "She <b>ran out of</b> patience. Means:", "options": ["gained", "used all of", "found", "saved"], "answer": "B"},
    {"id": 433, "topic": "B2: Phrasal Verbs", "text": "He <b>got away with</b> cheating. Means:", "options": ["was punished", "escaped punishment", "was caught", "apologised"], "answer": "B"},
    {"id": 434, "topic": "B2: Phrasal Verbs", "text": "I <b>fell behind</b> with my rent. Means:", "options": ["paid early", "owed money", "saved", "reduced"], "answer": "B"},
    {"id": 435, "topic": "B2: Phrasal Verbs", "text": "She <b>turned down</b> the job offer. Means:", "options": ["accepted", "refused", "applied for", "considered"], "answer": "B"},
    {"id": 436, "topic": "B2: Word Formation", "text": "The opposite of 'agree' is:", "options": ["unagree", "disagree", "inagree", "misagree"], "answer": "B"},
    {"id": 437, "topic": "B2: Word Formation", "text": "The noun form of 'succeed' is:", "options": ["succession", "success", "successful", "succeeding"], "answer": "B"},
    {"id": 438, "topic": "B2: Word Formation", "text": "The adjective form of 'danger' is:", "options": ["dangering", "dangerful", "dangerous", "dangered"], "answer": "C"},
    {"id": 439, "topic": "B2: Word Formation", "text": "The noun form of 'weak' is:", "options": ["weakment", "weakness", "weakful", "weaking"], "answer": "B"},
    {"id": 440, "topic": "B2: Word Formation", "text": "The opposite of 'patient' is:", "options": ["unpatient", "impatient", "dispatient", "inpatient"], "answer": "B"},
    {"id": 441, "topic": "B2: Word Formation", "text": "The noun form of 'know' is:", "options": ["knowment", "knowledge", "knowful", "knowing"], "answer": "B"},
    {"id": 442, "topic": "B2: Word Formation", "text": "The adjective form of 'rely' is:", "options": ["reliant", "reliable", "relying", "relianced"], "answer": "B"},
    {"id": 443, "topic": "B2: Word Formation", "text": "The noun form of 'create' is:", "options": ["creation", "creative", "creating", "creatment"], "answer": "A"},
    {"id": 444, "topic": "B2: Word Formation", "text": "The opposite of 'legal' is:", "options": ["unlegal", "illegal", "inlegal", "dislegal"], "answer": "B"},
    {"id": 445, "topic": "B2: Word Formation", "text": "The noun form of 'happy' is:", "options": ["happiment", "happiness", "happiful", "happying"], "answer": "B"},
    {"id": 446, "topic": "B2: Word Formation", "text": "The adjective form of 'comfort' is:", "options": ["comforting", "comfortable", "comforted", "comfortness"], "answer": "B"},
    {"id": 447, "topic": "B2: Word Formation", "text": "The verb form of 'strength' is:", "options": ["strengthy", "strengthen", "strongen", "strengting"], "answer": "B"},
    {"id": 448, "topic": "B2: Word Formation", "text": "The noun form of 'develop' is:", "options": ["developness", "development", "develope", "developing"], "answer": "B"},
    {"id": 449, "topic": "B2: Word Formation", "text": "The opposite of 'responsible' is:", "options": ["unresponsible", "irresponsible", "disresponsible", "inresponsible"], "answer": "B"},
    {"id": 450, "topic": "B2: Word Formation", "text": "The noun form of 'free' is:", "options": ["freement", "freedom", "freeness", "freeful"], "answer": "B"},
    {"id": 451, "topic": "B2: Word Formation", "text": "The adverb form of 'careful' is:", "options": ["carefulment", "carefully", "carefulling", "carefuls"], "answer": "B"},
    {"id": 452, "topic": "B2: Word Formation", "text": "The noun form of 'imagine' is:", "options": ["imaginement", "imagination", "imaginal", "imaging"], "answer": "B"},
    {"id": 453, "topic": "B2: Word Formation", "text": "The adjective form of 'economy' is:", "options": ["economied", "economic", "economying", "economing"], "answer": "B"},
    {"id": 454, "topic": "B2: Word Formation", "text": "The opposite of 'polite' is:", "options": ["unpolite", "impolite", "dispolite", "inpolite"], "answer": "B"},
    {"id": 455, "topic": "B2: Word Formation", "text": "The noun form of 'solve' is:", "options": ["solving", "solution", "solvement", "solvation"], "answer": "B"},
    {"id": 456, "topic": "B2: Collocations", "text": "She ___ a deep breath before the speech.", "options": ["did", "made", "took", "had"], "answer": "C"},
    {"id": 457, "topic": "B2: Collocations", "text": "We need to ___ an effort to finish on time.", "options": ["do", "make", "take", "have"], "answer": "B"},
    {"id": 458, "topic": "B2: Collocations", "text": "Can you ___ me a favour?", "options": ["make", "give", "do", "take"], "answer": "C"},
    {"id": 459, "topic": "B2: Collocations", "text": "He ___ a terrible mistake.", "options": ["did", "made", "took", "had"], "answer": "B"},
    {"id": 460, "topic": "B2: Collocations", "text": "Let me ___ a suggestion.", "options": ["do", "make", "take", "have"], "answer": "B"},
    {"id": 461, "topic": "B2: Collocations", "text": "She ___ a complaint about the service.", "options": ["did", "made", "took", "had"], "answer": "B"},
    {"id": 462, "topic": "B2: Collocations", "text": "I need to ___ a phone call.", "options": ["do", "make", "take", "have"], "answer": "B"},
    {"id": 463, "topic": "B2: Collocations", "text": "He ___ the responsibility for the error.", "options": ["did", "made", "took", "had"], "answer": "C"},
    {"id": 464, "topic": "B2: Collocations", "text": "She ___ her best to help us.", "options": ["made", "did", "took", "had"], "answer": "B"},
    {"id": 465, "topic": "B2: Collocations", "text": "The news ___ very disappointing.", "options": ["was", "were", "are", "have been"], "answer": "A"},
    {"id": 466, "topic": "B2: Collocations", "text": "I need some ___ about the course.", "options": ["informations", "information", "an information", "the informations"], "answer": "B"},
    {"id": 467, "topic": "B2: Collocations", "text": "She gave me good ___.", "options": ["advise", "advice", "advices", "advises"], "answer": "B"},
    {"id": 468, "topic": "B2: Collocations", "text": "There are ___ people in the park today.", "options": ["few", "a few", "little", "a little"], "answer": "B"},
    {"id": 469, "topic": "B2: Collocations", "text": "I have very ___ money left.", "options": ["few", "a few", "little", "a little"], "answer": "C"},
    {"id": 470, "topic": "B2: Collocations", "text": "She has ___ experience in marketing.", "options": ["many", "much", "a lot", "lots"], "answer": "B"},
    {"id": 471, "topic": "B2: Collocations", "text": "There were ___ cars on the road.", "options": ["much", "many", "a lot", "plenty"], "answer": "B"},
    {"id": 472, "topic": "B2: Collocations", "text": "He speaks English very ___.", "options": ["good", "well", "nice", "fine"], "answer": "B"},
    {"id": 473, "topic": "B2: Collocations", "text": "I ___ with you completely.", "options": ["agree", "accept", "admit", "allow"], "answer": "A"},
    {"id": 474, "topic": "B2: Collocations", "text": "She ___ me to the party.", "options": ["invited", "suggested", "proposed", "offered"], "answer": "A"},
    {"id": 475, "topic": "B2: Collocations", "text": "He ___ to fix the computer.", "options": ["managed", "succeeded", "achieved", "completed"], "answer": "A"},
    {"id": 476, "topic": "B2: Collocations", "text": "I ___ seeing that film.", "options": ["remember", "remind", "recall", "recollect"], "answer": "A"},
    {"id": 477, "topic": "B2: Collocations", "text": "She ___ for making a lot of noise.", "options": ["excused", "apologised", "pardoned", "forgave"], "answer": "B"},
    {"id": 478, "topic": "B2: Collocations", "text": "He ___ me to be more careful.", "options": ["said", "told", "spoke", "talked"], "answer": "B"},
    {"id": 479, "topic": "B2: Collocations", "text": "I ___ forward to hearing from you.", "options": ["look", "am looking", "see", "am seeing"], "answer": "B"},
    {"id": 480, "topic": "B2: Collocations", "text": "She ___ in love with him instantly.", "options": ["fell", "dropped", "went", "came"], "answer": "A"},
    {"id": 481, "topic": "B2: Linking Words", "text": "___ the rain, we enjoyed the picnic.", "options": ["Despite", "Although", "Because", "However"], "answer": "A"},
    {"id": 482, "topic": "B2: Linking Words", "text": "He failed the exam ___ he studied hard.", "options": ["despite", "although", "because", "however"], "answer": "B"},
    {"id": 483, "topic": "B2: Linking Words", "text": "She's talented. ___, she's also hardworking.", "options": ["Moreover", "However", "Although", "Despite"], "answer": "A"},
    {"id": 484, "topic": "B2: Linking Words", "text": "I was exhausted. ___, I finished the project.", "options": ["Moreover", "Therefore", "Nevertheless", "Because"], "answer": "C"},
    {"id": 485, "topic": "B2: Linking Words", "text": "___ having a headache, she went to work.", "options": ["Although", "Despite", "However", "Because"], "answer": "B"},
    {"id": 486, "topic": "B2: Linking Words", "text": "He lost his job. ___, he remained optimistic.", "options": ["Moreover", "Therefore", "Nonetheless", "Because"], "answer": "C"},
    {"id": 487, "topic": "B2: Linking Words", "text": "The hotel was expensive. ___, the service was poor.", "options": ["Furthermore", "However", "Therefore", "Moreover"], "answer": "A"},
    {"id": 488, "topic": "B2: Linking Words", "text": "___ to the bad weather, the flight was delayed.", "options": ["Due", "Despite", "Although", "However"], "answer": "A"},
    {"id": 489, "topic": "B2: Linking Words", "text": "Not only was she late, ___ she forgot the documents.", "options": ["and", "but", "so", "or"], "answer": "B"},
    {"id": 490, "topic": "B2: Linking Words", "text": "I'll help you ___ you promise to try harder.", "options": ["unless", "provided that", "despite", "although"], "answer": "B"},
    {"id": 491, "topic": "B2: Linking Words", "text": "He works hard. ___, his results are still poor.", "options": ["Consequently", "Nevertheless", "Therefore", "Moreover"], "answer": "B"},
    {"id": 492, "topic": "B2: Linking Words", "text": "She left early ___ to avoid the traffic.", "options": ["so as", "in order", "because", "due"], "answer": "B"},
    {"id": 493, "topic": "B2: Linking Words", "text": "___ the fact that he was ill, he came to work.", "options": ["Although", "Despite", "However", "Because"], "answer": "B"},
    {"id": 494, "topic": "B2: Linking Words", "text": "He's rich; ___, he's not happy.", "options": ["however", "moreover", "therefore", "furthermore"], "answer": "A"},
    {"id": 495, "topic": "B2: Linking Words", "text": "She passed the exam ___ her hard work.", "options": ["thanks to", "despite", "although", "however"], "answer": "A"},
    {"id": 496, "topic": "B2: Linking Words", "text": "I stayed home, ___ I wasn't feeling well.", "options": ["as", "despite", "however", "although"], "answer": "A"},
    {"id": 497, "topic": "B2: Linking Words", "text": "___ arriving early, she missed the bus.", "options": ["Despite", "Although", "However", "Since"], "answer": "A"},
    {"id": 498, "topic": "B2: Linking Words", "text": "The food was delicious. ___, the portions were generous.", "options": ["However", "Moreover", "Nevertheless", "Despite"], "answer": "B"},
    {"id": 499, "topic": "B2: Linking Words", "text": "I won't go ___ you come with me.", "options": ["if", "unless", "although", "despite"], "answer": "B"},
    {"id": 500, "topic": "B2: Linking Words", "text": "He succeeded ___ having no support.", "options": ["despite", "although", "however", "because"], "answer": "A"},
    {"id": 501, "topic": "B2: Used to", "text": "I ___ live in London when I was a child.", "options": ["used to", "would", "use to", "was used to"], "answer": "A"},
    {"id": 502, "topic": "B2: Used to", "text": "She ___ play tennis every weekend. (repeated action in past)", "options": ["used to", "would", "use to", "was used to"], "answer": "B"},
    {"id": 503, "topic": "B2: Used to", "text": "I'm getting ___ to the cold weather.", "options": ["use", "used", "using", "uses"], "answer": "B"},
    {"id": 504, "topic": "B2: Used to", "text": "He didn't ___ like vegetables.", "options": ["used to", "use to", "would", "get used to"], "answer": "B"},
    {"id": 505, "topic": "B2: Used to", "text": "She ___ to living alone now.", "options": ["used", "is used", "was used", "use"], "answer": "B"},
    {"id": 506, "topic": "B2: Used to", "text": "It took me a while to ___ to the new job.", "options": ["used", "get used", "be used", "use"], "answer": "B"},
    {"id": 507, "topic": "B2: Used to", "text": "We ___ go camping every summer when I was a child.", "options": ["would", "used", "were used to", "are used to"], "answer": "A"},
    {"id": 508, "topic": "B2: Used to", "text": "I can't ___ to this noise.", "options": ["used", "get used", "be use", "use"], "answer": "B"},
    {"id": 509, "topic": "B2: Used to", "text": "She ___ to be very shy, but now she's confident.", "options": ["use", "used", "would", "is used"], "answer": "B"},
    {"id": 510, "topic": "B2: Used to", "text": "He hasn't ___ to working nights yet.", "options": ["get used", "got used", "getting used", "gets used"], "answer": "B"},
    {"id": 511, "topic": "B2: Vocabulary", "text": "'Ambiguous' means:", "options": ["clear", "unclear/having two meanings", "simple", "serious"], "answer": "B"},
    {"id": 512, "topic": "B2: Vocabulary", "text": "'Pragmatic' means:", "options": ["theoretical", "practical and realistic", "artistic", "emotional"], "answer": "B"},
    {"id": 513, "topic": "B2: Vocabulary", "text": "'Deteriorate' means to:", "options": ["improve", "get worse", "stay the same", "get faster"], "answer": "B"},
    {"id": 514, "topic": "B2: Vocabulary", "text": "'Empathy' is the ability to:", "options": ["command", "understand others' feelings", "forget", "lie"], "answer": "B"},
    {"id": 515, "topic": "B2: Vocabulary", "text": "'Inevitable' means:", "options": ["avoidable", "certain to happen", "unlikely", "unknown"], "answer": "B"},
    {"id": 516, "topic": "B2: Vocabulary", "text": "'Undermine' means to:", "options": ["support", "weaken gradually", "build", "praise"], "answer": "B"},
    {"id": 517, "topic": "B2: Vocabulary", "text": "'Reluctant' means:", "options": ["eager", "unwilling", "happy", "confused"], "answer": "B"},
    {"id": 518, "topic": "B2: Vocabulary", "text": "A 'setback' is:", "options": ["progress", "a problem causing delay", "a victory", "a reward"], "answer": "B"},
    {"id": 519, "topic": "B2: Vocabulary", "text": "'Comprehensive' means:", "options": ["limited", "thorough and complete", "simple", "short"], "answer": "B"},
    {"id": 520, "topic": "B2: Vocabulary", "text": "'To acknowledge' means to:", "options": ["deny", "accept or recognise", "forget", "hide"], "answer": "B"},
    {"id": 521, "topic": "B2: Vocabulary", "text": "'Controversy' is:", "options": ["agreement", "disagreement/debate", "solution", "celebration"], "answer": "B"},
    {"id": 522, "topic": "B2: Vocabulary", "text": "'Profound' means:", "options": ["shallow", "very deep or intense", "simple", "short"], "answer": "B"},
    {"id": 523, "topic": "B2: Vocabulary", "text": "'To enhance' means to:", "options": ["reduce", "improve/increase", "destroy", "delay"], "answer": "B"},
    {"id": 524, "topic": "B2: Vocabulary", "text": "'Bias' means:", "options": ["fairness", "prejudice/favouritism", "honesty", "clarity"], "answer": "B"},
    {"id": 525, "topic": "B2: Vocabulary", "text": "'To coincide' means to:", "options": ["differ", "happen at the same time", "end", "begin"], "answer": "B"},
    {"id": 526, "topic": "B2: Vocabulary", "text": "'Crucial' means:", "options": ["unimportant", "extremely important", "simple", "boring"], "answer": "B"},
    {"id": 527, "topic": "B2: Vocabulary", "text": "'Obstacle' means:", "options": ["help", "something that blocks progress", "reward", "solution"], "answer": "B"},
    {"id": 528, "topic": "B2: Vocabulary", "text": "'To flourish' means to:", "options": ["fail", "grow and succeed", "stop", "shrink"], "answer": "B"},
    {"id": 529, "topic": "B2: Vocabulary", "text": "'Subtle' means:", "options": ["obvious", "not immediately noticeable", "loud", "bright"], "answer": "B"},
    {"id": 530, "topic": "B2: Vocabulary", "text": "'To allocate' means to:", "options": ["waste", "distribute for a purpose", "lose", "hide"], "answer": "B"},
    {"id": 531, "topic": "B2: Vocabulary", "text": "'Diverse' means:", "options": ["similar", "showing variety", "small", "boring"], "answer": "B"},
    {"id": 532, "topic": "B2: Vocabulary", "text": "'Constraint' means:", "options": ["freedom", "limitation", "opportunity", "reward"], "answer": "B"},
    {"id": 533, "topic": "B2: Vocabulary", "text": "'To implement' means to:", "options": ["plan", "put into action", "delay", "cancel"], "answer": "B"},
    {"id": 534, "topic": "B2: Vocabulary", "text": "'Resilient' means:", "options": ["fragile", "able to recover quickly", "slow", "weak"], "answer": "B"},
    {"id": 535, "topic": "B2: Vocabulary", "text": "'Spontaneous' means:", "options": ["planned", "unplanned and natural", "forced", "boring"], "answer": "B"},
    {"id": 536, "topic": "B2: Grammar", "text": "I'd rather you ___ smoking.", "options": ["stop", "stopped", "will stop", "stopping"], "answer": "B"},
    {"id": 537, "topic": "B2: Grammar", "text": "It's high time you ___ a job.", "options": ["get", "got", "will get", "getting"], "answer": "B"},
    {"id": 538, "topic": "B2: Grammar", "text": "She insisted ___ paying for the meal.", "options": ["on", "to", "for", "about"], "answer": "A"},
    {"id": 539, "topic": "B2: Grammar", "text": "He's not used to ___ early.", "options": ["get up", "getting up", "gets up", "got up"], "answer": "B"},
    {"id": 540, "topic": "B2: Grammar", "text": "The sooner we leave, the ___ we'll arrive.", "options": ["sooner", "soonest", "soon", "more soon"], "answer": "A"},
    {"id": 541, "topic": "B2: Grammar", "text": "Not until I read the book ___ I understand the film.", "options": ["do", "did", "have", "was"], "answer": "B"},
    {"id": 542, "topic": "B2: Grammar", "text": "By no means ___ this acceptable.", "options": ["is", "was", "does", "has"], "answer": "A"},
    {"id": 543, "topic": "B2: Grammar", "text": "She had her car ___ last week.", "options": ["service", "serviced", "servicing", "to service"], "answer": "B"},
    {"id": 544, "topic": "B2: Grammar", "text": "I regret ___ you that you've been rejected.", "options": ["inform", "to inform", "informing", "informed"], "answer": "B"},
    {"id": 545, "topic": "B2: Grammar", "text": "He stopped ___ because he was out of breath.", "options": ["run", "to run", "running", "ran"], "answer": "C"},
    {"id": 546, "topic": "B2: Grammar", "text": "I remember ___ the door. (= I did lock it and I remember that)", "options": ["lock", "to lock", "locking", "locked"], "answer": "C"},
    {"id": 547, "topic": "B2: Grammar", "text": "I remembered ___ the door. (= I didn't forget to do it)", "options": ["lock", "to lock", "locking", "locked"], "answer": "B"},
    {"id": 548, "topic": "B2: Grammar", "text": "She's ___ intelligent woman I've ever met.", "options": ["most", "the most", "more", "the more"], "answer": "B"},
    {"id": 549, "topic": "B2: Grammar", "text": "Scarcely ___ he arrived when the meeting began.", "options": ["has", "had", "did", "does"], "answer": "B"},
    {"id": 550, "topic": "B2: Grammar", "text": "He's the man ___ I was telling you about.", "options": ["who", "whom", "which", "whose"], "answer": "B"},
    {"id": 551, "topic": "B2: Grammar", "text": "This is the house ___ roof was damaged.", "options": ["who", "which", "whose", "whom"], "answer": "C"},
    {"id": 552, "topic": "B2: Grammar", "text": "It's no use ___ over spilt milk.", "options": ["cry", "to cry", "crying", "cried"], "answer": "C"},
    {"id": 553, "topic": "B2: Grammar", "text": "I look forward to ___ from you.", "options": ["hear", "hearing", "heard", "hears"], "answer": "B"},
    {"id": 554, "topic": "B2: Grammar", "text": "There's no point ___ about it.", "options": ["worry", "to worry", "worrying", "worried"], "answer": "C"},
    {"id": 555, "topic": "B2: Grammar", "text": "He can't help ___ when he's nervous.", "options": ["laugh", "to laugh", "laughing", "laughed"], "answer": "C"},
    {"id": 556, "topic": "B1: Present Perfect Cont.", "text": "I ___ (wait) for you for an hour!", "options": ["have been waiting", "have waited", "am waiting", "was waiting"], "answer": "A"},
    {"id": 558, "topic": "B1: Present Perfect Cont.", "text": "She ___ (study) all morning.", "options": ["has been studying", "has studied", "is studying", "was studying"], "answer": "A"},
    {"id": 560, "topic": "B1: Present Perfect Cont.", "text": "How long ___ you been learning English?", "options": ["have", "has", "are", "were"], "answer": "A"},
    {"id": 562, "topic": "B1: Present Perfect Cont.", "text": "It ___ (rain) since yesterday.", "options": ["has been raining", "has rained", "is raining", "was raining"], "answer": "A"},
    {"id": 564, "topic": "B1: Present Perfect Cont.", "text": "They ___ (play) tennis for two hours.", "options": ["have been playing", "have played", "are playing", "were playing"], "answer": "A"},
    {"id": 566, "topic": "B1: Present Perfect Cont.", "text": "He ___ (work) here since 2020.", "options": ["has been working", "has worked", "is working", "was working"], "answer": "A"},
    {"id": 568, "topic": "B1: Present Perfect Cont.", "text": "We ___ (travel) all day. We're exhausted.", "options": ["have been travelling", "have travelled", "are travelling", "were travelling"], "answer": "A"},
    {"id": 570, "topic": "B1: Present Perfect Cont.", "text": "She ___ (cook) for hours. The kitchen smells great.", "options": ["has been cooking", "has cooked", "is cooking", "was cooking"], "answer": "A"},
    {"id": 572, "topic": "B1: Present Perfect Cont.", "text": "You look tired. ___ you been running?", "options": ["Have", "Has", "Are", "Were"], "answer": "A"},
    {"id": 574, "topic": "B1: Present Perfect Cont.", "text": "I ___ (read) this book for a week. It's very long.", "options": ["have been reading", "have read", "am reading", "was reading"], "answer": "A"},
    {"id": 576, "topic": "B1: Present Perfect Cont.", "text": "He ___ (try) to call you all day.", "options": ["has been trying", "has tried", "is trying", "was trying"], "answer": "A"},
    {"id": 578, "topic": "B1: Present Perfect Cont.", "text": "She ___ (teach) for twenty years.", "options": ["has been teaching", "has taught", "is teaching", "was teaching"], "answer": "A"},
    {"id": 580, "topic": "B1: Present Perfect Cont.", "text": "They ___ (build) this house for months.", "options": ["have been building", "have built", "are building", "were building"], "answer": "A"},
    {"id": 582, "topic": "B1: Present Perfect Cont.", "text": "I ___ (think) about changing my job.", "options": ["have been thinking", "have thought", "am thinking", "was thinking"], "answer": "A"},
    {"id": 584, "topic": "B1: Present Perfect Cont.", "text": "Why are your eyes red? ___ you been crying?", "options": ["Have", "Has", "Are", "Were"], "answer": "A"},
    {"id": 586, "topic": "B1: Present Perfect Cont.", "text": "We ___ (live) here since March.", "options": ["have been living", "have lived", "are living", "were living"], "answer": "A"},
    {"id": 588, "topic": "B1: Present Perfect Cont.", "text": "She ___ (learn) to drive for six months.", "options": ["has been learning", "has learnt", "is learning", "was learning"], "answer": "A"},
    {"id": 590, "topic": "B1: Present Perfect Cont.", "text": "He ___ (not/feel) well lately.", "options": ["hasn't been feeling", "hasn't felt", "isn't feeling", "wasn't feeling"], "answer": "A"},
    {"id": 592, "topic": "B1: Present Perfect Cont.", "text": "How long ___ it been snowing?", "options": ["has", "have", "is", "was"], "answer": "A"},
    {"id": 594, "topic": "B1: Present Perfect Cont.", "text": "I ___ (practise) the piano every day this week.", "options": ["have been practising", "have practised", "am practising", "was practising"], "answer": "A"},
    {"id": 596, "topic": "B1: Question Tags", "text": "She's coming to the party, ___?", "options": ["isn't she", "is she", "doesn't she", "does she"], "answer": "A"},
    {"id": 598, "topic": "B1: Question Tags", "text": "You haven't seen my keys, ___?", "options": ["have you", "haven't you", "did you", "do you"], "answer": "A"},
    {"id": 600, "topic": "B1: Question Tags", "text": "He can swim, ___?", "options": ["can't he", "can he", "doesn't he", "does he"], "answer": "A"},
    {"id": 602, "topic": "B1: Question Tags", "text": "They won't be late, ___?", "options": ["will they", "won't they", "are they", "do they"], "answer": "A"},
    {"id": 604, "topic": "B1: Question Tags", "text": "Let's go out, ___?", "options": ["shall we", "will we", "do we", "can we"], "answer": "A"},
    {"id": 606, "topic": "B1: Question Tags", "text": "You're a student, ___?", "options": ["aren't you", "are you", "don't you", "do you"], "answer": "A"},
    {"id": 608, "topic": "B1: Question Tags", "text": "She doesn't like coffee, ___?", "options": ["does she", "doesn't she", "is she", "isn't she"], "answer": "A"},
    {"id": 610, "topic": "B1: Question Tags", "text": "We should leave now, ___?", "options": ["shouldn't we", "should we", "don't we", "do we"], "answer": "A"},
    {"id": 612, "topic": "B1: Question Tags", "text": "He was late, ___?", "options": ["wasn't he", "was he", "didn't he", "did he"], "answer": "A"},
    {"id": 614, "topic": "B1: Question Tags", "text": "There are lots of people here, ___?", "options": ["aren't there", "are there", "isn't it", "is it"], "answer": "A"},
    {"id": 616, "topic": "B1: Question Tags", "text": "Nobody called, ___?", "options": ["did they", "didn't they", "do they", "don't they"], "answer": "A"},
    {"id": 618, "topic": "B1: Question Tags", "text": "I'm right, ___?", "options": ["aren't I", "am I", "don't I", "do I"], "answer": "A"},
    {"id": 620, "topic": "B1: Question Tags", "text": "You've been to Paris, ___?", "options": ["haven't you", "have you", "didn't you", "did you"], "answer": "A"},
    {"id": 622, "topic": "B1: Question Tags", "text": "She'd already left, ___?", "options": ["hadn't she", "had she", "wouldn't she", "didn't she"], "answer": "A"},
    {"id": 624, "topic": "B1: Question Tags", "text": "This is your bag, ___?", "options": ["isn't it", "is it", "doesn't it", "does it"], "answer": "A"},
    {"id": 626, "topic": "B1: Question Tags", "text": "He never goes to the gym, ___?", "options": ["does he", "doesn't he", "is he", "isn't he"], "answer": "A"},
    {"id": 628, "topic": "B1: Question Tags", "text": "They could hear us, ___?", "options": ["couldn't they", "could they", "didn't they", "can't they"], "answer": "A"},
    {"id": 630, "topic": "B1: Question Tags", "text": "You'll help me, ___?", "options": ["won't you", "will you", "don't you", "do you"], "answer": "A"},
    {"id": 632, "topic": "B1: Question Tags", "text": "We had a great time, ___?", "options": ["didn't we", "did we", "hadn't we", "weren't we"], "answer": "A"},
    {"id": 634, "topic": "B1: Question Tags", "text": "She hardly ever complains, ___?", "options": ["does she", "doesn't she", "is she", "has she"], "answer": "A"},
    {"id": 636, "topic": "B1: Reported Speech", "text": "'I like pizza,' he said. → He said he ___ pizza.", "options": ["likes", "liked", "has liked", "is liking"], "answer": "B"},
    {"id": 638, "topic": "B1: Reported Speech", "text": "'I am tired,' she said. → She said she ___ tired.", "options": ["is", "was", "has been", "will be"], "answer": "B"},
    {"id": 640, "topic": "B1: Reported Speech", "text": "'We will come,' they said. → They said they ___ come.", "options": ["will", "would", "can", "shall"], "answer": "B"},
    {"id": 642, "topic": "B1: Reported Speech", "text": "'I can help,' she said. → She said she ___ help.", "options": ["can", "could", "will", "may"], "answer": "B"},
    {"id": 644, "topic": "B1: Reported Speech", "text": "'I have finished,' he said. → He said he ___ finished.", "options": ["has", "had", "was", "is"], "answer": "B"},
    {"id": 646, "topic": "B1: Reported Speech", "text": "'Don't touch it!' she said. → She told me ___ touch it.", "options": ["don't", "not to", "to not", "not"], "answer": "B"},
    {"id": 648, "topic": "B1: Reported Speech", "text": "'Where do you live?' he asked. → He asked where I ___.", "options": ["live", "lived", "am living", "have lived"], "answer": "B"},
    {"id": 650, "topic": "B1: Reported Speech", "text": "'Are you coming?' she asked. → She asked ___ I was coming.", "options": ["that", "if", "what", "when"], "answer": "B"},
    {"id": 652, "topic": "B1: Reported Speech", "text": "'I saw her yesterday,' he said. → He said he ___ seen her the day before.", "options": ["has", "had", "was", "is"], "answer": "B"},
    {"id": 654, "topic": "B1: Reported Speech", "text": "'Open the door,' she said. → She told me ___ the door.", "options": ["open", "to open", "opening", "opened"], "answer": "B"},
    {"id": 656, "topic": "B1: Reported Speech", "text": "'I'm leaving tomorrow,' he said. → He said he was leaving ___.", "options": ["tomorrow", "the next day", "yesterday", "the day before"], "answer": "B"},
    {"id": 658, "topic": "B1: Reported Speech", "text": "'I went to London,' she said. → She said she ___ to London.", "options": ["went", "had gone", "has gone", "goes"], "answer": "B"},
    {"id": 660, "topic": "B1: Reported Speech", "text": "'We are having fun,' they said. → They said they ___ having fun.", "options": ["are", "were", "have been", "will be"], "answer": "B"},
    {"id": 662, "topic": "B1: Reported Speech", "text": "'I don't understand,' he said. → He said he ___ understand.", "options": ["doesn't", "didn't", "hasn't", "won't"], "answer": "B"},
    {"id": 664, "topic": "B1: Reported Speech", "text": "'What time is it?' she asked. → She asked what time it ___.", "options": ["is", "was", "has been", "will be"], "answer": "B"},
    {"id": 666, "topic": "B2: Mixed Tenses", "text": "I ___ (live) in three countries before I turned 30.", "options": ["lived", "have lived", "had lived", "was living"], "answer": "C"},
    {"id": 668, "topic": "B2: Mixed Tenses", "text": "She ___ (work) when I called, so she couldn't answer.", "options": ["worked", "was working", "has worked", "had worked"], "answer": "B"},
    {"id": 670, "topic": "B2: Mixed Tenses", "text": "By next year, we ___ (be) married for 25 years.", "options": ["will be", "will have been", "are", "have been"], "answer": "B"},
    {"id": 672, "topic": "B2: Mixed Tenses", "text": "I ___ (not see) him since the party.", "options": ["didn't see", "haven't seen", "hadn't seen", "wasn't seeing"], "answer": "B"},
    {"id": 674, "topic": "B2: Mixed Tenses", "text": "She ___ (teach) at this school for over a decade.", "options": ["teaches", "has been teaching", "is teaching", "taught"], "answer": "B"},
    {"id": 676, "topic": "B2: Mixed Tenses", "text": "He finally ___ (admit) that he was wrong.", "options": ["admits", "has admitted", "admitted", "had admitted"], "answer": "C"},
    {"id": 678, "topic": "B2: Mixed Tenses", "text": "They ___ (travel) to Japan three times so far.", "options": ["travelled", "have travelled", "had travelled", "were travelling"], "answer": "B"},
    {"id": 680, "topic": "B2: Mixed Tenses", "text": "I ___ (just/finish) lunch when she arrived.", "options": ["just finished", "have just finished", "had just finished", "was just finishing"], "answer": "C"},
    {"id": 682, "topic": "B2: Mixed Tenses", "text": "We ___ (wait) for two hours before the doctor saw us.", "options": ["waited", "have waited", "had been waiting", "were waiting"], "answer": "C"},
    {"id": 684, "topic": "B2: Mixed Tenses", "text": "This time next week, I ___ (relax) on the beach.", "options": ["relax", "will relax", "will be relaxing", "am relaxing"], "answer": "C"},
    {"id": 686, "topic": "B2: Mixed Tenses", "text": "She ___ (study) law at university at the moment.", "options": ["studies", "is studying", "has studied", "studied"], "answer": "B"},
    {"id": 688, "topic": "B2: Mixed Tenses", "text": "By the time he retires, he ___ (work) for 40 years.", "options": ["will work", "will be working", "will have worked", "works"], "answer": "C"},
    {"id": 690, "topic": "B2: Mixed Tenses", "text": "I ___ (know) her since we were children.", "options": ["know", "have known", "knew", "had known"], "answer": "B"},
    {"id": 692, "topic": "B2: Mixed Tenses", "text": "He ___ (break) his arm twice before he was ten.", "options": ["broke", "has broken", "had broken", "was breaking"], "answer": "C"},
    {"id": 694, "topic": "B2: Mixed Tenses", "text": "She always ___ (complain) about the food.", "options": ["complains", "is complaining", "has complained", "complained"], "answer": "B"},
    {"id": 696, "topic": "B2: Mixed Tenses", "text": "We ___ (move) to a new flat next month.", "options": ["move", "are moving", "will moving", "moved"], "answer": "B"},
    {"id": 698, "topic": "B2: Mixed Tenses", "text": "I ___ (read) 50 pages by the time I fell asleep.", "options": ["read", "have read", "had read", "was reading"], "answer": "C"},
    {"id": 700, "topic": "B2: Mixed Tenses", "text": "He ___ (not/eat) anything all day.", "options": ["doesn't eat", "hasn't eaten", "didn't eat", "hadn't eaten"], "answer": "B"},
    {"id": 702, "topic": "B2: Mixed Tenses", "text": "She ___ (learn) to drive at the moment.", "options": ["learns", "is learning", "has learnt", "learnt"], "answer": "B"},
    {"id": 704, "topic": "B2: Mixed Tenses", "text": "By midnight, they ___ (dance) for five hours.", "options": ["will dance", "will be dancing", "will have been dancing", "dance"], "answer": "C"},
    {"id": 706, "topic": "B2: Mixed Tenses", "text": "I ___ (think) about what you said yesterday.", "options": ["think", "have been thinking", "am thinking", "was thinking"], "answer": "B"},
    {"id": 708, "topic": "B2: Mixed Tenses", "text": "He ___ (work) here since he graduated.", "options": ["works", "has worked", "worked", "had worked"], "answer": "B"},
    {"id": 710, "topic": "B2: Mixed Tenses", "text": "When I arrived, everyone ___ (already/leave).", "options": ["already left", "has already left", "had already left", "already leaves"], "answer": "C"},
    {"id": 712, "topic": "B2: Mixed Tenses", "text": "She ___ (rarely/go) to the theatre.", "options": ["rarely goes", "is rarely going", "has rarely gone", "rarely went"], "answer": "A"},
    {"id": 714, "topic": "B2: Mixed Tenses", "text": "I ___ (never/taste) anything so delicious.", "options": ["never taste", "have never tasted", "never tasted", "had never tasted"], "answer": "B"},
    {"id": 716, "topic": "B2: Relative Clauses", "text": "The hotel, ___ we stayed last year, has closed.", "options": ["which", "where", "that", "whose"], "answer": "B"},
    {"id": 718, "topic": "B2: Relative Clauses", "text": "She's the woman ___ I told you about.", "options": ["who", "whom", "which", "whose"], "answer": "B"},
    {"id": 720, "topic": "B2: Relative Clauses", "text": "The house ___ roof was damaged has been repaired.", "options": ["who", "which", "whose", "that"], "answer": "C"},
    {"id": 722, "topic": "B2: Relative Clauses", "text": "That's the reason ___ he resigned.", "options": ["which", "where", "why", "when"], "answer": "C"},
    {"id": 724, "topic": "B2: Relative Clauses", "text": "My brother, ___ lives in Canada, is visiting us.", "options": ["who", "which", "that", "whose"], "answer": "A"},
    {"id": 726, "topic": "B2: Relative Clauses", "text": "The car ___ he bought turned out to be stolen.", "options": ["who", "which", "whose", "whom"], "answer": "B"},
    {"id": 728, "topic": "B2: Relative Clauses", "text": "The year ___ I graduated was 2020.", "options": ["which", "where", "when", "that"], "answer": "C"},
    {"id": 730, "topic": "B2: Relative Clauses", "text": "She married a man ___ family owned the company.", "options": ["who", "which", "whose", "whom"], "answer": "C"},
    {"id": 732, "topic": "B2: Relative Clauses", "text": "The city ___ she grew up is very small.", "options": ["which", "where", "that", "whose"], "answer": "B"},
    {"id": 734, "topic": "B2: Relative Clauses", "text": "The film, ___ was directed by Nolan, won an award.", "options": ["who", "which", "that", "whose"], "answer": "B"},
    {"id": 736, "topic": "B2: Relative Clauses", "text": "He's the person to ___ I sent the letter.", "options": ["who", "whom", "which", "whose"], "answer": "B"},
    {"id": 738, "topic": "B2: Relative Clauses", "text": "The day ___ we met changed my life.", "options": ["which", "where", "when", "whose"], "answer": "C"},
    {"id": 740, "topic": "B2: Relative Clauses", "text": "Everything ___ he said was true.", "options": ["who", "which", "that", "whose"], "answer": "C"},
    {"id": 742, "topic": "B2: Relative Clauses", "text": "The teacher ___ class I attend is excellent.", "options": ["who", "which", "whose", "whom"], "answer": "C"},
    {"id": 744, "topic": "B2: Relative Clauses", "text": "I visited Rome, ___ is a beautiful city.", "options": ["that", "which", "where", "whose"], "answer": "B"},
    {"id": 746, "topic": "B2: Relative Clauses", "text": "The woman ___ bag was stolen reported it to police.", "options": ["who", "which", "whose", "whom"], "answer": "C"},
    {"id": 748, "topic": "B2: Relative Clauses", "text": "He gave me a book, ___ I found very interesting.", "options": ["who", "which", "that", "whose"], "answer": "B"},
    {"id": 750, "topic": "B2: Relative Clauses", "text": "Is there anyone ___ can help me?", "options": ["whom", "which", "who", "whose"], "answer": "C"},
    {"id": 752, "topic": "B2: Relative Clauses", "text": "The place ___ we had lunch was by the river.", "options": ["which", "where", "that", "whose"], "answer": "B"},
    {"id": 754, "topic": "B2: Relative Clauses", "text": "Her latest novel, ___ I haven't read yet, is a bestseller.", "options": ["who", "which", "that", "whose"], "answer": "B"},
    {"id": 756, "topic": "B2: Articles", "text": "___ rich should help ___ poor.", "options": ["A/a", "The/the", "—/—", "A/the"], "answer": "B"},
    {"id": 758, "topic": "B2: Articles", "text": "He plays ___ violin in an orchestra.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 760, "topic": "B2: Articles", "text": "___ happiness is what everyone wants.", "options": ["A", "The", "An", "—"], "answer": "D"},
    {"id": 762, "topic": "B2: Articles", "text": "I read it in ___ Times.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 764, "topic": "B2: Articles", "text": "She's ___ only person who understands.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 766, "topic": "B2: Articles", "text": "___ Alps are beautiful in winter.", "options": ["A", "An", "The", "—"], "answer": "C"},
    {"id": 768, "topic": "B2: Articles", "text": "He was elected ___ president last year.", "options": ["a", "an", "the", "—"], "answer": "D"},
    {"id": 770, "topic": "B2: Articles", "text": "What ___ lovely day!", "options": ["a", "an", "the", "—"], "answer": "A"},
    {"id": 772, "topic": "B2: Articles", "text": "___ Mount Everest is the highest peak.", "options": ["A", "The", "An", "—"], "answer": "D"},
    {"id": 774, "topic": "B2: Articles", "text": "She goes to ___ church every Sunday.", "options": ["a", "an", "the", "—"], "answer": "D"},
    {"id": 776, "topic": "B2: Articles", "text": "He's in ___ hospital after the accident.", "options": ["a", "an", "the", "—"], "answer": "D"},
    {"id": 778, "topic": "B2: Articles", "text": "I had ___ lunch with ___ CEO.", "options": ["—/the", "a/a", "the/the", "a/the"], "answer": "A"},
    {"id": 780, "topic": "B2: Articles", "text": "___ United States is a large country.", "options": ["A", "An", "The", "—"], "answer": "C"},
    {"id": 782, "topic": "B2: Articles", "text": "She became ___ first woman to win the prize.", "options": ["a", "an", "the", "—"], "answer": "C"},
    {"id": 784, "topic": "B2: Articles", "text": "He went to ___ bed early.", "options": ["a", "an", "the", "—"], "answer": "D"},
    {"id": 786, "topic": "B2: Formal Grammar", "text": "It is essential that he ___ on time.", "options": ["is", "be", "was", "will be"], "answer": "B"},
    {"id": 788, "topic": "B2: Formal Grammar", "text": "I suggest that she ___ a lawyer.", "options": ["consults", "consult", "consulting", "consulted"], "answer": "B"},
    {"id": 790, "topic": "B2: Formal Grammar", "text": "The doctor recommended that he ___ more exercise.", "options": ["takes", "take", "took", "taking"], "answer": "B"},
    {"id": 792, "topic": "B2: Formal Grammar", "text": "It is vital that the report ___ finished today.", "options": ["is", "be", "was", "will be"], "answer": "B"},
    {"id": 794, "topic": "B2: Formal Grammar", "text": "I demand that he ___ immediately.", "options": ["leaves", "leave", "left", "leaving"], "answer": "B"},
    {"id": 796, "topic": "B2: Formal Grammar", "text": "She requested that the meeting ___ postponed.", "options": ["is", "be", "was", "will be"], "answer": "B"},
    {"id": 798, "topic": "B2: Formal Grammar", "text": "It is important that everyone ___ the rules.", "options": ["follows", "follow", "followed", "following"], "answer": "B"},
    {"id": 800, "topic": "B2: Formal Grammar", "text": "He proposed that the company ___ its strategy.", "options": ["changes", "change", "changed", "changing"], "answer": "B"},
    {"id": 802, "topic": "B2: Formal Grammar", "text": "The teacher insisted that the student ___ the test again.", "options": ["takes", "take", "took", "taking"], "answer": "B"},
    {"id": 804, "topic": "B2: Formal Grammar", "text": "It is necessary that she ___ her visa renewed.", "options": ["gets", "get", "got", "getting"], "answer": "B"},
    {"id": 806, "topic": "B2: Formal Grammar", "text": "I would rather she ___ here.", "options": ["stays", "stayed", "stay", "staying"], "answer": "B"},
    {"id": 808, "topic": "B2: Formal Grammar", "text": "It's about time we ___ going.", "options": ["get", "got", "getting", "will get"], "answer": "B"},
    {"id": 810, "topic": "B2: Formal Grammar", "text": "Suppose he ___ to come, what would we do?", "options": ["refuses", "refused", "refuse", "refusing"], "answer": "B"},
    {"id": 812, "topic": "B2: Formal Grammar", "text": "If it ___ for your help, I would have failed.", "options": ["isn't", "wasn't", "weren't", "hadn't been"], "answer": "D"},
    {"id": 814, "topic": "B2: Formal Grammar", "text": "Much ___ I admire her, I disagree with her decision.", "options": ["as", "so", "that", "like"], "answer": "A"},
    {"id": 816, "topic": "B2: Prepositions", "text": "She succeeded ___ getting the job.", "options": ["in", "on", "at", "for"], "answer": "A"},
    {"id": 818, "topic": "B2: Prepositions", "text": "He objected ___ the proposal.", "options": ["for", "to", "on", "at"], "answer": "B"},
    {"id": 820, "topic": "B2: Prepositions", "text": "I'm accustomed ___ working late.", "options": ["for", "to", "at", "in"], "answer": "B"},
    {"id": 822, "topic": "B2: Prepositions", "text": "She's capable ___ running the company.", "options": ["for", "to", "of", "in"], "answer": "C"},
    {"id": 824, "topic": "B2: Prepositions", "text": "He takes pride ___ his work.", "options": ["on", "in", "for", "at"], "answer": "B"},
    {"id": 826, "topic": "B2: Prepositions", "text": "I have no intention ___ leaving.", "options": ["for", "to", "of", "in"], "answer": "C"},
    {"id": 828, "topic": "B2: Prepositions", "text": "She insisted ___ paying for everything.", "options": ["for", "on", "to", "at"], "answer": "B"},
    {"id": 830, "topic": "B2: Prepositions", "text": "He's obsessed ___ fitness.", "options": ["for", "to", "with", "in"], "answer": "C"},
    {"id": 832, "topic": "B2: Prepositions", "text": "I'm fed up ___ this weather.", "options": ["of", "with", "from", "about"], "answer": "B"},
    {"id": 834, "topic": "B2: Prepositions", "text": "She's devoted ___ her family.", "options": ["for", "to", "with", "in"], "answer": "B"},
    {"id": 836, "topic": "B2: Prepositions", "text": "He was charged ___ fraud.", "options": ["for", "of", "with", "about"], "answer": "C"},
    {"id": 838, "topic": "B2: Prepositions", "text": "I'm grateful ___ your help.", "options": ["about", "for", "to", "with"], "answer": "B"},
    {"id": 840, "topic": "B2: Prepositions", "text": "She's allergic ___ cats.", "options": ["from", "to", "with", "for"], "answer": "B"},
    {"id": 842, "topic": "B2: Prepositions", "text": "He specialises ___ heart surgery.", "options": ["on", "at", "in", "for"], "answer": "C"},
    {"id": 844, "topic": "B2: Prepositions", "text": "I'm committed ___ this project.", "options": ["for", "to", "with", "in"], "answer": "B"},
    {"id": 846, "topic": "B2: Prepositions", "text": "She's addicted ___ social media.", "options": ["for", "to", "with", "on"], "answer": "B"},
    {"id": 848, "topic": "B2: Prepositions", "text": "He's eligible ___ the scholarship.", "options": ["to", "for", "of", "at"], "answer": "B"},
    {"id": 850, "topic": "B2: Prepositions", "text": "I'm indifferent ___ the outcome.", "options": ["for", "to", "with", "about"], "answer": "B"},
    {"id": 852, "topic": "B2: Prepositions", "text": "She's envious ___ his success.", "options": ["about", "for", "of", "with"], "answer": "C"},
    {"id": 854, "topic": "B2: Prepositions", "text": "He's prone ___ making mistakes.", "options": ["for", "to", "with", "in"], "answer": "B"},
    {"id": 856, "topic": "B2: Transformations", "text": "'It's a pity I can't swim.' → I wish I ___ swim.", "options": ["can", "could", "would", "should"], "answer": "B"},
    {"id": 858, "topic": "B2: Transformations", "text": "'She started working here in 2015.' → She ___ here since 2015.", "options": ["works", "has worked", "worked", "is working"], "answer": "B"},
    {"id": 860, "topic": "B2: Transformations", "text": "'They cancelled the match.' → The match ___.", "options": ["was cancelled", "cancelled", "has cancelled", "is cancelling"], "answer": "A"},
    {"id": 862, "topic": "B2: Transformations", "text": "'I regret not studying harder.' → I wish I ___ harder.", "options": ["study", "studied", "had studied", "would study"], "answer": "C"},
    {"id": 864, "topic": "B2: Transformations", "text": "'People say he is very rich.' → He ___ to be very rich.", "options": ["says", "is said", "said", "was saying"], "answer": "B"},
    {"id": 866, "topic": "B2: Transformations", "text": "'Without your help, I'd have failed.' → If you ___ helped me, I'd have failed.", "options": ["haven't", "hadn't", "didn't", "wouldn't"], "answer": "B"},
    {"id": 868, "topic": "B2: Transformations", "text": "'She's too young to drive.' → She isn't ___ to drive.", "options": ["enough old", "old enough", "very old", "so old"], "answer": "B"},
    {"id": 870, "topic": "B2: Transformations", "text": "'Despite being tired, she continued.' → Although she ___ tired, she continued.", "options": ["is", "was", "has been", "had been"], "answer": "B"},
    {"id": 872, "topic": "B2: Transformations", "text": "'He can run faster than me.' → I can't run as ___ as him.", "options": ["faster", "fast", "fastest", "more fast"], "answer": "B"},
    {"id": 874, "topic": "B2: Transformations", "text": "'It's not necessary to book in advance.' → You ___ book in advance.", "options": ["mustn't", "don't have to", "shouldn't", "can't"], "answer": "B"},
    {"id": 876, "topic": "B2: Transformations", "text": "'I last saw her in June.' → I ___ her since June.", "options": ["didn't see", "haven't seen", "don't see", "hadn't seen"], "answer": "B"},
    {"id": 878, "topic": "B2: Transformations", "text": "'It started raining an hour ago.' → It ___ raining for an hour.", "options": ["is", "has been", "was", "had been"], "answer": "B"},
    {"id": 880, "topic": "B2: Transformations", "text": "'She is the tallest in the class.' → Nobody in the class is ___ than her.", "options": ["tall", "taller", "tallest", "as tall"], "answer": "B"},
    {"id": 882, "topic": "B2: Transformations", "text": "'He said: I'll help you.' → He promised ___ help me.", "options": ["will", "to", "would", "he will"], "answer": "B"},
    {"id": 884, "topic": "B2: Transformations", "text": "'I've never eaten such good food.' → This is the ___ food I've ever eaten.", "options": ["good", "better", "best", "most good"], "answer": "C"},
    {"id": 886, "topic": "B2: Transformations", "text": "'Someone stole my bike.' → My bike ___.", "options": ["was stolen", "stole", "has stolen", "is stealing"], "answer": "A"},
    {"id": 888, "topic": "B2: Transformations", "text": "'He's so kind that everyone likes him.' → He's ___ kind that everyone likes him.", "options": ["too", "enough", "such", "so"], "answer": "D"},
    {"id": 890, "topic": "B2: Transformations", "text": "'She said: Don't touch it!' → She told me ___ it.", "options": ["don't touch", "not to touch", "to not touch", "not touching"], "answer": "B"},
    {"id": 892, "topic": "B2: Transformations", "text": "'We must leave now.' → It's ___ that we leave now.", "options": ["necessary", "possible", "probable", "certain"], "answer": "A"},
    {"id": 894, "topic": "B2: Transformations", "text": "'He didn't pass because he was lazy.' → If he ___ lazy, he would have passed.", "options": ["isn't", "wasn't", "hadn't been", "weren't"], "answer": "C"},
    {"id": 896, "topic": "B2: Transformations", "text": "'The film was so boring that I fell asleep.' → It was such a ___ film that I fell asleep.", "options": ["bored", "boring", "bore", "boredom"], "answer": "B"},
    {"id": 898, "topic": "B2: Transformations", "text": "'It's possible that she missed the bus.' → She ___ have missed the bus.", "options": ["must", "might", "should", "would"], "answer": "B"},
    {"id": 900, "topic": "B2: Transformations", "text": "'He speaks English very well.' → He is very good ___ speaking English.", "options": ["in", "on", "at", "for"], "answer": "C"},
    {"id": 902, "topic": "B2: Transformations", "text": "'They built this castle 500 years ago.' → This castle ___ 500 years ago.", "options": ["was built", "built", "has been built", "is built"], "answer": "A"},
    {"id": 904, "topic": "B2: Transformations", "text": "'No one in the team is faster than him.' → He is the ___ in the team.", "options": ["fast", "faster", "fastest", "most fast"], "answer": "C"},
    {"id": 906, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["She don't like coffee.", "She doesn't likes coffee.", "She doesn't like coffee.", "She not like coffee."], "answer": "C"},
    {"id": 908, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I have been to Paris last year.", "I went to Paris last year.", "I have gone to Paris last year.", "I was going to Paris last year."], "answer": "B"},
    {"id": 910, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["He suggested to go out.", "He suggested going out.", "He suggested go out.", "He suggested that going out."], "answer": "B"},
    {"id": 912, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I'm used to get up early.", "I'm used to getting up early.", "I used to getting up early.", "I'm use to get up early."], "answer": "B"},
    {"id": 914, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["Despite of the rain, we went out.", "Despite the rain, we went out.", "Despite it rained, we went out.", "Despite to rain, we went out."], "answer": "B"},
    {"id": 916, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["She told me don't worry.", "She told me not to worry.", "She said me not to worry.", "She told to me not worry."], "answer": "B"},
    {"id": 918, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I look forward to hear from you.", "I look forward to hearing from you.", "I look forward hearing from you.", "I look forward to heard from you."], "answer": "B"},
    {"id": 920, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["He made me to wait.", "He made me wait.", "He made me waiting.", "He made me waited."], "answer": "B"},
    {"id": 922, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["If I would know, I would tell you.", "If I knew, I would tell you.", "If I know, I would tell you.", "If I known, I would tell you."], "answer": "B"},
    {"id": 924, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["She's more taller than me.", "She's taller than me.", "She's most taller than me.", "She's taller that me."], "answer": "B"},
    {"id": 926, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I've been here since three hours.", "I've been here for three hours.", "I've been here during three hours.", "I've been here from three hours."], "answer": "B"},
    {"id": 928, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["He doesn't must go.", "He mustn't go.", "He don't must go.", "He must doesn't go."], "answer": "B"},
    {"id": 930, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I wish I can fly.", "I wish I could fly.", "I wish I will fly.", "I wish I would can fly."], "answer": "B"},
    {"id": 932, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["She is interested on art.", "She is interested in art.", "She is interested for art.", "She is interested at art."], "answer": "B"},
    {"id": 934, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["There are less people today.", "There are fewer people today.", "There are few people today than yesterday.", "There are lesser people today."], "answer": "B"},
    {"id": 936, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["He asked where do I live.", "He asked where I lived.", "He asked where did I live.", "He asked where I live."], "answer": "B"},
    {"id": 938, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I'm not agree with you.", "I don't agree with you.", "I'm not agreeing to you.", "I don't agree to you."], "answer": "B"},
    {"id": 940, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["He let me to go.", "He let me go.", "He let me going.", "He let me gone."], "answer": "B"},
    {"id": 942, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["It depends of the weather.", "It depends on the weather.", "It depends from the weather.", "It depends to the weather."], "answer": "B"},
    {"id": 944, "topic": "B2: Error Correction", "text": "Which sentence is CORRECT?", "options": ["I can't afford buying it.", "I can't afford to buy it.", "I can't afford buy it.", "I can't afford bought it."], "answer": "B"},
    {"id": 946, "topic": "B2: Idioms", "text": "'Break the ice' means:", "options": ["Destroy something", "Start a conversation in a social setting", "Freeze water", "Win a competition"], "answer": "B"},
    {"id": 948, "topic": "B2: Idioms", "text": "'Hit the nail on the head' means:", "options": ["Injure yourself", "Describe exactly what is right", "Build something", "Miss the point"], "answer": "B"},
    {"id": 950, "topic": "B2: Idioms", "text": "'A piece of cake' means:", "options": ["A dessert", "Something very easy", "A reward", "An exam"], "answer": "B"},
    {"id": 952, "topic": "B2: Idioms", "text": "'Let the cat out of the bag' means:", "options": ["Free an animal", "Reveal a secret", "Pack a bag", "Tell a joke"], "answer": "B"},
    {"id": 954, "topic": "B2: Idioms", "text": "'Burn the midnight oil' means:", "options": ["Cook late", "Work or study late at night", "Waste resources", "Start a fire"], "answer": "B"},
    {"id": 956, "topic": "B2: Idioms", "text": "'Cost an arm and a leg' means:", "options": ["Be free", "Be very expensive", "Be dangerous", "Be easy"], "answer": "B"},
    {"id": 958, "topic": "B2: Idioms", "text": "'Once in a blue moon' means:", "options": ["Very often", "Very rarely", "At night", "In winter"], "answer": "B"},
    {"id": 960, "topic": "B2: Idioms", "text": "'The ball is in your court' means:", "options": ["You love sports", "It's your decision now", "You lost", "Game over"], "answer": "B"},
    {"id": 962, "topic": "B2: Idioms", "text": "'Bite the bullet' means:", "options": ["Eat something hard", "Face a difficult situation bravely", "Fight", "Give up"], "answer": "B"},
    {"id": 964, "topic": "B2: Idioms", "text": "'Under the weather' means:", "options": ["Outside", "Feeling ill", "Wet", "Cold"], "answer": "B"},
    {"id": 966, "topic": "B2: Idioms", "text": "'Beat around the bush' means:", "options": ["Garden", "Avoid saying what you mean directly", "Run fast", "Search"], "answer": "B"},
    {"id": 968, "topic": "B2: Idioms", "text": "'See eye to eye' means:", "options": ["Stare", "Agree completely", "Fight", "Watch TV"], "answer": "B"},
    {"id": 970, "topic": "B2: Idioms", "text": "'Miss the boat' means:", "options": ["Go swimming", "Miss an opportunity", "Travel by sea", "Arrive late"], "answer": "B"},
    {"id": 972, "topic": "B2: Idioms", "text": "'On the same page' means:", "options": ["Reading together", "In agreement", "Lost", "Confused"], "answer": "B"},
    {"id": 974, "topic": "B2: Idioms", "text": "'Pull someone's leg' means:", "options": ["Hurt them", "Joke with them", "Help them stand", "Trip them"], "answer": "B"},
    {"id": 976, "topic": "B2: Idioms", "text": "'Spill the beans' means:", "options": ["Cook badly", "Reveal secret information", "Drop food", "Lie"], "answer": "B"},
    {"id": 978, "topic": "B2: Idioms", "text": "'The last straw' means:", "options": ["A drink", "The final problem that makes something unbearable", "Hay", "A tool"], "answer": "B"},
    {"id": 980, "topic": "B2: Idioms", "text": "'Cut corners' means:", "options": ["Use scissors", "Do something in the easiest/cheapest way", "Turn", "Drive carefully"], "answer": "B"},
    {"id": 982, "topic": "B2: Idioms", "text": "'Get cold feet' means:", "options": ["Feel cold", "Become nervous about something planned", "Run fast", "Take a bath"], "answer": "B"},
    {"id": 984, "topic": "B2: Idioms", "text": "'It's raining cats and dogs' means:", "options": ["Animals falling", "Raining very heavily", "A pet show", "A strange event"], "answer": "B"},
    {"id": 986, "topic": "B2: Idioms", "text": "'Sit on the fence' means:", "options": ["Rest outside", "Avoid making a decision", "Exercise", "Guard something"], "answer": "B"},
    {"id": 988, "topic": "B2: Idioms", "text": "'Call it a day' means:", "options": ["Phone someone", "Stop working for the day", "Name something", "Start over"], "answer": "B"},
    {"id": 990, "topic": "B2: Idioms", "text": "'Go the extra mile' means:", "options": ["Run far", "Make more effort than expected", "Get lost", "Travel"], "answer": "B"},
    {"id": 992, "topic": "B2: Idioms", "text": "'Keep an eye on' means:", "options": ["Ignore", "Watch carefully", "Close your eyes", "Wink"], "answer": "B"},
    {"id": 994, "topic": "B2: Idioms", "text": "'Wrap your head around' means:", "options": ["Wear a hat", "Understand something complicated", "Turn around", "Sleep"], "answer": "B"},
    {"id": 996, "topic": "B2: Formal/Informal", "text": "Formal for 'start':", "options": ["commence", "go", "kick off", "fire up"], "answer": "A"},
    {"id": 998, "topic": "B2: Formal/Informal", "text": "Formal for 'ask for':", "options": ["request", "beg", "want", "need"], "answer": "A"},
    {"id": 1000, "topic": "B2: Formal/Informal", "text": "Formal for 'get':", "options": ["obtain", "grab", "score", "nab"], "answer": "A"},
    {"id": 1002, "topic": "B2: Formal/Informal", "text": "Formal for 'help':", "options": ["assist", "give a hand", "pitch in", "help out"], "answer": "A"},
    {"id": 1004, "topic": "B2: Formal/Informal", "text": "Formal for 'buy':", "options": ["purchase", "grab", "snap up", "pick up"], "answer": "A"},
    {"id": 1006, "topic": "B2: Formal/Informal", "text": "Formal for 'end':", "options": ["terminate", "wrap up", "finish off", "wind down"], "answer": "A"},
    {"id": 1008, "topic": "B2: Formal/Informal", "text": "Formal for 'tell':", "options": ["inform", "fill in", "let know", "tip off"], "answer": "A"},
    {"id": 1010, "topic": "B2: Formal/Informal", "text": "Formal for 'think about':", "options": ["consider", "mull over", "chew on", "sleep on"], "answer": "A"},
    {"id": 1012, "topic": "B2: Formal/Informal", "text": "Formal for 'go up':", "options": ["increase", "shoot up", "skyrocket", "jump"], "answer": "A"},
    {"id": 1014, "topic": "B2: Formal/Informal", "text": "Formal for 'deal with':", "options": ["address", "sort out", "tackle", "handle"], "answer": "A"},
    {"id": 1016, "topic": "B2: Formal/Informal", "text": "Formal for 'enough':", "options": ["sufficient", "plenty", "loads", "tons"], "answer": "A"},
    {"id": 1018, "topic": "B2: Formal/Informal", "text": "Formal for 'try':", "options": ["attempt", "have a go", "give it a shot", "take a stab"], "answer": "A"},
    {"id": 1020, "topic": "B2: Formal/Informal", "text": "Formal for 'about':", "options": ["approximately", "around", "roughly", "more or less"], "answer": "A"},
    {"id": 1022, "topic": "B2: Formal/Informal", "text": "Formal for 'very important':", "options": ["crucial", "massive", "huge", "mega"], "answer": "A"},
    {"id": 1024, "topic": "B2: Formal/Informal", "text": "Formal for 'stop':", "options": ["cease", "quit", "knock off", "pack in"], "answer": "A"},
    {"id": 1026, "topic": "B2: Formal/Informal", "text": "Formal for 'give':", "options": ["provide", "hand over", "dish out", "fork out"], "answer": "A"},
    {"id": 1028, "topic": "B2: Formal/Informal", "text": "Formal for 'show':", "options": ["demonstrate", "show off", "point out", "flag up"], "answer": "A"},
    {"id": 1030, "topic": "B2: Formal/Informal", "text": "Formal for 'fix':", "options": ["rectify", "sort out", "patch up", "mend"], "answer": "A"},
    {"id": 1032, "topic": "B2: Formal/Informal", "text": "Formal for 'happen':", "options": ["occur", "crop up", "come about", "pop up"], "answer": "A"},
    {"id": 1034, "topic": "B2: Formal/Informal", "text": "Formal for 'need':", "options": ["require", "be after", "be dying for", "could do with"], "answer": "A"},
    {"id": 1036, "topic": "B2: Cloze", "text": "She ___ no attention to the warning signs.", "options": ["paid", "gave", "made", "took"], "answer": "A"},
    {"id": 1038, "topic": "B2: Cloze", "text": "They took it ___ granted that he would come.", "options": ["as", "for", "by", "in"], "answer": "B"},
    {"id": 1040, "topic": "B2: Cloze", "text": "I couldn't make ___ what the sign said.", "options": ["up", "out", "off", "in"], "answer": "B"},
    {"id": 1042, "topic": "B2: Cloze", "text": "He has a lot in ___ with his brother.", "options": ["common", "general", "particular", "total"], "answer": "A"},
    {"id": 1044, "topic": "B2: Cloze", "text": "She burst ___ tears when she heard the news.", "options": ["in", "into", "out", "with"], "answer": "B"},
    {"id": 1046, "topic": "B2: Cloze", "text": "The project was carried ___ successfully.", "options": ["on", "out", "up", "off"], "answer": "B"},
    {"id": 1048, "topic": "B2: Cloze", "text": "I can't ___ up with his behaviour any longer.", "options": ["put", "keep", "give", "take"], "answer": "A"},
    {"id": 1050, "topic": "B2: Cloze", "text": "She takes ___ her mother — they look identical.", "options": ["after", "on", "up", "over"], "answer": "A"},
    {"id": 1052, "topic": "B2: Cloze", "text": "He came ___ a great idea during the meeting.", "options": ["up with", "across", "down to", "out of"], "answer": "A"},
    {"id": 1054, "topic": "B2: Cloze", "text": "We ran ___ of time before finishing the test.", "options": ["out", "off", "up", "down"], "answer": "A"},
    {"id": 1056, "topic": "B2: Cloze", "text": "I'm looking ___ to seeing you again.", "options": ["ahead", "up", "forward", "after"], "answer": "C"},
    {"id": 1058, "topic": "B2: Cloze", "text": "She turned the offer ___ because the salary was too low.", "options": ["up", "off", "out", "down"], "answer": "D"},
    {"id": 1060, "topic": "B2: Cloze", "text": "He takes great ___ in his appearance.", "options": ["pride", "proud", "proudly", "priding"], "answer": "A"},
    {"id": 1062, "topic": "B2: Cloze", "text": "It makes no ___ complaining about it.", "options": ["point", "sense", "use", "difference"], "answer": "D"},
    {"id": 1064, "topic": "B2: Cloze", "text": "She has a good ___ of humour.", "options": ["sense", "feeling", "way", "manner"], "answer": "A"},
    {"id": 1066, "topic": "B2: Cloze", "text": "He did it on ___ — it wasn't an accident.", "options": ["purpose", "reason", "aim", "intention"], "answer": "A"},
    {"id": 1068, "topic": "B2: Cloze", "text": "There's no ___ worrying about things you can't change.", "options": ["point in", "use to", "way of", "sense of"], "answer": "A"},
    {"id": 1070, "topic": "B2: Cloze", "text": "I ___ the impression that she was unhappy.", "options": ["got", "made", "took", "had"], "answer": "A"},
    {"id": 1072, "topic": "B2: Cloze", "text": "She lost her ___ and started shouting.", "options": ["temper", "mood", "mind", "nerve"], "answer": "A"},
    {"id": 1074, "topic": "B2: Cloze", "text": "He keeps himself ___ himself — he's very private.", "options": ["to", "by", "for", "with"], "answer": "A"},
    {"id": 1076, "topic": "B2: Cloze", "text": "I wouldn't dream ___ asking her that.", "options": ["about", "of", "for", "to"], "answer": "B"},
    {"id": 1078, "topic": "B2: Cloze", "text": "She set her heart ___ becoming a doctor.", "options": ["on", "to", "for", "in"], "answer": "A"},
    {"id": 1080, "topic": "B2: Cloze", "text": "It never ___ to me that he was lying.", "options": ["came", "occurred", "happened", "struck"], "answer": "B"},
    {"id": 1082, "topic": "B2: Cloze", "text": "He went to great ___ to help us.", "options": ["lengths", "distances", "efforts", "ways"], "answer": "A"},
    {"id": 1084, "topic": "B2: Cloze", "text": "I've had ___ of waiting — let's go.", "options": ["enough", "plenty", "lots", "much"], "answer": "A"},
    {"id": 1086, "topic": "B2: Confusing Words", "text": "___ vs ___: 'I ___ you to come.' (= recommended)", "options": ["advise", "advice", "adviced", "advising"], "answer": "A"},
    {"id": 1088, "topic": "B2: Confusing Words", "text": "Choose the correct word: 'The ___ of the film was unexpected.'", "options": ["affect", "effect", "affection", "effective"], "answer": "B"},
    {"id": 1090, "topic": "B2: Confusing Words", "text": "Choose: 'He's very ___ — he works 12 hours a day.'", "options": ["efficient", "effective", "affective", "effected"], "answer": "A"},
    {"id": 1092, "topic": "B2: Confusing Words", "text": "Choose: 'She ___ the job offer without hesitation.'", "options": ["accepted", "excepted", "expected", "adapted"], "answer": "A"},
    {"id": 1094, "topic": "B2: Confusing Words", "text": "Choose: '___ from the bad weather, the trip was great.'", "options": ["Apart", "Except", "Accept", "Beside"], "answer": "A"},
    {"id": 1096, "topic": "B2: Confusing Words", "text": "Choose: 'The exam ___ of three parts.'", "options": ["consists", "contains", "includes", "involves"], "answer": "A"},
    {"id": 1098, "topic": "B2: Confusing Words", "text": "'Lose' vs 'loose': 'These trousers are too ___.'", "options": ["lose", "loose", "lost", "loosing"], "answer": "B"},
    {"id": 1100, "topic": "B2: Confusing Words", "text": "'Rise' vs 'raise': 'The sun ___ in the east.'", "options": ["rises", "raises", "risen", "raised"], "answer": "A"},
    {"id": 1102, "topic": "B2: Confusing Words", "text": "'Lay' vs 'lie': 'She ___ down on the sofa.'", "options": ["laid", "lay", "lied", "layed"], "answer": "B"},
    {"id": 1104, "topic": "B2: Confusing Words", "text": "'Borrow' vs 'lend': 'Can you ___ me £10?'", "options": ["borrow", "lend", "loan", "rent"], "answer": "B"},
    {"id": 1106, "topic": "B2: Confusing Words", "text": "'Remind' vs 'remember': 'Please ___ me to call her.'", "options": ["remember", "remind", "recall", "recollect"], "answer": "B"},
    {"id": 1108, "topic": "B2: Confusing Words", "text": "'Rob' vs 'steal': 'Someone ___ my wallet.'", "options": ["robbed", "stole", "theft", "burgled"], "answer": "B"},
    {"id": 1110, "topic": "B2: Confusing Words", "text": "'Do' vs 'make': 'She ___ an appointment with the dentist.'", "options": ["did", "made", "took", "had"], "answer": "B"},
    {"id": 1112, "topic": "B2: Confusing Words", "text": "'Say' vs 'tell': 'He ___ me a secret.'", "options": ["said", "told", "spoke", "talked"], "answer": "B"},
    {"id": 1114, "topic": "B2: Confusing Words", "text": "'Travel' vs 'trip': 'We had a wonderful ___ to Italy.'", "options": ["travel", "trip", "journey", "voyage"], "answer": "B"},
    {"id": 1116, "topic": "B2: Confusing Words", "text": "'Fun' vs 'funny': 'The party was really ___.'", "options": ["funny", "fun", "funnily", "funly"], "answer": "B"},
    {"id": 1118, "topic": "B2: Confusing Words", "text": "'Historic' vs 'historical': 'This is a ___ moment for the country.'", "options": ["historical", "historic", "history", "historically"], "answer": "B"},
    {"id": 1120, "topic": "B2: Confusing Words", "text": "'Economic' vs 'economical': 'This car is very ___.' (= saves money)", "options": ["economic", "economical", "economy", "economics"], "answer": "B"},
    {"id": 1122, "topic": "B2: Confusing Words", "text": "'Sensible' vs 'sensitive': 'She's very ___ — she cries easily.'", "options": ["sensible", "sensitive", "sensuous", "sensational"], "answer": "B"},
    {"id": 1124, "topic": "B2: Confusing Words", "text": "'Possibility' vs 'opportunity': 'This is a great ___ to learn.'", "options": ["possibility", "opportunity", "occasion", "chance"], "answer": "B"},
    {"id": 1126, "topic": "B1: Countable/Uncountable", "text": "I need ___ information.", "options": ["a", "an", "some", "many"], "answer": "C"},
    {"id": 1128, "topic": "B1: Countable/Uncountable", "text": "How ___ money do you have?", "options": ["many", "much", "few", "several"], "answer": "B"},
    {"id": 1130, "topic": "B1: Countable/Uncountable", "text": "There aren't ___ chairs in the room.", "options": ["much", "many", "a lot", "plenty"], "answer": "B"},
    {"id": 1132, "topic": "B1: Countable/Uncountable", "text": "She has ___ friends at school.", "options": ["much", "a lot of", "a", "an"], "answer": "B"},
    {"id": 1134, "topic": "B1: Countable/Uncountable", "text": "I'd like ___ water, please.", "options": ["a", "an", "some", "many"], "answer": "C"},
    {"id": 1136, "topic": "B1: Countable/Uncountable", "text": "There isn't ___ milk in the fridge.", "options": ["many", "much", "few", "several"], "answer": "B"},
    {"id": 1138, "topic": "B1: Countable/Uncountable", "text": "How ___ apples did you buy?", "options": ["much", "many", "a lot", "plenty"], "answer": "B"},
    {"id": 1140, "topic": "B1: Countable/Uncountable", "text": "She gave me ___ good advice.", "options": ["a", "an", "some", "many"], "answer": "C"},
    {"id": 1142, "topic": "B1: Countable/Uncountable", "text": "There are ___ students in the class.", "options": ["much", "a few", "a little", "an"], "answer": "B"},
    {"id": 1144, "topic": "B1: Countable/Uncountable", "text": "I have ___ homework tonight.", "options": ["many", "a lot of", "few", "several"], "answer": "B"},
    {"id": 1146, "topic": "B1: Countable/Uncountable", "text": "Would you like ___ tea?", "options": ["a", "an", "some", "many"], "answer": "C"},
    {"id": 1148, "topic": "B1: Countable/Uncountable", "text": "He doesn't have ___ experience.", "options": ["many", "much", "few", "several"], "answer": "B"},
    {"id": 1150, "topic": "B1: Countable/Uncountable", "text": "There are ___ eggs in the box.", "options": ["much", "a little", "a few", "an"], "answer": "C"},
    {"id": 1152, "topic": "B1: Countable/Uncountable", "text": "I need ___ sugar for the cake.", "options": ["a few", "a little", "many", "several"], "answer": "B"},
    {"id": 1154, "topic": "B1: Countable/Uncountable", "text": "She bought ___ new furniture.", "options": ["a", "an", "some", "many"], "answer": "C"},
    {"id": 1156, "topic": "B1: Countable/Uncountable", "text": "___ luggage do you have?", "options": ["How many", "How much", "How few", "How several"], "answer": "B"},
    {"id": 1158, "topic": "B1: Countable/Uncountable", "text": "I have very ___ time left.", "options": ["few", "little", "many", "several"], "answer": "B"},
    {"id": 1160, "topic": "B1: Countable/Uncountable", "text": "There are very ___ seats available.", "options": ["little", "few", "much", "a lot"], "answer": "B"},
    {"id": 1162, "topic": "B1: Countable/Uncountable", "text": "She has ___ patience with children.", "options": ["many", "a lot of", "few", "several"], "answer": "B"},
    {"id": 1164, "topic": "B1: Countable/Uncountable", "text": "I ate ___ rice for dinner.", "options": ["a", "an", "some", "many"], "answer": "C"},
    {"id": 1166, "topic": "B1: So/Such/Too/Enough", "text": "It was ___ cold that we stayed inside.", "options": ["so", "such", "too", "enough"], "answer": "A"},
    {"id": 1168, "topic": "B1: So/Such/Too/Enough", "text": "She is ___ a kind person.", "options": ["so", "such", "too", "enough"], "answer": "B"},
    {"id": 1170, "topic": "B1: So/Such/Too/Enough", "text": "The coffee is ___ hot to drink.", "options": ["so", "such", "too", "enough"], "answer": "C"},
    {"id": 1172, "topic": "B1: So/Such/Too/Enough", "text": "He's old ___ to drive.", "options": ["so", "such", "too", "enough"], "answer": "D"},
    {"id": 1174, "topic": "B1: So/Such/Too/Enough", "text": "It was ___ nice weather that we went to the park.", "options": ["so", "such", "too", "enough"], "answer": "B"},
    {"id": 1176, "topic": "B1: So/Such/Too/Enough", "text": "She speaks ___ quietly that I can't hear her.", "options": ["so", "such", "too", "enough"], "answer": "A"},
    {"id": 1178, "topic": "B1: So/Such/Too/Enough", "text": "This bag is ___ heavy for me to carry.", "options": ["so", "such", "too", "enough"], "answer": "C"},
    {"id": 1180, "topic": "B1: So/Such/Too/Enough", "text": "He isn't tall ___ to reach the shelf.", "options": ["so", "such", "too", "enough"], "answer": "D"},
    {"id": 1182, "topic": "B1: So/Such/Too/Enough", "text": "It was ___ an interesting book!", "options": ["so", "such", "too", "enough"], "answer": "B"},
    {"id": 1184, "topic": "B1: So/Such/Too/Enough", "text": "She was ___ tired that she fell asleep.", "options": ["so", "such", "too", "enough"], "answer": "A"},
    {"id": 1186, "topic": "B1: So/Such/Too/Enough", "text": "The music is ___ loud.", "options": ["so", "such", "too", "enough"], "answer": "C"},
    {"id": 1188, "topic": "B1: So/Such/Too/Enough", "text": "He's smart ___ to solve this problem.", "options": ["so", "such", "too", "enough"], "answer": "D"},
    {"id": 1190, "topic": "B1: So/Such/Too/Enough", "text": "They had ___ a good time at the party.", "options": ["so", "such", "too", "enough"], "answer": "B"},
    {"id": 1192, "topic": "B1: So/Such/Too/Enough", "text": "The dress was ___ expensive for me.", "options": ["so", "such", "too", "enough"], "answer": "C"},
    {"id": 1194, "topic": "B1: So/Such/Too/Enough", "text": "I don't have ___ money to buy it.", "options": ["so", "such", "too", "enough"], "answer": "D"},
    {"id": 1196, "topic": "B2: Cleft Sentences", "text": "It was John ___ broke the window.", "options": ["who", "which", "what", "where"], "answer": "A"},
    {"id": 1198, "topic": "B2: Cleft Sentences", "text": "What I need is ___ good rest.", "options": ["a", "the", "an", "some"], "answer": "A"},
    {"id": 1200, "topic": "B2: Cleft Sentences", "text": "It was in London ___ they met.", "options": ["who", "which", "that", "what"], "answer": "C"},
    {"id": 1202, "topic": "B2: Cleft Sentences", "text": "What annoys me ___ his attitude.", "options": ["are", "is", "were", "have"], "answer": "B"},
    {"id": 1204, "topic": "B2: Cleft Sentences", "text": "It's the weather ___ I don't like here.", "options": ["who", "that", "what", "where"], "answer": "B"},
    {"id": 1206, "topic": "B2: Cleft Sentences", "text": "All I want ___ some peace and quiet.", "options": ["are", "is", "were", "have"], "answer": "B"},
    {"id": 1208, "topic": "B2: Cleft Sentences", "text": "It was yesterday ___ she arrived.", "options": ["who", "which", "that", "what"], "answer": "C"},
    {"id": 1210, "topic": "B2: Cleft Sentences", "text": "What she said ___ absolutely true.", "options": ["are", "was", "were", "have"], "answer": "B"},
    {"id": 1212, "topic": "B2: Cleft Sentences", "text": "It's not money ___ makes you happy.", "options": ["who", "that", "what", "where"], "answer": "B"},
    {"id": 1214, "topic": "B2: Cleft Sentences", "text": "The thing ___ bothers me is the noise.", "options": ["who", "that", "what", "where"], "answer": "B"},
    {"id": 1216, "topic": "B2: Cleft Sentences", "text": "What happened ___ that the bus broke down.", "options": ["are", "was", "were", "is"], "answer": "B"},
    {"id": 1218, "topic": "B2: Cleft Sentences", "text": "It was his laziness ___ caused the problem.", "options": ["who", "that", "what", "where"], "answer": "B"},
    {"id": 1220, "topic": "B2: Cleft Sentences", "text": "The reason ___ I called is to apologise.", "options": ["who", "that", "why", "where"], "answer": "C"},
    {"id": 1222, "topic": "B2: Cleft Sentences", "text": "What matters ___ your health.", "options": ["are", "is", "were", "have"], "answer": "B"},
    {"id": 1224, "topic": "B2: Cleft Sentences", "text": "It's the first time ___ I've been here.", "options": ["who", "that", "what", "when"], "answer": "B"},
    {"id": 1226, "topic": "B2: Wish & Regret", "text": "I wish I ___ taller.", "options": ["am", "was", "were", "will be"], "answer": "C"},
    {"id": 1228, "topic": "B2: Wish & Regret", "text": "She wishes she ___ so much yesterday.", "options": ["doesn't eat", "didn't eat", "hadn't eaten", "won't eat"], "answer": "C"},
    {"id": 1230, "topic": "B2: Wish & Regret", "text": "If only I ___ more money!", "options": ["have", "had", "would have", "will have"], "answer": "B"},
    {"id": 1232, "topic": "B2: Wish & Regret", "text": "I wish you ___ stop making that noise.", "options": ["will", "would", "can", "could"], "answer": "B"},
    {"id": 1234, "topic": "B2: Wish & Regret", "text": "She regrets ___ the truth.", "options": ["tell", "to tell", "telling", "told"], "answer": "C"},
    {"id": 1236, "topic": "B2: Wish & Regret", "text": "I wish I ___ accepted that job.", "options": ["have", "has", "had", "would"], "answer": "C"},
    {"id": 1238, "topic": "B2: Wish & Regret", "text": "If only she ___ to me!", "options": ["listens", "listened", "had listened", "will listen"], "answer": "B"},
    {"id": 1240, "topic": "B2: Wish & Regret", "text": "He wishes he ___ study law.", "options": ["doesn't", "didn't have to", "hadn't to", "won't"], "answer": "B"},
    {"id": 1242, "topic": "B2: Wish & Regret", "text": "I wish it ___ raining.", "options": ["stops", "stopped", "would stop", "will stop"], "answer": "C"},
    {"id": 1244, "topic": "B2: Wish & Regret", "text": "She wishes she ___ come to the party last night.", "options": ["can", "could", "could have", "will"], "answer": "C"},
    {"id": 1246, "topic": "B2: Wish & Regret", "text": "I regret not ___ harder at school.", "options": ["study", "studying", "studied", "to study"], "answer": "B"},
    {"id": 1248, "topic": "B2: Wish & Regret", "text": "If only we ___ more time!", "options": ["have", "had", "would have", "will have"], "answer": "B"},
    {"id": 1250, "topic": "B2: Wish & Regret", "text": "I wish I ___ younger.", "options": ["am", "were", "will be", "have been"], "answer": "B"},
    {"id": 1252, "topic": "B2: Wish & Regret", "text": "He wishes he ___ about the party earlier.", "options": ["knows", "knew", "had known", "will know"], "answer": "C"},
    {"id": 1254, "topic": "B2: Wish & Regret", "text": "I wish she ___ always complaining.", "options": ["isn't", "wasn't", "wouldn't be", "won't be"], "answer": "C"},
    {"id": 1256, "topic": "B2: Gerund/Infinitive", "text": "I remember ___ this film before. (= I have a memory of it)", "options": ["see", "to see", "seeing", "seen"], "answer": "C"},
    {"id": 1258, "topic": "B2: Gerund/Infinitive", "text": "I remembered ___ the door. (= I didn't forget)", "options": ["lock", "to lock", "locking", "locked"], "answer": "B"},
    {"id": 1260, "topic": "B2: Gerund/Infinitive", "text": "She stopped ___ a cigarette. (= in order to smoke)", "options": ["smoke", "to smoke", "smoking", "smoked"], "answer": "B"},
    {"id": 1262, "topic": "B2: Gerund/Infinitive", "text": "He stopped ___ junk food. (= quit)", "options": ["eat", "to eat", "eating", "eaten"], "answer": "C"},
    {"id": 1264, "topic": "B2: Gerund/Infinitive", "text": "I regret ___ you this bad news. (= I'm sorry to say)", "options": ["tell", "to tell", "telling", "told"], "answer": "B"},
    {"id": 1266, "topic": "B2: Gerund/Infinitive", "text": "I regret ___ that job. (= I wish I hadn't)", "options": ["take", "to take", "taking", "taken"], "answer": "C"},
    {"id": 1268, "topic": "B2: Gerund/Infinitive", "text": "She tried ___ the window, but it was stuck.", "options": ["open", "to open", "opening", "opened"], "answer": "B"},
    {"id": 1270, "topic": "B2: Gerund/Infinitive", "text": "Try ___ some honey in your tea. (= experiment)", "options": ["put", "to put", "putting", "puts"], "answer": "C"},
    {"id": 1272, "topic": "B2: Gerund/Infinitive", "text": "He went on ___ about his holiday for hours.", "options": ["talk", "to talk", "talking", "talked"], "answer": "C"},
    {"id": 1274, "topic": "B2: Gerund/Infinitive", "text": "After the speech, she went on ___ answer questions.", "options": ["—", "to", "for", "with"], "answer": "B"},
    {"id": 1276, "topic": "B2: Gerund/Infinitive", "text": "I can't help ___ sorry for him.", "options": ["feel", "to feel", "feeling", "felt"], "answer": "C"},
    {"id": 1278, "topic": "B2: Gerund/Infinitive", "text": "The film is worth ___.", "options": ["see", "to see", "seeing", "seen"], "answer": "C"},
    {"id": 1280, "topic": "B2: Gerund/Infinitive", "text": "She pretended ___ asleep.", "options": ["be", "to be", "being", "been"], "answer": "B"},
    {"id": 1282, "topic": "B2: Gerund/Infinitive", "text": "He admitted ___ the money.", "options": ["steal", "to steal", "stealing", "stolen"], "answer": "C"},
    {"id": 1284, "topic": "B2: Gerund/Infinitive", "text": "She can't stand ___ in traffic.", "options": ["sit", "to sit", "sitting", "sat"], "answer": "C"},
    {"id": 1286, "topic": "B2: Academic Vocab", "text": "'Analyse' means to:", "options": ["ignore", "examine in detail", "create", "simplify"], "answer": "B"},
    {"id": 1288, "topic": "B2: Academic Vocab", "text": "'Significant' means:", "options": ["unimportant", "important/meaningful", "small", "unclear"], "answer": "B"},
    {"id": 1290, "topic": "B2: Academic Vocab", "text": "'Furthermore' is used to:", "options": ["contrast", "add information", "conclude", "question"], "answer": "B"},
    {"id": 1292, "topic": "B2: Academic Vocab", "text": "'Hypothesis' means:", "options": ["a fact", "a theory to be tested", "a conclusion", "a summary"], "answer": "B"},
    {"id": 1294, "topic": "B2: Academic Vocab", "text": "'To illustrate' means to:", "options": ["hide", "explain with examples", "confuse", "delete"], "answer": "B"},
    {"id": 1296, "topic": "B2: Academic Vocab", "text": "'Approximately' means:", "options": ["exactly", "about/roughly", "certainly", "definitely"], "answer": "B"},
    {"id": 1298, "topic": "B2: Academic Vocab", "text": "'Substantial' means:", "options": ["tiny", "large/considerable", "unimportant", "temporary"], "answer": "B"},
    {"id": 1300, "topic": "B2: Academic Vocab", "text": "'Nevertheless' means:", "options": ["because", "however/despite that", "therefore", "moreover"], "answer": "B"},
    {"id": 1302, "topic": "B2: Academic Vocab", "text": "'To imply' means to:", "options": ["state directly", "suggest indirectly", "deny", "prove"], "answer": "B"},
    {"id": 1304, "topic": "B2: Academic Vocab", "text": "'Subsequent' means:", "options": ["previous", "following/next", "current", "initial"], "answer": "B"},
    {"id": 1306, "topic": "B2: Academic Vocab", "text": "'To evaluate' means to:", "options": ["ignore", "assess/judge", "create", "memorise"], "answer": "B"},
    {"id": 1308, "topic": "B2: Academic Vocab", "text": "'Coherent' means:", "options": ["confusing", "logical and consistent", "short", "loud"], "answer": "B"},
    {"id": 1310, "topic": "B2: Academic Vocab", "text": "'To distinguish' means to:", "options": ["mix up", "see the difference between", "ignore", "combine"], "answer": "B"},
    {"id": 1312, "topic": "B2: Academic Vocab", "text": "'Prevalent' means:", "options": ["rare", "widespread/common", "ancient", "hidden"], "answer": "B"},
    {"id": 1314, "topic": "B2: Academic Vocab", "text": "'To contradict' means to:", "options": ["agree", "say the opposite", "support", "repeat"], "answer": "B"},
    {"id": 1316, "topic": "B2: Academic Vocab", "text": "'Relevant' means:", "options": ["unrelated", "connected to the topic", "boring", "complex"], "answer": "B"},
    {"id": 1318, "topic": "B2: Academic Vocab", "text": "'To justify' means to:", "options": ["criticise", "give reasons for", "deny", "ignore"], "answer": "B"},
    {"id": 1320, "topic": "B2: Academic Vocab", "text": "'Vague' means:", "options": ["clear", "not clear/imprecise", "loud", "fast"], "answer": "B"},
    {"id": 1322, "topic": "B2: Academic Vocab", "text": "'To emerge' means to:", "options": ["disappear", "appear/come out", "hide", "stay"], "answer": "B"},
    {"id": 1324, "topic": "B2: Academic Vocab", "text": "'Ultimately' means:", "options": ["never", "in the end/finally", "firstly", "probably"], "answer": "B"},
    {"id": 1326, "topic": "B1: Expressions", "text": "'Could you ___ the door, please?'", "options": ["close", "closing", "to close", "closed"], "answer": "A"},
    {"id": 1328, "topic": "B1: Expressions", "text": "'Would you ___ having the meeting tomorrow?'", "options": ["mind", "like", "want", "prefer"], "answer": "A"},
    {"id": 1330, "topic": "B1: Expressions", "text": "'I'm ___ forward to the holiday.'", "options": ["looking", "watching", "seeing", "viewing"], "answer": "A"},
    {"id": 1332, "topic": "B1: Expressions", "text": "'It's not ___ learning English — it's essential!'", "options": ["worthy", "worth", "value", "valuable"], "answer": "B"},
    {"id": 1334, "topic": "B1: Expressions", "text": "'Can I ___ a suggestion?'", "options": ["do", "make", "take", "give"], "answer": "B"},
    {"id": 1336, "topic": "B1: Expressions", "text": "'I'd ___ stay at home tonight.'", "options": ["rather", "better", "prefer", "like"], "answer": "A"},
    {"id": 1338, "topic": "B1: Expressions", "text": "'She's ___ of working overtime.'", "options": ["bored", "fed up", "tired", "enough"], "answer": "C"},
    {"id": 1340, "topic": "B1: Expressions", "text": "'There's no ___ arguing about it.'", "options": ["point", "use", "way", "reason"], "answer": "A"},
    {"id": 1342, "topic": "B1: Expressions", "text": "'I ___ no idea what happened.'", "options": ["have", "do", "make", "take"], "answer": "A"},
    {"id": 1344, "topic": "B1: Expressions", "text": "'Let me ___ it over and get back to you.'", "options": ["think", "thought", "thinking", "thinks"], "answer": "A"},
    {"id": 1346, "topic": "B1: Expressions", "text": "'In my ___, the plan is too risky.'", "options": ["opinion", "view", "thinking", "idea"], "answer": "A"},
    {"id": 1348, "topic": "B1: Expressions", "text": "'She ___ a lot of attention to detail.'", "options": ["pays", "gives", "does", "makes"], "answer": "A"},
    {"id": 1350, "topic": "B1: Expressions", "text": "'Can you ___ me a hand with this?'", "options": ["give", "do", "make", "take"], "answer": "A"},
    {"id": 1352, "topic": "B1: Expressions", "text": "'I don't ___ about the delay — let's just go.'", "options": ["care", "mind", "worry", "bother"], "answer": "A"},
    {"id": 1354, "topic": "B1: Expressions", "text": "'It ___ without saying that safety comes first.'", "options": ["goes", "comes", "takes", "makes"], "answer": "A"},
    {"id": 1356, "topic": "B1: Expressions", "text": "'She ___ an important role in the project.'", "options": ["played", "did", "made", "took"], "answer": "A"},
    {"id": 1358, "topic": "B1: Expressions", "text": "'I ___ the impression that he was bored.'", "options": ["got", "made", "did", "took"], "answer": "A"},
    {"id": 1360, "topic": "B1: Expressions", "text": "'Let's ___ the most of this opportunity.'", "options": ["make", "do", "take", "have"], "answer": "A"},
    {"id": 1362, "topic": "B1: Expressions", "text": "'I'm ___ two minds about accepting the offer.'", "options": ["in", "on", "at", "of"], "answer": "A"},
    {"id": 1364, "topic": "B1: Expressions", "text": "'To ___ the truth, I didn't enjoy the film.'", "options": ["tell", "say", "speak", "talk"], "answer": "A"},
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
  .jump-grid { margin-bottom:20px; }
  .jump-group { margin-bottom:12px; }
  .jump-group-header { display:flex; align-items:center; gap:8px; cursor:pointer; padding:6px 0; user-select:none; }
  .jump-group-title { font-size:.82rem; font-weight:600; color:var(--accent); }
  .jump-group-stats { font-size:.75rem; color:var(--muted); }
  .jump-group-arrow { font-size:.7rem; color:var(--muted); transition:transform .15s; }
  .jump-group-arrow.open { transform:rotate(90deg); }
  .jump-group-buttons { display:flex; flex-wrap:wrap; gap:4px; padding:4px 0 0 0; }
  .jump-group.collapsed .jump-group-buttons { display:none; }
  .jump-group.collapsed .jump-group-arrow { transform:rotate(0deg); }
  .jump-btn { width:32px; height:32px; border-radius:5px; font-size:.72rem; padding:0;
    background:var(--card); border:1px solid var(--border); color:var(--muted); cursor:pointer; }
  .jump-btn:hover { border-color:var(--accent); color:var(--accent); }
  .jump-btn.correct { background:rgba(34,197,94,.3); border-color:var(--green); color:var(--green); }
  .jump-btn.incorrect { background:rgba(248,81,73,.25); border-color:var(--red); color:var(--red); }
  .jump-btn.answered { background:rgba(59,130,246,.25); border-color:var(--accent); color:var(--text); }
  .jump-btn.current { border-color:var(--accent); color:var(--accent); font-weight:700; }
  .jump-progress { height:3px; background:var(--border); border-radius:2px; margin-top:3px; overflow:hidden; }
  .jump-progress-fill { height:100%; background:var(--green); border-radius:2px; transition:width .2s; }

  @keyframes blink-correct { 0%,100%{background:rgba(34,197,94,.1)} 50%{background:rgba(34,197,94,.5)} }
  .option.blink-correct { animation: blink-correct 0.4s ease 3; border-color:var(--green); }
  .option.blink-correct .option-label { background:var(--green); color:#fff; }
  .option.show-wrong { border-color:var(--red); opacity:0.7; }
  .option.show-wrong .option-label { background:var(--red); color:#fff; }
</style>
</head>
<body>
<div class="container">

<div id="name-screen">
  <h1>🇬🇧 English B1-B2 Quiz</h1>
  <p class="subtitle">960 questions · Grammar & Vocabulary · Good luck!</p>
  <input type="text" id="student-name" placeholder="Enter your first and last name" maxlength="60">
  <br>
  <button id="btn-start" onclick="startQuiz()">Start Quiz</button>
</div>

<div id="quiz-screen" style="display:none">
  <h1>🇬🇧 English B1-B2 Quiz</h1>
  <p class="subtitle" id="quiz-student-name"></p>
  <p class="progress-text" id="progress-text"></p>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  <div class="nav-buttons" style="margin-bottom:12px">
    <button class="btn-secondary" onclick="prevQ()">← Back</button>
    <button class="btn-secondary" id="btn-next" onclick="nextQ()">Next →</button>
    <button class="btn-finish" onclick="finishQuiz()">Finish Quiz</button>
  </div>
  <div id="question-container"></div>
  <div class="jump-grid" id="jump-grid"></div>
</div>

<div id="result-screen" style="display:none">
  <div class="result-card">
    <h1>Result</h1>
    <div class="score-big" id="result-score"></div>
    <div class="score-label">correct answers out of 960</div>
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
let waitingNext = false;  // true = wrong answer shown, need second Next
let checkedAnswers = {};  // {qid: true} = answer was checked (for coloring)
const QUESTIONS_FULL = __FULL_QUESTIONS__;

function updateURL() {
  const qid = QUESTIONS[currentQ].id;
  history.replaceState(null, '', '#q=' + qid);
}

window.onload = function() {
  if (TEACHER_MODE) { showTeacherList(); return; }
  if (VIEW_STUDENT) { showViewScreen(VIEW_STUDENT, false); return; }
  // Check if we can auto-restore session from localStorage + URL hash
  const hash = location.hash;
  let savedName = null;
  try { savedName = localStorage.getItem('eng_quiz_name'); } catch(e) {}
  if (savedName && hash && hash.match(/^#q=\d+$/)) {
    // Auto-restore: fill in name and start
    document.getElementById('student-name').value = savedName;
    document.getElementById('name-screen').style.display = 'block';
    startQuiz();
    return;
  }
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
  // Save name to localStorage for session restore
  try { localStorage.setItem('eng_quiz_name', n); localStorage.setItem('eng_quiz_started', startedAt); } catch(e) {}
  document.getElementById('name-screen').style.display = 'none';
  document.getElementById('quiz-screen').style.display = 'block';
  document.getElementById('quiz-student-name').textContent = n;
  // Restore question from URL hash
  const hash = location.hash;
  if (hash && hash.match(/^#q=(\d+)$/)) {
    const qnum = parseInt(hash.substring(3));
    const idx = QUESTIONS.findIndex(q => q.id === qnum);
    if (idx >= 0) currentQ = idx;
  }
  // Restore answers from localStorage
  try {
    const saved = localStorage.getItem('eng_quiz_answers');
    if (saved) { const parsed = JSON.parse(saved); if (typeof parsed === 'object') Object.assign(answers, parsed); }
  } catch(e) {}
  renderJumpGrid();
  renderQuestion();
  updateURL();
}

function renderJumpGrid() {
  const grid = document.getElementById('jump-grid');
  // Group questions by topic
  const groups = [];
  let lastTopic = '';
  QUESTIONS.forEach((q, i) => {
    if (q.topic !== lastTopic) {
      groups.push({ topic: q.topic, items: [] });
      lastTopic = q.topic;
    }
    groups[groups.length - 1].items.push({ q, i });
  });
  let html = '';
  groups.forEach((g, gi) => {
    const answered = g.items.filter(x => answers[x.q.id]).length;
    const total = g.items.length;
    const hasCurrent = g.items.some(x => x.i === currentQ);
    const collapsed = !hasCurrent && answered === total ? ' collapsed' : '';
    const pct = total > 0 ? Math.round(answered / total * 100) : 0;
    html += '<div class="jump-group' + collapsed + '" id="jg-' + gi + '">';
    html += '<div class="jump-group-header" onclick="toggleGroup(' + gi + ')">';
    html += '<span class="jump-group-arrow' + (collapsed ? '' : ' open') + '" id="jga-' + gi + '">&#9654;</span>';
    html += '<span class="jump-group-title">' + g.topic + '</span>';
    html += '<span class="jump-group-stats">' + answered + '/' + total + '</span>';
    html += '</div>';
    html += '<div class="jump-progress"><div class="jump-progress-fill" style="width:' + pct + '%"></div></div>';
    html += '<div class="jump-group-buttons">';
    g.items.forEach(x => {
      const ans = answers[x.q.id];
      let cls = 'jump-btn';
      if (x.i === currentQ) cls += ' current';
      if (ans) {
        const isCorrect = QUESTIONS_FULL && QUESTIONS_FULL[x.i] && QUESTIONS_FULL[x.i].answer === ans;
        cls += (checkedAnswers[x.q.id]) ? (isCorrect ? ' correct' : ' incorrect') : ' answered';
      }
      html += '<button class="' + cls + '" onclick="goToQ(' + x.i + ')">' + x.q.id + '</button>';
    });
    html += '</div></div>';
  });
  grid.innerHTML = html;
}

function toggleGroup(gi) {
  const el = document.getElementById('jg-' + gi);
  const arrow = document.getElementById('jga-' + gi);
  el.classList.toggle('collapsed');
  arrow.classList.toggle('open');
}

function goToQ(i) { currentQ = i; renderQuestion(); renderJumpGrid(); updateURL(); }

function renderQuestion() {
  waitingNext = false;
  var btnNext = document.getElementById('btn-next');
  if (btnNext) btnNext.textContent = 'Next \u2192';
  const q = QUESTIONS[currentQ];
  const total = QUESTIONS.length;
  document.getElementById('progress-text').textContent =
    'Question '+(currentQ+1)+' of '+total+'  ·  Answered: '+Object.keys(answers).length;
  document.getElementById('progress-fill').style.width = ((currentQ+1)/total*100)+'%';

  let html = '<div class="question-card"><div class="question-num">Question '+q.id+' · '+q.topic+'</div><div class="question-text">'+q.text+'</div><div class="options">';
  q.options.forEach((opt, i) => {
    const label = ['A','B','C','D'][i];
    const sel = answers[q.id] === label ? ' selected' : '';
    html += '<div class="option'+sel+'" onclick="selectAnswer('+q.id+',&#39;'+label+'&#39;,this)"><span class="option-label">'+label+'</span><span>'+opt+'</span></div>';
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
  // Save answers to localStorage
  try { localStorage.setItem('eng_quiz_answers', JSON.stringify(answers)); } catch(e) {}
}

function prevQ() { if (currentQ > 0) { currentQ--; renderQuestion(); renderJumpGrid(); updateURL(); } }
function nextQ() {
  if (currentQ >= QUESTIONS.length-1) return;
  // If waiting for second Next (after showing correct answer), just proceed
  if (waitingNext) {
    waitingNext = false;
    currentQ++;
    renderQuestion();
    renderJumpGrid();
    updateURL();
    return;
  }
  // If current question is answered, check it
  const q = QUESTIONS[currentQ];
  const given = answers[q.id];
  if (given && QUESTIONS_FULL) {
    const fullQ = QUESTIONS_FULL[currentQ];
    checkedAnswers[q.id] = true;
    if (fullQ && given !== fullQ.answer) {
      // Wrong answer — show correct with blink
      const correctIdx = ['A','B','C','D'].indexOf(fullQ.answer);
      const givenIdx = ['A','B','C','D'].indexOf(given);
      const options = document.querySelectorAll('.option');
      if (options[givenIdx]) options[givenIdx].classList.add('show-wrong');
      if (options[correctIdx]) options[correctIdx].classList.add('blink-correct');
      waitingNext = true;
      document.getElementById('btn-next').textContent = 'Next → →';
      renderJumpGrid();
      return;
    }
  }
  // Correct or unanswered — proceed
  currentQ++;
  renderQuestion();
  renderJumpGrid();
  updateURL();
}

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
      try { localStorage.removeItem('eng_quiz_answers'); localStorage.removeItem('eng_quiz_name'); localStorage.removeItem('eng_quiz_started'); } catch(e) {}
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
    html = html.replace("__FULL_QUESTIONS__", json.dumps(ENGLISH_QUESTIONS, ensure_ascii=False))
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
