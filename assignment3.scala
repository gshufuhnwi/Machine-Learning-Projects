
Home Work 3 5040

Gerard Shu Fuhnwi

Question 1
var CoinBaseDF = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/home/gshu/Downloads/coinbaseUSD_1-min_data_2014-12-01_to_2018-06-27.csv")

CoinBaseDF.show(1)
+----------+-----+-----+-----+-----+------------+-----------------+--------------+
| Timestamp| Open| High|  Low|Close|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+-----+-----+-----+-----+------------+-----------------+--------------+
|1417411980|300.0|300.0|300.0|300.0|        0.01|              3.0|         300.0|
+----------+-----+-----+-----+-----+------------+-----------------+-------------

var CoinCheckDF = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/home/gshu/Downloads/coincheckJPY_1-min_data_2014-10-31_to_2018-06-27.csv")

+----------+-----+-----+-----+-----+------------+-----------------+--------------+
| Timestamp| Open| High|  Low|Close|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+-----+-----+-----+-----+------------+-----------------+--------------+
|1414735920|36880|36880|36880|36880|      0.0951|         3507.288|       36880.0|
+----------+-----+-----+-----+-----+------------+-----------------+--------------+


var BitStampDF=spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/home/gshu/Downloads/bitstampUSD_1-min_data_2012-01-01_to_2018-06-27.csv")

BitStampDF.show(1)
+----------+----+----+----+-----+------------+-----------------+--------------+ 
| Timestamp|Open|High| Low|Close|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+----+----+----+-----+------------+-----------------+--------------+
|1325317920|4.39|4.39|4.39| 4.39|  0.45558087|     2.0000000193|          4.39|
+----------+----+----+----+-----+------------+-----------------+--------------+

var BitFlyerDF = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/home/gshu/Downloads/bitflyerJPY_1-min_data_2017-07-04_to_2018-06-27.csv")

+----------+------+------+------+------+------------+-----------------+--------------+
| Timestamp|  Open|  High|   Low| Close|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+------+------+------+------+------------+-----------------+--------------+
|1499155260|296127|296558|296016|296540|      1.1586|      343244.1384|  296257.67168|
+----------+------+------+------+------+------------+-----------------+---------

Question 2

var CB = CoinBaseDF.withColumnRenamed("Close", "CoinBase")
CB.show(1)
+----------+-----+-----+-----+--------+------------+-----------------+--------------+
| Timestamp| Open| High|  Low|CoinBase|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+-----+-----+-----+--------+------------+-----------------+--------------+
|1417411980|300.0|300.0|300.0|   300.0|        0.01|              3.0|         300.0|
+----------+-----+-----+-----+--------+------------+-----------------+----------

var CC = CoinCheckDF.withColumnRenamed("Close", "CoinCheck")

CC.show(1)
+----------+-----+-----+-----+---------+------------+-----------------+--------------+
| Timestamp| Open| High|  Low|CoinCheck|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+-----+-----+-----+---------+------------+-----------------+--------------+
|1414735920|36880|36880|36880|    36880|      0.0951|         3507.288|       36880.0|
+----------+-----+-----+-----+---------+------------+-----------------+---------

var BS = BitStampDF.withColumnRenamed("Close", "BitStamp")

+----------+----+----+----+--------+------------+-----------------+--------------+
| Timestamp|Open|High| Low|BitStamp|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+----+----+----+--------+------------+-----------------+--------------+
|1325317920|4.39|4.39|4.39|    4.39|  0.45558087|     2.0000000193|          4.39|

var BF = BitFlyerDF.withColumnRenamed("Close","BitFlyer")

+----------+------+------+------+---------+------------+-----------------+--------------+
| Timestamp|  Open|  High|   Low| BitFlyer|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+------+------+------+---------+------------+-----------------+--------------+
|1499155260|296127|296558|296016|   296540|      1.1586|      343244.1384|  296257.67168|
+----------+------+------+------+---------+------------+-----------------+------

Question 3

var JoinDF= CB.join(CC, "Timestamp").join(BS, "Timestamp").join(BF, "Timestamp")
JoinDF.count()
Long = 511575  

