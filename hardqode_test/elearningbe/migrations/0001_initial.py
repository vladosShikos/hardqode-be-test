# Generated by Django 4.2.3 on 2023-09-26 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('length_in_seconds', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProductLessonHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatch_time', models.IntegerField(default=0)),
                ('been_watched', models.BooleanField(default=False)),
                ('last_watch_date', models.DateTimeField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearningbe.lesson')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearningbe.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearningbe.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_acquired', models.DateTimeField()),
                ('valid_thru', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearningbe.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearningbe.user')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='owners',
            field=models.ManyToManyField(through='elearningbe.ProductAccessToken', to='elearningbe.user'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='accessable_to',
            field=models.ManyToManyField(through='elearningbe.UserProductLessonHistory', to='elearningbe.user'),
        ),
    ]
