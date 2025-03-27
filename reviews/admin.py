from django.contrib import admin
from .models import PerfReview, Achievement, AchievementScore

@admin.register(PerfReview)
class PerfReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'created')
    list_filter = ('team', 'created')
    search_fields = ('user__email', 'user__user_name', 'team__team_name')
    date_hierarchy = 'created'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'perfreview', 'self_score', 'created')
    list_filter = ('self_score', 'created')
    search_fields = ('title', 'perfreview__user__email')

@admin.register(AchievementScore)
class AchievementScoreAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'user', 'score')
    list_filter = ('score', 'created')
    search_fields = ('achievement__title', 'user__email', 'comment')
