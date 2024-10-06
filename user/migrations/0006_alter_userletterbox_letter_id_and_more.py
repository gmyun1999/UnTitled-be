# Generated by Django 5.0.6 on 2024-10-06 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lucky_letter", "0006_rename_stamp_letter_stamp_id"),
        ("user", "0005_rename_letter_userletterbox_letter_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userletterbox",
            name="letter_id",
            field=models.ForeignKey(
                db_constraint=False,
                max_length=36,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="lucky_letter.letter",
            ),
        ),
        migrations.AlterField(
            model_name="userletterbox",
            name="user_id",
            field=models.ForeignKey(
                db_constraint=False,
                max_length=36,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="user.user",
            ),
        ),
        migrations.AlterField(
            model_name="userrelation",
            name="from_id",
            field=models.ForeignKey(
                db_constraint=False,
                max_length=36,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="user.user",
            ),
        ),
        migrations.AlterField(
            model_name="userrelation",
            name="to_id",
            field=models.ForeignKey(
                db_constraint=False,
                max_length=36,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="user.user",
            ),
        ),
    ]
