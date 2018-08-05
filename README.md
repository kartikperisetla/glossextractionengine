```
GlossExtractionEngine
Copyright (c) Kartik Perisetla, Carnegie Mellon University, 2015
kperisetla@cmu.edu
This work was done during my Masters at Carnegie Mellon University under Professor William Cohen.

GlossExtractionEngine is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GlossExtractionEngine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GlossExtractionEngine.  If not, see <http://www.gnu.org/licenses/>.
```

## GlossExtractionEngine

It is a framework to extract definitional sentences from large datasets. 

The core of the framework is based on the filters, transformations, parsers, feature extractors, samplers and modelers you use. Thus it is extensible and customizable for your needs. All you need to do is extend the base functionatlity and write your own filters, transformations, parsers, feature extractors, samplers and modelers. 

The framework provides components for your NLP pipeline, you can extend these components according to your task and datasource:

1. #### Filters: 
	Basic sentence level filters. eg. length filter, english token filter, etc.

2. #### Transformations: 
	Basic token level components(called as 'transformers') that transforms tokens. eg. Lowercase transformation, remove non alphanumeric transformation, remove non english tokens, wiktionary definition transformation

3. #### Parsers: 
	Basic Parsers. eg. Wikipedia parser- to parse wikipedia articles

4. #### Samplers: 
	Basic components to sample instances from a pool of instances. eg. Random sampler(basic random sampler implementation)

5. #### Feature Extractors: 
	Basic feature extractors for your NLP tasks. eg.

	**SentenceTokensFeatureExtractor**: extracts basic sentence features like tokens

	**POSContextSequenceFeatureExtractor**: extracts contextual features based on Part of speech tags around the word of interest(head noun phrase)

	**MaltParsedSentenceFeatureExtractor**: extracts basic sentence features for sentences that are parsed with malt parser( i.e tokens in sentence have pos tags with them)

	**MaltParsedPOSContextSequenceFeatureExtractor**: extracts contextual features based on Part of speech tags around the word of interest for sentences that are parsed with malt parser( i.e tokens in sentence have pos tags with them)

6. #### Interfaces:
	You can interact with samplers and feature extractors through a simple commands.
	**SamplingInterface**: to interact with Samplers
	
     	python sample_interface.py -sampler <sampler_implementation> -positive <positive_source_file> -negative <negative_source_file> -train_size <train_set_size> -test_size <test_set_size>
    	
	
	**FeatureExtractionInterface**: to interact with Feature Extractors
	
		python feature_extraction_interface.py -fe_mapper <feature_extraction_mapper> -fe_mapper_params  <mapper_params> -fe_reducer <feature_extraction_reducer> -fe_reducer_params <reducer_params> -train_dataset <dataset_location> -train_size <train_set_size> -test_size <test_set_size>

