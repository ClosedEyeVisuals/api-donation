from django.db.models import Count, Sum
from django.contrib import admin


from donations.models import Collect, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    inlines = (PaymentInline,)
    list_display = (
        'title',
        'reason',
        'finish_at',
        'owner',
        'participants',
        'collected',
        'goal_value'
    )
    search_fields = (
        'title',
        'owner__email'
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(participants=Count('payments'),
                                     collected=Sum('payments__total'))
        return queryset

    @admin.decorators.display(description='Участников')
    def participants(self, obj):
        return obj.participants

    @admin.decorators.display(description='Собрано')
    def collected(self, obj):
        return obj.collected


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'collect',
        'total',
        'payment_date',
        'payer'

    )
    search_fields = (
        'payer',
        'collect'
    )
