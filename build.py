import os

# package glossextractionengine
os.system("rm -rf glossextractionengine.mod ")
os.system("winrar a -r -ep1 glossextractionengine.zip glossextractionengine/lib glossextractionengine/saved_models")
os.system("mv glossextractionengine.zip glossextractionengine.mod")

# # package numpy
# os.system("rm -rf numpy.mod ")
# os.system("winrar a -r numpy.zip numpy/*")
# os.system("mv numpy.zip numpy.mod")