import argparse

from create_bags.digitization_pipeline import DigitizationPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Uses DART Runner to create bags of digitized content that will be sent to Zorya.")
    parser.add_argument(
        '-l',
        '--list',
        nargs='+',
        help='List of rights IDs (integers). E.g.: -l 2 4',
        type=int,
        required=True)
    args = parser.parse_args()
    DigitizationPipeline().run(args.list)


if __name__ == "__main__":
    main()
