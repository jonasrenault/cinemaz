from django.db import models


class CodeName(models.Model):
    name = models.CharField(max_length=512)
    code = models.IntegerField(unique=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cinema(models.Model):
    name = models.CharField(max_length=512)
    code = models.CharField(unique=True, max_length=50)
    address = models.CharField(max_length=512)
    postal_code = models.CharField(max_length=256)
    city = models.CharField(max_length=512)
    area = models.CharField(max_length=256)
    subway = models.CharField(max_length=512)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    screen_count = models.IntegerField(blank=True, null=True)
    has_PRM_access = models.BooleanField(default=False)
    has_event = models.BooleanField(default=False)
    open_to_external_sales = models.BooleanField(default=False)
    chain = models.ForeignKey('cinemas.CodeName', related_name='cinema_chain', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Artwork(models.Model):
    href = models.CharField(max_length=1024)
    path = models.CharField(max_length=1024)


class PersonName(models.Model):
    given = models.CharField(max_length=1024)
    family = models.CharField(max_length=1024)


class ShortPerson(models.Model):
    name = models.CharField(max_length=512)
    code = models.IntegerField(unique=True)
    gender = models.IntegerField()
    birthdate = models.CharField(max_length=512)
    activity = models.ManyToManyField('cinemas.CodeName', related_name='short_person_activity')
    nationality = models.ManyToManyField('cinemas.CodeName', related_name='short_person_nationality')
    picture = models.ForeignKey('cinemas.Artwork', related_name='short_person_picture', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_male(self):
        return self.gender == 1

    def is_female(self):
        return self.gender == 2


class CastMember(models.Model):
    short_person = models.ForeignKey('cinemas.ShortPerson', related_name='cast_person')
    activity = models.ForeignKey('cinemas.CodeName', related_name='cast_activity')
    picture = models.ForeignKey('cinemas.Artwork', related_name='cast_picture', blank=True, null=True)
    role = models.CharField(max_length=1024)
    is_lead_actor = models.BooleanField(default=False)


class Release(models.Model):
    release_date = models.CharField(max_length=512)
    country = models.ForeignKey('cinemas.CodeName', related_name='release_country', blank=True, null=True)
    distributor = models.ForeignKey('cinemas.CodeName', related_name='release_distributor', blank=True, null=True)
    release_state = models.ForeignKey('cinemas.CodeName', related_name='release_release_state', blank=True, null=True)


class CastingShort(models.Model):
    directors = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True)


class Movie(models.Model):
    code = models.IntegerField(unique=True)
    title = models.CharField(max_length=1024)
    original_title = models.CharField(max_length=1024)
    synopsys = models.TextField()
    synopsys_short = models.TextField()
    nationality = models.ManyToManyField('cinemas.CodeName', related_name='movie_nationality')
    genre = models.ManyToManyField('cinemas.CodeName', related_name='movie_genre')
    cast_member = models.ManyToManyField('cinemas.CastMember', related_name='movie_cast')
    # Statistics
    user_rating = models.FloatField(blank=True, null=True)
    user_rating_count = models.IntegerField(blank=True, null=True)
    user_review_count = models.IntegerField(blank=True, null=True)
    press_rating = models.FloatField(blank=True, null=True)
    press_review_count = models.IntegerField(blank=True, null=True)
    editorial_rating_count = models.IntegerField(blank=True, null=True)

    release = models.ForeignKey('cinemas.Release', related_name='movie_release', blank=True, null=True)
    # Casting Short
    directors = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    creators = models.TextField(blank=True, null=True)

    poster = models.ForeignKey('cinemas.Artwork', related_name='movie_poster', blank=True, null=True)
    tags = models.ManyToManyField('cinemas.CastMember', related_name='movie_tag')

    runtime = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class Screening(models.Model):
    date = models.DateField()
    time = models.TextField()


class ShowTime(models.Model):
    preview = models.BooleanField(default=False)
    releaseWeek = models.BooleanField(default=False)
    on_show = models.ForeignKey('cinemas.Movie', related_name='showtime_movie')
    screen_format = models.ForeignKey('cinemas.CodeName', related_name='showtime_screen_format')
    display = models.TextField()
    version_code = models.IntegerField()
    version_original = models.BooleanField(default=True)
    version_name = models.CharField(max_length=512)
    screening = models.ManyToManyField('cinemas.Screening', related_name='showtime_screening')
    place = models.ForeignKey('cinemas.Cinema', related_name='showtime_cinema')
    updated_at = models.DateTimeField(auto_now=True)