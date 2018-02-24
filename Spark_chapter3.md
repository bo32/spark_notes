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
* __map()__: takes a function as a parameter and applies to the all elements of the RDD.
* __filter()__: takes a function as a parameter and returns the elements of the RDD matching the function.
* __flatmap()__: similar to map(), it transforms each eelement of the RDD to 0 or more elements.

```java
JavaRDD<Integer> rdd = sc.parallelize(Arrays.asList(1, 2, 3, 4));
JavaRDD<Integer> squares = rdd.map(new Function<Integer, Integer>() {
    public Integer call(Integer x) {
        return x * x;
    }
});

rdd = sc.parallelize(Arrays.asList("Hi there", "Apache Spark", "Lorem ipsum dolor"));
JavaRDD<Integer> splits = rdd.flatmap(new Function<String, String>() {
    public Iterable<String> call(String words) {
        return Arrays.asList(words.split(" "));
    }
});
```

#### Pseudo set operations
Spark also implements manipulation of sets:
* __distinct()__: produces a new RDD with unique elements (the duplicates are removed). Expensive executionexecution, as it requires shuffling. The RDDs must be of the same type.
* __union()__: returns a RDD containing the elements of 2 RDDs, including duplicates. The RDDs must be of the same type.
* __intersection()__: returns a RDD containing elements only in both input RDDs, removing duplicates. Expensive execution, as it requires shuffling. The RDDs must be of the same type.
* __substract()__: Returns a RDD that contains elements only in the first input RDD and not in the second. Expensive execution, as it requires shuffling. The RDDs must be of the same type.
* __cartesian()__: returns the product of 2 RDDs (all combinaisons possible of the elements). Ex: RDD1 [1, 2] x RDD ["Spark", "ML"] -> RDD3 [{1, "Spark"}, {2, "Spark"}, {1, "ML"}, {2, "ML"}]. Expensive execution for large RDDs.

#### Actions
* __reduce()__: useful some some aggregations, it returns the result of an operation applied on the elements of the RDD. The result is an element of the same type of the elements in the RDD.
```python
sum = rdd.reduce(lambda x, y: x + y)
```

* __fold()__: same as `reduce()` but add a *zero value* or *identity element* for the first call of the function. Ex: 0 for an addiction, 1 for a product, an empty list for a concatenation... The result is an element of the same type of the elements in the RDD.

* __aggregate()__: returns the result of an aggregation with a type that can be different from the type of the elements in the RDD. Also takes an *identity element*.
```python
sumCOunt = nums.aggregate((0, 0),
    (lambda acc, value: (acc[0] + value, acc[1] + 1)),
    (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1]))
)
return sumCount[0] / float(sumCount[1])
```

* __collect()__: returns the elements of a RDD. Commonly used in unit tests.

* __take()__: returns *n* first elements of a RDD.

* __top()__: returns the *n* last elements of a RDD.

* __takeOrdered()__: returns the *n* first elements of a RDD, according to the order defined by the ordering function passed as a parameter.

* __takeSample()__: returns *n* elements of a RDD, randomly picked.

* __foreach()__: applies a functions to the elements of the RDD.

* __count()__: returns the number of elements of a RDD.

* __countByValue()__: returns the number of occurences for each element of a RDD.

### Converting between RDD types

## Persistence (Caching)

**to be completed**

[- Index](./README.md)  
[< Previous](./Spark_chapter2.md)  
[> Next](./Spark_chapter4.md)
