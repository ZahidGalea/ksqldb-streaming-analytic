from confluent_kafka import Producer
import time

# Debes reemplazar 'localhost:9092' con la dirección IP y el puerto de tu servicio Kafka
# Si estás usando Minikube, puedes obtener la dirección IP con 'minikube ip'
# y el puerto con 'kubectl get service kafka-service'
p = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    """ Muestra si se ha producido un error al enviar el mensaje """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

for data in ['Hello, Kafka', 'Goodbye, Kafka']:
    p.produce('mytopic', data.encode('utf-8'), callback=delivery_report)
    p.poll(0)

p.flush()
