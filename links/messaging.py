# from celery.messaging import establish_connection
# from kombu.compat import Publisher, Consumer
# from links.models import Click

# def send_increment_clicks(obj, pk):
# 	"""Send a message for incrementing the click count for an URL."""
# 	connection = establish_connection()
# 	publisher = Publisher(connection=connection, exchange="clicks", routing_key="increment_click", exchange_type="direct")

# 	publisher.send(obj, pk)

# 	publisher.close()
# 	connection.close()


# def process_clicks():
# 	connection = establish_connection()
# 	consumer = Consumer(connection=connection, queue="clicks", exchange="clicks", routing_key="increment_click", exchange_type="direct")

# 	clicks_for_url = {}
# 	message_for_url = {}

# 	for message in consumer.iterqueue():
# 		obj = message.body
# 		clicks_for_url[obj]= clicks_for_url.get(obj, 0) + 1
# 		if obj in messages_for_url:
# 			messages_for_url[obj].append(message)
# 		else:
# 			messages_for_url[obj] = [message]

# 	for obj, click_count in clicks_for_url.items():
# 		Click.objects.increment_click(obj, click_count)
# 		[message.ack() for message in messages_for_url[obj]]

# 	consumer.close()
# 	connection.close()
