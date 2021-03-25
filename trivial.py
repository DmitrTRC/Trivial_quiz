import time
import requests
import random


class Question:

    def __init__(self, category, q_type, difficulty, quest, ans_arr, ans):
        self.category = category
        self.q_type = q_type
        self.difficulty = difficulty
        self.question = quest
        self.incorrect_answers = ans_arr
        self._answer = ans

    def show(self):
        print(self.question, end='\n\n')
        time.sleep(1)
        for index, answer in enumerate(self.answers, 1):
            print(f'\n{index}. {answer}')
        print()

    def get_answer(self):
        return self._answer

    def get_complexity(self, num):
        return self.difficulty


def load_questions(complexity=None):
    api_url = 'https://opentdb.com/api.php?amount=10&category=9'
    params = {
        'amount': 5,
        'category': 9
    }
    response = requests.get(api_url, params=params)
    qa_base = []
    for record in response.json().get('results'):
        qa_base.append(Question(
            record.get('category'),
            record.get('type'),
            record.get('difficulty'),
            record.get('question'),
            record.get('incorrect_answers'),
            record.get('correct_answer'),
        ))

    # random.shuffle(answers)

    # return Question(response.get('question'), answers, answer)


def main():
    load_questions()
    # wins = 0
    # name = input('Enter your name => ')
    # questions_num = int(input('Enter how many questions do you like to get => '))
    # complexity = 1
    # for _ in range(questions_num):
    #     question = load_question(complexity=complexity)
    #     print(f'DIFFICULTY : {question.get_complexity(complexity)}')
    #     question.show()
    #     while True:
    #         user_answer = int(input('Enter your answer => '))
    #         if user_answer in range(1, len(question.answers) + 1):
    #             break
    #
    #     if question.answers[user_answer - 1] == question.get_answer():
    #         print(f'\n{name} fine! Correct answer.\n')
    #         complexity += 1 if complexity < 3 else -3
    #         wins += 1
    #     else:
    #         print(f'\n{name} OOPS! You FAIL.\n')
    #         if complexity > 1: complexity -= 1
    #
    # print(f'{name} - You win {wins} points and that is {round(wins / questions_num * 100)} %')


if __name__ == '__main__':
    main()
