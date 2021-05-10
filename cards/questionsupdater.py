class QuestionContainer:
    def __init__(self, question_id,
                 question_text,
                 question_group,
                 question_group_title,
                 answer_text,
                 answer_correct,
                 ):
        self.answer_text = []
        self.question_id = question_id
        self.question_text = question_text
        self.question_group = question_group
        self.question_group_title = question_group_title
        self.answer_text = []
        self.answer_text = answer_text
        self.answer_correct = answer_correct


class QuestionsUpdater:
    def __init__(self, file_path):

        question_text = ""
        question_group = ""
        question_group_title = ""
        answer_text = []
        answer_correct = []
        self.questions = []

        file = open(file_path, "r+")
        text = file.read()
        file.close()

        text = text[text.find("AMERICAN GOVERNMENT"):].splitlines()

        def append_question():
            self.questions.append(QuestionContainer(len(self.questions) + 1,
                                                    question_text[question_text.find(".") + 2:],
                                                    question_group[3:],
                                                    question_group_title.capitalize(),
                                                    tuple(answer_text),
                                                    tuple(answer_correct),
                                                    ))
            answer_text.clear()
            answer_correct.clear()

        for count, line in enumerate(text):

            if len(line) < 2:
                continue

            if (line[1].__eq__(".") or line[2].__eq__(".") or line[3].__eq__(".") or line[4].__eq__(".")) \
                    and not line[1:4].__contains__("U"):
                if len(answer_text) > 0:
                    append_question()
                question_text = line
                continue
            elif line[1].__eq__(":"):
                question_group = line
                continue
            elif not line[0].__eq__(".") and not line[0].__eq__("["):
                question_group_title = line
                continue

            if line[0].__eq__("."):
                answer_text.append(line[2:].strip())
                answer_correct.append(True)

        append_question()

# for q in QuestionsUpdater("uploads\\new_2.txt").questions:
#     print(q.question_id,
#               q.question_group_title,
#               q.question_group,
#               q.question_text,
#               q.answer_text,
#               q.answer_correct)
