# Generated by Django 4.2.21 on 2025-05-13 05:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIHandler',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='generated_audio/')),
                ('original_request', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