7. #### Single-point-of-Interaction: 
	You can interact with framework through a single point which interacts with components to perform operations.

	**run.py** : you can interact with samplers and feature extractors through this.

	```
	python run.py -operation <operation_name> <parameters for operation>
	```

	**supported operations(NOTE: Use operation name without quotes)**

	*(1) operation name: 'sampling' , parameters: -sampler <sampler_implementation>  -positive <positive_source_file> -negative <negative_source_file> -train_size <train_set_size> -test_size <test_set_size>*

	Example:
	```
	python glossextractionengine/run.py -operation sampling -sampler lib.sampler.random_sampler.RandomSampler -positive final_dataset/positive_instances -negative final_dataset/negative_instances -train_size 200 -test_size 10
	```

	*(2) operation name: 'extract_features' , parameters: -fe_mapper <feature_extraction_mapper> -fe_mapper_params  <mapper_params> -fe_reducer <feature_extraction_reducer> -fe_reducer_params <reducer_params> -train_dataset <dataset_location> -train_size <train_set_size> -test_size <test_set_size> -sampler <sampler_implementation>*

		-this operation will implicitly invoke sampling operation on dataset provided
		-you will get a directory named 'feature_set_for_modeling' as the output in 'extract_features' mode of operation

	Example: using feature extractors provided by framework:
	```
	python glossextractionengine/run.py -operation extract_features -fe_mapper glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py  -fe_reducer glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -train_dataset final_dataset/ -train_size 200 -test_size 10 -positive final_dataset/positive_instances  -negative final_dataset/negative_instances -sampler lib.sampler.random_sampler.RandomSampler
	```

	Example: using your own custom feature extractors:
	```
	python glossextractionengine/run.py -operation extract_features -fe_mapper kartik_fe_map.py -fe_reducer kartik_fe_red.py  -train_dataset final_dataset/ -train_size 200 -test_size 10 -sampler lib.sampler.random_sampler.RandomSampler -positive final_dataset/positive_instances -negative final_dataset/negative_instances
	```


	*(3) operation name: 'modeling'*


	if you want to generate model for one feature set file:

	```
	parameters: -feature_set_location <feature_set_file_location> -model_name <model_name_to_save_as>
	```

	if you want to generate models for different feature set files:

	```
	parameters: *-feature_set_location <feature_set_location_directory>
	```

	Example:	
	```
	python glossextractionengine/run.py  -operation modeling -feature_set_location feature_set_for_modeling/
	```

	*(4) operation name: 'classification' , parameters: -cl_mapper <classification_mapper> -cl_mapper_params <mapper_params> -cl_reducer <classification_reducer> -cl_reducer_params <reducer_params> -test_dataset <dataset_location> -model <model_file>*

		if you want to provide custom parameters to mapper and reducer for classification operation, just remember that model file will be the first parameter to them followed by custom parameters

	Example:
	```
	python glossextractionengine/run.py -operation classification -cl_mapper glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_mapper.py  -cl_reducer glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_reducer.py -test_dataset test_data/ -model trained_models/200_output.model
	```

	(5) operation name: 'default' , parameters:

	```
	-fe_mapper <feature_extraction_mapper> -fe_mapper_params  <mapper_params> -fe_reducer <feature_extraction_reducer> -fe_reducer_params <reducer_params> -train_dataset <dataset_location> -train_size <train_set_size> -test_size <test_set_size> -sampler <sampler_implementation> -cl_mapper <classification_mapper> -cl_mapper_params <mapper_params> -cl_reducer <classification_reducer> -cl_reducer_params <reducer_params> -test_dataset <dataset_location>
	```

	OR

	```
	-fe_mapper <feature_extraction_mapper> -fe_mapper_params  <mapper_params> -fe_reducer <feature_extraction_reducer> -fe_reducer_params <reducer_params> -train_dataset <dataset_location> -train_size <train_set_size> -test_size <test_set_size> -sampler <sampler_implementation> -cl_mapper <classification_mapper> -cl_mapper_params <mapper_params> -cl_reducer <classification_reducer> -cl_reducer_params <reducer_params> -test_dataset <dataset_location>
	```
	

	This mode basically executes the default behavior/flow of the framework. i.e. it handles sampling, feature extraction, modeling and classification flows for you with just single command.

	```
	-fe_mapper : option to indicate is the mapper you want to use for feature extraction task

	-fe_mapper_params : option to indicate the custom parameters you want to pass to the feature extraction mapper. parameters must be separated by #. For example: 4#4#True

	-fe_reducer : option to indicate the reducer you want to use for feature extraction task

	-fe_reducer_params : option to indicate the custom parameters you want to pass to the feature extraction reducer. parameters must be separated by #. For example: 4#4#True

	-train_dataset : option to specify location on file system where training dataset is present.

	-train_size : option to specify the size of sampled training set you want to generate through sampling algorithm on actual training dataset.

	-test_size : option to specify the size of sampled test set you want to generate through sampling algorithm on actual training dataset( useful in cross validation).

	-sampler : option to indicate the sampler implementation you want to use for sampling.

	-cl_mapper : option to indicate is the mapper you want to use for classification task.

	-cl_mapper_params :option to indicate the custom parameters you want to pass to the classification mapper. parameters must be separated by #. For example: 4#4#True

	-cl_reducer : option to indicate the reducer you want to use for classification task

	-cl_reducer_params : option to indicate the custom parameters you want to pass to the classification reducer. parameters must be separated by #. For example: 4#4#True

	-test_dataset : option to specify where your test dataset is located on local file system.
			
	-model : option to specify the model to be used for the classification task.( give the location where your model will be generated )
	```		
