# Generated by Django 4.2.7 on 2025-03-29 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="users",
            field=models.ManyToManyField(
                related_name="team_set",
                through="teams.TeamUsers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="teamusers",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team_users",
                to="teams.team",
            ),
        ),
        migrations.AlterField(
            model_name="teamusers",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team_relations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
