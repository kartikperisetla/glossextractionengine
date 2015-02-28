import os

# package glossextractionengine
os.system("rm -rf glossextractionengine.mod ")
os.system("winrar a -r -ep1 glossextractionengine.zip lib saved_models")
os.system("mv glossextractionengine.zip glossextractionengine.mod")


