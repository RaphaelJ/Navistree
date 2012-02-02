#!/usr/bin/python2
#-*- coding: Utf-8 -*-

import datetime, random, os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

import settings

path_validator = RegexValidator(r'^/[A–Za-z0–9_/-]{0,254}$')
domain_validator = RegexValidator(r'^[a-z][a-z0-9-]{1,61}[a-z0-9]\.[a-z]{2,6}$')
host_validator = RegexValidator(r'^(?:\*|[a-z][a-z0-9-]{1,61}[a-z0-9])$')

# ** USERS ***

class UserType(models.Model):
    name = models.CharField(max_length=255)
    disk_space = models.IntegerField(null=True) # null = unlimited
    traffic = models.IntegerField(null=True)
    domains = models.IntegerField(null=True)
    backups = models.IntegerField(null=True, default=24)
    max_db = models.IntegerField(null=True)
    max_db_size = models.IntegerField(null=True)
    max_db_connections = models.IntegerField(null=True)
    distant_db_user = models.BooleanField()

    class Meta:
        verbose_name = 'type d\'utilisateur'
        verbose_name_plural = 'types d\'utilisateurs'

    def __unicode__(self):
        return self.name

    @staticmethod
    def default():
        return UserType.objects.get(id=1)

class UserProfile(models.Model):
    """ doc. http://sontek.net/extending-the-django-user-model """
    user = models.OneToOneField(
        User, primary_key=True,  related_name="profiles"
    )
    
    basedir = models.CharField(
        verbose_name="dossier de l'utilisateur",
        max_length=255,
        help_text="Chemin vers le dossier personnel.",
        validators=[path_validator]
    )
    
    country = models.CharField(max_length=25)
    type = models.ForeignKey(UserType, null=True)#, default=UserType.default)

    email_after_operation = models.BooleanField(default=False)
    
    activation_key = models.BigIntegerField(
        null=True,
        default=lambda: random.getrandbits(63),
        db_index=True
    )
    activation_key_expire = models.DateTimeField(
        null=True,
        default=lambda: datetime.datetime.today() + \
            datetime.timedelta(hours=settings.REGISTER_DELAY)
    )

    class Meta:
        verbose_name = 'profil utilisateur'
        verbose_name_plural = 'profils utilisateurs'

    def activate(self):
        self.user.is_active = True
        self.user.save()

        self.activation_key = None
        self.activation_key_expire = None
        self.save()

    def __unicode__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def user_save(sender, instance, created, **args):
        if created:
            UserProfile.objects.get_or_create(user=instance)
            instance.is_active = False
            instance.save()

class UserChange(models.Model):
    USER_CHANGE_TYPES = (
        (u'NEW', u"Création d'un nouvel utilisateur"),
        (u'CHANGE', u"Modification d'un utilisateur"),
        (u'REMOVE', u"Supression d'un utilisateur"),
    )

    user = models.ForeignKey(
        User, related_name="changes", db_index=True
    )
    type = models.CharField(max_length=16, choices=USER_CHANGE_TYPES)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-id']

    @receiver(post_save, sender=User)
    def user_save(sender, instance, created, **args):
        if created:
            UserChange.objects.create(user=instance, type="NEW")
        #else:
            #UserChange.objects.create(user=instance, type="CHANGE")

# ** DOMAINS **

class DomainIcon(models.Model):
    path = models.CharField(
        verbose_name="icone du domaine",
        max_length=255,
        help_text="Chemin vers l'icone du domaine",
        validators=[path_validator],
        unique=True
    )

    class Meta:
        verbose_name = 'icone du domaine'
        verbose_name_plural = 'icônes des domaines'

    def __unicode__(self):
        return self.path

