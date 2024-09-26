from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все публикации из конкретной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.write(f'Список всех существующих категорий {[cat for cat in Category.objects.all()]}')
        self.stdout.write(f'Do you really want to delete all products in {options['category']} ? yes/no')
        answer = input()

        if answer == 'yes':
            try:
                category = Category.objects.get(category_name=options['category'])
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Succesfully deleted all posts from category {category.category_name}'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {options['category']}'))
            return

        self.stdout.write(self.style.ERROR('Отмена команды'))