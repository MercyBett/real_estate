from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()




class UserAdmin(admin.ModelAdmin):
    using = 'user'
    list_display = ('id', 'name', 'email', 'password')
    list_display_links = ('id', 'name', 'email', 'password')
    search_fields = ('name', 'email',)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(User, UserAdmin)
