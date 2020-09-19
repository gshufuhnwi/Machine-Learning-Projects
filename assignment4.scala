
Gerard Shu Fuhnwi

Home work 4

Question 1

val NM = spark.read.format("csv").option("header", "true").option("inferSchema", "true").option("delimiter", ",").load("/home/gshu/Downloads/NM.TXT")

NM.show(2)
+-----+---+----+-----+-----+                                                    
|State|Sex|Year| Name|Count|
+-----+---+----+-----+-----+
|   NM|  F|1910| Mary|   98|
|   NM|  F|1910|Maria|   40|
+-----+---+----+-----+-----+

val OK = spark.read.format("csv").option("header", "true").option("inferSchema", "true").option("delimiter", ",").load("/home/gshu/Downloads/OK.TXT")

OK.show(2)
+-----+---+----+----+-----+                                                     
|State|Sex|Year|Name|Count|
+-----+---+----+----+-----+
|   OK|  F|1910|Mary|  326|
|   OK|  F|1910|Ruth|  165|
+-----+---+----+----+-----+

val LA = spark.read.format("csv").option("header", "true").option("inferSchema", "true").option("delimiter", ",").load("/home/gshu/Downloads/LA.TXT")

 LA.show(2)
+-----+---+----+-----+-----+                                                    
|State|Sex|Year| Name|Count|
+-----+---+----+-----+-----+
|   LA|  F|1910| Mary|  586|
|   LA|  F|1910|Annie|  169|
+-----+---+----+-----+-----+

val TX = spark.read.format("csv").option("header", "true").option("inferSchema",  "true").option("delimiter", ",").load("/home/gshu/Downloads/TX.TXT")

TX.show(2)
+-----+---+----+----+-----+                                                     
|State|Sex|Year|Name|Count|
+-----+---+----+----+-----+
|   TX|  F|1910|Mary|  895|
|   TX|  F|1910|Ruby|  314|
+-----+---+----+----+-----+

Question 2

val CON1 = NM.union(OK)
val CON2 = CON1.union(LA)
val CONFOURDF = CON2.union(TX)

+-----+---+----+---------+-----+                                                
|State|Sex|Year|     Name|Count|
+-----+---+----+---------+-----+
|   NM|  F|1910|     Mary|   98|
|   NM|  F|1910|    Maria|   40|
|   NM|  F|1910| Margaret|   38|
|   NM|  F|1910|Josephine|   35|
|   NM|  F|1910|    Helen|   26|
+-----+---+----+---------+-----+

Question 3

val pivotF = CONFOURDF.groupBy("Sex").pivot("State").agg(sum("Count"))

+---+-------+------+-------+--------+                                           
|Sex|     LA|    NM|     OK|      TX|
+---+-------+------+-------+--------+
|  F|2758772|787618|2054884|11005243|
|  M|2974836|913039|2230391|11863190|
+---+-------+------+-------+--------+

Question 4

val pivotDF = CONFOURDF.groupBy("State").pivot("Sex").agg(sum("Count"))
pivotDF.select($"State", $"M" + $"F" as "State Total").show()

+-----+-----------+                                                             
|State|State Total|
+-----+-----------+
|   LA|    5733608|
|   NM|    1700657|
|   TX|   22868433|
|   OK|    4285275|
+-----+-----------+

Question 5
val pivotDF = CONFOURDF.groupBy("Name").pivot("Sex").agg(sum("Count"))

pivotDF.select($"Name", $"M"+$"F" as "Total").sort($"Total".desc).show(5)


+-------+------+                                                                
|   Name| Total|
+-------+------+
|  James|459406|
|   John|399363|
|   Mary|369303|
|Michael|365411|
| Robert|363314|
+-------+------+


Question 6
val pivotDF = CONFOURDF.groupBy("Name").pivot("Sex").agg(sum("Count"))
pivotDF.select($"Name",$"F").sort($"F".desc).show(5)

+---------+------+                                                              
|     Name|     F|
+---------+------+
|     Mary|367936|
|    Maria|146003|
| Jennifer|144332|
|Elizabeth|140560|
|    Linda|139445|
+---------+------+

Question 7
val pivotDF = CONFOURDF.groupBy("Name").pivot("Sex").agg(sum("Count"))

pivotDF.select($"Name",$"M").sort($"M".desc).show(5)
+-------+------+                                                                
|   Name|     M|
+-------+------+
|  James|457172|
|   John|397573|
|Michael|363409|
| Robert|361769|
|  David|336110|
+-------+------+


