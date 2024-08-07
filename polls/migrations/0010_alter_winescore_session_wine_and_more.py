# Generated by Django 4.2.7 on 2024-07-28 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_populate_session_wine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winescore',
            name='session_wine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.sessionwine'),
        ),
        migrations.AlterUniqueTogether(
            name='winescore',
            unique_together={('user_score', 'session_wine')},
        ),
        migrations.RemoveField(
            model_name='winescore',
            name='wine',
        ),
    ]
