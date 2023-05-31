# PoC KSQL - Acid Labs Data team

---

## Introducción:

**Descripción general de la herramienta/solución evaluada**.

![Diagrama sin título.png](/docs/architecture.png)

**Objetivos de la PoC**.

**Justificación de la PoC (por ejemplo, problemas o desafíos actuales que la herramienta/solución puede abordar)**.

**Metodología**

**Descripción del enfoque utilizado para realizar la PoC, incluyendo las fuentes de datos, casos de uso, pruebas y
métricas empleadas.**

## Resultados:

**Presentación de los resultados de las pruebas y evaluaciones realizadas durante la PoC, organizados por objetivos o
áreas de interés.**
(Incluir gráficos, tablas o visualizaciones para facilitar la comprensión de los resultados.)

**Análisis de los resultados obtenidos, discutiendo el rendimiento, la escalabilidad, la facilidad de uso, la seguridad
y otros aspectos relevantes de la herramienta/solución evaluada.**
(Comparación con soluciones existentes o alternativas, si corresponde.)

**Discusión de los desafíos o limitaciones encontradas durante la PoC.**

* Lack de documentacion, no existe casi documentacion al respecto, me costo encontrar un error, el cual era que si los
  datos dentro del json de kafka tienen reserved keywords, estas quedan como null en los stream de ksqldb

**Conclusiones y recomendaciones.**

**Recomendaciones para la implementación, la adopción o la mejora de la herramienta/solución, basadas en los resultados
de la PoC.**

**Referencias**

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

### Good documentation:

https://www.youtube.com/watch?v=Z8_O0wEIafw&t=1178s

https://ksqldb.io/