#/bin/bash

/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic $TOPIC_NAME --bootstrap-server broker-1:29092
echo "topic $TOPIC_NAME was created"
