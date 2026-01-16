from django.contrib import admin
from .models import login, registration, tbl_contact, tbl_Usm, upload_lecture, Upload_Assignment , tbl_noti
# Register your models here.

admin.site.register(login)
admin.site.register(registration)
admin.site.register(tbl_contact)
admin.site.register(tbl_Usm)
admin.site.register(upload_lecture)
admin.site.register(Upload_Assignment)
admin.site.register(tbl_noti)