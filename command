Файл с описанием команд по заданию
_____________________________
#создала миграци
python manage.py makemigrations

#применила миграции
python manage.py migrate

#перешла в shell
python manage.py shell

#импортировала все модели из models.py
from news.models import *

#создала двух пользователей (с помощью метода User.objects.create_user('username'))
u1 = User.objects.create_user(username='Kristina')
u2 = User.objects.create_user(username='Sergey')

#cоздала два объекта модели Author, связанные с пользователями u1 и u2
a1 = Author.objects.create(name=u1)
a2 = Author.objects.create(name=u2)

#добавила 4 категории в модель Category
cat1 = Category.objects.create(category_name='Политика')
cat2 = Category.objects.create(category_name='Спорт')
cat3 = Category.objects.create(category_name='Экономика')
cat4 = Category.objects.create(category_name='Общество')

#добавила 2 статьи и 1
art1 = Post.objects.create(author=a1, heading='Политическая статья', text='Тут что-то о политике')
art2 = Post.objects.create(author=a2, heading='Экономическая статья', text='Тут что-то об экономике')
news1 = Post.objects.create(type='NW', author=a2, heading='Срочная новость!', text='Тут что-то о недавнем происшествии в обществе')

#присвоила категории постам(как минимум в одной статье/новости должно быть не меньше 2 категорий).
art1.category.add(cat1)
art1.category.add(cat4)
art2.category.add(cat3)
art2.category.add(cat2)
news1.category.add(cat4)
news1.category.add(cat3)

#cоздала 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
с1 = Comment.objects.create(post=art1, user=u1, text='Политика это так скучно')
с2 = Comment.objects.create(post=art2, user=u2, text='Опять повысили ключевую ставку!?')
с3 = Comment.objects.create(post=news1, user=u2, text='Ну и дела...')
с4 = Comment.objects.create(post=news1, user=u1, text='Вот это новости! Как здорово)')

#применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировала рейтинги этих объектов.
art1.like()
art1.dislike()
art1.dislike()
art2.like()
art2.like()
news1.like()
news1.like()
news1.like()
_____________
с1.like()
с1.like()
с2.like()
с3.dislike()
с4.like()
с4.like()

#обновила рейтинги пользователей
a1.update_rating()
a2.update_rating()


#вывела username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.order_by('-rating').values('name__username', 'rating').first()

#вывела дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_post = Post.objects.order_by('-rating')
best_post.values('author__name__username', 'rating', 'heading').first()
best_post.first().preview()

#вывела все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
best_post.first().comment_set.all().values('creation_time', 'user__username', 'rating', 'text')
