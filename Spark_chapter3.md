# Chapter 3: Programming with RDDs
## Basics
A Resilient Distributed Dataset (RDD) is simply a distributed collection of elements. In Spark, everything we do is about creating RDDs, transforming RDDs, or performing some operations on RDDs to get a result.  
The RDDs can contain and manipulate any type of data, even user created objects. In our previous examples, we were manipulating RDDs of strings.  

Here is the creation of a RDD:
```python
>>> lines = sc.textFile("README.md")
```
2 kinds of operations can be done on a RDD:
* transformation: construction of a RDD from another. It returns a RDD.
* action: calculates a result based on a RDD. It return a non-RDD data type object.

Example of a `transformation`:
```python
>>> pythonLines = lines.filter(lambda line: "Python" in line)
```
Example of an `action`:
```python
>>> pythonLines.first()
```

The reason for the distinction between `transformations` and `actions` is, that Spark is lazy: the whole transformations are performed at the first called action, so that Spark saves some memory by loading only the necessary data.
In our example above, Spark doesn't do anything when calling `filter()`, but only does it when `first()` is called. So Spark knows that it doesn't have to read the whole file, since we only want the first line.

If we want to reuse a RDD on multiple actions, we can `persist` it but using the `persist()` method. The RDD is then stored in memory (of the cluster).

```python
>>> pythonLines.persist()
>>> pythonLines.count()
>>> pythonLines.first()
```

## Creating a RDD
An RDD can be created by loading and external dataset (from a file, for example) or parallelizing a collection (a collection defined on the fly).

```python
>>> lines = sc.parallelize(["pandas", "bears"])
>>> lines = sc.textFile("./README.md")
```

```java
JavaRDD<String> lines = sc.parallelize(Arrays.asList("pandas", "bears"));
lines = sc.textFile("./README.md");
```

## RDD Operations





[- Index](./Spark.md)  
[< Previous](./Spark_chapter2.md)  
[> Next](./Spark_chapter4.md)
