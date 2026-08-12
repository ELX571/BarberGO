# Generated manually to add Comment after the field rename.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_username'),
        ('base', '0001_initial'),
        ('posts', '0002_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.basemodel')),
                ('text', models.TextField()),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='accounts.account')),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=('base.basemodel',),
        ),
    ]
