# A Tool for Finding Overlapping Normalization Rules

We find overlapping/conflicting vaule normalization rules by applying all the value normalization rules for a particular attribute to all the values of a source attribute.

The screipts `docker-build.sh`, `docker-start.sh` and `docker-stop.sh` respectively build a docker for the web application, start a Django server containing this application inside the docker, and stop the service. After starting the server, the web application would be accessible on http://hostaddress:8000/rule\_overlaps/.

##### Inputs

The web application takes the following inputs:

   * "**Target normalization rule attribute**" corresponds to the `relation.rule_result` property of the normalization rules. All the rules having this values for their `relation.rule_result` property would be considered as target normalization rules to be investigated.
   * "**Target product attribute name**" refers to the name of an attribute's *normalized name*. We extract the *source values* for this attribute and apply all the target normalization rules to them.

The input rules and values are given as files which are specified by the `rule_overlap.cfg` configuration file. The configurations in this file are as follows:

   * `rule_file` indicates the path to a file containing the normalization rules in a tab-separated format. See below for more information on how to obtain this file.
   * `value_file_directory` indicates a directory in which the value files are stored. Each file contains values of one attribute. The file name is the same as the normalized attribute name. See below for more information on how to create these files.

##### Outputs

It then generates a list of pairs of normalization rules which overlap. For each rule pair, it also shows a list of values they both match and the number of product items with those values for the target attribute.

### `rule_file` Format

We create this file based on the Microsoft Excel dump of the rules, as follows:

   1. First, we "Save As" the Excel file as a tab-separated (TSV) text file. We might want to replace the end-of-line (EOL) characters if they are not saved appropriately.
   2. We then feed this file to `convert_pcs_value_rule_rules.py` using the following command:

   `python convert_pcs_value_rule_rules.py <input_file> <output_file>` |
   ---------------------------------------------------------------------

   where `<input_file>` is the TSV file of rules and `<output_file>` is the name of the file we want to save the reformatted rules in.
   3. Finally we set the value of `rule_file` configuration in `rule_overlap.cfg` to the above `<output_file>` value.

### `value_file_directory` Directory Content

The directory with the name equal to the value of `value_file_directory` configuration contains one file per attribute. Each file contains a set of lines, each line consists of a single JSON object. Each JSON object corresponds to an attribute value and has the following format:
```
{ <value> :
   {
      'sample_product_ids' : [<prod_id_1>, ...] ,
      'prod_cnt' : <cnt>
   }
}
```
where `<value>` is an attribute value, `<prod_id_1>` is the id of a sample product having `<value>` for its attribute and `<cnt>` is the number of procuts having `<value>` for their attribute.
These files are created using the Python script `extract_source_values_from_json.py`. The help for this command reads as follows:

```
Usage: python extract_source_values_from_json.py <input_json_file_name_list> <input_json_files_folder> <output_folder>

Arguments:

   <input_json_file_name_list>: A file containing the list of input files 
      each of which cotain JSON objects of product items.

   <input_json_files_folder>: The folder containing the files with the 
      names in <input_json_file_name_list>.

   <output_folder>: The folder to which the extracted values should be 
      writtten. Each attribute's values are stored in a file named by the attributes name.

Please modify the code to change the following parameters:

   1. Attributes to extract source values for (`attributes`).
   2. Maximum number of sample product ids to store per attribute value (`max_prod_ids`).
```
