import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello", durable=True, arguments={"x-queue-type": "quorum"})
channel.basic_publish(exchange="", routing_key="hello", body="hello world :: rabbit mq")

print("sent message > hello world :: rabbit mq")
connection.close()
