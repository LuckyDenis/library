from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Language(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['name'], name="language_name_idx")
        ]
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ["name"]

    class LanguageForBook(models.TextChoices):
        #  ISO:639-1
        EN = 'en', _('English')
        RU = 'ru', _('Russian'),

    name = models.CharField(
        verbose_name=_("Language"),
        max_length=2,
        choices=LanguageForBook.choices,
        default=LanguageForBook.RU,
        help_text=_("language")
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        ordering = ["-name"]

    class GenreForBook(models.TextChoices):
        ANTHOLOGY = "anthology", _("anthology")
        AUTOBIOGRAPHY = "autobiography", _("autobiography")
        BUSINESS_AND_FINANCE = "business & finance", _("business & finance")
        CHILDREN_BOOK = "children's books", _("children's books")
        COOKBOOK = "cookbook", _("cookbook")
        DICTIONARY = "dictionary", _("dictionary")
        ENCYCLOPEDIA = "encyclopedia", _("encyclopedia")
        EROTICA = "erotica", _("erotica")
        FANTASY = "fantasy", _("fantasy")
        HEALTH_AND_MEDICINE = "health & medicine", _("health& medicine")
        HISTORY = "history", _("history")
        HORROR = "horror", _("horror")
        INSPIRATIONAL = "inspirational", _("inspirational")
        LIGHT_FICTION = "light fiction", _("light fiction")
        MYSTERY = "mystery", _("mystery")
        NON_FICTION = "non-fiction", _("non-fiction")
        POLITICS = "politics", _("politics"),
        RELIGIOUS = "religious", _("religious")
        ROMANCE = "romance", _("romance")
        SATIRE = "satire", _("satire")
        SCIENCE_FICTION = "science fiction", _("science fiction")
        SERIES = "series", _("series")
        THRILLER = "thriller", _("thriller")
        TRAVEL = "travel", _("travel")
        FICTION = "fiction", _("fiction")

    name = models.Field(
        verbose_name=_("Genre type"),
        max_length=32,
        choices=GenreForBook.choices,
        default=GenreForBook.ANTHOLOGY,
        help_text=_("Genre's book")
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["first_name", "last_name"], name="author_name_idx"),
            models.Index(fields=["first_name"], name="author_first_name_idx"),
            models.Index(fields=["last_name"], name="author_last_name_idx")
        ]
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        ordering = ["first_name", "last_name"]

    first_name = models.CharField(
        verbose_name=_("Firs Name"),
        max_length=100,
        help_text=_("Author's first name")
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=100,
        help_text=_("Author's last name")
    )
    date_of_birth = models.DateField(
        verbose_name=_("Date Of Birth"),
        help_text=_("Date of birth"),
        null=True, blank=True
    )
    date_of_death = models.DateField(
        verbose_name=_("Date Of Death"),
        help_text=_("Date of death"),
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['title'], name="book_title_idx"),
            models.Index(fields=['author'], name="book_author_idx"),
            models.Index(fields=['isbn'], name="book_isbn_idx"),
        ]
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['author']

    ISBN_LINK = 'https://www.isbn-international.org/content/what-isbn'
    ISBN_HINT = _(f'13 Character <a href="{ISBN_LINK}">ISBN number</a>')
    isbn = models.CharField(
        primary_key=True,
        verbose_name=_("ISBN"),
        help_text=_(ISBN_HINT),
        max_length=13
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=200,
        help_text=_("Book's title")
    )
    author = models.ForeignKey(
        Author,
        verbose_name=_("Author's book"),
        on_delete=models.PROTECT
    )
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=1000,
        null=True, blank=True,
        help_text=_("Description of the book")
    )
    imprint = models.CharField(
        verbose_name=_("Imprint"),
        max_length=200
    )
    year = models.DateField(
        verbose_name=_("Year"),
        help_text=_("Year of publication"),
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name=_("Genre's Book"),
        help_text=_("Select a genre's book"),
        blank=True,
        on_delete=models.PROTECT
    )
    language = models.ForeignKey(
        Language,
        verbose_name=_("Book Language"),
        help_text=_("Book's language"),
        on_delete=models.PROTECT,
        blank=True
    )

    def __str__(self):
        return f'{self.author} - {self.title}'

    def get_absolute_url(self):
        return "/catalog/books/%s/" % self.isbn


class BookInstance(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["book"], name="book_instance_unique_id_idx"),
            models.Index(fields=["status"], name="book_instance_status_idx")
        ]
        ordering = ['due_back']

    id = models.UUIDField(
        primary_key=True, default=uuid4,
        verbose_name=_("Book's instance id")
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT
    )
    due_back = models.DateField(
        verbose_name=_("Due Back"),
        help_text=_("Instance book due back"),
        null=True, blank=True
    )

    class StatusForInstanceBook(models.TextChoices):
        AVAILABLE = 'a', _('Available')
        MAINTENANCE = 'm', _('Maintenance')
        ON_LOAN = 'o', _('On loan')
        RESERVED = 'r', _('Reserved')

    status = models.CharField(
        help_text=_("Book's instance status"),
        max_length=1, choices=StatusForInstanceBook.choices,
        default=StatusForInstanceBook.AVAILABLE
    )

    def __str__(self):
        return f'{self.book} - {self.id}'
