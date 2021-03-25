import time
import requests
import random
import json
from types import SimpleNamespace
from html.parser import HTMLParser
import html


class Question:

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def show(self):
        print('\n', html.unescape(getattr(self, 'question')), end='\n\n')
        time.sleep(1)
        random.shuffle(answers := [getattr(self, 'correct_answer')] + getattr(self, 'incorrect_answers'))
        for index, answer in enumerate(answers, 1):
            print(f'\n{index}. {html.unescape(answer)}')
        print()
        return len(answers), answers.index(self.get_correct_answer()) + 1

    def get_correct_answer(self):
        return getattr(self, 'correct_answer')

    def __str__(self):
        return str(self.__dict__)


def load_questions(amount=5, category=None, difficulty=None):
    api_url = 'https://opentdb.com/api.php?amount=10&category=9'
    params = {
        'amount': amount,
        'category': category,
        'difficulty': difficulty,
    }
    response = requests.get(api_url, params=params)
    qa_base = []
    for record in response.json().get('results'):
        qa_base.append(Question(**record))
    return qa_base


def main():
    difficulty = ['easy', 'medium', 'hard']
    wins = 0
    name = input('Enter your name => ')
    questions_num = int(input('Enter how many questions do you like to get => '))
    cur_difficulty = difficulty[int(input('Enter the difficulty from 1 to 3 (easy/medium/hard) => ')) - 1]
    questions = load_questions(difficulty=cur_difficulty, amount=questions_num)
    for question in questions:
        ans_count, correct_number = question.show()
        while True:
            user_answer = int(input('Enter your answer => '))
            if user_answer in range(1, ans_count + 1):
                break

        if user_answer == correct_number:
            print(f'\n{name} fine! Correct answer.\n')
            wins += 1
        else:
            print(f'\n{name} OOPS! You FAIL.\n')

    print(f'{name} - You win {wins} points and that is {round(wins / questions_num * 100)} %')


if __name__ == '__main__':
    main()
