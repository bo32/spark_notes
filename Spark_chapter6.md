# Chapter 6: Advanced Spark programming
When calling a function in Spark, a variable can be passed as a parameter. Each driver on the cluster gets a copy of this variable. But if this variable gets updated, the changes are not propagated. To bypass this problem, Spark has some shared variables that can be used: *accumulators* and *broadcast variables*. 

## Accumulators
Accumulators are variables used for aggregating information accross the drivers in the cluster.

```python
file = sc.textFile(inputFile)
blankLines = sc.accumulator(0) # accumulator created, initialized to 0

def extractCallSigns(line):
    global blankLines
    if (line == "")
        blankLines += 1
    return line.split(" ")

callSigns = file.flatMap(extractCallSigns)
callSigns.saveAsTextFile(outputDir + "/callSigns") # first action, so the lazy transformations can be performed
print "Blank lines: %d" % blankLines.value # the value properly is explicitely called to get the value of the accumulator
```

### Accumulators and fault tolerance


### Custom accumulators

* __broadcast variables__: 
