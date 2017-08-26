import logging
import os
import sys

from Giveme5W_enhancer.heideltime import Heideltime
from extractor.configuration import Configuration as Config
from extractor.extractor import FiveWExtractor
from extractor.tools.file.handler import Handler
from extractors import environment_extractor

# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))

"""
Advanced example to use the extractor in combination with NewsPlease files
 - The output of the core_nlp_host is saved in the cache directory to speed up multiple runs. 
 - Documents are preloaded into memory and stay persistent for further calculations.
 - Enhancer is used to process the result further

Documents are preprocessed just once, you have to set is_preprocessed to false, 
if you want to process them again by core_nlp (or just delete cache and output)
"""


if __name__ == '__main__':
    Config.get()['information']['nlpIndexSentence'] = False
    # Config.get()['enhancements']['Giveme5W_enhancer']['enabled'] = True

    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    extractor = FiveWExtractor(extractors=[
        # action_extractor.ActionExtractor(),
        environment_extractor.EnvironmentExtractor(),
        # cause_extractor.CauseExtractor(),
        # method_extractor.MethodExtractor()
    ], enhancement=[
        Heideltime()
    ])
    inputPath = os.path.dirname(__file__) + '/input'
    outputPath = os.path.dirname(__file__) + '/output'
    preprocessedPath = os.path.dirname(__file__) + '/cache'

    documents = (
        # initiate the file handler with the input directory
        Handler(inputPath)
            ## everything else is optional:

            # set a output directory
            .set_output_path(outputPath)
            # set a path to save and load preprocessed documents (CoreNLP result)
            .set_preprocessed_path(preprocessedPath)
            # limit the documents read from the input directory (handy for development)
            .set_limit(1)
            # .skip_documents_with_output()
            # add an optional extractor (it would do only copying without...)
            .set_extractor(extractor)
            # load and saves all document objects for further programming
            .preload_and_cache_documents()

            ## setup is done:

            # executing it
            .process()
            # get the processed documents
            .get_documents()
    )