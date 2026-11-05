import os
import sys
import time

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True, arguments={"x-queue-type": "quorum"})
    print("waiting for messages")

    def callback(ch, method, properties, body):
        print(f"received message > {body.decode()}")
        time.sleep(5)
        print("worker done..")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="task_queue", on_message_callback=callback)

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
