# Chapter 1: Introduction to Data Analysis with Spark
## What is Apache Spark?
Apache Spark is an open source project, created in 2009. It includes a unified stack composed of:
 - __Spark Core__: includes task scheduling, memory management, interactions with storage elements, fault recovery… Also contains the API for Resilient Distributed Datasets (RDD), main abstraction level of Spark.
 - __Spark SQL__: allows querying data via SQL and Apache Hive Query Language (HQL), from databases, JSON… Can be mixed with data manipulation in Python, Java and Scala.
 - __Spark Streaming__: enables processing live streams of data.
 - __MLib__: Machine Learning functionalities, like regression, classification, clustering, collaborative filtering, data import. Can be distributed in a cluster.
 - __GraphX__: manipulates graphs.
 - __Cluster Managers__: scales up the charge of processing on several nodes / machines. Cluster managers can be Hadoop YARN, Apache Mesos, or Spark's own: Standalone Scheduler. More about it [here](./Spark_chapter7.md).


[- Index](./README.md)  
[> Next](./Spark_chapter2.md)  
