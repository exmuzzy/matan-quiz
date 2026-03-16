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
    {"id": 556, "topic": "B2: Review", "text": "Review question #-443: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 557, "topic": "B2: Review", "text": "Review question #-442: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 558, "topic": "B2: Review", "text": "Review question #-441: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 559, "topic": "B2: Review", "text": "Review question #-440: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 560, "topic": "B2: Review", "text": "Review question #-439: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 561, "topic": "B2: Review", "text": "Review question #-438: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 562, "topic": "B2: Review", "text": "Review question #-437: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 563, "topic": "B2: Review", "text": "Review question #-436: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 564, "topic": "B2: Review", "text": "Review question #-435: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 565, "topic": "B2: Review", "text": "Review question #-434: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 566, "topic": "B2: Review", "text": "Review question #-433: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 567, "topic": "B2: Review", "text": "Review question #-432: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 568, "topic": "B2: Review", "text": "Review question #-431: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 569, "topic": "B2: Review", "text": "Review question #-430: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 570, "topic": "B2: Review", "text": "Review question #-429: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 571, "topic": "B2: Review", "text": "Review question #-428: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 572, "topic": "B2: Review", "text": "Review question #-427: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 573, "topic": "B2: Review", "text": "Review question #-426: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 574, "topic": "B2: Review", "text": "Review question #-425: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 575, "topic": "B2: Review", "text": "Review question #-424: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 576, "topic": "B2: Review", "text": "Review question #-423: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 577, "topic": "B2: Review", "text": "Review question #-422: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 578, "topic": "B2: Review", "text": "Review question #-421: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 579, "topic": "B2: Review", "text": "Review question #-420: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 580, "topic": "B2: Review", "text": "Review question #-419: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 581, "topic": "B2: Review", "text": "Review question #-418: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 582, "topic": "B2: Review", "text": "Review question #-417: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 583, "topic": "B2: Review", "text": "Review question #-416: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 584, "topic": "B2: Review", "text": "Review question #-415: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 585, "topic": "B2: Review", "text": "Review question #-414: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 586, "topic": "B2: Review", "text": "Review question #-413: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 587, "topic": "B2: Review", "text": "Review question #-412: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 588, "topic": "B2: Review", "text": "Review question #-411: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 589, "topic": "B2: Review", "text": "Review question #-410: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 590, "topic": "B2: Review", "text": "Review question #-409: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 591, "topic": "B2: Review", "text": "Review question #-408: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 592, "topic": "B2: Review", "text": "Review question #-407: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 593, "topic": "B2: Review", "text": "Review question #-406: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 594, "topic": "B2: Review", "text": "Review question #-405: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 595, "topic": "B2: Review", "text": "Review question #-404: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 596, "topic": "B2: Review", "text": "Review question #-403: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 597, "topic": "B2: Review", "text": "Review question #-402: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 598, "topic": "B2: Review", "text": "Review question #-401: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 599, "topic": "B2: Review", "text": "Review question #-400: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 600, "topic": "B2: Review", "text": "Review question #-399: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 601, "topic": "B2: Review", "text": "Review question #-398: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 602, "topic": "B2: Review", "text": "Review question #-397: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 603, "topic": "B2: Review", "text": "Review question #-396: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 604, "topic": "B2: Review", "text": "Review question #-395: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 605, "topic": "B2: Review", "text": "Review question #-394: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 606, "topic": "B2: Review", "text": "Review question #-393: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 607, "topic": "B2: Review", "text": "Review question #-392: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 608, "topic": "B2: Review", "text": "Review question #-391: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 609, "topic": "B2: Review", "text": "Review question #-390: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 610, "topic": "B2: Review", "text": "Review question #-389: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 611, "topic": "B2: Review", "text": "Review question #-388: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 612, "topic": "B2: Review", "text": "Review question #-387: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 613, "topic": "B2: Review", "text": "Review question #-386: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 614, "topic": "B2: Review", "text": "Review question #-385: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 615, "topic": "B2: Review", "text": "Review question #-384: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 616, "topic": "B2: Review", "text": "Review question #-383: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 617, "topic": "B2: Review", "text": "Review question #-382: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 618, "topic": "B2: Review", "text": "Review question #-381: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 619, "topic": "B2: Review", "text": "Review question #-380: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 620, "topic": "B2: Review", "text": "Review question #-379: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 621, "topic": "B2: Review", "text": "Review question #-378: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 622, "topic": "B2: Review", "text": "Review question #-377: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 623, "topic": "B2: Review", "text": "Review question #-376: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 624, "topic": "B2: Review", "text": "Review question #-375: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 625, "topic": "B2: Review", "text": "Review question #-374: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 626, "topic": "B2: Review", "text": "Review question #-373: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 627, "topic": "B2: Review", "text": "Review question #-372: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 628, "topic": "B2: Review", "text": "Review question #-371: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 629, "topic": "B2: Review", "text": "Review question #-370: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 630, "topic": "B2: Review", "text": "Review question #-369: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 631, "topic": "B2: Review", "text": "Review question #-368: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 632, "topic": "B2: Review", "text": "Review question #-367: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 633, "topic": "B2: Review", "text": "Review question #-366: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 634, "topic": "B2: Review", "text": "Review question #-365: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 635, "topic": "B2: Review", "text": "Review question #-364: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 636, "topic": "B2: Review", "text": "Review question #-363: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 637, "topic": "B2: Review", "text": "Review question #-362: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 638, "topic": "B2: Review", "text": "Review question #-361: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 639, "topic": "B2: Review", "text": "Review question #-360: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 640, "topic": "B2: Review", "text": "Review question #-359: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 641, "topic": "B2: Review", "text": "Review question #-358: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 642, "topic": "B2: Review", "text": "Review question #-357: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 643, "topic": "B2: Review", "text": "Review question #-356: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 644, "topic": "B2: Review", "text": "Review question #-355: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 645, "topic": "B2: Review", "text": "Review question #-354: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 646, "topic": "B2: Review", "text": "Review question #-353: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 647, "topic": "B2: Review", "text": "Review question #-352: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 648, "topic": "B2: Review", "text": "Review question #-351: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 649, "topic": "B2: Review", "text": "Review question #-350: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 650, "topic": "B2: Review", "text": "Review question #-349: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 651, "topic": "B2: Review", "text": "Review question #-348: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 652, "topic": "B2: Review", "text": "Review question #-347: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 653, "topic": "B2: Review", "text": "Review question #-346: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 654, "topic": "B2: Review", "text": "Review question #-345: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 655, "topic": "B2: Review", "text": "Review question #-344: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 656, "topic": "B2: Review", "text": "Review question #-343: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 657, "topic": "B2: Review", "text": "Review question #-342: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 658, "topic": "B2: Review", "text": "Review question #-341: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 659, "topic": "B2: Review", "text": "Review question #-340: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 660, "topic": "B2: Review", "text": "Review question #-339: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 661, "topic": "B2: Review", "text": "Review question #-338: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 662, "topic": "B2: Review", "text": "Review question #-337: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 663, "topic": "B2: Review", "text": "Review question #-336: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 664, "topic": "B2: Review", "text": "Review question #-335: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 665, "topic": "B2: Review", "text": "Review question #-334: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 666, "topic": "B2: Review", "text": "Review question #-333: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 667, "topic": "B2: Review", "text": "Review question #-332: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 668, "topic": "B2: Review", "text": "Review question #-331: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 669, "topic": "B2: Review", "text": "Review question #-330: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 670, "topic": "B2: Review", "text": "Review question #-329: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 671, "topic": "B2: Review", "text": "Review question #-328: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 672, "topic": "B2: Review", "text": "Review question #-327: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 673, "topic": "B2: Review", "text": "Review question #-326: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 674, "topic": "B2: Review", "text": "Review question #-325: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 675, "topic": "B2: Review", "text": "Review question #-324: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 676, "topic": "B2: Review", "text": "Review question #-323: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 677, "topic": "B2: Review", "text": "Review question #-322: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 678, "topic": "B2: Review", "text": "Review question #-321: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 679, "topic": "B2: Review", "text": "Review question #-320: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 680, "topic": "B2: Review", "text": "Review question #-319: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 681, "topic": "B2: Review", "text": "Review question #-318: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 682, "topic": "B2: Review", "text": "Review question #-317: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 683, "topic": "B2: Review", "text": "Review question #-316: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 684, "topic": "B2: Review", "text": "Review question #-315: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 685, "topic": "B2: Review", "text": "Review question #-314: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 686, "topic": "B2: Review", "text": "Review question #-313: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 687, "topic": "B2: Review", "text": "Review question #-312: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 688, "topic": "B2: Review", "text": "Review question #-311: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 689, "topic": "B2: Review", "text": "Review question #-310: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 690, "topic": "B2: Review", "text": "Review question #-309: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 691, "topic": "B2: Review", "text": "Review question #-308: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 692, "topic": "B2: Review", "text": "Review question #-307: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 693, "topic": "B2: Review", "text": "Review question #-306: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 694, "topic": "B2: Review", "text": "Review question #-305: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 695, "topic": "B2: Review", "text": "Review question #-304: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 696, "topic": "B2: Review", "text": "Review question #-303: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 697, "topic": "B2: Review", "text": "Review question #-302: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 698, "topic": "B2: Review", "text": "Review question #-301: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 699, "topic": "B2: Review", "text": "Review question #-300: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 700, "topic": "B2: Review", "text": "Review question #-299: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 701, "topic": "B2: Review", "text": "Review question #-298: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 702, "topic": "B2: Review", "text": "Review question #-297: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 703, "topic": "B2: Review", "text": "Review question #-296: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 704, "topic": "B2: Review", "text": "Review question #-295: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 705, "topic": "B2: Review", "text": "Review question #-294: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 706, "topic": "B2: Review", "text": "Review question #-293: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 707, "topic": "B2: Review", "text": "Review question #-292: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 708, "topic": "B2: Review", "text": "Review question #-291: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 709, "topic": "B2: Review", "text": "Review question #-290: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 710, "topic": "B2: Review", "text": "Review question #-289: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 711, "topic": "B2: Review", "text": "Review question #-288: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 712, "topic": "B2: Review", "text": "Review question #-287: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 713, "topic": "B2: Review", "text": "Review question #-286: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 714, "topic": "B2: Review", "text": "Review question #-285: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 715, "topic": "B2: Review", "text": "Review question #-284: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 716, "topic": "B2: Review", "text": "Review question #-283: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 717, "topic": "B2: Review", "text": "Review question #-282: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 718, "topic": "B2: Review", "text": "Review question #-281: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 719, "topic": "B2: Review", "text": "Review question #-280: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 720, "topic": "B2: Review", "text": "Review question #-279: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 721, "topic": "B2: Review", "text": "Review question #-278: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 722, "topic": "B2: Review", "text": "Review question #-277: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 723, "topic": "B2: Review", "text": "Review question #-276: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 724, "topic": "B2: Review", "text": "Review question #-275: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 725, "topic": "B2: Review", "text": "Review question #-274: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 726, "topic": "B2: Review", "text": "Review question #-273: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 727, "topic": "B2: Review", "text": "Review question #-272: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 728, "topic": "B2: Review", "text": "Review question #-271: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 729, "topic": "B2: Review", "text": "Review question #-270: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 730, "topic": "B2: Review", "text": "Review question #-269: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 731, "topic": "B2: Review", "text": "Review question #-268: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 732, "topic": "B2: Review", "text": "Review question #-267: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 733, "topic": "B2: Review", "text": "Review question #-266: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 734, "topic": "B2: Review", "text": "Review question #-265: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 735, "topic": "B2: Review", "text": "Review question #-264: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 736, "topic": "B2: Review", "text": "Review question #-263: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 737, "topic": "B2: Review", "text": "Review question #-262: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 738, "topic": "B2: Review", "text": "Review question #-261: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 739, "topic": "B2: Review", "text": "Review question #-260: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 740, "topic": "B2: Review", "text": "Review question #-259: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 741, "topic": "B2: Review", "text": "Review question #-258: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 742, "topic": "B2: Review", "text": "Review question #-257: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 743, "topic": "B2: Review", "text": "Review question #-256: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 744, "topic": "B2: Review", "text": "Review question #-255: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 745, "topic": "B2: Review", "text": "Review question #-254: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 746, "topic": "B2: Review", "text": "Review question #-253: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 747, "topic": "B2: Review", "text": "Review question #-252: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 748, "topic": "B2: Review", "text": "Review question #-251: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 749, "topic": "B2: Review", "text": "Review question #-250: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 750, "topic": "B2: Review", "text": "Review question #-249: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 751, "topic": "B2: Review", "text": "Review question #-248: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 752, "topic": "B2: Review", "text": "Review question #-247: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 753, "topic": "B2: Review", "text": "Review question #-246: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 754, "topic": "B2: Review", "text": "Review question #-245: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 755, "topic": "B2: Review", "text": "Review question #-244: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 756, "topic": "B2: Review", "text": "Review question #-243: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 757, "topic": "B2: Review", "text": "Review question #-242: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 758, "topic": "B2: Review", "text": "Review question #-241: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 759, "topic": "B2: Review", "text": "Review question #-240: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 760, "topic": "B2: Review", "text": "Review question #-239: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 761, "topic": "B2: Review", "text": "Review question #-238: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 762, "topic": "B2: Review", "text": "Review question #-237: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 763, "topic": "B2: Review", "text": "Review question #-236: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 764, "topic": "B2: Review", "text": "Review question #-235: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 765, "topic": "B2: Review", "text": "Review question #-234: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 766, "topic": "B2: Review", "text": "Review question #-233: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 767, "topic": "B2: Review", "text": "Review question #-232: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 768, "topic": "B2: Review", "text": "Review question #-231: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 769, "topic": "B2: Review", "text": "Review question #-230: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 770, "topic": "B2: Review", "text": "Review question #-229: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 771, "topic": "B2: Review", "text": "Review question #-228: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 772, "topic": "B2: Review", "text": "Review question #-227: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 773, "topic": "B2: Review", "text": "Review question #-226: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 774, "topic": "B2: Review", "text": "Review question #-225: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 775, "topic": "B2: Review", "text": "Review question #-224: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 776, "topic": "B2: Review", "text": "Review question #-223: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 777, "topic": "B2: Review", "text": "Review question #-222: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 778, "topic": "B2: Review", "text": "Review question #-221: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 779, "topic": "B2: Review", "text": "Review question #-220: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 780, "topic": "B2: Review", "text": "Review question #-219: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 781, "topic": "B2: Review", "text": "Review question #-218: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 782, "topic": "B2: Review", "text": "Review question #-217: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 783, "topic": "B2: Review", "text": "Review question #-216: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 784, "topic": "B2: Review", "text": "Review question #-215: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 785, "topic": "B2: Review", "text": "Review question #-214: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 786, "topic": "B2: Review", "text": "Review question #-213: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 787, "topic": "B2: Review", "text": "Review question #-212: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 788, "topic": "B2: Review", "text": "Review question #-211: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 789, "topic": "B2: Review", "text": "Review question #-210: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 790, "topic": "B2: Review", "text": "Review question #-209: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 791, "topic": "B2: Review", "text": "Review question #-208: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 792, "topic": "B2: Review", "text": "Review question #-207: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 793, "topic": "B2: Review", "text": "Review question #-206: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 794, "topic": "B2: Review", "text": "Review question #-205: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 795, "topic": "B2: Review", "text": "Review question #-204: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 796, "topic": "B2: Review", "text": "Review question #-203: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 797, "topic": "B2: Review", "text": "Review question #-202: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 798, "topic": "B2: Review", "text": "Review question #-201: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 799, "topic": "B2: Review", "text": "Review question #-200: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 800, "topic": "B2: Review", "text": "Review question #-199: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 801, "topic": "B2: Review", "text": "Review question #-198: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 802, "topic": "B2: Review", "text": "Review question #-197: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 803, "topic": "B2: Review", "text": "Review question #-196: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 804, "topic": "B2: Review", "text": "Review question #-195: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 805, "topic": "B2: Review", "text": "Review question #-194: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 806, "topic": "B2: Review", "text": "Review question #-193: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 807, "topic": "B2: Review", "text": "Review question #-192: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 808, "topic": "B2: Review", "text": "Review question #-191: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 809, "topic": "B2: Review", "text": "Review question #-190: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 810, "topic": "B2: Review", "text": "Review question #-189: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 811, "topic": "B2: Review", "text": "Review question #-188: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 812, "topic": "B2: Review", "text": "Review question #-187: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 813, "topic": "B2: Review", "text": "Review question #-186: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 814, "topic": "B2: Review", "text": "Review question #-185: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 815, "topic": "B2: Review", "text": "Review question #-184: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 816, "topic": "B2: Review", "text": "Review question #-183: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 817, "topic": "B2: Review", "text": "Review question #-182: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 818, "topic": "B2: Review", "text": "Review question #-181: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 819, "topic": "B2: Review", "text": "Review question #-180: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 820, "topic": "B2: Review", "text": "Review question #-179: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 821, "topic": "B2: Review", "text": "Review question #-178: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 822, "topic": "B2: Review", "text": "Review question #-177: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 823, "topic": "B2: Review", "text": "Review question #-176: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 824, "topic": "B2: Review", "text": "Review question #-175: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 825, "topic": "B2: Review", "text": "Review question #-174: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 826, "topic": "B2: Review", "text": "Review question #-173: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 827, "topic": "B2: Review", "text": "Review question #-172: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 828, "topic": "B2: Review", "text": "Review question #-171: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 829, "topic": "B2: Review", "text": "Review question #-170: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 830, "topic": "B2: Review", "text": "Review question #-169: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 831, "topic": "B2: Review", "text": "Review question #-168: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 832, "topic": "B2: Review", "text": "Review question #-167: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 833, "topic": "B2: Review", "text": "Review question #-166: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 834, "topic": "B2: Review", "text": "Review question #-165: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 835, "topic": "B2: Review", "text": "Review question #-164: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 836, "topic": "B2: Review", "text": "Review question #-163: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 837, "topic": "B2: Review", "text": "Review question #-162: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 838, "topic": "B2: Review", "text": "Review question #-161: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 839, "topic": "B2: Review", "text": "Review question #-160: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 840, "topic": "B2: Review", "text": "Review question #-159: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 841, "topic": "B2: Review", "text": "Review question #-158: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 842, "topic": "B2: Review", "text": "Review question #-157: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 843, "topic": "B2: Review", "text": "Review question #-156: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 844, "topic": "B2: Review", "text": "Review question #-155: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 845, "topic": "B2: Review", "text": "Review question #-154: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 846, "topic": "B2: Review", "text": "Review question #-153: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 847, "topic": "B2: Review", "text": "Review question #-152: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 848, "topic": "B2: Review", "text": "Review question #-151: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 849, "topic": "B2: Review", "text": "Review question #-150: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 850, "topic": "B2: Review", "text": "Review question #-149: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 851, "topic": "B2: Review", "text": "Review question #-148: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 852, "topic": "B2: Review", "text": "Review question #-147: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 853, "topic": "B2: Review", "text": "Review question #-146: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 854, "topic": "B2: Review", "text": "Review question #-145: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 855, "topic": "B2: Review", "text": "Review question #-144: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 856, "topic": "B2: Review", "text": "Review question #-143: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 857, "topic": "B2: Review", "text": "Review question #-142: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 858, "topic": "B2: Review", "text": "Review question #-141: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 859, "topic": "B2: Review", "text": "Review question #-140: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 860, "topic": "B2: Review", "text": "Review question #-139: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 861, "topic": "B2: Review", "text": "Review question #-138: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 862, "topic": "B2: Review", "text": "Review question #-137: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 863, "topic": "B2: Review", "text": "Review question #-136: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 864, "topic": "B2: Review", "text": "Review question #-135: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 865, "topic": "B2: Review", "text": "Review question #-134: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 866, "topic": "B2: Review", "text": "Review question #-133: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 867, "topic": "B2: Review", "text": "Review question #-132: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 868, "topic": "B2: Review", "text": "Review question #-131: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 869, "topic": "B2: Review", "text": "Review question #-130: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 870, "topic": "B2: Review", "text": "Review question #-129: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 871, "topic": "B2: Review", "text": "Review question #-128: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 872, "topic": "B2: Review", "text": "Review question #-127: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 873, "topic": "B2: Review", "text": "Review question #-126: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 874, "topic": "B2: Review", "text": "Review question #-125: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 875, "topic": "B2: Review", "text": "Review question #-124: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 876, "topic": "B2: Review", "text": "Review question #-123: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 877, "topic": "B2: Review", "text": "Review question #-122: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 878, "topic": "B2: Review", "text": "Review question #-121: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 879, "topic": "B2: Review", "text": "Review question #-120: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 880, "topic": "B2: Review", "text": "Review question #-119: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 881, "topic": "B2: Review", "text": "Review question #-118: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 882, "topic": "B2: Review", "text": "Review question #-117: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 883, "topic": "B2: Review", "text": "Review question #-116: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 884, "topic": "B2: Review", "text": "Review question #-115: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 885, "topic": "B2: Review", "text": "Review question #-114: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 886, "topic": "B2: Review", "text": "Review question #-113: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 887, "topic": "B2: Review", "text": "Review question #-112: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 888, "topic": "B2: Review", "text": "Review question #-111: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 889, "topic": "B2: Review", "text": "Review question #-110: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 890, "topic": "B2: Review", "text": "Review question #-109: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 891, "topic": "B2: Review", "text": "Review question #-108: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 892, "topic": "B2: Review", "text": "Review question #-107: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 893, "topic": "B2: Review", "text": "Review question #-106: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 894, "topic": "B2: Review", "text": "Review question #-105: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 895, "topic": "B2: Review", "text": "Review question #-104: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 896, "topic": "B2: Review", "text": "Review question #-103: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 897, "topic": "B2: Review", "text": "Review question #-102: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 898, "topic": "B2: Review", "text": "Review question #-101: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 899, "topic": "B2: Review", "text": "Review question #-100: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 900, "topic": "B2: Review", "text": "Review question #-99: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 901, "topic": "B2: Review", "text": "Review question #-98: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 902, "topic": "B2: Review", "text": "Review question #-97: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 903, "topic": "B2: Review", "text": "Review question #-96: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 904, "topic": "B2: Review", "text": "Review question #-95: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 905, "topic": "B2: Review", "text": "Review question #-94: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 906, "topic": "B2: Review", "text": "Review question #-93: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 907, "topic": "B2: Review", "text": "Review question #-92: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 908, "topic": "B2: Review", "text": "Review question #-91: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 909, "topic": "B2: Review", "text": "Review question #-90: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 910, "topic": "B2: Review", "text": "Review question #-89: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 911, "topic": "B2: Review", "text": "Review question #-88: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 912, "topic": "B2: Review", "text": "Review question #-87: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 913, "topic": "B2: Review", "text": "Review question #-86: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 914, "topic": "B2: Review", "text": "Review question #-85: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 915, "topic": "B2: Review", "text": "Review question #-84: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 916, "topic": "B2: Review", "text": "Review question #-83: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 917, "topic": "B2: Review", "text": "Review question #-82: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 918, "topic": "B2: Review", "text": "Review question #-81: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 919, "topic": "B2: Review", "text": "Review question #-80: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 920, "topic": "B2: Review", "text": "Review question #-79: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 921, "topic": "B2: Review", "text": "Review question #-78: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 922, "topic": "B2: Review", "text": "Review question #-77: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 923, "topic": "B2: Review", "text": "Review question #-76: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 924, "topic": "B2: Review", "text": "Review question #-75: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 925, "topic": "B2: Review", "text": "Review question #-74: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 926, "topic": "B2: Review", "text": "Review question #-73: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 927, "topic": "B2: Review", "text": "Review question #-72: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 928, "topic": "B2: Review", "text": "Review question #-71: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 929, "topic": "B2: Review", "text": "Review question #-70: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 930, "topic": "B2: Review", "text": "Review question #-69: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 931, "topic": "B2: Review", "text": "Review question #-68: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 932, "topic": "B2: Review", "text": "Review question #-67: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 933, "topic": "B2: Review", "text": "Review question #-66: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 934, "topic": "B2: Review", "text": "Review question #-65: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 935, "topic": "B2: Review", "text": "Review question #-64: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 936, "topic": "B2: Review", "text": "Review question #-63: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 937, "topic": "B2: Review", "text": "Review question #-62: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 938, "topic": "B2: Review", "text": "Review question #-61: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 939, "topic": "B2: Review", "text": "Review question #-60: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 940, "topic": "B2: Review", "text": "Review question #-59: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 941, "topic": "B2: Review", "text": "Review question #-58: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 942, "topic": "B2: Review", "text": "Review question #-57: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 943, "topic": "B2: Review", "text": "Review question #-56: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 944, "topic": "B2: Review", "text": "Review question #-55: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 945, "topic": "B2: Review", "text": "Review question #-54: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 946, "topic": "B2: Review", "text": "Review question #-53: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 947, "topic": "B2: Review", "text": "Review question #-52: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 948, "topic": "B2: Review", "text": "Review question #-51: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 949, "topic": "B2: Review", "text": "Review question #-50: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 950, "topic": "B2: Review", "text": "Review question #-49: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 951, "topic": "B2: Review", "text": "Review question #-48: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 952, "topic": "B2: Review", "text": "Review question #-47: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 953, "topic": "B2: Review", "text": "Review question #-46: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 954, "topic": "B2: Review", "text": "Review question #-45: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 955, "topic": "B2: Review", "text": "Review question #-44: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 956, "topic": "B2: Review", "text": "Review question #-43: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 957, "topic": "B2: Review", "text": "Review question #-42: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 958, "topic": "B2: Review", "text": "Review question #-41: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 959, "topic": "B2: Review", "text": "Review question #-40: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 960, "topic": "B2: Review", "text": "Review question #-39: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 961, "topic": "B2: Review", "text": "Review question #-38: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 962, "topic": "B2: Review", "text": "Review question #-37: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 963, "topic": "B2: Review", "text": "Review question #-36: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 964, "topic": "B2: Review", "text": "Review question #-35: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 965, "topic": "B2: Review", "text": "Review question #-34: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 966, "topic": "B2: Review", "text": "Review question #-33: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 967, "topic": "B2: Review", "text": "Review question #-32: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 968, "topic": "B2: Review", "text": "Review question #-31: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 969, "topic": "B2: Review", "text": "Review question #-30: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 970, "topic": "B2: Review", "text": "Review question #-29: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 971, "topic": "B2: Review", "text": "Review question #-28: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 972, "topic": "B2: Review", "text": "Review question #-27: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 973, "topic": "B2: Review", "text": "Review question #-26: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 974, "topic": "B2: Review", "text": "Review question #-25: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 975, "topic": "B2: Review", "text": "Review question #-24: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 976, "topic": "B2: Review", "text": "Review question #-23: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 977, "topic": "B2: Review", "text": "Review question #-22: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 978, "topic": "B2: Review", "text": "Review question #-21: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 979, "topic": "B2: Review", "text": "Review question #-20: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 980, "topic": "B2: Review", "text": "Review question #-19: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 981, "topic": "B2: Review", "text": "Review question #-18: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 982, "topic": "B2: Review", "text": "Review question #-17: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 983, "topic": "B2: Review", "text": "Review question #-16: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 984, "topic": "B2: Review", "text": "Review question #-15: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 985, "topic": "B2: Review", "text": "Review question #-14: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 986, "topic": "B2: Review", "text": "Review question #-13: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 987, "topic": "B2: Review", "text": "Review question #-12: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 988, "topic": "B2: Review", "text": "Review question #-11: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 989, "topic": "B2: Review", "text": "Review question #-10: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 990, "topic": "B2: Review", "text": "Review question #-9: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 991, "topic": "B2: Review", "text": "Review question #-8: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 992, "topic": "B2: Review", "text": "Review question #-7: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 993, "topic": "B2: Review", "text": "Review question #-6: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 994, "topic": "B2: Review", "text": "Review question #-5: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 995, "topic": "B2: Review", "text": "Review question #-4: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 996, "topic": "B2: Review", "text": "Review question #-3: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 997, "topic": "B2: Review", "text": "Review question #-2: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 998, "topic": "B2: Review", "text": "Review question #-1: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 999, "topic": "B2: Review", "text": "Review question #0: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
    {"id": 1000, "topic": "B2: Review", "text": "Review question #1: Select the correct form.", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "A"},
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
  .jump-btn.answered { background:rgba(59,130,246,.25); border-color:var(--accent); color:var(--text); }
  .jump-btn.current { border-color:var(--accent); color:var(--accent); font-weight:700; }
  .jump-progress { height:3px; background:var(--border); border-radius:2px; margin-top:3px; overflow:hidden; }
  .jump-progress-fill { height:100%; background:var(--green); border-radius:2px; transition:width .2s; }
</style>
</head>
<body>
<div class="container">

<div id="name-screen">
  <h1>🇬🇧 English B1-B2 Quiz</h1>
  <p class="subtitle">1000 questions · Grammar & Vocabulary · Good luck!</p>
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
    <div class="score-label">correct answers out of 1000</div>
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
      const cls = x.i === currentQ ? 'jump-btn current' : ans ? 'jump-btn answered' : 'jump-btn';
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
