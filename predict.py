import os
import json
import subprocess
import pickle

def run(place_name):

    # we check if the place has already been processed before
    if os.path.exists('./sorted_descending/' + place_name):
        with open('./sorted_descending/' + place_name, 'rb') as fin:
            sorted_list = pickle.load(fin)
            return sorted_list

    cwd = os.getcwd()

    # otherwise, we run the neural network on the pictures in our ./pictures/<place_name> file
    with open('predictions.tmp', "wb", 0) as command_out:
        prediction = subprocess.call(['sudo', cwd + '/predict', '--docker-image', 'nima-cpu', '--base-model-name',
                'MobileNet', '--weights-file', cwd + '/models/MobileNet/weights_mobilenet_technical_0.11.hdf5',
                '--image-source', cwd + '/photos/' + place_name], stdout=command_out)
        command_out.close()

    # we parse the output
    with open('predictions.tmp', 'r') as json_file:
        file_lines = json_file.readlines()
        while file_lines[0][0] != '[':
            file_lines.pop(0)
        prediction_list = json.loads(''.join(file_lines))
        # we sort the files by score in descending order
        sorted_list = [d['image_id'] for d in sorted(prediction_list, key=lambda k: -k['mean_score_prediction'])]

    os.remove('predictions.tmp')

    # we cache the scores for future use
    with open('./sorted_descending/' + place_name, 'wb') as fout:
        pickle.dump(sorted_list, fout)

    return sorted_list

