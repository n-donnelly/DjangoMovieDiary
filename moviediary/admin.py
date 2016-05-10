from django.contrib import admin

from moviediary.models import Reviewer, Movie, Review, Following, Wishlist


# Register your models here.
admin.site.register(Reviewer)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Following)
admin.site.register(Wishlist)