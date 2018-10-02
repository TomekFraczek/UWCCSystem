
import core.models.MemberModels
import core.models.TransactionModels
import core.models.fields.PrimaryKeyField
import core.models.fields.RFIDField
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('primary_key', core.models.fields.PrimaryKeyField.PrimaryKeyField(default=core.models.fields.PrimaryKeyField.make_id, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('rfid', core.models.fields.RFIDField.RFIDField(verbose_name='RFID')),
                ('picture', models.ImageField(default='Shaka.png', null=True, upload_to=core.models.MemberModels.get_profile_pic_upload_location, verbose_name='Profile Picture')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('date_expires', models.DateField()),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=100)),
                ('answer_phrase', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('requirements', models.TextField(verbose_name='Minimum Certification Requirements')),
            ],
        ),
        migrations.CreateModel(
            name='CustomDataField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('data_type', models.CharField(choices=[('rfid', '10 digit RFID'), ('text', 'String of any length'), ('string', 'Short string of up to 50 characters'), ('boolean', 'True/False value'), ('int', 'Integer value'), ('float', 'Float value'), ('choice', 'Short string selectable from a list')], max_length=20)),
                ('suffix', models.CharField(blank=True, default='', max_length=10)),
                ('required', models.BooleanField(default=False)),
                ('label', models.CharField(default='', max_length=30)),
                ('help_text', models.CharField(blank=True, default='', max_length=200)),
                ('choices', models.TextField(blank=True, default='None; No choices provided\nNope; Also not a choice', help_text="Must use this format to define choices!\nEach choice must be on it's own line, and consist of a short name (used internally), and a description (seen by the user). Name description pairs must be separated by a semicolon, and no semicolons are allowed in either the name or the description", max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('primary_key', core.models.fields.PrimaryKeyField.PrimaryKeyField(default=core.models.fields.PrimaryKeyField.make_id, primary_key=True, serialize=False)),
                ('rfid', models.CharField(max_length=10, unique=True)),
                ('status', models.IntegerField(choices=[(0, 'In Stock'), (1, 'Checked Out'), (2, 'Broken'), (3, 'Missing'), (4, 'Dormant'), (5, 'Removed')])),
                ('due_date', models.DateField(blank=True, default=None, null=True)),
                ('gear_data', models.CharField(max_length=2000)),
                ('checked_out_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Gear',
            },
        ),
        migrations.CreateModel(
            name='GearType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('data_fields', models.ManyToManyField(to='core.CustomDataField')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(choices=[('membership', 'membership quiz questions'), ('staffhood', 'stafhood quiz questions'), ('special', 'special questions for special purposes'), ('other', 'yeah, not sure. something else')], max_length=20)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('question_text', models.CharField(max_length=100)),
                ('error_message', models.CharField(max_length=100)),
                ('answers', models.ManyToManyField(to='core.Answer')),
                ('correct_answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Staffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exc_email', models.EmailField(max_length=255, unique=True, verbose_name='Official ExC Email')),
                ('autobiography', models.TextField(default='I am too lazy and lame to upload a bio!', verbose_name='Self Description of the staffer')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('primary_key', core.models.fields.PrimaryKeyField.PrimaryKeyField(default=core.models.fields.PrimaryKeyField.make_id, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Rental', (('CheckOut', 'Check Out'), ('CheckIn', 'Check In'), ('Inventory', 'In Stock'))), ('Admin Actions', (('Create', 'New Gear'), ('Delete', 'Remove Gear'), ('ReTag', 'Change Tag'), ('Break', 'Set Broken'), ('Fix', 'Set Fixed'), ('Override', 'Admin Change'))), ('Auto Updates', (('Missing', 'Gear Missing'), ('Expire', 'Gear Expiration')))], max_length=20)),
                ('comments', models.TextField(default='')),
                ('authorizer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='has_authorized', to=settings.AUTH_USER_MODEL, validators=[core.models.TransactionModels.validate_auth])),
                ('gear', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='has_checked_out', to='core.Gear', validators=[core.models.TransactionModels.validate_available])),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gear',
            name='geartype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.GearType'),
        ),
        migrations.AddField(
            model_name='gear',
            name='min_required_certs',
            field=models.ManyToManyField(to='core.Certification', verbose_name='Minimal Certifications Required for Rental'),
        ),
        migrations.AddField(
            model_name='department',
            name='stls',
            field=models.ManyToManyField(related_name='STLs_of', to='core.Staffer'),
        ),
        migrations.AddField(
            model_name='member',
            name='certifications',
            field=models.ManyToManyField(to='core.Certification'),
        ),
        migrations.AddField(
            model_name='member',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group'),
        ),
    ]
