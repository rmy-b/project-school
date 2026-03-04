from django.db import models
from users.models import CustomUser 
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint,Q


class Class(models.Model):
    class_code = models.CharField(max_length=10, unique=True, editable=False)
    class_name = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.class_code:
            last_class = Class.objects.all().order_by('id').last()
            if last_class:
                last_id = int(last_class.class_code.replace('C', ''))
                new_code = f"C{last_id + 1:02d}"
            else:
                new_code = "C01"
            self.class_code = new_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_code} - {self.class_name}"


class Section(models.Model):
    section_name = models.CharField(max_length=5)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
 
    class Meta:
        unique_together = ('section_name', 'class_obj')
    

    def __str__(self):
        return f"{self.class_obj.class_name} - {self.section_name}"



class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True, editable=False)
    subject_name = models.CharField(max_length=50)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.subject_code:
            last_subject = Subject.objects.all().order_by('id').last()
            if last_subject:
                last_id = int(last_subject.subject_code.replace('SUB', ''))
                new_code = f"SUB{last_id + 1:02d}"
            else:
                new_code = "SUB01"
            self.subject_code = new_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"



class Student(models.Model):
    student_code = models.CharField(max_length=10, unique=True, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,limit_choices_to={'role':'student'})
    roll_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    joining_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.section.class_obj!=self.class_obj:
            raise ValidationError("Selected Section Does Not Belong To Selected Class.")

    def save(self, *args, **kwargs):
        if not self.student_code:
            last_student = Student.objects.all().order_by('id').last()
            if last_student:
                last_id = int(last_student.student_code.replace('STU', ''))
                new_code = f"STU{last_id + 1:02d}"
            else:
                new_code = "STU01"
            self.student_code = new_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_code} - {self.name} -  {self.class_obj.class_name}{self.section.section_name}"
    

class Faculty(models.Model):
    faculty_code = models.CharField(max_length=10, unique=True, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'faculty'}
    )
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.faculty_code:
            last_faculty = Faculty.objects.all().order_by('id').last()
            if last_faculty:
                last_id = int(last_faculty.faculty_code.replace('FAC', ''))
                new_code = f"FAC{last_id + 1:02d}"
            else:
                new_code = "FAC01"
            self.faculty_code = new_code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.faculty_code} - {self.name}"
    

class FacultyAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    is_class_incharge = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            # 1. Same subject cannot be assigned twice for same class+section
            UniqueConstraint(
                fields=['subject', 'class_obj', 'section'],
                name='unique_subject_per_class'
            ),

            # 2. Same faculty cannot teach two subjects in same class+section
            UniqueConstraint(
                fields=['faculty', 'class_obj', 'section'],
                name='faculty_one_subject_per_class'
            ),

            # 3. Only ONE class teacher per class+section
            UniqueConstraint(
                fields=['class_obj', 'section'],
                condition=Q(is_class_incharge=True),
                name='only_one_class_incharge_per_section'
            ),
        ]
    def clean(self):
        if self.section.class_obj != self.class_obj:
            raise ValidationError("Selected Section Does Not Belong To Selected Class.")
    def __str__(self):
        return f"{self.faculty.name} - {self.subject.subject_name} - {self.class_obj.class_name}{self.section.section_name}"



class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.get_status_display()}"


class Exam(models.Model):
    exam_name = models.CharField(max_length=100)

    def __str__(self):
        return self.exam_name
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    internal_marks = models.FloatField()
    external_marks = models.FloatField()
    total_marks = models.FloatField(editable=False)

    class Meta:
        unique_together = ('student', 'subject', 'exam')

    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.external_marks
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.exam.exam_name}"
