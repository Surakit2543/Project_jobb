from random import randint
from django.conf import settings
from django.http import FileResponse

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import serializers,generics

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Course, Lesson, Comment, Category, Quiz, File
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonListSerializer, CommentsSerializer, CategorySerializer, QuizSerializer, UserSerializer, FileSerializer
import json
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
        created_by=request.user,
        image=request.FILES.get('image')
    )

    for id in request.data.get('categories'):
        course.categories.add(id)
    
    course.save()

    # Lessons
    lessons_json = request.POST.get('lessons', '[]')
    lessons = json.loads(lessons_json)

    for lesson in lessons:
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
    print("yeah course")
    print(id)
    print(request.data)
    print(request.FILES.get('image'))
    course = Course.objects.get(id=id)
    course.title=request.data.get('title')
    course.short_description=request.data.get('short_description')
    course.long_description=request.data.get('long_description')
    if(request.FILES.get('image') is not None):
        course.image=request.FILES.get('image')
    course.save()
    lesson_serializer = LessonListSerializer(course.lessons.all(), many=True)
    #v2
    print("lesson_serializer")
    if lesson_serializer is not None and len(lesson_serializer.data) > 0:
        print('lesson_serializer is not none ')
        print(lesson_serializer.data)
        for item in lesson_serializer.data:
            print("item")
            print(item)
            lesson = Lesson.objects.get(id=item['id'])
            lesson.delete()
        
    print('\n\nlessons\n\n')
    print(request.data.get('lessons'))
    lessons_json = request.POST.get('lessons', '[]')
    lessons = json.loads(lessons_json)

    if lessons is not None:
        for lesson in lessons:
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
def get_my_courses(request):
    print('\n\n\n\n\nget_my_courses\n\n\n\n\n')
    print(request.user)
    courses = Course.objects.filter(status=Course.PUBLISHED)
    courses = courses.filter(created_by=request.user)
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

@api_view(['POST'])
def create_file(request):
    file = File.objects.create(
        name = request.data.get('name'),
        file = request.FILES.get('file'),
        description = request.data.get('description')
    )
    file.save()
    return Response({'save': 'Success'})

@api_view(['PUT'])
def edit_file(request,id):
    file = File.objects.get(id=id)
    file.name = request.data.get('name')
    file.description = request.data.get('description')
    file.save()
    return Response('Edit Success')


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_file(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_file(request,id):
    file = File.objects.get(id=id)
    file.delete()
    return Response("Deleted")

api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def downloadFile(request,id):
    file = File.objects.get(id=id)
    file_path = file.file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response
