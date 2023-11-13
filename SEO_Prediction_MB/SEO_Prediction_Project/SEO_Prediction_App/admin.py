from django.contrib import admin

from .models import Keyword
from .models import Data


admin.site.register(Keyword)
admin.site.register(Data)
# Register your models here.
