import time
import requests
import random
import html


class Question:

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def show(self, need_translate=False):
        header = html.unescape(getattr(self, 'question'))
        print('\n', header, end='\n\n')
        time.sleep(1)
        random.shuffle(answers := [getattr(self, 'correct_answer')] + getattr(self, 'incorrect_answers'))
        for index, answer in enumerate(answers, 1):
            answer = html.unescape(answer)
            print(f'\n{index}. {answer}')
        print()
        return len(answers), answers.index(self.get_correct_answer()) + 1

    def get_correct_answer(self):
        return getattr(self, 'correct_answer')

    def __str__(self):
        return str(self.__dict__)


class User:
    def __init__(self, user_name='Ghost', wins=0):
        self.user_name = user_name
        self.wins = wins


class Game:
    difficulty_range = ['easy', 'medium', 'hard']

    def __init__(self, user: User, amount=5, category=None, difficulty=None):
        self.amount = amount
        self.category = category
        self.difficulty = self.difficulty_range[difficulty]
        self.user = user

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

    def show_results(self):
        print(f'{self.user.user_name} - You win {self.user.wins} points and that is'
              f' {round(self.user.wins / self.amount * 100)} %')

    def run(self):
        for question in self.load_questions():
            ans_count, correct_number = question.show()
            while True:
                user_answer = int(input('Enter your answer => '))
                if user_answer in range(1, ans_count + 1):
                    break

            if user_answer == correct_number:
                print(f'\n{self.user.user_name} fine! Correct answer.\n')
                self.user.wins += 1
            else:
                print(f'\n{self.user.user_name} OOPS! You FAIL.\n')
                print(f'Correct answer is: {question.get_correct_answer()}')


def main():

    user = User(user_name=input('Enter your name => '))
    questions_num = int(input('Enter how many questions do you like to get => '))
    cur_difficulty = int(input('Enter the difficulty from 1 to 3 (easy/medium/hard ) => ')) - 1
    game = Game(user=user, amount=questions_num, difficulty=cur_difficulty)
    game.run()
    game.show_results()


if __name__ == '__main__':
    main()
