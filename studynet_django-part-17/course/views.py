from random import randint

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import serializers,generics

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Course, Lesson, Comment, Category, Quiz
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonListSerializer, CommentsSerializer, CategorySerializer, QuizSerializer, UserSerializer

@api_view(['POST'])
def create_course(request):
    status = request.data.get('status')
       
    
    print(request.data)
    print('status')
    print(status)

    # if status == 'published':
    #     status = 'draft'

    course = Course.objects.create(
        title=request.data.get('title'),
        slug='%s-%s' % (slugify(request.data.get('title')), randint(1000, 10000)),
        short_description=request.data.get('short_description'),
        long_description=request.data.get('long_description'),
        status=status,
        created_by=request.user
    )

    for id in request.data.get('categories'):
        course.categories.add(id)
    
    course.save()

    # Lessons

    for lesson in request.data.get('lessons'):
        type = lesson.get('lesson_type')
        if(type == 'article'):
            type = Lesson.ARTICLE
        elif(type == 'quiz'):
            type = Lesson.QUIZ
        elif (type == 'video'):
            type = Lesson.VIDEO
        
        tmp_lesson = Lesson.objects.create(
            course=course,
            title=lesson.get('title'),
            slug='%s-%s' % (slugify(lesson.get('title')), randint(1000, 10000)),
            short_description=lesson.get('short_description'),
            long_description=lesson.get('long_description'),
            status=Lesson.DRAFT,
            lesson_type = type,
            youtube_id=lesson.get('youtube_id')
        )
        if(type == Lesson.QUIZ):
            quiz = lesson.get('quiz')
            Quiz.objects.create(
                lesson = tmp_lesson,
                question = quiz.get('question'),
                answer = quiz.get('answer'),
                op1 = quiz.get('op1'),
                op2 = quiz.get('op2'),
                op3 = quiz.get('op3')
            )


    return Response({'course_id': course.id})

@api_view(['PUT'])
def edit_course(request,id):
    print("yeah")
    # print(request.data)
    print("pk")
    # print(pk)
    print("yeah course")
    print(id)
    course = Course.objects.get(id=id)
    course.title=request.data.get('title')
    course.short_description=request.data.get('short_description')
    course.long_description=request.data.get('long_description')
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)
    #v2
    if lesson_serializer is not None:
        for item in lesson_serializer.data:
            lesson = Lesson.objects.get(id=item['id'])
            lesson.delete()
        
        for lesson in request.data.get('lessons'):
            type = lesson.get('lesson_type')
            if(type == 'article'):
                type = Lesson.ARTICLE
            elif(type == 'quiz'):
                type = Lesson.QUIZ
            elif (type == 'video'):
                type = Lesson.VIDEO
            
            tmp_lesson = Lesson.objects.create(
                course=course,
                title=lesson.get('title'),
                slug=slugify(lesson.get('title')),
                short_description=lesson.get('short_description'),
                long_description=lesson.get('long_description'),
                status=Lesson.DRAFT,
                lesson_type = type,
                youtube_id=lesson.get('youtube_id')
            )
            if(type == Lesson.QUIZ):
                quiz = lesson.get('quiz')
                Quiz.objects.create(
                    lesson = tmp_lesson,
                    question = quiz.get('question'),
                    answer = quiz.get('answer'),
                    op1 = quiz.get('op1'),
                    op2 = quiz.get('op2'),
                    op3 = quiz.get('op3')
                )

    # v1
    # newlesson = request.data.get('lessons')
    # print("newlesson")
    # print(newlesson)
    # print("lesson_serializer")
    # print(lesson_serializer.data)
    # if(lesson_serializer is not None):
    #     for index,item in enumerate(lesson_serializer.data):
    #         selected = next((l for l in newlesson if l["id"] == item["id"]), False)
    #         print("selected")
    #         print(selected)
    #         print("item")
    #         print(item)
    #         if (selected):
    #             item = Lesson.objects.get(id=selected['id'])
    #             if(item is not None):
    #                 newtype = selected['lesson_type']
    #                 if(newtype == 'article'):
    #                     newtype = Lesson.ARTICLE
    #                 elif(newtype == 'quiz'):
    #                     newtype = Lesson.QUIZ
    #                 elif (newtype == 'video'):
    #                     newtype = Lesson.VIDEO
    #                 type = newtype
    #                 if(type == Lesson.QUIZ):
    #                     selectedQuiz = selected['quiz']
    #                     quiz = Quiz.objects.get(id=selectedQuiz['id'])
    #                     if quit is not None:
    #                         quiz.answer = selectedQuiz['answer']
    #                         quiz.op1 = selectedQuiz['op1']
    #                         quiz.op2 = selectedQuiz['op2']
    #                         quiz.op3 = selectedQuiz['op3']
    #                         quiz.question = selectedQuiz['question']
    #                         quiz.save()
    #                     else :
    #                         Quiz.objects.create(
    #                             lesson = item,
    #                             question = selectedQuiz['question'],
    #                             answer = selectedQuiz['answer'],
    #                             op1 = selectedQuiz['op1'],
    #                             op2 = selectedQuiz['op2'],
    #                             op3 = selectedQuiz['op3']
    #                         )
                    
    #                 item.long_description = selected['long_description']
    #                 item.short_description= selected['short_description']
    #                 item.title = selected['title']
    #                 item.youtube_id = selected['youtube_id']
    #                 item.save()
    #             else:
    #                 type = selected['lesson_type']
    #                 if(type == 'article'):
    #                     type = Lesson.ARTICLE
    #                 elif(type == 'quiz'):
    #                     type = Lesson.QUIZ
                        
    #                 elif (type == 'video'):
    #                     type = Lesson.VIDEO
    #                 newlesson = Lesson.objects.create(
    #                     course=course,
    #                     title=selected['title'],
    #                     slug=slugify(selected['title']),
    #                     short_description=selected['short_description'],
    #                     long_description=selected['long_description'],
    #                     status=Lesson.PUBLISHED,
    #                     lesson_type = type,
    #                     youtube_id=selected['youtube_id']
    #                 )
    #                 if(type == Lesson.QUIZ):
    #                     Quiz.objects.create(
    #                             lesson = newlesson,
    #                             question = selectedQuiz['question'],
    #                             answer = selectedQuiz['answer'],
    #                             op1 = selectedQuiz['op1'],
    #                             op2 = selectedQuiz['op2'],
    #                             op3 = selectedQuiz['op3']
    #                     )
                    
    #         else:
    #             lesson = Lesson.objects.get(id=item["id"])
    #             lesson.delete()
    # else:
    #     print('abc')  
    # course.save()
    # # serializer = CourseListSerializer(course,data=request.data)
    # # serializer.save()
    # print(course)
    return Response()

