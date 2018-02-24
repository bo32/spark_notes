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

Example of a **transformation**:
```python
>>> pythonLines = lines.filter(lambda line: "Python" in line)
```
Example of an **action**:
```python
>>> pythonLines.first()
```

The reason for the distinction between **transformations** and **actions** is, that Spark is lazy: the whole transformations are performed at the first called action, so that Spark saves some memory by loading only the necessary data.
In our example above, Spark doesn't do anything when calling `filter()`, but only does it when `first()` is called. So Spark knows that it doesn't have to read the whole file, since we only want the first line.

If we want to reuse a RDD on multiple actions, we can **persist** it but using the `persist()` method. The RDD is then stored in memory (of the cluster).

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
inputRDD = sc.textFile("log.txt")
errorsRDD = inputRDD.filter(lambda x: "error" in x)
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
errorsRDD = inputRDD.filter(lambda x: "error" in x)
warningsRDD = inputRDD.filter(lambda x: "warning" in x)
badLinesRDD = errorsRDD.union(warningsRDD)
```

Spark keeps track of the RDDs and where they come from. In the previous example, `badLinesRDD` comes from the union of `warningsRDD` and `errorsRDD`, both coming from a filtering of `inputRDD`.  
This is called the **_lineage graph_** (a bit like a family tree).

### Actions
They are the operations that return a result to the program or write data on an external storage system.

Here an example of actions based on `badLinesRDD` defined above:
```python
print "badLinesRDD had " + badLinesRDD.count() + " lines."
print "Here are 10 of them:"
for line in badLinesRDD.take(10):
    print line
```
See [this python code](./ch3_standalone_badlines.py) for a standalone example.

```java
System.out.println("badLinesRDD had " + badLinesRDD.count() + " lines.")
System.out.println("Here are 10 of them:")
for (String line: badLinesRDD.take(10)) {
    System.out.println(line);
}
```

The `take()` method retrieves a small number of elements of the RDD, so we can then loop on them.  
`collect()` does the same, but retrieves all the elements of the RDD. We need to be careful though with the latter, as the entire dataset should fit in the memory of a single machine, so it should not be used on large datasets.

Every time an action is called, the entire RDD is calculated from scratch, which can be inefficient. We can then persist intermediate results to prevent from this [more here](#persistence-caching).

### Lazy Evaluation
Since the transformations are lazy, it's best to think of transformations as instructions on how to compute the data, instead as a "dataset" or RDD that would contain the data.  
In practive, when Spark sees a transformation, it records it internally as some metadata.  
Loading data from a source (like a file), is also lazily performed.

## Passing functions to Spark
Functions can be passed into Spark and used to compute data. They have different specificities according to the Spark core language.

### Python
We can use [lambda functions](https://en.wikipedia.org/wiki/Anonymous_function#Python) (mini-functions defined on the fly):
```python
word = rdd.filter(lambda s: "error" in s)
```

We can also use locally defined functions:
```python
def containsError(s):
    return "error" in s
word = rdd.filter(containsError)
```
When doing this, we must be careful that we don't pass the object containing the function, which would cause passing larger data to the program (like self.myproperty). Good practice would to extract the property value and pass to the function.

### Scala
Inline functions, references to methods, or static functions can be passed in Scala.

The inconvenient we have in Python is also present in Scala.

### Java
In Java, a function is an object that implements the interface `org.apache.spark.api.java.function.Function`.

## Common Transformations and Actions
### Basic RDDs
#### Element-wise transformations
* map(): takes a function as a parameter and applies to the all elements of the RDD.
* filter(): takes a function as a parameter and returns the elements of the RDD matching the function.

```java
JavaRDD<Integer> rdd = sc.parallelize(Arrays.asList(1, 2, 3, 4));
JavaRDD<Integer> squares = rdd.map(new Function<Integer, Integer>() {
    public Integer call(Integer x) {
        return x * x;
    }
});
```

## Persistence (Caching)

**to be completed**

[- Index](./README.md)  
[< Previous](./Spark_chapter2.md)  
[> Next](./Spark_chapter4.md)
