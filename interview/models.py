from django.db import models


class Interview(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    content = models.TextField()
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Answer(models.Model):
    transcription = models.TextField(null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        if self.transcription:
            return f"Answer: {self.transcription[:50]}..."
        return f"Answer for Question ID: {self.question_id} (No transcription provided)"


class Score(models.Model):
    score = models.IntegerField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.score


class Feedback(models.Model):
    feedback = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.feedback
