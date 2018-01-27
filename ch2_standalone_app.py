from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("My App") # cluster is defined here, and is localhost
sc = SparkContext(conf = conf)

lines = sc.textFile("Spark.md")
print str(lines.count()) + " lines"

pythonLines = lines.filter(lambda line: "Spark" in line)
print "First line with Spark: " + pythonLines.first().encode('utf-8')