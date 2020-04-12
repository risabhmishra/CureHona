# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

def user_directory_path(instance,filename):

    return '{}/Images/{}'.format(instance.fk_user.username,filename)

class Images(models.Model):
    pk_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=user_directory_path)
    fk_model = models.ForeignKey('Models', models.DO_NOTHING, db_column='fk_model', blank=True, null=True)
    fk_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='fk_user', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class ImagesProperties(models.Model):
    pk_image_property = models.AutoField(primary_key=True)
    fk_image = models.ForeignKey('Images',models.DO_NOTHING,db_column='fk_image')
    fk_image_property_type = models.ForeignKey('ImagesPropertiesTypes', models.DO_NOTHING, db_column='fk_image_property_type', blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images_properties'


class ImagesPropertiesTypes(models.Model):
    pk_image_property_type = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'images_properties_types'


class PPECompliances(models.Model):
    pk_ppe_compliance = models.AutoField(primary_key=True)
    fk_image = models.ForeignKey('Images',models.DO_NOTHING,db_column='fk_image')
    result_image = models.CharField(max_length=255,blank=True)
    created = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'ppe_compliances'

class PPEComplianceProperties(models.Model):
    pk_ppe_compliance_property = models.AutoField(primary_key=True)
    fk_ppe_compliance = models.ForeignKey('PPECompliances',models.DO_NOTHING,db_column='fk_ppe_compliance',blank=True,null=True)
    fk_image_property_type = models.ForeignKey(ImagesPropertiesTypes, models.DO_NOTHING, db_column='fk_image_property_type', blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ppe_compliances_properties'

class Models(models.Model):
    pk_model = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'models'


class ModelsProperties(models.Model):
    pk_sn_model_property = models.AutoField(primary_key=True)
    fk_model = models.ForeignKey(Models, models.DO_NOTHING, db_column='fk_model', blank=True, null=True)
    fk_model_property_type = models.ForeignKey('ModelsPropertiesTypes', models.DO_NOTHING, db_column='fk_model_property_type', blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'models_properties'


class ModelsPropertiesTypes(models.Model):
    pk_model_property_type = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'models_properties_types'

class Users(models.Model):
    pk_user = models.AutoField(primary_key=True)
    customer_uid = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


