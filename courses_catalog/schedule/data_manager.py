# schedule/data_manager.py
from catalog.data import courses, authors

class DataManager:
    """Класс для управления данными из catalog.data"""
    
    @staticmethod
    def get_all_teachers():
        """Получить всех преподавателей (авторов)"""
        return authors
    
    @staticmethod
    def get_teacher_by_id(teacher_id):
        """Получить преподавателя по ID"""
        for author in authors:
            if author['id'] == teacher_id:
                return author
        return None
    
    @staticmethod
    def get_all_courses():
        """Получить все курсы"""
        return courses
    
    @staticmethod
    def get_course_by_id(course_id):
        """Получить курс по ID"""
        for course in courses:
            if course['id'] == course_id:
                return course
        return None
    
    @staticmethod
    def get_courses_for_teacher(teacher_id):
        """Получить курсы, которые ведет преподаватель"""
        teacher_courses = []
        for course in courses:
            if teacher_id in course['author_id']:
                teacher_courses.append(course)
        return teacher_courses
    
    @staticmethod
    def get_teachers_for_course(course_id):
        """Получить преподавателей, которые ведут курс"""
        course = DataManager.get_course_by_id(course_id)
        if not course:
            return []
        
        course_teachers = []
        for teacher_id in course['author_id']:
            teacher = DataManager.get_teacher_by_id(teacher_id)
            if teacher:
                course_teachers.append(teacher)
        return course_teachers
    
    @staticmethod
    def add_teacher(teacher_data):
        """Добавить нового преподавателя"""
        new_id = max([author['id'] for author in authors]) + 1
        new_teacher = {
            'id': new_id,
            'name': teacher_data['full_name'],
            'bio': teacher_data.get('bio', ''),
            'specialization': teacher_data.get('specialization', '')
        }
        authors.append(new_teacher)
        return new_teacher