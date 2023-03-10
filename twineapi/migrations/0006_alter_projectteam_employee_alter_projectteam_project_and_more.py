# Generated by Django 4.1.7 on 2023-03-08 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twineapi', '0005_alter_ticketflag_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectteam',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='number_of_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_members', to='twineapi.project'),
        ),
        migrations.AlterField(
            model_name='ticketflag',
            name='flag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twineapi.flag'),
        ),
        migrations.AlterField(
            model_name='ticketflag',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_flags', to='twineapi.ticket'),
        ),
    ]
