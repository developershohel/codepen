import datetime
from django.db import models
from django.utils.html import format_html
from codepen.functions import change_button, delete_button
from user.models import User
from taggit.managers import TaggableManager
from datetime import date


def upload_path(instance, filename):
    today = date.today()
    year = str(today.strftime("%Y"))
    month = str(today.strftime("%m"))
    name = instance.user.username
    return f'users/{name}/pen/{year}/{month}/{filename}'


class Pen(models.Model):
    choices = (
        ('html', 'HTML'), ('javascript', 'JavaScript (JSX)'), ('c', 'C, C++, C#'), ('php', 'PHP'), ('python', 'Python'),
        ('java', 'Java'), ('kotlin', 'Kotlin'), ('django', 'Django'), ('jinja', 'Jinja2'), ('go', 'Go'),
        ('groovy', 'Groovy'), ('R', 'R'), ('ruby', 'Ruby'), ('swift', 'Swift'), ('vue', 'Vue.js'), ('xml', 'XML/HTML'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pen_title = models.CharField(max_length=255, null=False, blank=False)
    pen_description = models.TextField(null=True, blank=True)
    pen_slug = models.SlugField(max_length=100, null=False, blank=False, unique=True)
    pen_tag = TaggableManager()
    pen_thumbnail = models.ImageField(upload_to=upload_path, null=True, blank=True)
    pen_status = models.CharField(max_length=32,
                                  choices=(('published', 'Published'), ('private', 'Private'), ('draft', "Draft"),
                                           ('trash', 'Trash')),
                                  default='publish')
    pen_type = models.CharField(max_length=16, null=False, blank=False, choices=choices)
    pen_love = models.ManyToManyField(User, related_name='love', blank=True)
    pen_view = models.ManyToManyField(User, related_name='view', blank=True)
    pen_comments = models.BigIntegerField(blank=True, null=True)
    pen_published = models.DateTimeField(auto_now=True)
    pen_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} {self.user.username} {self.pen_title} {self.pen_status} {self.pen_modified}'

    def get_datetime(self):
        return self.pen_modified.strftime("%b %d %Y %H: %M %p")

    def get_date(self):
        return self.pen_modified.strftime("%b %d %Y")

    def username(self):
        return self.user.username

    def tag_list(self):
        return self.pen_tag.instance

    def change_button(self):
        change_button('pen', 'pen', self.id)

    def delete_button(self):
        delete_button('pen', 'pen', self.id)

    def delete(self, *args, **kwargs):
        self.pen_thumbnail.delete()
        super().delete(*args, **kwargs)


class PenData(models.Model):
    pen = models.OneToOneField(Pen, on_delete=models.CASCADE)
    html = models.TextField(null=True, blank=True)
    css = models.TextField(null=True, blank=True)
    scss = models.TextField(null=True, blank=True)
    sass = models.TextField(null=True, blank=True)
    javascript = models.TextField(null=True, blank=True)
    cpp = models.TextField(null=True, blank=True)
    php = models.TextField(null=True, blank=True)
    python = models.TextField(null=True, blank=True)
    java = models.TextField(null=True, blank=True)
    go = models.TextField(null=True, blank=True)
    r = models.TextField(null=True, blank=True)
    ruby = models.TextField(null=True, blank=True)
    vue = models.TextField(null=True, blank=True)
    react = models.TextField(null=True, blank=True)
    xml = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pen data'
        verbose_name_plural = 'Pen data'

    def username(self):
        return self.pen.user.username

    def pen_title(self):
        return self.pen.pen_title


class Assets(models.Model):
    pen = models.OneToOneField(Pen, on_delete=models.CASCADE)
    html = models.CharField(max_length=255, null=True, blank=True)
    head = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255, null=True, blank=True)
    css1 = models.CharField(max_length=255, null=True, blank=True)
    css2 = models.CharField(max_length=255, null=True, blank=True)
    css3 = models.CharField(max_length=255, null=True, blank=True)
    css4 = models.CharField(max_length=255, null=True, blank=True)
    css5 = models.CharField(max_length=255, null=True, blank=True)
    css6 = models.CharField(max_length=255, null=True, blank=True)
    css7 = models.CharField(max_length=255, null=True, blank=True)
    css8 = models.CharField(max_length=255, null=True, blank=True)
    css9 = models.CharField(max_length=255, null=True, blank=True)
    css10 = models.CharField(max_length=255, null=True, blank=True)
    css11 = models.CharField(max_length=255, null=True, blank=True)
    css12 = models.CharField(max_length=255, null=True, blank=True)
    css13 = models.CharField(max_length=255, null=True, blank=True)
    css14 = models.CharField(max_length=255, null=True, blank=True)
    css15 = models.CharField(max_length=255, null=True, blank=True)
    css16 = models.CharField(max_length=255, null=True, blank=True)
    css17 = models.CharField(max_length=255, null=True, blank=True)
    css18 = models.CharField(max_length=255, null=True, blank=True)
    css19 = models.CharField(max_length=255, null=True, blank=True)
    css20 = models.CharField(max_length=255, null=True, blank=True)
    js1 = models.CharField(max_length=255, null=True, blank=True)
    js2 = models.CharField(max_length=255, null=True, blank=True)
    js3 = models.CharField(max_length=255, null=True, blank=True)
    js4 = models.CharField(max_length=255, null=True, blank=True)
    js5 = models.CharField(max_length=255, null=True, blank=True)
    js6 = models.CharField(max_length=255, null=True, blank=True)
    js7 = models.CharField(max_length=255, null=True, blank=True)
    js8 = models.CharField(max_length=255, null=True, blank=True)
    js9 = models.CharField(max_length=255, null=True, blank=True)
    js10 = models.CharField(max_length=255, null=True, blank=True)
    js11 = models.CharField(max_length=255, null=True, blank=True)
    js12 = models.CharField(max_length=255, null=True, blank=True)
    js13 = models.CharField(max_length=255, null=True, blank=True)
    js14 = models.CharField(max_length=255, null=True, blank=True)
    js15 = models.CharField(max_length=255, null=True, blank=True)
    js16 = models.CharField(max_length=255, null=True, blank=True)
    js17 = models.CharField(max_length=255, null=True, blank=True)
    js18 = models.CharField(max_length=255, null=True, blank=True)
    js19 = models.CharField(max_length=255, null=True, blank=True)
    js20 = models.CharField(max_length=255, null=True, blank=True)

    def username(self):
        return self.pen.user.username

    def pen_title(self):
        return self.pen.pen_title


