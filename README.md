# PoC KSQL - Acid Labs Data team

---

## Introducción:

**Descripción general de la herramienta/solución evaluada**.

![Diagrama sin título.png](/docs/architecture.png)



Esta prueba de concepto (PoC) se realizó para evaluar una solución de procesamiento de datos en tiempo real
utilizando Apache Kafka y ksqlDB. Kafka es una plataforma de streaming distribuida que permite publicar y 
suscribir a colas de registros, pero con capacidad de almacenamiento. ksqlDB, 
por otro lado, es un sistema de base de datos para flujos de eventos en tiempo real 
que permite ejecutar consultas SQL hacia topicos kafka directamente.

**Objetivos de la PoC**.

El objetivo de esta PoC es determinar la facilidad de implementacion y practicar el uso de de Kafka y ksqlDB

**Justificación de la PoC (por ejemplo, problemas o desafíos actuales que la herramienta/solución puede abordar)**.

Dado el creciente volumen de datos generados por las operaciones comerciales, se ha vuelto esencial 
para las empresas procesar y analizar estos datos en tiempo real para tomar decisiones basadas en datos.
Como ACID queremos estar a la par de las tecnologias innovadoras

**Metodología**

Para llevar a cabo esta PoC, utilizamos un conjunto de datos de prueba que consiste en eventos generados por un simulador.
Realizamos una serie de pruebas que incluyen la ingestión de datos y el procesamiento en tiempo real.


## Resultados:

**Presentación de los resultados de las pruebas y evaluaciones realizadas durante la PoC, organizados por objetivos o
áreas de interés.**
(Incluir gráficos, tablas o visualizaciones para facilitar la comprensión de los resultados.)

![kafkaui.png](/docs/kafkaui.png)

![img.png](/docs/img.png)

**Discusión de los desafíos o limitaciones encontradas durante la PoC.**

* Lack de documentacion, no existe casi documentacion al respecto, me costo encontrar un error, el cual era que si los
  datos dentro del json de kafka tienen reserved keywords, estas quedan como null en los stream de ksqldb


**Referencias**

https://www.youtube.com/watch?v=Z8_O0wEIafw&t=1178s

https://ksqldb.io/


---

## How to replicate

**requirements**:

* kubectl
* minikube
* helm
* kustomize

---

* Deploys kafka cluster with data in it. also a ksqldb and visualization.
  ```bash
  kubectl kustomize --enable-helm . | kubectl apply -f -
  ```
* If you want to monitor the kafka server.
  ```bash
  minikube service kafka-ui --url
  ```
* to use kafkasql cli use the following command.
  ```bash
  kubectl delete pod ksql-cli
  kubectl run -i --rm --tty ksql-cli --image=confluentinc/ksqldb-cli:latest --restart=Never -- ksql http://ksqldb-service:8088
  ```

* to use a python script to test kafka api
  ```bash
  # First expose the pod port, not required in case your script is in minikube
  kubectl port-forward service/ksqldb-service 8088:8088
  # Run your python scripts in a new terminal...
  ```

* to deploy visualization
  ```bash
  # Build consumption image, first deployment will be failing if this step is not produced
  docker build -t "zahidgalea/data-visualization:0.2.7" -f consumption/Dockerfile consumption/
  docker push zahidgalea/data-visualization:0.2.7
  ```
  ```bash
  kubectl port-forward service/data-visualization-service 5006:5006
  # Open localhost:5006 in your web browser
  ```

* To delete everything
  ```bash
  kubectl kustomize --enable-helm . | kubectl delete -f -
  ```

---

### How to contribute

* Fork the project or clone it
* Create your own branch following this pattern:
    * type/your initials/title or jira issue
        * type:
            * feature
            * hotfix
* Open a PR and assing it to @Zahid Galea

---