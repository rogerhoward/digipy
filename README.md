# dzpy
Digizuite Python client implementations

## Importing Tree Files
The first module in this package, "treeimport", takes a data file representing a hierarchy and imports it into an existing tree field in a Digizuite solution.

### The data file format
The file format required for this tool is very simple and demonstrated with an example in the samples/ directory. The text file was generated directly out of the corresponding Excel file; the assumption is that Excel is used to prepare the hierarchy definition, and then simply copying all the relevant rows and pasting into a text file creates the appropriate format.

Alternately you can create this file directly using whatever tool you're comfortable with:

* Each node is a line in the file
* the nesting of each node is defined by how many tabs it has at the beginning of the line. 
* There can be no empty rows
* If a node already exists it will generate an error

## Common usage
This is a command line application - currently built for Windows, but is easily run on Mac OSX or Linux as well.

The most common usage (using a Windows example) would look like:

	treeimport.exe --file="import.txt" --field=50751 --baseurl="http://dc.acme.com" --username="System" --password="P@ssW0rD"

All five parameters are required and should be set according to these guidelines:

* file: this is a path (relative or absolute) to the import data file
* field: this is the unique field ID of a Tree field in your Digizuite solution
* baseurl: this is the base URL to your Digizuite solution
* username: this defaults to "System" so use that unless you know better!
* password: this is the actual password for the provided username

## Questions? 

I'll add them to an FAQ here.