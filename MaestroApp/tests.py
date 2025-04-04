from django.test import TestCase
from django.utils.timezone import now
from .models import MaestroInstrument, MaestroClass, MaestroLesson, MaestroAssignment, MaestroUser, \
    MaestroNotification, UserNotificationStatus
from django.utils.text import slugify
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class MaestroModelTests(TestCase):
    def setUp(self):
        self.instrument = MaestroInstrument.objects.create(instrument='violin')
        self.user = MaestroUser.objects.create(username='testuser', first_name='John', last_name='Doe')
        self.class_instance = MaestroClass.objects.create(
            title='Violin Masterclass', duration=10, instrument=self.instrument
        )
        self.lesson = MaestroLesson.objects.create(
            title='Violin Basics', duration=60, price=50.0, dt=now(), associated_class=self.class_instance
        )
        self.assignment = MaestroAssignment.objects.create(
            title='Practice Scales', text='Practice C major scale', date_due=now(), lesson=self.lesson
        )
        self.notification = MaestroNotification.objects.create(
            title='New Class Added', message='You have been added to a new class', notification_type='class_added'
        )

        self.class_instance.students.add(self.user)
        self.user.assignments.add(self.assignment)
        UserNotificationStatus.objects.create(user=self.user, notification=self.notification, is_read=False)

    def test_maestro_instrument_creation(self):
        self.assertEqual(str(self.instrument), 'Violin')

    def test_maestro_class_creation(self):
        self.assertEqual(str(self.class_instance), 'Violin Masterclass')
        self.assertEqual(self.class_instance.instrument, self.instrument)
        self.assertTrue(self.class_instance.students.filter(id=self.user.id).exists())

    def test_maestro_lesson_creation(self):
        self.assertEqual(str(self.lesson), 'Violin Basics')
        self.assertEqual(self.lesson.associated_class, self.class_instance)

    def test_maestro_assignment_creation(self):
        self.assertEqual(str(self.assignment), 'Practice Scales')
        self.assertEqual(self.assignment.lesson, self.lesson)
        self.assertTrue(self.user.assignments.filter(id=self.assignment.id).exists())

    def test_maestro_user_creation(self):
        self.assertEqual(str(self.user), 'John Doe')
        self.assertTrue(self.user.assignments.exists())

    def test_maestro_notification_creation(self):
        self.assertEqual(str(self.notification), '[class_added] New Class Added')
        self.assertTrue(UserNotificationStatus.objects.filter(user=self.user, notification=self.notification).exists())

    def test_maestro_slug_generation(self):
        self.assertEqual(self.class_instance.slug, 'violin-masterclass')
        self.assertEqual(self.lesson.slug, 'violin-basics')
        self.assertTrue(self.assignment.slug.startswith('practice-scales'))

    def test_mark_notification_as_read(self):
        user_notification = UserNotificationStatus.objects.get(user=self.user, notification=self.notification)
        user_notification.is_read = True
        user_notification.save()

        updated_notification = UserNotificationStatus.objects.get(user=self.user, notification=self.notification)
        self.assertTrue(updated_notification.is_read)






class MaestroClassModelTest(TestCase):
    def setUp(self):
        self.instrument = MaestroInstrument.objects.create(instrument="Guitar")
        self.teacher = MaestroUser.objects.create(username="teacher1", email="teacher@example.com")
        self.student = MaestroUser.objects.create(username="student1", email="student@example.com")

    def test_create_class_with_required_fields(self):
        mc = MaestroClass.objects.create(
            title="Beginner Guitar",
            duration=12,
            capacity=10,
            instrument=self.instrument
        )
        self.assertEqual(mc.title, "Beginner Guitar")
        self.assertEqual(mc.duration, 12)
        self.assertEqual(mc.capacity, 10)
        self.assertEqual(mc.instrument.instrument, "Guitar")
        self.assertTrue(mc.available)
        self.assertEqual(mc.slug, slugify("Beginner Guitar"))

    def test_slug_is_autogenerated(self):
        mc = MaestroClass.objects.create(
            title="My Custom Class!",
            duration=6,
            instrument=self.instrument
        )
        expected_slug = slugify("My Custom Class!")
        self.assertEqual(mc.slug, expected_slug)

    def test_slug_is_not_overwritten_if_exists(self):
        mc = MaestroClass.objects.create(
            title="Advanced Violin",
            duration=8,
            instrument=self.instrument,
            slug="custom-slug"
        )
        self.assertEqual(mc.slug, "custom-slug")

    def test_many_to_many_teachers_students(self):
        mc = MaestroClass.objects.create(
            title="Ensemble Workshop",
            duration=4,
            instrument=self.instrument
        )
        mc.teachers.add(self.teacher)
        mc.students.add(self.student)

        self.assertIn(self.teacher, mc.teachers.all())
        self.assertIn(self.student, mc.students.all())

        # Reverse relations
        self.assertIn(mc, self.teacher.teaching_classes.all())
        self.assertIn(mc, self.student.enrolled_classes.all())

    def test_default_capacity_and_is_group(self):
        mc = MaestroClass.objects.create(
            title="Solo Piano",
            duration=10,
            instrument=self.instrument
        )
        self.assertEqual(mc.capacity, 20)
        self.assertEqual(mc.is_group, False)

    def test_str_representation(self):
        mc = MaestroClass.objects.create(
            title="Jazz Improvisation",
            duration=8,
            instrument=self.instrument
        )
        self.assertEqual(str(mc), "Jazz Improvisation")


