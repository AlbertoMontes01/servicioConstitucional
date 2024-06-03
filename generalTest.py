import matplotlib.pyplot as plt

class User:
    def __init__(self, name, language):
        self.name = name
        self.language = language
        self.level = None  # Nivel MCER inicial

    def update_level(self, level):
        self.level = level

class LanguageTest:
    def __init__(self):
        self.questions = []
        self.answers = []
        self.correct_count = 0
        self.incorrect_count = 0

    def add_question(self, question, correct_answer):
        self.questions.append(question)
        self.answers.append(correct_answer)

    def evaluate(self, user_answers):
        self.correct_count = 0
        self.incorrect_count = 0
        for user_answer, correct_answer in zip(user_answers, self.answers):
            if user_answer.lower() == correct_answer.lower():
                self.correct_count += 1
            else:
                self.incorrect_count += 1

        total_questions = len(self.questions)
        percentage = (self.correct_count / total_questions) * 100

        if percentage >= 90:
            return "C2"
        elif percentage >= 75:
            return "C1"
        elif percentage >= 60:
            return "B2"
        elif percentage >= 45:
            return "B1"
        elif percentage >= 30:
            return "A2"
        else:
            return "A1"

    def generate_result_chart(self, user):
        labels = ['Correct', 'Incorrect']
        counts = [self.correct_count, self.incorrect_count]

        plt.bar(labels, counts, color=['green', 'red'])
        plt.xlabel('Results')
        plt.ylabel('Count')
        plt.title(f'{user.name}\'s Test Results - Level: {user.level}')
        plt.show()

def main():
    users = []
    test = LanguageTest()
    
    # Añadir preguntas según los niveles MCER
    nivel_A1 = [
        "¿Puedes decir qué hora es?",
        "¿Puedes describir un objeto que ves?",
        "¿Puedes pedir ayuda para encontrar algo?",
        "¿Puedes decir qué te gusta hacer?",
        "¿Puedes describir a alguien que conoces?"
    ]
    nivel_A2 = [
        "¿Puedes describir un lugar que has visitado?",
        "¿Puedes explicar qué te gusta hacer en tu tiempo libre?",
        "¿Puedes pedir ayuda para encontrar un lugar en una ciudad desconocida?",
        "¿Puedes describir a alguien que te gusta?",
        "¿Puedes explicar qué es lo que te gusta comer?"
    ]
    nivel_B1 = [
        "¿Puedes describir un proceso o una actividad que has realizado?",
        "¿Puedes explicar tus preferencias y opiniones sobre algo?",
        "¿Puedes describir un lugar que has visitado y qué te gustó de él?",
        "¿Puedes pedir ayuda para encontrar un lugar en una ciudad desconocida y explicar por qué lo necesitas?",
        "¿Puedes describir a alguien que te gusta y qué te gusta de esa persona?"
    ]
    nivel_B2 = [
        "¿Puedes describir un proceso o una actividad que has realizado y explicar por qué lo hiciste?",
        "¿Puedes explicar tus preferencias y opiniones sobre algo y justificar tus razones?",
        "¿Puedes describir un lugar que has visitado y qué te gustó de él, y explicar por qué lo prefieres?",
        "¿Puedes pedir ayuda para encontrar un lugar en una ciudad desconocida y explicar por qué lo necesitas, y también ofrecer alternativas?",
        "¿Puedes describir a alguien que te gusta y qué te gusta de esa persona, y explicar por qué te gusta?"
    ]
    nivel_C1 = [
        "¿Puedes describir un proceso o una actividad que has realizado y explicar por qué lo hiciste, y también ofrecer consejos a alguien que quiera hacer lo mismo?",
        "¿Puedes explicar tus preferencias y opiniones sobre algo y justificar tus razones, y también ofrecer argumentos para respaldar tus opiniones?",
        "¿Puedes describir un lugar que has visitado y qué te gustó de él, y explicar por qué lo prefieres, y también ofrecer recomendaciones a alguien que quiera visitarlo?",
        "¿Puedes pedir ayuda para encontrar un lugar en una ciudad desconocida y explicar por qué lo necesitas, y también ofrecer alternativas y justificar tus razones?",
        "¿Puedes describir a alguien que te gusta y qué te gusta de esa persona, y explicar por qué te gusta, y también ofrecer consejos a alguien que quiera conocer a alguien como esa persona?"
    ]
    nivel_C2 = [
        "¿Puedes describir un proceso o una actividad que has realizado y explicar por qué lo hiciste, y también ofrecer consejos a alguien que quiera hacer lo mismo, y también justificar tus razones?",
        "¿Puedes explicar tus preferencias y opiniones sobre algo y justificar tus razones, y también ofrecer argumentos para respaldar tus opiniones, y también justificar tus razones?",
        "¿Puedes describir un lugar que has visitado y qué te gustó de él, y explicar por qué lo prefieres, y también ofrecer recomendaciones a alguien que quiera visitarlo, y también justificar tus razones?",
        "¿Puedes pedir ayuda para encontrar un lugar en una ciudad desconocida y explicar por qué lo necesitas, y también ofrecer alternativas y justificar tus razones, y también ofrecer consejos a alguien que quiera hacer lo mismo?",
        "¿Puedes describir a alguien que te gusta y qué te gusta de esa persona, y explicar por qué te gusta, y también ofrecer consejos a alguien que quiera conocer a alguien como esa persona, y también justificar tus razones?"
    ]

    while True:
        print("\nMenu:")
        print("1. Register User")
        print("2. Add Test Question")
        print("3. Evaluate User")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter user's name: ")
            language = input("Enter user's language: ")
            user = User(name, language)
            users.append(user)
            print(f"User {name} registered.")

        elif choice == "2":
            level = input("Enter the level (A1, A2, B1, B2, C1, C2): ")
            if level == "A1":
                for question in nivel_A1:
                    correct_answer = input(f"Enter the correct answer for '{question}': ")
                    test.add_question(question, correct_answer)
            elif level == "A2":
                for question in nivel_A2:
                    correct_answer = input(f"Enter the correct answer for '{question}': ")
                    test.add_question(question, correct_answer)
            elif level == "B1":
                for question in nivel_B1:
                    correct_answer = input(f"Enter the correct answer for '{question}': ")
                    test.add_question(question, correct_answer)
            elif level == "B2":
                for question in nivel_B2:
                    correct_answer = input(f"Enter the correct answer for '{question}': ")
                    test.add_question(question, correct_answer)
            elif level == "C1":
                for question in nivel_C1:
                    correct_answer = input(f"Enter the correct answer for '{question}': ")
                    test.add_question(question, correct_answer)
            elif level == "C2":
                for question in nivel_C2:
                    correct_answer = input(f"Enter the correct answer for '{question}': ")
                    test.add_question(question, correct_answer)
            else:
                print("Invalid level. Please try again.")

            print("Questions added.")

        elif choice == "3":
            name = input("Enter user's name for evaluation: ")
            user = next((u for u in users if u.name == name), None)
            if not user:
                print("User not found.")
                continue

            print("Answer the following questions:")
            user_answers = []
            for question in test.questions:
                answer = input(f"{question} ")
                user_answers.append(answer)

            level = test.evaluate(user_answers)
            user.update_level(level)
            print(f"{user.name}'s MCER level is: {user.level}")

            # Generar el gráfico de resultados
            test.generate_result_chart(user)

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
