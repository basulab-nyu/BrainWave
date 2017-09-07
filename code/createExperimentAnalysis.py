import os
import ConfigParser
def listdir_nohidden(path):
	for f in os.listdir(path):
		if not f.startswith('.'):
			if not f.endswith('p'):
				yield f


f = open('../currentDataset.txt', 'r')
dataset = f.read()
f.close()

def makeSubfolders(dataset):
	try:
		os.mkdir('../analyzedDatasets/' + dataset)
	except:
		pass

	subfolders = next(os.walk('../analyzedDatasets/datasetFrame'))[1]
	for folder in subfolders:
		try:
			os.mkdir('../analyzedDatasets/' + dataset + "/" + folder)
		except:
			pass



	if 'analysis.config' not in os.listdir('../datasets/' + dataset):
		config = ConfigParser.RawConfigParser()
		config.add_section('analysis')
		config.set('analysis', 'total_number_of_frames_in_trial', '')
		config.set('analysis', 'number_of_shuffles', '')
		config.set('analysis', 'number_of_frames_before', '')
		config.set('analysis', 'number_of_frames_after', '')
		config.set('analysis', 'threshold', '')
		config.set('analysis', 'number_of_shuffles_for_correlation_analysis', '')
		config.set('analysis', 'number_of_shuffles_for_similarity_analysis', '')
		config.set('analysis', 'group_size', '')

		
		config.add_section('intersection_analysis')
		config.set('intersection_analysis', 'percentage_of_trials_spiking_to_be_considered_signficant', '')

		config.add_section('sungear_analysis')
		config.set('sungear_analysis', 'percentage_of_trials_spiking_to_be_considered_signficant', '')
		config.set('sungear_analysis', 'stimulus_order', '')




		with open('../datasets/' + dataset + '/analysis.config', 'wb') as configfile:
			config.write(configfile)

#makeSubfolders(dataset)
#write initial config file

if __name__ == "__main__":
	dirs = []
	for f in os.listdir('../datasets'):
		if not f.startswith('.'):
			makeSubfolders(f)


