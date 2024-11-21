from django.contrib import admin
from .models import Product, Category, Checkout
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    search_fields = ('title', 'description')
    list_filter = ('category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'approval_status', 'order_status', 'payment_status', 'created_at')
    list_filter = ('approval_status', 'order_status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'order_items')
    readonly_fields = ('created_at', 'user', 'total_price', 'payment_status')
    actions = ['accept_order', 'reject_order']

    # Action to accept the order
    def accept_order(self, request, queryset):
        updated = queryset.filter(approval_status='Pending').update(approval_status='Accepted', order_status='Processing')
        self.message_user(request, f"{updated} orders have been accepted.")
    accept_order.short_description = "Accept selected orders"

    # Action to reject the order
    def reject_order(self, request, queryset):
        updated = queryset.filter(approval_status='Pending').update(approval_status='Rejected', order_status='Rejected')
        self.message_user(request, f"{updated} orders have been rejected.")
    reject_order.short_description = "Reject selected orders"