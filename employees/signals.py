from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Balance, MonthBalanceStatistics, YearlyBalanceStatistics


@receiver(post_save, sender=Balance)
def balance_saved(sender, instance, created, **kwargs):
    """Balance yozilganda yoki o'zgarganda statistikani yangilash"""
    MonthBalanceStatistics.update_statistics(
        instance.employee,
        instance.date.year,
        instance.date.month
    )

    # Yillik statistikani ham yangilash
    YearlyBalanceStatistics.update_yearly_statistics(
        instance.employee,
        instance.date.year
    )


@receiver(post_delete, sender=Balance)
def balance_deleted(sender, instance, **kwargs):
    """Balance o'chirilganda statistikani yangilash"""
    MonthBalanceStatistics.update_statistics(
        instance.employee,
        instance.date.year,
        instance.date.month
    )

    # Yillik statistikani ham yangilash
    YearlyBalanceStatistics.update_yearly_statistics(
        instance.employee,
        instance.date.year
    )
