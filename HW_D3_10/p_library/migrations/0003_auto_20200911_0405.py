# Generated by Django 3.1.1 on 2020-09-10 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('p_library', '0002_auto_20200910_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishers',
            name='name',
            field=models.CharField(default='NAME', max_length=150, verbose_name='Наименование издательства'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='p_library.publishers', verbose_name='Издательство'),
        ),
    ]
