import argparse
from cli.cards_from_csv import cards_from_csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f --file', dest='csv_file', type=str, help='caminho para o arquivo csv', required=True)
    args = parser.parse_args()
    cards_from_csv(args.csv_file)
    print('Importação concluída')