-----+-------+-------+-------+--------+------------+-----------------+--------------+------+------+------+---------+------------+-----------------+--------------+-------+-------+-------+--------+------------+-----------------+--------------+------+------+------+---------+------------+-----------------+--------------+
| Timestamp|   Open|   High|    Low|CoinBase|Volume_(BTC)|Volume_(Currency)|Weighted_Price|  Open|  High|   Low|CoinCheck|Volume_(BTC)|Volume_(Currency)|Weighted_Price|   Open|   High|    Low|BitStamp|Volume_(BTC)|Volume_(Currency)|Weighted_Price|  Open|  High|   Low| BitFlyer|Volume_(BTC)|Volume_(Currency)|Weighted_Price|
+----------+-------+-------+-------+--------+------------+-----------------+--------------+------+------+------+---------+------------+-----------------+--------------+-------+-------+-------+--------+------------+-----------------+--------------+------+------+------+---------+------------+-----------------+--------------+
|1499165640|2590.69|2590.69|2590.69| 2590.69|        0.26|         673.5794|       2590.69|291869|291869|291214|   291717|  3.41662505|     995866.11872|  291476.56068|2593.21|2593.21|2593.21| 2593.21|  0.13059644|     338.66399417|       2593.21|291971|291986|291760|   291760|  3.37423797|     984541.37113|  291781.84227|
+----------+-------+-------+-------+-

Question 4

var selectFiveDF = JoinDF.select("Timestamp", "CoinBase", "BitFlyer", "BitStamp", "CoinCheck")
electFiveDF.show(5)
+----------+--------+--------+--------+---------+                               
| Timestamp|CoinBase|BitFlyer|BitStamp|CoinCheck|
+----------+--------+--------+--------+---------+
|1499165640| 2590.69|  291760| 2593.21|   291717|
|1499182620|  2582.0|  291041| 2575.88|   291230|
|1499192400|  2592.3|  290599| 2582.37|   290876|
|1499201460| 2584.77|  291500| 2582.92|   291712|
|1499206800| 2592.96|  292780|  2590.0|   292532|
+----------+--------+--------+--------+---------+

Question 5
var AverageDF = selectFiveDF.select(avg("CoinBase").alias("avg_coinbase"), avg("BitFlyer").alias("avg_BitFlyer"),avg("BitStamp").alias("avg_bitstamp"),avg("CoinCheck").alias("avg_coincheck"))

+-----------------+-----------------+------------------+-----------------+      
|     avg_coinbase|     avg_BitFlyer|      avg_bitstamp|    avg_coincheck|
+-----------------+-----------------+------------------+-----------------+
|7829.741536451156|875535.1022489371|7803.3529590773505|871944.2258613106|
+-----------------+-----------------+------------------+-----------------+

Question 6

var SampleStd = selectFiveDF.select(stddev_samp("CoinBase"), stddev_samp("CoinCheck"), stddev_samp("BitStamp"), stddev_samp("BitFlyer")) 

SampleStd.show()
+---------------------+----------------------+---------------------+---------------------+
|stddev_samp(CoinBase)|stddev_samp(CoinCheck)|stddev_samp(BitStamp)|stddev_samp(BitFlyer)|
+---------------------+----------------------+---------------------+---------------------+
|   3745.9565719572693|    438059.62103949254|   3701.5838070501454|   440008.46528322017|
+---------------------+----------------------+---------------------+------------

Question 7

var Coefvar = selectFiveDF.select((stddev_samp("CoinBase")/avg("CoinBase")).alias("coefvar_coinbase"),(stddev_samp("CoinCheck")/avg("CoinCheck")).alias("coefvar_coincheck"),(stddev_samp("BitStamp")/avg("BitStamp")).alias("coefvar_bitstamp"))

+------------------+------------------+-------------------+------------------+  
|  coefvar_coinbase| coefvar_coincheck|   coefvar_bitstamp|  coefvar_bitflyer|
+------------------+------------------+-------------------+------------------+
|0.4784265935878045|0.5023940844459118|0.47435811585893095|0.5025594795148652|
+------------------+------------------+-------------------+------------------+

Question 8

BitStamp has the smallest coefficient of variation, hence it is stable to price fluctuations.


Question 9

var TimeStampDF = selectFiveDF.select(expr("Timestamp/86400 as timestampdivide")

TimeStampDF.show(5)
+------------------+                                                            
|   timestampdivide|
+------------------+
|17351.454166666666|
|17351.650694444445|
| 17351.76388888889|
|       17351.86875|
|17351.930555555555|
+------------------+

Converting to Floor, that is roundUp

var TimeStampDiv =  selectFiveDF.select(floor(expr("Timestamp/86400")).alias("timestampdivide"))

TimeStampDiv.show(10)
+---------------+                                                               
|timestampdivide|
+---------------+
|          17351|
|          17351|
|          17351|
|          17351|
|          17351|
|          17351|
|          17352|
|          17353|
|          17353|
|          17353|
+---------------+


Counts

TimeStampDiv.select(countDistinct("timestampdivide")).show()
+-------------------------------+                                               
|count(DISTINCT timestampdivide)|
+-------------------------------+
|                            357|
+-------------------------------+


Question 10

TimeStampDiv.select(approx_count_distinct("timestampdivide", 0.1)).show() 
+--------------------------------------+                                        
|approx_count_distinct(timestampdivide)|
+--------------------------------------+
|                                   346|
+--------------------------------------+


