# A Tool for Finding Overlapping Normalization Rules

We find overlapping/conflicting vaule normalization rules by applying all the rules for a particular attribute to all the values of a source attribute.

The inputs are as follows:

   * "**target normalization rule attribute**" corresponds to the *relation.rule_result* property of the normalization rules. All the rules having this values for their *relation.rule_result* property would be considered as target normalization rules to be investigated.
   * "**target product attribute name**" refers to the name of an attribute's *normalized name*. We extract the *source values* for this attribute and apply all the target normalization rules to them.

The input rules and values are given as files which are specified by the *rule_overlap.cfg* configuration file. The configurations in this file are as follows:

   * *rule_file* indicates the path to a file containing the normalization rules in a tab-separated format. See below for more information on how to obtain this file.
   * *value_file_directory* indicates a directory in which the value files are stored. Each file contains values of one attribute. The file name is the same as the normalized attribute name. See below for more information on how to create these files.


