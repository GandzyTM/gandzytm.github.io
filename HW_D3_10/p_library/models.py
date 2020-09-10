from django.db import models


# Create your models here.

class Author(models.Model):
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()
    country = models.TextField()

    def __str__(self):
        return self.full_name


class Publishers(models.Model):
    name = models.CharField(max_length=150, default="NAME", verbose_name="Наименование издательства")

    def __str__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=13, verbose_name="Международный стандартный книжный номер")
    title = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    year_release = models.SmallIntegerField(verbose_name="Год издания")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    copy_count = models.SmallIntegerField(verbose_name="Количество копий")
    price = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Цена")
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE, null=True, blank=True, related_name='books', verbose_name="Издательство")

    def __str__(self):
        return self.title
