from django.core.management.base import BaseCommand
from learning.models import Lesson


class Command(BaseCommand):
    help = 'Publish all available lessons'

    def add_arguments(self, parser):
        parser.add_argument(
            '--unpublish',
            action='store_true',
            help='Unpublish all lessons instead',
        )

    def handle(self, *args, **options):
        unpublish = options.get('unpublish', False)
        
        if unpublish:
            # Unpublish all lessons
            count = Lesson.objects.filter(is_published=True).update(is_published=False)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully unpublished {count} lesson(s)')
            )
        else:
            # Publish all lessons
            count = Lesson.objects.filter(is_published=False).update(is_published=True)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully published {count} lesson(s)')
            )
            
            # Show all published lessons
            all_lessons = Lesson.objects.all()
            self.stdout.write('\nPublished Lessons:')
            for lesson in all_lessons:
                status = '✓ Published' if lesson.is_published else '✗ Draft'
                self.stdout.write(f'  - {lesson.title} ({status})')
