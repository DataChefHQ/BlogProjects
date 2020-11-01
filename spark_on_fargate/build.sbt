import Dependencies._

ThisBuild / scalaVersion     := "2.12.8"
ThisBuild / version          := "0.1.0"
ThisBuild / organization     := "co.datachef"

lazy val root = (project in file("."))
  .settings(
    scalaVersion := "2.12.11",
    name := "simple-spark",
    libraryDependencies ++= Seq(
      Libraries.sparkSQL,
      Libraries.sparkHive,
      Libraries.scopt
    )
  )

