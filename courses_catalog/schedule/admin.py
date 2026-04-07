from django.contrib import admin
from .models import Teacher, TeacherInfo, Course, Student


class TeacherInfoInline(admin.StackedInline):
    model = TeacherInfo
    can_delete = False
    verbose_name = "Информация о преподавателе"
    verbose_name_plural = "Информация о преподавателях"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'email', 'hire_date', 'is_active']
    list_filter = ['is_active', 'hire_date']
    search_fields = ['last_name', 'first_name', 'patronymic', 'email']
    inlines = [TeacherInfoInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('last_name', 'first_name', 'patronymic', 'email', 'phone')
        }),
        ('Статус и даты', {
            'fields': ('hire_date', 'is_active')
        }),
    )


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'degree', 'specialization', 'years_of_experience']
    list_filter = ['degree']
    search_fields = ['teacher__last_name', 'teacher__first_name', 'specialization']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'level', 'credits', 'start_date', 'is_active']
    list_filter = ['level', 'is_active', 'teacher']
    search_fields = ['title', 'description']
    # Для связи 1:N используем обычный выпадающий список
    raw_id_fields = ['teacher']  # Опционально: для удобства поиска при большом количестве


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'email', 'enrollment_date', 'is_active']
    list_filter = ['is_active', 'enrollment_date']
    search_fields = ['last_name', 'first_name', 'patronymic', 'email']
    filter_horizontal = ['courses']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('last_name', 'first_name', 'patronymic', 'email', 'phone')
        }),
        ('Личные данные', {
            'fields': ('date_of_birth', 'address')
        }),
        ('Обучение', {
            'fields': ('courses', 'is_active')
        }),
    )