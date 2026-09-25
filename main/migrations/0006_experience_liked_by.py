from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_achievements_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="liked_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="liked_experiences",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
