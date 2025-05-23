# Generated by Django 5.2 on 2025-04-22 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('cover', models.ImageField(blank=True, null=True, upload_to='game_covers/')),
                ('rating', models.FloatField(default=0)),
                ('total_votes', models.IntegerField(default=0)),
                ('category', models.CharField(choices=[('Action', 'Action'), ('RPG', 'RPG'), ('Strategy', 'Strategy')], max_length=100)),
                ('direct_link', models.URLField(blank=True, null=True)),
                ('torrent_file', models.FileField(blank=True, null=True, upload_to='torrents/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='games.game')),
            ],
        ),
        migrations.CreateModel(
            name='GameFavorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'game')},
            },
        ),
        migrations.AddField(
            model_name='game',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_games', through='games.GameFavorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='games.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_games', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'game')},
            },
        ),
    ]
