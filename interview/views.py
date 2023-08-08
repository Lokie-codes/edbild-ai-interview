from django.shortcuts import render
from .models import Interview, Candidate, Question, Answer, Score, Feedback
from django.views import View
import openai
import requests
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest

openai.api_key = "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"


def convert_audio_to_text(request):
    audio = request.FILES.get("audio")
    # Check if the audio file exists and if it is in the supported format
    if audio is None:
        return "Audio file not found."
    supported_formats = [
        "m4a",
        "mp3",
        "webm",
        "mp4",
        "mpga",
        "wav",
        "mpeg",
        "ogg",
        "oga",
        "flac",
    ]
    if audio.name.split(".")[-1] not in supported_formats:
        return f"Invalid audio file format. Supported formats: {', '.join(supported_formats)}"

    try:
        response = openai.Audio.transcribe("whisper-1", audio)
        if response["text"]:
            transcription = response["text"].strip()
            return transcription
        else:
            return "No transcription available"
    except Exception as e:
        print("Error : ", e)
        return "Error occurred during audio transcription."


def gpt3_chat(message):
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content


def question_generation(role, itr):
    if itr == 0:
        prompt = f"Generate an interview question for the role {role} that is about candidate's background and introduction."
    elif itr == 1:
        prompt = f"Generate an interview question for the role {role} that pertains to past work experience in the field."
    elif itr == 2:
        prompt = f"Generate an interview question for the role {role} about candidate's projects and achievements."
    elif itr == 3:
        prompt = f"Generate an technical question for the role {role}."
    else:
        prompt = f"Generate an interview question for the role {role} regarding the candidate's future outlook for taking a job in this role."
    content = gpt3_chat(prompt)
    if Question.objects.filter(content=content).exists():
        question = Question.objects.get(content=content)
    else:
        question = Question.objects.create(
            content=content, interview=Interview.objects.get(role=role)
        )
        question.save()
    return question


# Create your views here.


class CandidateView(View):
    def post(self, request):
        if not Candidate.objects.filter(name=request.POST.get("name")).exists():
            candidate_name = request.POST.get("name")
            candidate_email = request.POST.get("email")
            candidate_phone_number = request.POST.get("phone_number")
            candidate = Candidate.objects.create(
                name=candidate_name,
                email=candidate_email,
                phone_number=candidate_phone_number,
            )
            candidate.save()
        else:
            candidate_name = request.POST.get("name")
        candidate = Candidate.objects.get(name=candidate_name)
        return render(request, "interview/index.html", {"candidate": candidate})

    def get(self, request):
        return render(request, "interview/candidate.html")


class Index(TemplateView):
    template_name = "interview/index.html"


class InterviewView(View):
    def get(self, request):
        return render(request, "interview/interview.html")

    def post(self, request):
        role = request.POST.get("role")
        if not Interview.objects.filter(role=role).exists():
            interview = Interview.objects.create(role=role)
            interview.save()
            questions = []
            for i in range(5):
                question = question_generation(role, i)
                questions.append(question)
        else:
            interview = Interview.objects.get(role=role)
            questions = Question.objects.filter(interview=interview)
        return render(
            request,
            "interview/interview.html",
            {"questions": questions, "role": role},
        )


class AnswerView(View):
    def post(self, request):
        role = request.POST.get("role")
        if not Candidate.objects.filter(name=request.POST.get("name")).exists():
            candidate_name = request.POST.get("name")
            candidate_email = request.POST.get("email")
            candidate_phone_number = request.POST.get("phone_number")
            candidate = Candidate.objects.create(
                name=candidate_name,
                email=candidate_email,
                phone_number=candidate_phone_number,
            )
            candidate.save()
        else:
            candidate_name = request.POST.get("name")
        questions = Question.objects.filter(interview=Interview.objects.get(role=role))

        answers = []
        for question in questions:
            # print("Question : ", question)
            transcription = convert_audio_to_text(request)
            if isinstance(transcription, str):
                answer = Answer.objects.create(
                    transcription=transcription,
                    question=question,
                    candidate=Candidate.objects.get(name=candidate_name),
                )
                answer.save()
                answers.append(answer)
                # print("Answers are: ", answers)
            else:
                print("Error during audio transcription.", transcription)
        answer_pairs = zip(questions, answers)
        context = {
            "answer_pairs": answer_pairs,
        }
        return render(
            request,
            "interview/answer.html",
            context,
        )

    def get(self, request):
        return render(request, "interview/answer.html")
