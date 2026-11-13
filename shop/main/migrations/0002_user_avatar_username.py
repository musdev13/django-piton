from django.db import migrations, models


def fill_usernames(apps, schema_editor):
    User = apps.get_model('main', 'User')
    for user in User.objects.all():
        base = user.email.split('@')[0] if user.email else f'user{user.pk}'
        base = base or f'user{user.pk}'
        username = base
        i = 1
        while User.objects.filter(username=username).exclude(pk=user.pk).exists():
            i += 1
            username = f'{base}{i}'
        user.username = username
        user.save(update_fields=['username'])


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(old_name='AppUser', new_name='User'),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.RunPython(fill_usernames, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
