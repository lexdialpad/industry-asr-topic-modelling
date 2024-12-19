[WIP] Topic Modeling for Industry-Specific ASR

Introduction
This project uses topic modeling to analyze and extract meaningful themes from industry-specific call transcripts. It leverages the BERTopic package to uncover these topics and generate visualizations for easier interpretation of the results.

The repository contains the following scripts:
bigquery_pull.py, which pulls the data to be used for topic modelling from a BigQuery table and saves the transcripts as .txt files in a new directory.
topicmodel.py, which preprocesses and cleans the transcripts, initializes and fits the BERTopic model to the preprocessed texts, and generates a topic distribution, an intertopic distance map, and by-topic wordclouds to guide interpretation of the results.

The repository also contains a custom_stopwords list that extends the default mltk stopwords with industry- and dataset-specific terms to improve the accuracy of the topic modelling results.
All necessary packages have been frozen in requirements.txt.

Setup
Before you begin, create a virtual environment and activate it before pulling the repository from github so that you have a clean working environment. Once you have cloned the repository, install the required packages with `pip install -r requirements.txt`.

From the VSCode extensions, install Live Server. This will allow you to view the model's output files by loading them in your local machine's default browser. Once the .html files have been generated, you can right click and select "Open with Live Server" to view them. 

Make sure you have your gcloud authentication activated and stored as a default credential before running bigquery_pull.py. If you have not yet done this, you can do so by running the following command in your vm: `gcloud auth application-default login`.
You will be prompted to authenticate as usual; afterwards, your credentials will be saved.

Usage
Run bigquery_pull.py to pull the data from BigQuery and save the transcripts. This will create a folder within your vm directory called "transcript_text_files" and save as a .txt file each transcript in the table. 

Once the transcripts are saved, run topicmodel.py to perform topic modelling and generate the outputs. This will create two folders in your vm: one called "topicmodel" that stores model data, and one called "wordclouds", which contains .png images of the by-topic wordclouds. The script will also generate two additional files, "topic_distribution.html" and "topic_map.html". As mentioned previously, you can view these in your local machine's default browser by right clicking and selecting "Open with Live Server". 

Review the results and iterate as necessary until you are satisfied with the output. [More details on this to be added.]