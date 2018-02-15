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
Transformations return a new RDD, and Actions return a result.

### Transformations
Transformations return a new RDD and are performed lazily, only at the moment of a call of an action.

```python
>>> inputRDD = sc.textFile("log.txt")
>>> errorsRDD = inputRDD.filter(lambda x: "error" in x)
```

```java
JavaRDD<String> inputRDD = sc.textFile("log.txt");
JavaRDD<String> errorsRDD = inputRDD.filter(
    new Function<String, Boolean>() {
        public Boolean call(String x) {
            return x.contains("error");
        }
    }
);
```

In these examples, `filter()` does not mutate `inputRDD`, but returns a pointer to a new RDD. `inputRDD` can then be reused later on:

```python
>>> errorsRDD = inputRDD.filter(lambda x: "error" in x)
>>> warningsRDD = inputRDD.filter(lambda x: "warning" in x)
>>> badLinesRDD = errorsRDD.union(warningsRDD)
```

Spark keeps track of the RDDs and where they come from. In the previous example, `badLinesRDD` comes from the union of `warningsRDD` and `errorsRDD`, both coming from a filtering of `inputRDD`.  
This is called the **_lineage graph_** (a bit like a family tree).

### Actions
They are the operations that return a result to the program or write data on an external storage system.

[- Index](./Spark.md)  
[< Previous](./Spark_chapter2.md)  
[> Next](./Spark_chapter4.md)
