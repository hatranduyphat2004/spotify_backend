# Generated by Django 4.2.7 on 2025-04-03 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('cover_img_url', models.ImageField(blank=True, null=True, upload_to='albums/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('artist_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='artists/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ArtistAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artist')),
            ],
            options={
                'unique_together': {('artist', 'album')},
            },
        ),
        migrations.AddField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(related_name='albums', through='api.ArtistAlbum', to='api.artist'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('account_type', models.CharField(choices=[('free', 'Free'), ('premium', 'Premium')], default='free', max_length=20)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('profile_picture', models.ImageField(blank=True, upload_to='users/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
