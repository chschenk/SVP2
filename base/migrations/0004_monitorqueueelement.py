# Generated by Django 2.1.5 on 2019-01-16 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_funprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorQueueElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queued', models.DateTimeField(auto_now=True)),
                ('monitor_setting', models.CharField(choices=[('N', 'Nothing'), ('S', 'ShotImage'), ('P', 'ShotImageWithPoints'), ('A', 'EverythingAnonym'), ('E', 'Everything')], max_length=1)),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Sequence')),
            ],
        ),
    ]
