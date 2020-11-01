import sbt._


object Dependencies {
  object Versions {
    val sparkVersion = "3.0.1"
    val scoptVersion = "3.7.1"
  }

  object Libraries {
    import Versions._

    val sparkSQL = "org.apache.spark" %% "spark-sql" % sparkVersion % Provided
    val sparkHive = "org.apache.spark" %% "spark-hive" % sparkVersion % Provided
    val scopt = "com.github.scopt" %% "scopt" % scoptVersion
  }

}
