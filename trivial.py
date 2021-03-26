import time
import requests
import random
import html
from googletrans import Translator

translator = Translator()


class Question:

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def show(self, need_translate=False):
        header = html.unescape(getattr(self, 'question'))
        if need_translate: header = translator.translate(header, 'ru').text
        print('\n', header, end='\n\n')
        time.sleep(1)
        random.shuffle(answers := [getattr(self, 'correct_answer')] + getattr(self, 'incorrect_answers'))
        for index, answer in enumerate(answers, 1):
            answer = html.unescape(answer)
            if need_translate: answer = translator.translate(answer, 'ru').text
            print(f'\n{index}. {answer}')
        print()
        return len(answers), answers.index(self.get_correct_answer()) + 1

    def get_correct_answer(self):
        return getattr(self, 'correct_answer')

    def __str__(self):
        return str(self.__dict__)


class Game:
    difficulty_range = ['easy', 'medium', 'hard']

    def __init__(self, amount=5, category=None, difficulty=None):
        self.amount = amount
        self.category = category
        self.difficulty = self.difficulty_range[difficulty]

    def load_questions(self):
        api_url = 'https://opentdb.com/api.php'
        params = {
            'amount': self.amount,
            'category': self.category,
            'difficulty': self.difficulty,
        }
        response = requests.get(api_url, params=params)
        qa_base = []
        for record in response.json().get('results'):
            qa_base.append(Question(**record))
        return qa_base

    def run(self):
        pass


def main():
    difficulty = ['easy', 'medium', 'hard']
    wins = 0
    name = input('Enter your name => ')
    questions_num = int(input('Enter how many questions do you like to get => '))
    cur_difficulty = difficulty[int(input('Enter the difficulty from 1 to 3 (easy/medium/hard ) => ')) - 1]
    if input('Do you need to translate ? y/n ').lower() == 'y':
        need_translate = True
    else:
        need_translate = False
    game = Game(amount=questions_num, difficulty=cur_difficulty)

    for question in questions:
        ans_count, correct_number = question.show(need_translate=need_translate)
        while True:
            user_answer = int(input('Enter your answer => '))
            if user_answer in range(1, ans_count + 1):
                break

        if user_answer == correct_number:
            print(f'\n{name} fine! Correct answer.\n')
            wins += 1
        else:
            print(f'\n{name} OOPS! You FAIL.\n')
            if need_translate:
                help_str = translator.translate(question.get_correct_answer(), 'ru').text
            else:
                help_str = question.get_correct_answer()
            print(f'Correct answer is: {help_str}')
    print(f'{name} - You win {wins} points and that is {round(wins / questions_num * 100)} %')


if __name__ == '__main__':
    main()
