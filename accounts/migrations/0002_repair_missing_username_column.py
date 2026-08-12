from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.AddField(
                    model_name="account",
                    name="username",
                    field=models.CharField(max_length=10, unique=True),
                ),
            ],
            state_operations=[],
        ),
    ]
