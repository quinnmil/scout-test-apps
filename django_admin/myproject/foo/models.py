from django.db import models
from django.conf import settings
from django.contrib import admin


class Foo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Bar(models.Model):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)


class FooAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ["id", "bars", "user"]

    def bars(self, obj):
        return ", ".join([str(b.id) for b in obj.bar_set.all()])

    def user(self, obj):
        return obj.user


class BarAdmin(admin.ModelAdmin):
    list_per_page = 300
    list_display = ["id", "foo", "user"]

    def foo(self, obj):
        return obj.foo

    def user(self, obj):
        return obj.foo.user


admin.site.register(Foo, FooAdmin)
admin.site.register(Bar, BarAdmin)
