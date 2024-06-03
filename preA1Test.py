import matplotlib.pyplot as plt

class PreA1Test:
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

        if percentage >= 50:
            return "Pass"
        else:
            return "Fail"

    def generate_result_chart(self):
        labels = ['Correct', 'Incorrect']
        counts = [self.correct_count, self.incorrect_count]

        plt.bar(labels, counts, color=['green', 'red'])
        plt.xlabel('Results')
        plt.ylabel('Count')
        plt.title('User Test Results')
        plt.show()

def main():
    test = PreA1Test()
    
    # Añadir algunas preguntas de ejemplo
    test.add_question("What color is the sky on a clear day?", "Blue")
    test.add_question("What is 2 + 2?", "4")
    test.add_question("How do you say 'cat' in Spanish?", "gato")
    test.add_question("¿Puedes decir tu nombre y dónde vives?", "si")
    test.add_question("¿Puedes describir a alguien que conoces?", "si")
    test.add_question("¿Puedes explicar qué te gusta hacer en tu tiempo libre?", "si")
    test.add_question("¿Puedes pedir ayuda para encontrar algo en una tienda?", "si")
    test.add_question("¿Puedes describir cómo te sientes cuando te duele la cabeza?", "si")
    test.add_question("¿Puedes decir adónde vas a ir hoy?", "si")
    test.add_question("¿Puedes explicar qué es lo que te gusta comer?", "si")
    test.add_question("¿Puedes pedir ayuda para encontrar un lugar en una ciudad desconocida?", "si")
    test.add_question("¿Puedes describir a alguien que te gusta?", "si")
    test.add_question("¿Puedes explicar qué es lo que te gusta hacer en tu tiempo libre?", "si")

    while True:
        print("\nMenu:")
        print("1. Add Test Question")
        print("2. Evaluate User")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            question = input("Enter the question: ")
            correct_answer = input("Enter the correct answer: ")
            test.add_question(question, correct_answer)
            print("Question added.")

        elif choice == "2":
            user_answers = []
            for question in test.questions:
                answer = input(f"{question} ")
                user_answers.append(answer)

            # Asegurarse de que el usuario ha respondido a todas las preguntas
            if len(user_answers) == len(test.questions):
                result = test.evaluate(user_answers)
                print(f"Evaluation result: {result}")

                # Generar el gráfico de resultados solo si todas las preguntas han sido respondidas
                test.generate_result_chart()
                break
            else:
                print("You did not answer all the questions. Please answer all the questions.")

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
