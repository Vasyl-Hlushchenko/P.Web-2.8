from producer import Contact
import pika


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="sending email")

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        contact = Contact.objects(id=contact_id)
        contact.update(send_massage=True)
        print(" [x] Received email:", body.decode())

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue="sending email", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


if __name__ == "__main__":
    main()
