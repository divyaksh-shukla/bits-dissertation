#!/bin/bash

# Script to start zookeeper and kafka servers

/usr/confluent-5.4.0/bin/zookeeper-server-start /usr/confluent-5.4.0/etc/kafka/zookeeper.properties &

/usr/confluent-5.4.0/bin/kafka-server-start /usr/confluent-5.4.0/etc/kafka/server.properties
