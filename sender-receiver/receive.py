import os
import sys

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="hello", durable=True, arguments={"x-queue-type": "quorum"})

    def callback(ch, method, properties, body):
        print(f"received > {body.decode()}")
        channel.queue_delete(queue="hello")

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    print("waiting for messages")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("stopped")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
