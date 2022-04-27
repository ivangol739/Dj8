import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student
from rest_framework.reverse import reverse
from random import randint
import json


url = '/api/v1/courses/'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, students_factory, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=10)
    # Act
    response = client.get(f'{url}5/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 5


@pytest.mark.django_db
def test_get_course_list(client, students_factory, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=5)
    # Act
    response = client.get(url)
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_id(client, students_factory, courses_factory):
    # Arrange
    id_count = len(Course.objects.all())
    course_for_test = Course.objects.create(id=id_count + 1, name='name_test1')
    courses = courses_factory(_quantity=10)
    # Act
    response = client.get(f'{url}?id={course_for_test.id}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course_for_test.id


@pytest.mark.django_db
def test_filter_name(client, students_factory, courses_factory):
    # Arrange
    course_for_test = Course.objects.create(name='name_test2')
    courses = courses_factory(_quantity=10)
    # Act
    response = client.get(f'{url}?name={course_for_test.name}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_for_test.name


@pytest.mark.django_db
def test_create(client, students_factory, courses_factory):
    # Arrange
    data = {
        'name': 'name_test3'
    }
    # Act
    response = client.post(url, data)
    # Assert
    assert response.status_code == 201
    assert Course.objects.get(name='name_test3').name == 'name_test3'


@pytest.mark.django_db
def test_update(client, students_factory, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=1)
    data = {
        'name': 'name_test4'
    }
    # Act
    response = client.patch(f'{url}{courses[0].id}/', data)
    # Assert
    assert response.status_code == 200
    assert Course.objects.get(id=courses[0].id).name == data['name']


@pytest.mark.django_db
def test_delete(client, students_factory, courses_factory):
    # Arrange
    courses = courses_factory(_quantity=1)
    # Act
    response = client.delete(f'{url}{courses[0].id}/')
    # Assert
    assert response.status_code == 204
    assert courses[0].id not in list(course.id for course in Course.objects.all())
