# A Tool for Finding Overlapping Normalization Rules

We find overlapping/conflicting vaule normalization rules by applying all the rules for a particular attribute to all the values of a source attribute.

The inputs are as follows:

   * "**Target normalization rule attribute**" corresponds to the `relation.rule_result` property of the normalization rules. All the rules having this values for their `relation.rule_result` property would be considered as target normalization rules to be investigated.
   * "**Target product attribute name**" refers to the name of an attribute's *normalized name*. We extract the *source values* for this attribute and apply all the target normalization rules to them.

The input rules and values are given as files which are specified by the `rule_overlap.cfg` configuration file. The configurations in this file are as follows:

   * `rule_file` indicates the path to a file containing the normalization rules in a tab-separated format. See below for more information on how to obtain this file.
   * `value_file_directory` indicates a directory in which the value files are stored. Each file contains values of one attribute. The file name is the same as the normalized attribute name. See below for more information on how to create these files.

### `rule_file` Format

We create this file based on the Microsoft Excel dump of the rules, as follows:

   1. First, we "Save As" the Excel file as a tab-separated (TSV) text file. We might want to replace the end-of-line (EOL) characters if they are not saved appropriately.
   2. We then feed this file to `convert_pcs_value_rule_rules.py` using the following command:
   > `python convert_pcs_value_rule_rules.py <input_file> <output_file>`
   where `<input_file>` is the TSV file of rules and `<output_file>` is the name of the file we want to save the reformatted rules in.

