from django.test import TestCase
from django.utils.timezone import now
from .models import MaestroInstrument, MaestroClass, MaestroLesson, MaestroAssignment, MaestroUser, \
    MaestroNotification


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
        self.notification.users.add(self.user)

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
        self.assertTrue(self.notification.users.filter(id=self.user.id).exists())

    def test_maestro_slug_generation(self):
        self.assertEqual(self.class_instance.slug, 'violin-masterclass')
        self.assertEqual(self.lesson.slug, 'violin-basics')
        self.assertEqual(self.assignment.slug.startswith('practice-scales'), True)

    def test_mark_notification_as_read(self):
        self.notification.mark_as_read(self.user)
        self.assertFalse(self.notification.users.filter(id=self.user.id).exists())
