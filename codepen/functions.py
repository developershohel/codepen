import base64
import json
import random
import re
import mimetypes
import site
from datetime import date
from urllib import request as urlrequest

from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.serializers import serialize
from django.http.request import HttpHeaders
from django.shortcuts import render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.html import format_html_join, format_html
from django.http import HttpRequest, HttpResponseRedirect


def admin_url():
    return '/admin'


def dashboard_url():
    return reverse('dashboard:dashboard_url')


def home_url():
    return reverse('home:home')


def user_auth(self):
    if self.user.is_authenticated:
        return True
    else:
        return False


def upload_path(instance, filename):
    today = date.today()
    year = str(today.strftime("%Y"))
    month = str(today.strftime("%m"))
    name = instance.user.username
    return f'users/{name}/other/{year}/{month}/{filename}'


def create_file_directory(request):
    today = date.today()
    year = str(today.strftime("%Y"))
    month = str(today.strftime("%m"))
    name = request.user.username
    return f'users/{name}/{year}/{month}'


def user_validation(username):
    regex = r"^[\w_]+\Z"
    match = re.match(regex, username)
    if match:
        return True
    else:
        return False


def password_validation(password):
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%&*.()_-])[A-Za-z\d!@#$%&.*()_-]{8,32}\Z"
    match = re.match(regex, password)
    if match:
        return True
    else:
        return False


def email_validation(email):
    regex = r'^[a-zA-Z0-9]+[a-zA-Z0-9-_.-]+@[a-zA-Z0-9]+\.[a-z]{1,3}\Z'
    match = re.match(regex, email)
    if match:
        return True
    else:
        return False


def name_validation(name):
    regex = r'^[\w\s]+\Z'
    match = re.match(regex, name)
    if match:
        return True
    else:
        return False


def password_helper_text():
    help_texts = ['The password length must be greater than or equal 8',
                  'The password must contain one or more uppercase and lowercase characters',
                  'The password must contain one or more special characters']
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html('<ul class="helper-list">{}</ul>', help_items) if help_items else ""


def html_content_list(items):
    help_items = format_html_join(
        "", "<li>{}</li>", ((item,) for item in items)
    )
    return format_html('<ul class="content-list">{}</ul>', help_items) if help_items else ""


def html_content_paragraph(items):
    help_items = format_html_join(
        "", "<p>{}</p>", ((item,) for item in items)
    )
    return format_html('<div class="content-paragraph">{}</div>', help_items) if help_items else ""


def random_token(length):
    return get_random_string(length=length)


def random_code(min_length, max_length):
    code = random.randint(min_length, max_length)
    return code


def delete_cookie(self, key, path="/", domain=None, samesite=None):
    # Browsers can ignore the Set-Cookie header if the cookie doesn't use
    # the secure flag and:
    # - the cookie name starts with "__Host-" or "__Secure-", or
    # - the samesite is "none".
    secure = key.startswith(("__Secure-", "__Host-")) or (
            samesite and samesite.lower() == "none"
    )
    self.set_cookie(
        key,
        max_age=0,
        path=path,
        domain=domain,
        secure=secure,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        samesite=samesite,
    )


def make_cookies_password(password):
    if password:
        random_string = get_random_string(20)
        prefix = 'pbkdf2_'
        suffix = random_string
        password = password
        utf_password = password.encode()
        encode_password = base64.b64encode(utf_password)
        str_password = str(encode_password)[2:-1]
        password = f'{prefix}{str_password}{suffix}'
        return password
    else:
        return False


def decode_cookies_password(hash_password):
    if hash_password:
        hash_password = hash_password
        encode_password = hash_password[7:-20].encode('utf-8')
        decode_password = base64.b64decode(encode_password)
        password = str(decode_password)[2:-1]
        return password
    else:
        return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_details_by_ip(ip):
    url = 'http://ip-api.com/json/' + str(ip)
    load_url = urlrequest.urlopen(url)
    if load_url:
        load_data = load_url.read()
        get_json = json.loads(load_data)
        if get_json:
            return get_json
        else:
            return False
    else:
        return False


def change_button(app_name, model_name, id):
    return format_html(f'<a class="btn" href="/admin/{app_name}/{model_name}/{id}/change/">Change</a>')


def delete_button(app_name, model_name, id):
    return format_html(f'<a class="btn" href="/admin/{app_name}/{model_name}/{id}/delete/">Delete</a>')


def get_mime_type():
    mime_type = ['.json', '.gif', '.jpg', '.jpe', '.jpeg', '.png', 'webp', '.svg', '.csv', '.txt', '.xml', '.mp4',
                 '.mpeg', '.m1v', '.mpa', '.mpe', '.mpg', '.mov', '.qt', '.webm', '.avi', '.movie']
    return mime_type


def new_name(file_name, count):
    file_name = file_name
    only_name = file_name[:file_name.rfind('.')]
    file_ext = file_name.split('.').pop()
    last_digit = only_name[-1]
    if isinstance(last_digit, int):
        if count > 1:
            new_digit = int(last_digit) + 1
        else:
            new_digit = int(count)
        return f'{only_name}_{new_digit}.{file_ext}'
    else:
        return f'{only_name}_{int(count)}.{file_ext}'


def codepen_platform():
    return (
        ('html', 'HTML'), ('javascript', 'JavaScript (JSX)'), ('c', 'C, C++, C#'), ('php', 'PHP'), ('python', 'Python'),
        ('java', 'Java'), ('kotlin', 'Kotlin'), ('django', 'Django'), ('jinja', 'Jinja2'), ('go', 'Go'),
        ('groovy', 'Groovy'), ('R', 'R'), ('ruby', 'Ruby'), ('swift', 'Swift'), ('vue', 'Vue.js'), ('xml', 'XML/HTML'))


def codepen_theme():
    return (('3024-day', '3024 day'), ('3024-night', '3024 night'), ('abbott', 'Abbott'), ('abcdef', 'Abcdef'),
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
            ('pastel-on-dark', 'Pastel on dark'), ('railscasts', 'Railscasts'), ('rubyblue', 'Rubyblue'),
            ('seti', 'Seti'),
            ('shadowfox', 'Shadowfox'), ('solarized', 'Solarized'), ('ssms', 'SSMS'), ('the-matrix', 'The matrix'),
            ('twilight', 'twilight'), ('vibrant-ink', 'Vibrant ink'), ('xq-dark', 'XQ dark'), ('xq-light', 'XQ light'),
            ('yeti', 'Yeti'), ('yonce', 'Yonce'), ('zenburn', 'Zenburn'))


def codepen_icon():
    return [
        'fa fa-facebook',
        'fa fa-facebook-f',
        'fa fa-facebook-square',
        'fa fa-facebook-messenger',
        'fa fa-twitter-square',
        'fa fa-twitter',
        'fa fa-instagram',
        'fa fa-instagram-square',
        'fa fa-linkedin',
        'fa fa-linkedin-in',
        'fa fa-whatsapp',
        'fa fa-whatsapp-square',
        'fa fa-yahoo',
        'fa fa-google',
        'fa fa-google-wallet',
        'fa fa-google-plus',
        'fa fa-google-plus-square',
        'fa fa-google-plus-g',
        'fa fa-vimeo',
        'fa fa-vimeo-square',
        'fa fa-vimeo-v',
        'fa fa-github',
        'fa fa-github-alt',
        'fa fa-github-square',
        'fa fa-skype',
        'fa fa-vk',
        'fa fa-pinterest',
        'fa fa-pinterest-p',
        'fa fa-pinterest-square',
        'fa fa-youtube-square',
        'fa fa-youtube',
        'fa fa-slack',
        'fa fa-slack-hash',
    ]


def codepen_font():
    return {
        'Abel': 'Abel',
        'Aclonica': 'Aclonica',
        'Actor': 'Actor',
        'Adamina': 'Adamina',
        'Aldrich': 'Aldrich',
        'Alef': 'Alef',
        'Alegreya Sans': 'Alegreya Sans',
        'Alice': 'Alice',
        'Alike': 'Alike',
        'Allan': 'Allan',
        'Allerta': 'Allerta',
        'Amarante': 'Amarante',
        'Amaranth': 'Amaranth',
        'Amiri': 'Amiri',
        'Andika': 'Andika',
        'Antic': 'Antic',
        'Anton': 'Anton',
        'Arimo': 'Arimo',
        'Artifika': 'Artifika',
        'Arvo': 'Arvo',
        'Assistant': 'Assistant',
        'Atma': 'Atma',
        'Baloo Da': 'Baloo Da',
        'Bitter': 'Bitter',
        'Brawler': 'Brawler',
        'Buda': 'Buda',
        'Butcherman': 'Butcherman',
        'Cabin': 'Cabin',
        'Cairo': 'Cairo',
        'Candal': 'Candal',
        'Cantarell': 'Cantarell',
        'Changa': 'Changa',
        'Cherry Swash': 'Cherry Swash',
        'Chivo': 'Chivo',
        'Coda': 'Coda',
        'Concert One': 'Concert One',
        'Copse': 'Copse',
        'Corben': 'Corben',
        'Cousine': 'Cousine',
        'Coustard': 'Coustard',
        'Covered By Your Grace': 'Covered By Your Grace',
        'Crafty Girls': 'Crafty Girls',
        'Crimson Text': 'Crimson Text',
        'Crushed': 'Crushed',
        'Cuprum': 'Cuprum',
        'Damion': 'Damion',
        'Dancing Script': 'Dancing Script',
        'David Libre': 'David Libre',
        'Dawning of a New Day': 'Dawning of a New Day',
        'Days One': 'Days One',
        'Delius': 'Delius',
        'Delius Swash Caps': 'Delius Swash Caps',
        'Delius Unicase': 'Delius Unicase',
        'Didact Gothic': 'Didact Gothic',
        'Dorsa': 'Dorsa',
        'Dosis': 'Dosis',
        'Droid Sans': 'Droid Sans',
        'Droid Sans Mono': 'Droid Sans Mono',
        'Droid Serif': 'Droid Serif',
        'EB Garamond': 'EB Garamond',
        'El Messiri': 'El Messiri',
        'Expletus Sans': 'Expletus Sans',
        'Fanwood Text': 'Fanwood Text',
        'Federo': 'Federo',
        'Fontdiner Swanky': 'Fontdiner Swanky',
        'Forum': 'Forum',
        'Francois One': 'Francois One',
        'Frank Ruhl Libre': 'Frank Ruhl Libre',
        'Galada': 'Galada',
        'Gentium Basic': 'Gentium Basic',
        'Gentium Book Basic': 'Gentium Book Basic',
        'Geo': 'Geo',
        'Geostar': 'Geostar',
        'Geostar Fill': 'Geostar Fill',
        'Gilda Display': 'Gilda Display',
        'Give You Glory': 'Give You Glory',
        'Gloria Hallelujah': 'Gloria Hallelujah',
        'Goblin One': 'Goblin One',
        'Goudy Bookletter 1911': 'Goudy Bookletter 1911',
        'Gravitas One': 'Gravitas One',
        'Gruppo': 'Gruppo',
        'Hammersmith One': 'Hammersmith One',
        'Heebo': 'Heebo',
        'Hind': 'Hind',
        'Hind Siliguri': 'Hind Siliguri',
        'Holtwood One SC': 'Holtwood One SC',
        'Homemade Apple': 'Homemade Apple',
        'Inconsolata': 'Inconsolata',
        'Indie Flower': 'Indie Flower',
        'IM Fell English': 'IM Fell English',
        'Irish Grover': 'Irish Grover',
        'Irish Growler': 'Irish Growler',
        'Istok Web': 'Istok Web',
        'Judson': 'Judson',
        'Julee': 'Julee',
        'Just Another Hand': 'Just Another Hand',
        'Just Me Again Down Here': 'Just Me Again Down Here',
        'Kameron': 'Kameron',
        'Katibeh': 'Katibeh',
        'Kelly Slab': 'Kelly Slab',
        'Kenia': 'Kenia',
        'Kranky': 'Kranky',
        'Kreon': 'Kreon',
        'Kristi': 'Kristi',
        'La Belle Aurore': 'La Belle Aurore',
        'Lalezar': 'Lalezar',
        'Lato': 'Lato',
        'League Script': 'League Script',
        'Leckerli One': 'Leckerli One',
        'Lekton': 'Lekton',
        'Lemonada': 'Lemonada',
        'Lily Script One': 'Lily Script One',
        'Limelight': 'Limelight',
        'Lobster': 'Lobster',
        'Lobster Two': 'Lobster Two',
        'Lora': 'Lora',
        'Love Ya Like A Sister': 'Love Ya Like A Sister',
        'Loved by the King': 'Loved by the King',
        'Lovers Quarrel': 'Lovers Quarrel',
        'Luckiest Guy': 'Luckiest Guy',
        'Mada': 'Mada',
        'Maiden Orange': 'Maiden Orange',
        'Mako': 'Mako',
        'Marvel': 'Marvel',
        'Maven Pro': 'Maven Pro',
        'Meddon': 'Meddon',
        'MedievalSharp': 'MedievalSharp',
        'Medula One': 'Medula One',
        'Megrim': 'Megrim',
        'Merienda One': 'Merienda One',
        'Merriweather': 'Merriweather',
        'Metrophobic': 'Metrophobic',
        'Michroma': 'Michroma',
        'Miltonian Tattoo': 'Miltonian Tattoo',
        'Miltonian': 'Miltonian',
        'Miriam Libre': 'Miriam Libre',
        'Mirza': 'Mirza',
        'Modern Antiqua': 'Modern Antiqua',
        'Molengo': 'Molengo',
        'Monofett': 'Monofett',
        'Monoton': 'Monoton',
        'Montaga': 'Montaga',
        'Montez': 'Montez',
        'Montserrat': 'Montserrat',
        'Mountains of Christmas': 'Mountains of Christmas',
        'Muli': 'Muli',
        'Neucha': 'Neucha',
        'Neuton': 'Neuton',
        'News Cycle': 'News Cycle',
        'Nixie One': 'Nixie One',
        'Nobile': 'Nobile',
        'Noto Sans': 'Noto Sans',
        'Nova Cut': 'Nova Cut',
        'Nova Flat': 'Nova Flat',
        'Nova Mono': 'Nova Mono',
        'Nova Oval': 'Nova Oval',
        'Nova Round': 'Nova Round',
        'Nova Script': 'Nova Script',
        'Nova Slim': 'Nova Slim',
        'Nova Square': 'Nova Square',
        'Numans': 'Numans',
        'Nunito': 'Nunito',
        'Open Sans': 'Open Sans',
        'Oswald': 'Oswald',
        'Over the Rainbow': 'Over the Rainbow',
        'Ovo': 'Ovo',
        'Oxygen': 'Oxygen',
        'Pacifico': 'Pacifico',
        'Passero One': 'Passero One',
        'Passion One': 'Passion One',
        'Patrick Hand': 'Patrick Hand',
        'Paytone One': 'Paytone One',
        'Permanent Marker': 'Permanent Marker',
        'Philosopher': 'Philosopher',
        'Play': 'Play',
        'Playfair Display': 'Playfair Display',
        'Podkova': 'Podkova',
        'Poller One': 'Poller One',
        'Pompiere': 'Pompiere',
        'Prata': 'Prata',
        'Prociono': 'Prociono',
        'PT Sans': 'PT Sans',
        'PT Sans Caption': 'PT Sans Caption',
        'PT Sans Narrow': 'PT Sans Narrow',
        'PT Serif': 'PT Serif',
        'PT Serif Caption': 'PT Serif Caption',
        'Puritan': 'Puritan',
        'Quattrocento': 'Quattrocento',
        'Quattrocento Sans': 'Quattrocento Sans',
        'Questrial': 'Questrial',
        'Radley': 'Radley',
        'Rakkas': 'Rakkas',
        'Raleway': 'Raleway',
        'Rationale': 'Rationale',
        'Redressed': 'Redressed',
        'Reenie Beanie': 'Reenie Beanie',
        'Roboto': 'Roboto',
        'Roboto Condensed': 'Roboto Condensed',
        'Rock Salt': 'Rock Salt',
        'Rochester': 'Rochester',
        'Rokkitt': 'Rokkitt',
        'Rosario': 'Rosario',
        'Rubik': 'Rubik',
        'Ruslan Display': 'Ruslan Display',
        'Sancreek': 'Sancreek',
        'Sansita One': 'Sansita One',
        'Schoolbell': 'Schoolbell',
        'Secular One': 'Secular One',
        'Shadows Into Light': 'Shadows Into Light',
        'Shanti': 'Shanti',
        'Short Stack': 'Short Stack',
        'Sigmar One': 'Sigmar One',
        'Six Caps': 'Six Caps',
        'Slackey': 'Slackey',
        'Smokum': 'Smokum',
        'Smythe': 'Smythe',
        'Sniglet': 'Sniglet',
        'Snippet': 'Snippet',
        'Sorts Mill Goudy': 'Sorts Mill Goudy',
        'Special Elite': 'Special Elite',
        'Spinnaker': 'Spinnaker',
        'Stardos Stencil': 'Stardos Stencil',
        'Sue Ellen Francisco': 'Sue Ellen Francisco',
        'Suez One': 'Suez One',
        'Sunshiney': 'Sunshiney',
        'Swanky and Moo Moo': 'Swanky and Moo Moo',
        'Syncopate': 'Syncopate',
        'Tangerine': 'Tangerine',
        'Tenor Sans': 'Tenor Sans',
        'Terminal Dosis Light': 'Terminal Dosis Light',
        'Tinos': 'Tinos',
        'Titillium Web': 'Titillium Web',
        'Tulpen One': 'Tulpen One',
        'Ubuntu': 'Ubuntu',
        'Ultra': 'Ultra',
        'UnifrakturCook': 'UnifrakturCook',
        'UnifrakturMaguntia': 'UnifrakturMaguntia',
        'Unkempt': 'Unkempt',
        'Unna': 'Unna',
        'Varela': 'Varela',
        'Varela Round': 'Varela Round',
        'Vibur': 'Vibur',
        'Vidaloka': 'Vidaloka',
        'Volkhov': 'Volkhov',
        'Vollkorn': 'Vollkorn',
        'Voltaire': 'Voltaire',
        'VT323': 'VT323',
        'Waiting for the Sunrise': 'Waiting for the Sunrise',
        'Wallpoet': 'Wallpoet',
        'Walter Turncoat': 'Walter Turncoat',
        'Wire One': 'Wire One',
        'Yanone Kaffeesatz': 'Yanone Kaffeesatz',
        'Yellowtail': 'Yellowtail',
        'Yeseva One': 'Yeseva One',
        'Zeyada': 'Zeyada'
    }


def codepen_font_weight():
    return {
        '100': 'Thin 100',
        '200': 'Ultra Light 200',
        '300': 'Light 300',
        '400': 'Regular 400',
        '500': 'Medium 500',
        '600': 'Semi Bold 600',
        '700': 'Bold 700',
        '800': 'Extra Bold 800',
        '900': 'Black 900',
    }


def datetime_converter(type, second=None, minute=None, hour=None, day=None, week=None, month=None, year=None):
    if type:
        value = []
        result = None
        if type == 'minute':
            if second:
                value.append(int(second)/60)
            if minute:
                value.append(int(minute))
            if hour:
                value.append(int(hour) * 60)
            if day:
                value.append(int(day) * 24 * 60)
            if week:
                value.append(int(week) * 7 * 24 * 60)
            if month:
                value.append(int(month) * 30 * 24 * 60)
            if year:
                value.append(int(year) * 365 * 24 * 60)
            result = sum(value)
            return result
        elif type == 'hour':
            if second:
                value.append(int(second)/3600)
            if minute:
                value.append(int(minute)/60)
            if hour:
                value.append(int(hour))
            if day:
                value.append(int(day) * 24)
            if week:
                value.append(int(week) * 7 * 24)
            if month:
                value.append(int(month) * 30 * 24)
            if year:
                value.append(int(year) * 365 * 24)
            result = sum(value)
            return result
        elif type == 'week':
            if second:
                value.append(int(second)/604800)
            if minute:
                value.append(int(minute)/10080)
            if hour:
                value.append(int(hour)/168)
            if day:
                value.append(int(day)/7)
            if week:
                value.append(int(week))
            if month:
                value.append((int(month) * 30)/7)
            if year:
                value.append((int(year) * 365)/7)
            result = sum(value)
            return result
        elif type == 'month':
            if second:
                value.append(int(second)/2592000)
            if minute:
                value.append(int(minute)/43200)
            if hour:
                value.append(int(hour)/720)
            if day:
                value.append(int(day)/30)
            if week:
                value.append((int(week)*7)/30)
            if month:
                value.append(int(month))
            if year:
                value.append((int(year) * 365)/30)
            result = sum(value)
            return result
        elif type == 'year':
            if second:
                value.append(int(second)/31536000)
            if minute:
                value.append(int(minute)/525600)
            if hour:
                value.append(int(hour)/8760)
            if day:
                value.append(int(day)/365)
            if week:
                value.append((int(week)*7)/365)
            if month:
                value.append((int(month)*30)/365)
            if year:
                value.append(int(year))
            result = sum(value)
            return result
        else:
            if second:
                value.append(int(second))
            if minute:
                value.append(int(minute) * 60)
            if hour:
                value.append(int(hour) * 60 * 60)
            if day:
                value.append(int(day) * 24 * 60 * 60)
            if week:
                value.append(int(week) * 7 * 24 * 60 * 60)
            if month:
                value.append(int(month) * 30 * 24 * 60 * 60)
            if year:
                value.append(int(year) * 365 * 24 * 60 * 60)
            result = sum(value)
            return result
    else:
        return ''