class MaestroLessonModelTest(TestCase):
    def setUp(self):
        self.instrument = MaestroInstrument.objects.create(instrument="Drums")
        self.associated_class = MaestroClass.objects.create(
            title="Drum Masterclass",
            duration=10,
            capacity=15,
            instrument=self.instrument
        )

    def test_create_lesson_with_required_fields(self):
        dt = timezone.now()
        lesson = MaestroLesson.objects.create(
            title="Snare Techniques",
            duration=90,
            is_group=True,
            price=50.000,
            dt=dt,
            associated_class=self.associated_class
        )
        self.assertEqual(lesson.title, "Snare Techniques")
        self.assertEqual(lesson.duration, 90)
        self.assertEqual(lesson.is_group, True)
        self.assertEqual(lesson.price, 50.000)
        self.assertEqual(lesson.dt, dt)
        self.assertEqual(lesson.associated_class, self.associated_class)
        self.assertEqual(lesson.slug, slugify("Snare Techniques"))

    def test_slug_is_autogenerated(self):
        lesson = MaestroLesson.objects.create(
            title="Groove Building",
            price=40.500,
            dt=timezone.now(),
            associated_class=self.associated_class
        )
        self.assertEqual(lesson.slug, slugify("Groove Building"))

    def test_slug_is_not_overwritten_if_exists(self):
        lesson = MaestroLesson.objects.create(
            title="Intro to Rhythms",
            slug="custom-slug",
            price=35.000,
            dt=timezone.now(),
            associated_class=self.associated_class
        )
        self.assertEqual(lesson.slug, "custom-slug")

    def test_default_duration_and_group(self):
        lesson = MaestroLesson.objects.create(
            title="Percussion Basics",
            price=20.000,
            dt=timezone.now(),
            associated_class=self.associated_class
        )
        self.assertEqual(lesson.duration, 60)
        self.assertEqual(lesson.is_group, False)

    def test_str_representation(self):
        lesson = MaestroLesson.objects.create(
            title="Latin Drumming",
            price=75.000,
            dt=timezone.now(),
            associated_class=self.associated_class
        )
        self.assertEqual(str(lesson), "Latin Drumming")



class MaestroAssignmentModelTest(TestCase):
    def setUp(self):
        self.instrument = MaestroInstrument.objects.create(instrument="Piano")
        self.associated_class = MaestroClass.objects.create(
            title="Piano Level 1",
            duration=10,
            instrument=self.instrument
        )
        self.lesson = MaestroLesson.objects.create(
            title="Chords Basics",
            price=45.000,
            dt=timezone.now(),
            associated_class=self.associated_class
        )

    def test_create_assignment_with_required_fields(self):
        due_date = timezone.now() + timezone.timedelta(days=7)
        assignment = MaestroAssignment.objects.create(
            title="Major Scales",
            text="Practice all major scales hands together.",
            date_due=due_date,
            lesson=self.lesson
        )
        self.assertEqual(assignment.title, "Major Scales")
        self.assertEqual(assignment.text, "Practice all major scales hands together.")
        self.assertEqual(assignment.date_due, due_date)
        self.assertEqual(assignment.lesson, self.lesson)
        self.assertEqual(assignment.slug, slugify("Major Scales"))
        self.assertFalse(assignment.attachment)

    def test_assignment_with_attachment(self):
        file = SimpleUploadedFile("scales.pdf", b"dummy content")
        assignment = MaestroAssignment.objects.create(
            title="Minor Scales",
            text="Practice all minor scales hands separately.",
            date_due=timezone.now() + timezone.timedelta(days=5),
            lesson=self.lesson,
            attachment=file
        )
        self.assertIsNotNone(assignment.attachment)
        self.assertTrue(assignment.attachment.name.startswith("assignments/"))

    def test_slug_is_autogenerated(self):
        assignment = MaestroAssignment.objects.create(
            title="Sight Reading",
            text="Daily 15-minute reading exercise.",
            date_due=timezone.now() + timezone.timedelta(days=3),
            lesson=self.lesson
        )
        expected_slug = slugify("Sight Reading")
        self.assertEqual(assignment.slug, expected_slug)

    def test_slug_uniqueness_with_collision(self):
        # First assignment with default slug
        MaestroAssignment.objects.create(
            title="Harmony Basics",
            text="Learn simple harmonic progressions.",
            date_due=timezone.now() + timezone.timedelta(days=2),
            lesson=self.lesson
        )
        second = MaestroAssignment.objects.create(
            title="Harmony Basics",
            text="Part 2 of harmony exploration.",
            date_due=timezone.now() + timezone.timedelta(days=4),
            lesson=self.lesson
        )
        self.assertTrue(second.slug.startswith(slugify("Harmony Basics")))
        self.assertNotEqual(second.slug, slugify("Harmony Basics"))

    def test_str_representation(self):
        assignment = MaestroAssignment.objects.create(
            title="Performance Prep",
            text="Prepare a solo piece for evaluation.",
            date_due=timezone.now() + timezone.timedelta(days=10),
            lesson=self.lesson
        )
        self.assertEqual(str(assignment), "Performance Prep")