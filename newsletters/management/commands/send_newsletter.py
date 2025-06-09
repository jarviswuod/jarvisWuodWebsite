
from django.core.management.base import BaseCommand
from newsletter.models import Newsletter, Subscriber
from newsletter.utils import send_newsletter_email


class Command(BaseCommand):
    help = 'Send a specific newsletter to all active subscribers'

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int,
                            help='Newsletter ID to send')

    def handle(self, *args, **options):
        try:
            newsletter = Newsletter.objects.get(id=options['newsletter_id'])
            if newsletter.is_sent:
                self.stdout.write(
                    self.style.ERROR('This newsletter has already been sent.')
                )
                return

            active_subscribers = Subscriber.objects.filter(is_active=True)
            sent_count = 0

            for subscriber in active_subscribers:
                if send_newsletter_email(newsletter, subscriber):
                    sent_count += 1

            newsletter.is_sent = True
            newsletter.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully sent newsletter to {sent_count} subscribers'
                )
            )

        except Newsletter.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Newsletter not found')
            )