class Domain(models.Model):
    name = models.CharField(
        verbose_name="nom de domaine",
        max_length=70,
        unique=True,
        help_text="Nom de domaine sans préfixe (par ex. : navistree.org)",
        validators=[domain_validator]
    )
    
    creation = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User, related_name="domains", db_index=True
    )

    icon = models.ForeignKey(DomainIcon, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'domaine'
        verbose_name_plural = 'domaines'
        
        ordering = ['name']

    @property
    def icon_url(self):
        if self.icon == None:
            return settings.DOMAINS_ICONS_DIR + "/default.png"
        else:
            return settings.DOMAINS_ICONS_DIR + self.icon.path

    @property
    def ongoing_operation(self):
        return self.changes.filter(active=True).exists()

    def __unicode__(self):
        return "{0} => {1}".format(self.name, self.path)

class DomainChange(models.Model):
    DOMAIN_CHANGE_TYPES = (
        (u'NEW', u"Création d'un nouveau domaine"),
        (u'CHANGE', u"Modification d'un domaine"),
        (u'REMOVE', u"Supression d'un domaine"),
    )

    domain = models.ForeignKey(
        Domain, related_name="changes", db_index=True
    )
    type = models.CharField(max_length=16, choices=DOMAIN_CHANGE_TYPES)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    @receiver(post_save, sender=Domain)
    def domain_save(sender, instance, created, **args):
        if created:
            DomainChange.objects.create(domain=instance, type="NEW")
        else:
            DomainChange.objects.create(domain=instance, type="CHANGE")

class Host(models.Model):
    name = models.CharField(
        verbose_name="nom d'hôte",
        max_length=63,
        help_text="Nom d'hôte sans le nom de domaine " +
            "(par ex. www, forum, admin ...).\n" +
            "La valeur * capture toutes les hôtes et une valeur " +
            "vide capute le domaine sans hôte.",
        validators=[host_validator],
        default="*",
        blank=True
    )
    path = models.CharField(
        verbose_name="chemin dans le système de fichiers",
        max_length=255,
        help_text="Chemin vers le dossier dans votre dossier personnel " +
            "(par ex. /www/forum)",
        validators=[path_validator],
        default="/www"
    )
    creation = models.DateTimeField(auto_now_add=True)

    domain = models.ForeignKey(
        Domain, related_name="hosts", db_index=True
    )
    user = models.ForeignKey(
        User, related_name="hosts", db_index=True
    )
    
    icon = models.ForeignKey(DomainIcon, null=True, on_delete=models.SET_NULL)
    
    class Meta:        
        verbose_name = 'hôte'
        verbose_name_plural = 'hôtes'
        
        unique_together = [
            ("name", "domain")
        ]

        ordering = ['name']

    @property
    def icon_url(self):
        if self.icon == None:
            return settings.DOMAINS_ICONS_DIR + "/default.png"
        else:
            return settings.DOMAINS_ICONS_DIR + self.icon.path
        
    @property
    def full_name(self):
        if self.name != "":
            return "{0}.{1}".format(self.name, self.domain.name)
        return self.domain.name

    @property
    def path_exists(self):
        full_path = os.path.join(
            self.user.get_profile().basedir,
            self.path
        )
        
        return os.path.is_dir(full_path)

    @property
    def ongoing_operation(self):
        return self.changes.filter(active=True).exists()

    @receiver(post_save, sender=User)
    def default_user_hosts(sender, instance, created, **args):
        """ Crée les hôtes par défaut lors de la création d'un membre """
        if created:
            for domain_id in settings.MAIN_DOMAINS:
                Host.objects.create(
                    name=instance.username, path="/www", user=instance,
                    domain=Domain.objects.get(id=domain_id)
                )

    @receiver(post_save, sender=Domain)
    def default_domain_hosts(sender, instance, created, **args):
        """ Crée les hôtes par défaut lors de la création d'un domaine """
        if created:
            Host.objects.create(
                name="", path="/www",
                user=instance.user, domain=instance,
            )
            Host.objects.create(
                name="www", path="/www",
                user=instance.user, domain=instance,
            )

    def __unicode__(self):
        return self.full_name

class HostChange(models.Model):
    HOST_CHANGE_TYPES = (
        (u'NEW', u"Création d'une nouvelle hote"),
        (u'CHANGE', u"Modification d'une hote"),
        (u'REMOVE', u"Supression d'une hote"),
    )

    host = models.ForeignKey(
        Host, related_name="changes", db_index=True
    )
    type = models.CharField(max_length=16, choices=HOST_CHANGE_TYPES)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    @receiver(post_save, sender=Host)
    def host_save(sender, instance, created, **args):
        if created:
            HostChange.objects.create(host=instance, type="NEW")
        else:
            HostChange.objects.create(host=instance, type="CHANGE")

# ** VERSIONS **

class Version(models.Model):
    software = models.CharField(max_length=64, primary_key=True)
    version = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'version du logiciel'
        verbose_name_plural = 'versions des logiciels'

    def __unicode__(self):
        return "{0}: {1}".format(self.software, self.version)

# ** WIKI **

class Article(models.Model):
    name = models.CharField(
        verbose_name="nom de l'article",
        max_length=255,
        help_text="Le nom de l'article ne peut contenir que des caractères " +
            "alphanumériques ou des espaces.",
        validators=[RegexValidator(r'^[A-Z0-9][a-zA-Z0-9 ]{0,254}$')],
        primary_key=True,
    )
    content = models.TextField() # Contenu géneré en HTML
    protected = models.BooleanField(default=False) # Uniquement modifiable par les administrateurs

    class Meta:
        verbose_name = 'article du Wiki'
        verbose_name_plural = 'articles du Wiki'

    def __unicode__(self):
        return "{0}: {1} ...".format(self.name, self.content[:100])

class ArticleRevision(models.Model):
    article = models.ForeignKey(
        Article, related_name="revisions", db_index=True
    )
    user = models.ForeignKey(User)
    creation = models.DateTimeField(auto_now_add=True)
    content = models.TextField() # Contenu au format Markdown

    class Meta:
        verbose_name = 'article du Wiki'
        verbose_name_plural = 'articles du Wiki'
        ordering = ['-id']

    def __unicode__(self):
        return "{0} revision by {1} ...".format(
            self.article.name, self.user.username
        )