@api_view(['DELETE'])
def delete_course(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    # serializer = CourseListSerializer(course,data=request.data)
    # serializer.save()
    return Response("Deleted")

@api_view(['GET'])
def get_quiz(request, course_slug, lesson_slug):
    print("\n\n\n\nget_quiz\n\n\n")
    print(request)
    print(course_slug)
    print(lesson_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)
    print(lesson)
    quiz = lesson.quizzes.first()
    print(quiz)
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_courses(request):
    category_id = request.GET.get('category_id', '')
    courses = Course.objects.filter(status=Course.PUBLISHED)

    if category_id:
        courses = courses.filter(categories__in=[int(category_id)])

    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_frontpage_courses(request):
    courses = Course.objects.filter(status=Course.PUBLISHED)[0:4]
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_course(request, slug):
    course = Course.objects.filter(status=Course.PUBLISHED).get(slug=slug)
    course_serializer = CourseDetailSerializer(course)
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)
    
    category = CategorySerializer(course)
    if request.user.is_authenticated:
        course_data = course_serializer.data
    else:
        course_data = {}

    return Response({
        'course': course_data,
        'lessons': lesson_serializer.data
    })

@api_view(['GET'])
def get_comments(request, course_slug, lesson_slug):
    lesson = Lesson.objects.get(slug=lesson_slug)
    serializer = CommentsSerializer(lesson.comments.all(), many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_comment(request, course_slug, lesson_slug):
    data = request.data
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)

    comment = Comment.objects.create(course=course, lesson=lesson, name=data.get('name'), content=data.get('content'), created_by=request.user)

    serializer = CommentsSerializer(comment)

    return Response(serializer.data)

@api_view(['GET'])
def get_author_courses(request, user_id):
    user = User.objects.get(pk=user_id)
    courses = user.courses.filter(status=Course.PUBLISHED)

    user_serializer = UserSerializer(user, many=False)
    courses_serializer = CourseListSerializer(courses, many=True)

    return Response({
        'courses': courses_serializer.data,
        'created_by': user_serializer.data
    })