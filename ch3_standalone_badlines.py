from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App") # cluster is defined here, and is localhost
sc = SparkContext(conf = conf)

inputRDD = sc.textFile("log.txt")
errorsRDD = inputRDD.filter(lambda x: "error" in x)
warningsRDD = inputRDD.filter(lambda x: "warning" in x)
badLinesRDD = errorsRDD.union(warningsRDD)

print "badLinesRDD had " + str(badLinesRDD.count()) + " lines."
print "Here are 10 of them:"
for line in badLinesRDD.take(10):
    print line
