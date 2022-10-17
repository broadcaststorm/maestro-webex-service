# Commands

[GET] svc:/project
project list
- returns JSON list of each project summary schema

[GET] svc:/project/name
project list name
- name needs to conform to URI standards
- title for a descriptive field to display
- description to briefly explain scenario
- returns JSON of project detail schema

[GET] svc:/scenario?project=pname
scenario list [project pname]

[GET] svc:/scenario/name?project=pname
scenario list name [project pname]
