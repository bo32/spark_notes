# Chapter 2: Downloading Spark and getting started
Apache Spark can be downloaded on the [project site](https://spark.apache.org/downloads.html).

## Start Apache Spark with Python
Run the following command, from the extracted archive of Apache Spark:
```bash
$ bin/pyspark
```

## Core Spark Concepts
A SparkContext object is created by the Spark app (when opening a Spark shell, for example), that is a connection to a cluster. It’s stored in the **sc** variable.
When having a cluster, executing a command like ``lines.count()`` will be performed by a cluster.

### Example in Python
```python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App") # cluster is defined here, and is localhost
sc = SparkContext(conf = conf)

lines = sc.textFile("Spark.md")
print str(lines.count()) + " lines"

pythonLines = lines.filter(lambda line: "Spark" in line)
print "First line with Spark: " + pythonLines.first().encode('utf-8')
```

Run the program via the command:
```bash
$ ~/spark-2.2.1-bin-hadoop2.7/bin/spark-submit ch2_standalone_app.py
```

### Example in Java
```xml
<project 
    xmlns="http://maven.apache.org/POM/4.0.0" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	
	<modelVersion>4.0.0</modelVersion>
	<groupId>com.david.spark</groupId>
	<artifactId>spark-standalone-app</artifactId>
	<version>0.0.1-SNAPSHOT</version>

	<dependencies>
		<dependency>
			<groupId>org.apache.spark</groupId>
			<artifactId>spark-core_2.10</artifactId>
			<version>2.2.1</version>
		</dependency>
	</dependencies>
    
	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-jar-plugin</artifactId>
				<configuration>
					<archive>
						<manifest>
							<mainClass>com.david.spark.Sample</mainClass>
						</manifest>
					</archive>
				</configuration>
			</plugin>
		</plugins>
	</build>
</project>
```

```java
package com.david.spark;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

public class Sample {
	
	public static void main(String[] args) {
		SparkConf conf = new SparkConf().setMaster("local").setAppName("My App");
		JavaSparkContext sc = new JavaSparkContext(conf);
		JavaRDD<String> lines = sc.textFile("src/main/resources/test.txt");
		System.out.println(lines.count());
	}
}
```

When building a standalone application, we first need to implement a Spark Context by providing it with a cluster (in our example `local`) and a name (in our example `My App`). The latter is a way of identifying the application.

```bash
$ mvn clean build
$ ~/spark-2.2.1-bin-hadoop2.7/bin/spark-submit target/spark-standalone-app-0.0.1-SNAPSHOT.jar 
```


[Index](./Spark.md)
[Previous](./Spark_chapter1.md)
[Next](./Spark_chapter3.md)
