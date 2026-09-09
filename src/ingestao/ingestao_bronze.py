"""
Ingestão Bronze — lê o CSV cru da ANAC e grava em Delta, fiel à origem.
Uso: spark-submit ingestao_bronze.py <ano>
"""
import sys
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main(ano: int):
    caminho_csv = f"/home/jovyan/work/dados-brutos/{ano}.csv"
    caminho_bronze = "/home/jovyan/work/lake/bronze"

    spark = SparkSession.builder.appName(f"ingestao-bronze-{ano}").getOrCreate()

    # Lê o CSV cru respeitando o contrato de dados
    df = (
        spark.read
        .option("header", "true")
        .option("sep", ";")
        .option("encoding", "ISO-8859-1")
        .csv(caminho_csv)
    )

    # Anexa metadados de ingestão (não altera os dados originais)
    df_bronze = (
        df
        .withColumn("_data_ingestao", F.current_timestamp())
        .withColumn("_arquivo_origem", F.lit(f"{ano}.csv"))
        .withColumn("ano_particao", F.lit(ano))
    )

    # Grava em Delta, particionado por ano, sobrescrevendo só a partição do ano
    (
        df_bronze.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("ano_particao")
        .option("replaceWhere", f"ano_particao = {ano}")
        .option("delta.columnMapping.mode", "name")
        .option("delta.minReaderVersion", "2")
        .option("delta.minWriterVersion", "5")
        .save(caminho_bronze)
    )

    total = df_bronze.count()
    print(f"=== BRONZE OK: {ano} → {total} linhas gravadas ===")

    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: spark-submit ingestao_bronze.py <ano>")
        sys.exit(1)
    main(int(sys.argv[1]))