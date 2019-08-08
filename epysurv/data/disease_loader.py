import os
import pickle


def load_diseases(path):
    disease_pickles = [
        file for file in os.listdir(path) if os.path.splitext(file)[-1] == ".pickle"
    ]
    disease_pickles = sorted(disease_pickles)
    for disease_pickle in disease_pickles:
        yield pickle.load(open(os.path.join(path, disease_pickle), "rb"))
