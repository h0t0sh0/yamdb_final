from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'USER'),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN'),
)

CODE_LENGTH = 64
PASSWORD_LENGTH = 256


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        username,
        email,
        password='',
        bio='',
        role='user',
        first_name='',
        last_name=''
    ):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            confirmation_code=self.make_random_password(length=CODE_LENGTH),
            password=password,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        user.email_user(
            subject='confirmation_code',
            message=user.confirmation_code,
            fail_silently=False
        )

        return user

    def create_superuser(
        self,
        username,
        email,
        password=None,
        bio='',
        role='admin',
        first_name='',
        last_name=''
    ):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            bio=bio,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        primary_key=True
    )
    email = models.EmailField(
        'Email',
        unique=True,
    )
    bio = models.TextField(
        'Bio',
        blank=True
    )
    role = models.CharField(
        'Role',
        max_length=16,
        choices=ROLE_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Confirmation code',
        max_length=CODE_LENGTH
    )
    password = models.CharField(
        'Password',
        max_length=PASSWORD_LENGTH,
        blank=True
    )

    objects = CustomUserManager()

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_staff or self.is_superuser:
            return True
        return False

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    class Meta:
        ordering = ['-date_joined']


class Genre(models.Model):
    name = models.TextField(
        'Genre',
        help_text='Enter genre'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ['-name']


class Category(models.Model):
    name = models.TextField(
        'Category',
        help_text='Enter category'
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ['-name']


class Title(models.Model):
    name = models.TextField(
        'Title',
        help_text='Enter title'
    )
    year = models.PositiveSmallIntegerField(
        help_text='Enter the year of publication'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title',
        verbose_name='Category'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField(
        'Description',
        help_text='Enter description',
        null=True,
        blank=True

    )

    class Meta:
        ordering = ['-year']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_title'),
        ]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True
    )

    text = models.TextField(
        'Post text',
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField(
        'Текст поста',
    )

    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
