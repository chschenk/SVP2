# Generated by Django 2.1.3 on 2018-12-07 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
        ('competition', '0002_auto_20181201_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_number', models.PositiveIntegerField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.Competition')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
            ],
        ),
        migrations.RemoveField(
            model_name='pricerecord',
            name='member',
        ),
        migrations.RemoveField(
            model_name='pricerecord',
            name='recordId',
        ),
        migrations.AlterField(
            model_name='weapon',
            name='current_record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='competition.CompetitionRecord'),
        ),
        migrations.AddField(
            model_name='pricerecord',
            name='competition_record',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='competition.CompetitionRecord'),
            preserve_default=False,
        ),
    ]
