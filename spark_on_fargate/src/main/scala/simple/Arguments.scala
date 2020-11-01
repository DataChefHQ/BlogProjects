package simple

case class Arguments(sourcePath: String = "", destPath: String = "")

object Arguments {
  private val argParser = new scopt.OptionParser[Arguments]("simple-spark") {
    opt[String]('s', "source-path")
      .valueName("<source path>")
      .action((source, arguments) => arguments.copy(sourcePath = source))
    opt[String]('d', "dest-path")
      .valueName("<dest path>")
      .action((dest, arguments) => arguments.copy(destPath = dest))
  }

  private def validate(args: Arguments): Arguments = {
    if (args.sourcePath.isEmpty)
      throw new IllegalArgumentException("Source path is required!")
    if (args.destPath.isEmpty)
      throw new IllegalArgumentException("Destination path is required!")

    args
  }

  def apply(args: Array[String]): Arguments = {
    argParser.parse(args, Arguments()) match {
      case Some(arguments) => validate(arguments)
      case None            => throw new IllegalArgumentException
    }
  }
}
