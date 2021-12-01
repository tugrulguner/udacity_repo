#!/usr/bin/env python
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="exercise_5", job_type="process_data")

    logger.info("Fetching the artifact")
    genres_mod = run.use_artifact(f'{args.input_artifact}')

    logger.info("Reading the fetched data")
    df = pd.read_parquet(genres_mode.file())

    logger.info("Preprocessing the data")
    df = df.drop_duplicates().reset_index(drop=True)
    df['title'].fillna(value='', inplace=True)
    df['song_name'].fillna(value='', inplace=True)
    df['text_feature'] = df['title'] + ' ' + df['song_name']

    logger.info("Saving to a file")
    outfile = args.artifact_name
    df.to_csv(outfile)

    logging.info("Attaching and running file to W&B")
    artifact = wandb.Artifact(
    name = args.artifact_name,
    type = args.artifact_type,
    description = args.artifact_description
    )
    artifact.add_file(outfile)
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)