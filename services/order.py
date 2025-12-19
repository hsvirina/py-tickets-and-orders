from typing import Optional, List, Dict

from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession


User = get_user_model()


def create_order(
    *,
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = parse_datetime(date)
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
            )

        return order


def get_orders(username: str | None = None) -> list[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
