#register '/user/Terje/MyUDFs.py' using org.apache.pig.scripting.jython.JythonScriptEngine as myudfs;

from pig_util import outputSchema

@outputSchema("word:chararray")
def myupper(word):  
  return word.upper()

@outputSchema("word:chararray")
def mylower(word):  
  return word.lower()
