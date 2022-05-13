# Generated by Django 4.0.3 on 2022-05-01 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resutlDate', models.DateTimeField(auto_now_add=True)),
                ('Keyword', models.TextField()),
                ('NumberOftweets', models.TextField()),
                ('FromDate', models.TextField()),
                ('ToDate', models.TextField()),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweetlID', models.BigIntegerField()),
                ('tweetUsername', models.CharField(max_length=100)),
                ('tweetNickname', models.TextField()),
                ('tweetText', models.TextField()),
                ('tweetDate', models.DateTimeField()),
                ('tweetLikes', models.IntegerField()),
                ('tweetRetweets', models.IntegerField()),
                ('tweetReplies', models.IntegerField()),
                ('tweetLocation', models.TextField()),
                ('tweetLink', models.TextField()),
                ('tweetLabel', models.IntegerField(default=5)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enSentiment.results')),
            ],
        ),
    ]
