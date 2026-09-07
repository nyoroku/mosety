# boats/settings.py
import mimetypes
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Windows does not always register modern image MIME types. Without this,
# nosniff-enabled browsers can intermittently reject otherwise valid WebP files.
mimetypes.add_type('image/webp', '.webp', strict=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='a-default-secret-key-for-dev-please-change')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://mosety.co.ke',
    'https://www.mosety.co.ke',
    'https://mosety.pythonanywhere.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'taggit',
    "tinymce",

    # Local Apps
    'core.apps.CoreConfig',
    'analytics.apps.AnalyticsConfig',
    'tours.apps.ToursConfig',
    'content.apps.ContentConfig',
    'pages.apps.PagesConfig',
    'bookings.apps.BookingsConfig',

    'dashboard.apps.DashboardConfig',
    'seo.apps.SeoConfig',
    'blog.apps.BlogConfig',
    'jobs.apps.JobsConfig',
    'services.apps.ServicesConfig',
    'testimonials.apps.TestimonialsConfig',
    'accommodation.apps.AccommodationConfig',
    'reputation.apps.ReputationConfig',
    'loyalty.apps.LoyaltyConfig',
    'resources.apps.ResourcesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seo.middleware.SEORedirectMiddleware',
    'analytics.middleware.UTMMiddleware',
]

# Security/Performance Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'boats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.mosety_site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'boats.wsgi.application'
TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": "100%",
    "menubar": False,
    "plugins": [
        "advlist autolink lists link image preview anchor",
        "searchreplace visualblocks code fullscreen",
        "media table paste code help wordcount"
    ],
    "toolbar": (
        "undo redo | "
        "formatselect | "
        "bold italic | "
        "bullist numlist | "
        "link image | "
        "removeformat | code"
    ),

    # ✅ H1 BLOCKED – ONLY H2–H4 ALLOWED
    "block_formats": "Paragraph=p;Heading 2=h2;Heading 3=h3;Heading 4=h4",

    # ✅ STRIP INLINE JUNK FROM WORD
    "paste_as_text": True,
    "paste_remove_spans": True,
    "paste_remove_styles": True,

    # ✅ IMAGE RULES
    "image_advtab": True,
    "automatic_uploads": True,
    "file_picker_types": "image",

    # ✅ CLEAN HTML OUTPUT
    "valid_elements": "p,h2,h3,h4,strong/b,em/i,ul,ol,li,a[href|title],img[src|alt|width|height]",
    "invalid_elements": "font,span,style",

    # ✅ FORCE REL=NOOPENER ON EXTERNAL LINKS
    "rel_list": [
        {"title": "No Referrer", "value": "noreferrer"},
        {"title": "No Opener", "value": "noopener"},
    ],
}

# Database
# Using SQLite for simplicity. Switch to PostgreSQL for production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise: Compression and Forever-cache
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# WhiteNoise settings
WHITENOISE_MAX_AGE = 31536000  # 1 year
WHITENOISE_INDEX_PAGE_SELF_REDIRECTION = True

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs for dashboard
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
ADMIN_TITLE = "Mosety Boat Rides Naivasha Admin"
ADMIN_HEADER = "Mosety Boat Rides Naivasha"
ADMIN_INDEX_TITLE = "Mosety Operations & Content Management"
ADMIN_NAME = "Mosety Boat Rides Naivasha"

# Launch-sensitive business details
SITE_WHATSAPP_NUMBER = config('SITE_WHATSAPP_NUMBER', default='+254 114 182706')
SITE_PHONE_NUMBER = config('SITE_PHONE_NUMBER', default='+254 114 182706')
SITE_BASE_URL = config('SITE_BASE_URL', default='https://mosety.co.ke').rstrip('/')
SITE_LAUNCH_POINT = config('SITE_LAUNCH_POINT', default='Karagita Public Beach / South Lake Road, Lake Naivasha')
SITE_LATITUDE = config('SITE_LATITUDE', default='-0.763400')
SITE_LONGITUDE = config('SITE_LONGITUDE', default='36.425800')
SITE_PRICE_RANGE = config('SITE_PRICE_RANGE', default='KES 2,000 - 15,000')
SITE_CONTENT_LAST_UPDATED = config('SITE_CONTENT_LAST_UPDATED', default='2026-09-07')

