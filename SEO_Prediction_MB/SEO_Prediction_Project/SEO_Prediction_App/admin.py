from django.contrib import admin

from .models import Keyword
from .models import Data
from .models import Data_Url
from .models import Keyword_Url
from .models import Test

admin.site.register(Keyword)
admin.site.register(Data)
admin.site.register(Data_Url)
admin.site.register(Keyword_Url)
admin.site.register(Test)

# Register your models here.
