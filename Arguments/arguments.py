import argparse
import logging
import logging.config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date', type=str, help='Fecha inicial', action="store_true")
    parser.add_argument('--end_date', type=str, help='Fecha final', action="store_true")
    parser.add_argument('--help', type=str, help='Agrega una nueva entrada en un rango de fechas', action="store_true")
    args = parser.parse_args()
