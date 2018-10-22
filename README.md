# dzpy
Digizuite Python client implementations

## Importing Combo Values
`valueimport.exe` can accept a data file representing a list of combo values and import it into an existing combo field in a Digizuite solution.

### The data file format
The file format required for this tool is very simple and demonstrated with the example file `combo.txt` in the `samples/` directory. The text file was generated directly out of the corresponding Excel file; the assumption is that Excel is used to prepare the combo values, and then simply copying all the relevant rows and pasting into a text file creates the appropriate format.

Alternately you can create this file directly using whatever tool you're comfortable with:

* The file has two columns, separated by a tab
* The first line must contain the column names
* The column names must be `Label` and `Value`
* Sort order in the Digizuite field is set based on the line number in the file

### Common usage
This is a command line application - currently built for Windows, but is easily run on Mac OSX or Linux as well if needed.

The most common usage (using a Windows example) would look like:

```
	valueimport.exe --file ".\samples\combo.txt" --field=52611 --field_type combo --baseurl="https://dam-center.acme.com" --username=SuperAdministrator --password=9615a54cca4df45bsb4412ab0b2c0379
```

All six parameters are required and should be set according to these guidelines:

* file: this is a path (relative or absolute) to the import data file
* field: this is the Metadata field label ID of a Tree field in your Digizuite solution
* field_type: this should be set to `combo` to import a list into a combo field
* baseurl: this is the base URL to your Digizuite solution
* username: a valid username for the DAM Center - defaults to System, which should be used unless you know better
* password: this is the MD5 of the password for the provided username; check the `members` table in the DAM if needed

### Interactive usage
You can also run the tool without any options and it'll prompt you for each needed value.


## Importing Tree Values
`valueimport.exe` can accept a data file representing a hierarchy and import it into an existing tree field in a Digizuite solution.

### The data file format
The file format required for this tool is very simple and demonstrated with the example file `tree.txt` in the `samples/` directory. The text file was generated directly out of the corresponding Excel file; the assumption is that Excel is used to prepare the hierarchy definition, and then simply copying all the relevant rows and pasting into a text file creates the appropriate format.

Alternately you can create this file directly using whatever tool you're comfortable with:

* Each node is a line in the file
* the nesting of each node is defined by how many tabs it has at the beginning of the line. 
* There can be no empty rows
* If a node already exists it will generate an error

### Common usage
This is a command line application - currently built for Windows, but is easily run on Mac OSX or Linux as well if needed.

The most common usage (using a Windows example) would look like:

```
	valueimport.exe --file ".\samples\tree.txt" --field=52611 --field_type tree --baseurl="https://dam-center.acme.com" --username=SuperAdministrator --password=9615a54cca4df45bsb4412ab0b2c0379
```

All six parameters are required and should be set according to these guidelines:

* file: this is a path (relative or absolute) to the import data file
* field: this is the Metadata field label ID of a Tree field in your Digizuite solution
* field_type: this should be set to `tree` to import a hierarchy into a tree field
* baseurl: this is the base URL to your Digizuite solution
* username: a valid username for the DAM Center - defaults to System, which should be used unless you know better
* password: this is the MD5 of the password for the provided username; check the `members` table in the DAM if needed

### Interactive usage
You can also run the tool without any options and it'll prompt you for each needed value.

## Questions? 

I'll add them to an FAQ here.