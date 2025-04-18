from django.db.models import Count
from django.contrib import admin


from donations.models import Collect, Payment


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'reason',
        'current_value',
        'finish_at',
        'owner'
    )
    search_fields = (
        'title',
        'owner__email'
    )

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(participants=Count('payments'))
    #     return queryset
    #
    # @admin.decorators.display(description='Участников')
    # def in_favorites_count(self, obj):
    #     return obj.participants


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_date',
        'total',
        'payer__username',
        'collect__title'
    )
    search_fields = (
        'payer',
        'collect'
    )
