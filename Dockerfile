FROM ubuntu:22.04

ARG SPARK_VERSION=3.4.4
ARG HADOOP_VERSION=3
ARG JAVA_VERSION=17
ARG PYTHON_VERSION=3.11

ENV SPARK_HOME=/opt/spark
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64
ENV PYSPARK_PYTHON=python${PYTHON_VERSION}
ENV PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin:$JAVA_HOME/bin

# Delta Lake configs
ENV PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:2.4.0 --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"

RUN apt-get update && apt-get install -y \
    openjdk-${JAVA_VERSION}-jdk wget python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Instalar Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -zxvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Instalar dependências Python
COPY kedro-pyspark-data-processing/requirements.txt /tmp/
RUN python${PYTHON_VERSION} -m pip install --upgrade pip && \
    python${PYTHON_VERSION} -m pip install -r /tmp/requirements.txt

# Copiar todo o projeto para dentro do container
COPY kedro-pyspark-data-processing /app/kedro-pyspark-data-processing

WORKDIR /app/kedro-pyspark-data-processing

# Rodar o pipeline Kedro
CMD ["kedro", "run"]