class PenSetting(models.Model):
    choices = (
        ('html', 'HTML'), ('javascript', 'JavaScript (JSX)'), ('c', 'C, C++, C#'), ('php', 'PHP'), ('python', 'Python'),
        ('java', 'Java'), ('kotlin', 'Kotlin'), ('django', 'Django'), ('jinja', 'Jinja2'), ('go', 'Go'),
        ('groovy', 'Groovy'), ('R', 'R'), ('ruby', 'Ruby'), ('swift', 'Swift'), ('vue', 'Vue.js'), ('xml', 'XML/HTML'))

    themes = (
        ('3024-day', '3024 day'), ('3024-night', '3024 night'), ('abbott', 'Abbott'), ('abcdef', 'Abcdef'),
        ('ambiance-mobile', 'Ambiance mobile'), ('ambiance', 'Ambiance'), ('ayu-dark', 'Ayu dark'),
        ('ayu-mirage', 'Ayu mirage'), ('base16-dark', 'Base16 dark'), ('base16-light', 'Base16 light'),
        ('bespin', 'Bespin'), ('blackboard', 'Blackboard'), ('cobalt', 'Bobalt'), ('colorforth', 'Colorforth'),
        ('darcula', 'Darcula'), ('duotone-dark', 'Duotone dark'),
        ('duotone-light', 'Duotone light'), ('eclipse', 'Eclipse'), ('elegant', 'Elegant'),
        ('erlang-dark', 'Erlang dark'), ('gruvbox-dark', 'Qruvbox dark'), ('hopscotch', 'Hopscotch'),
        ('icecoder', 'Icecoder'), ('idea', 'Idea'), ('isotope', 'Isotope'), ('juejin', 'Juejin'),
        ('lesser-dark', 'Lesser dark'), ('liquibyte', 'Liquibyte'), ('lucario', 'Lucario'),
        ('material-darker', 'Material darker'), ('material-ocean', 'Material ocean'),
        ('material-palenight', 'Material palenight'), ('material', 'Material'), ('mbo', 'MBO'),
        ('mdn-like', 'MDN like'), ('midnight', 'Midnight'), ('monokai', 'Monokai'), ('moxer', 'Moxer'),
        ('neat', 'Neat'), ('neo', 'Neo'), ('night', 'Night'), ('nord', 'Nord'), ('oceanic-next', 'Oceanic next'),
        ('panda-syntax', 'Panda syntax'), ('paraiso-dark', 'Paraiso dark'), ('paraiso-light', 'Paraiso light'),
        ('pastel-on-dark', 'Pastel on dark'), ('railscasts', 'Railscasts'), ('rubyblue', 'Rubyblue'), ('seti', 'Seti'),
        ('shadowfox', 'Shadowfox'), ('solarized', 'Solarized'), ('ssms', 'SSMS'), ('the-matrix', 'The matrix'),
        ('twilight', 'twilight'), ('vibrant-ink', 'Vibrant ink'), ('xq-dark', 'XQ dark'), ('xq-light', 'XQ light'),
        ('yeti', 'Yeti'), ('yonce', 'Yonce'), ('zenburn', 'Zenburn'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, null=True, blank=True, choices=themes)
    platform = models.CharField(max_length=100, null=False, blank=False, choices=choices)
    font = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.theme}'


class Comment(models.Model):
    pen = models.ForeignKey(Pen, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter", null=False, blank=False)
    comment_content = models.TextField(null=False, blank=False)
    comment_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    comment_modified = models.DateTimeField(auto_now_add=True)
    comment_published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.pen.id} {self.user.id} {self.commenter.id} {self.comment_modified} {self.comment_published}'

    def comment_pen_title(self):
        return self.pen.pen_title

    def comment_author_username(self):
        return self.user.username

    def change_button(self):
        return change_button('pen', 'comment', self.id)

    def delete_button(self):
        return delete_button('pen', 'comment', self.id)
