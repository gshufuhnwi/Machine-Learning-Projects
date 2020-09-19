
Gerard Shu Fuhnwi
Home Work 2

Reading the data
walmart = spark.read.format("csv").option("inferSchema", "true").option("header", "true").load("/home/gshu/Downloads/walmart.csv")

Question 1

from pyspark.sql.functions import *                                         
>>> walmart.select(max("Weekly_Sales")).show()
+-----------------+                                                             
|max(Weekly_Sales)|
+-----------------+
|        693099.36|
+-----------------+

Question 2

walmart.select("dept","store","weekly_sales").where("weekly_sales==693099.36").show()
+----+-----+------------+                                                       
|dept|store|weekly_sales|
+----+-----+------------+
|  72|   10|   693099.36|
+----+-----+------------+

Question 3

walsort = walmart.orderBy(col("Store").asc())
walsort.groupBy("Store").avg("Weekly_Sales").show()
+-----+------------------+                                                      
|Store| avg(Weekly_Sales)|
+-----+------------------+
|    1|21710.543620655928|
|    2|26898.070031256142|
|    3| 6373.033982957042|
|    4| 29161.21041471962|
|    5| 5053.415812868114|
|    6|21913.243623543225|
|    7| 8358.766148330214|
|    8|13133.014768064626|
|    9| 8772.890378933093|
|   10|26332.303818710607|
|   11| 19276.76275094412|
|   12|14867.308619268337|
|   13| 27355.13689134987|
|   14|28784.851727091544|
|   15|  9002.49307342695|
|   16| 7863.224123689504|
|   17|12954.393636455781|
|   18|15733.313136220786|
|   19|20362.126734331836|
|   20|29508.301591932617|
+-----+------------------+

Question 4

NegativeR = walmart.select("weekly_sales").where("weekly_sales<0")
>>> NegativeR.count()
1285 

Question 5

Records2011 = walmart.where("Date >= '2011-00-00' AND Date <= '2011-12-31'")
Records2011.count()

153453

Question 6. For this question, I created a new dataset

case class walmartdata(Store: BigInt, Dept: BigInt, Date: String, Weekly_Sales: Double, IsHoliday: Boolean)
defined class walmartdata

scala> val walD = walmart.as[walmartdata]
import org.apache.spark.sql.functions._

 walD.map( x => walmartdata(x.Store, x.Dept, x.Date, x.Weekly_Sales/1000, x.IsHoliday)).show(20)
+-----+----+-------------------+------------------+---------+                   
|Store|Dept|               Date|      Weekly_Sales|IsHoliday|
+-----+----+-------------------+------------------+---------+
|    1|   1|2010-02-05 00:00:00|           24.9245|    false|
|    1|   1|2010-02-12 00:00:00|          46.03949|     true|
|    1|   1|2010-02-19 00:00:00|          41.59555|    false|
|    1|   1|2010-02-26 00:00:00|          19.40354|    false|
|    1|   1|2010-03-05 00:00:00|21.827900000000003|    false|
|    1|   1|2010-03-12 00:00:00|          21.04339|    false|
|    1|   1|2010-03-19 00:00:00|          22.13664|    false|
|    1|   1|2010-03-26 00:00:00|          26.22921|    false|
|    1|   1|2010-04-02 00:00:00|          57.25843|    false|
|    1|   1|2010-04-09 00:00:00|42.960910000000005|    false|
|    1|   1|2010-04-16 00:00:00|          17.59696|    false|
|    1|   1|2010-04-23 00:00:00|          16.14535|    false|
|    1|   1|2010-04-30 00:00:00|          16.55511|    false|
|    1|   1|2010-05-07 00:00:00|          17.41394|    false|
|    1|   1|2010-05-14 00:00:00|18.926740000000002|    false|
|    1|   1|2010-05-21 00:00:00|14.773040000000002|    false|
|    1|   1|2010-05-28 00:00:00|          15.58043|    false|
|    1|   1|2010-06-04 00:00:00|          17.55809|    false|
|    1|   1|2010-06-11 00:00:00|          16.63762|    false|
|    1|   1|2010-06-18 00:00:00|          16.21627|    false|
+-----+----+-------------------+------------------+---------+
only showing top 20 rows

Question 7 . I still used the dataset I created above

walD.filter(v => v.Weekly_Sales<0).map(fr => walmartdata(fr.Store, fr.Dept, fr.Date, -fr.Weekly_Sales, fr.IsHoliday)).show(20)

-----+----+-------------------+------------+---------+                         
|Store|Dept|               Date|Weekly_Sales|IsHoliday|
+-----+----+-------------------+------------+---------+
|    1|   6|2012-08-10 00:00:00|      139.65|    false|
|    1|  18|2012-05-04 00:00:00|        1.27|    false|
|    1|  47|2010-02-19 00:00:00|       863.0|    false|
|    1|  47|2010-03-12 00:00:00|       698.0|    false|
|    1|  47|2010-10-08 00:00:00|        58.0|    false|
|    1|  47|2011-04-08 00:00:00|       298.0|    false|
|    1|  47|2011-07-08 00:00:00|       198.0|    false|
|    1|  47|2011-10-14 00:00:00|       498.0|    false|
|    1|  47|2011-12-23 00:00:00|       498.0|    false|
|    1|  47|2012-02-17 00:00:00|       198.0|    false|
|    1|  47|2012-03-16 00:00:00|       199.0|    false|
|    1|  48|2012-03-23 00:00:00|       223.0|    false|
|    1|  54|2011-01-21 00:00:00|        50.0|    false|
|    1|  54|2011-05-20 00:00:00|        15.0|    false|
|    1|  54|2012-03-09 00:00:00|        21.0|    false|
|    2|  18|2012-06-01 00:00:00|        1.97|    false|
|    2|  18|2012-07-27 00:00:00|        3.03|    false|
|    2|  45|2010-04-09 00:00:00|       118.0|    false|
|    2|  45|2010-05-07 00:00:00|        0.98|    false|
|    2|  47|2010-07-30 00:00:00|      1098.0|    false|
+-----+----+-------------------+------------+---------+


Question 9

import org.apache.spark.sql.functions._

val DH = walmart.select("*").where("Weekly_Sales<0 AND IsHoliday==true").count()
DH: Long = 98                                                                   

val ALLD = walmart.select("*").where("IsHoliday==true").count()
ALLD: Long = 29661   

val ratiodownday_allholidays =( DH.toFloat/ALLD.toFloat)*100
ratiodownday_allholidays: Float = 0.3304002

val DHNon = walmart.select("*").where("Weekly_Sales<0 AND IsHoliday==false").count()
DHNon: Long = 1187                                                              

scala> val ALLD = walmart.select("*").where("IsHoliday==true").count()
ALLD: Long = 29661                                                              

scala> val ALLDNon = walmart.select("*").where("IsHoliday==false").count()
ALLDNon: Long = 391909                                                          

scala> val rationondownday = (DHNon.toFloat/ALLDNon.toFloat)*100
rationondownday: Float = 0.30287644

Down days are most likely to happen on Holidays, because the percentage is higher than that for non-holidays.
