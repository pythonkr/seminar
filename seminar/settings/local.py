from seminar.settings.base import *

# email settings override
# if you use this setting, change EMAIL_HOST_USER and excute commands below
# $ export EMAIL_PASSWORD="<YOUR_EMAIL_PASSWORD>"
EMAIL_HOST_USER = 'makeajourney@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
