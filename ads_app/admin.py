from django.contrib import admin
from django.utils.safestring import mark_safe

from ads_app.models import Ad, ExchangeProposal


@admin.register(Ad)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image_url', 'condition', 'category', 'user')
    list_display_links = ('title', )


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_receiver', 'ad_sender', 'comment', 'status')
