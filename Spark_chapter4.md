# Chapter 4: Working with Key/Value pairs

A key/value pairs RDD is also called a pair RDD.

## Creating pair RDDs
Let's create a pair RDD having the first word of the line as the key.
* In Python
```python
pairs = lines.map(lambda x: (x.split(" ")[0], x)) 
```
From an in-memory collection, we can just call `SparkContext.parallelize()`.

* In Java
```java
PairFunction<String, String, String> keyData = new PairFunction<String, String, String>() {
    public Tuple2<String, String> call(String x) {
        return new Tuple2(x.split(" ")[0], x);
    }
};
JavaPairRDD<String, String> pairs = lines.mapToPair(keyData);
```
From an in-memory collection, we can just call `SparkContext.parallelizePairs()`.

## Transformations on pair RDDs
They can use the same trasnformations as on standard RDDs, and follow the same rules for the functions.

On one pair RDDs as {(1, 2), (3, 4), (5, 6)}:
* reduceByKey()
* groupByKey()
* combineByKey()
* mapValues()
* flatmapValues()
* keys()
* values()
* sortByKey()

On two pairs RDDs as rdd={(1, 2), (3, 4), (5, 6)}, other={(3, 9)}:
* substractByKey()
* join()
* rightOuterJoin()
* leftOuterJoin()
* cogroup()

[- Index](./README.md)  
[< Previous](./Spark_chapter3.md)  
[> Next](./Spark_chapter5.md)
