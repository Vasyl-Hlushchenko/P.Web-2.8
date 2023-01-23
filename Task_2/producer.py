from faker import Faker
from mongoengine import Document, connect
from mongoengine.fields import EmailField, StringField, BooleanField
import pika

connect(
    host="mongodb+srv://vasyliy:12345654321@cluster0.ay09rh2.mongodb.net/?retryWrites=true&w=majority",
    ssl=True,
)

fake = Faker("uk_Ua")


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField()
    city = StringField()
    birthday = StringField()
    send_massage = BooleanField(default=False)


def post_contact():
    for _ in range(10):
        new_contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            city=fake.city(),
            birthday=fake.date_of_birth().strftime("%d.%m.%Y"),
            send_massage=False,
        )
        new_contact.save()


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="sending email")

    contacts = Contact.objects()
    for contact in contacts:
        channel.basic_publish(
            exchange="", routing_key="sending email", body=f"{contact.id}".encode()
        )
        print(" [x] Sent email")
    connection.close()


if __name__ == "__main__":
    post_contact()
    main()
