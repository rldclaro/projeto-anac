"""
Leitura de validação do Bronze — confere fidelidade à origem.
Uso: spark-submit ler_bronze.py <ano>
"""
import sys
from pyspark.sql import SparkSession


def main(ano: int):
    caminho_bronze = "/home/jovyan/work/lake/bronze"

    spark = SparkSession.builder.appName(f"ler-bronze-{ano}").getOrCreate()

    df = spark.read.format("delta").load(caminho_bronze)

    print(f"=== LENDO BRONZE (ano {ano}) ===")
    print(f"Total de linhas na tabela: {df.count()}")

    # Só o ano pedido, pra checar a partição
    df_ano = df.filter(df.ano_particao == ano)
    print(f"Linhas na partição {ano}: {df_ano.count()}")

    # Mostra algumas colunas com acento pra provar o encoding
    print("=== AMOSTRA (colunas com acento) ===")
    df_ano.select("EMPRESA (NOME)", "AEROPORTO DE ORIGEM (REGIÃO)", "MÊS") \
          .show(5, truncate=False)

    # Confirma os metadados de ingestão
    print("=== METADADOS DE INGESTÃO ===")
    df_ano.select("_arquivo_origem", "_data_ingestao", "ano_particao") \
          .show(3, truncate=False)

    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: spark-submit ler_bronze.py <ano>")
        sys.exit(1)
    main(int(sys.argv[1]))