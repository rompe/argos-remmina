#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An Argos plugin that shows Remmina connections in a Gnome panel menu.

This plugin: https://github.com/rompe/argos-remmina
Argos: https://github.com/p-e-w/argos
Remmina: https://remmina.org
"""
import collections
import configparser
import glob
import os

remmina_cfg_path = os.path.expanduser(os.path.join("~", ".remmina"))

result = collections.defaultdict(dict)
errors = []

for snippet in glob.glob(os.path.join(remmina_cfg_path, "*.remmina")):
    config = configparser.ConfigParser()
    config.read(snippet)
    try:
        result[config["remmina"]["group"]][config["remmina"]["name"]] = \
            {"path": snippet, "protocol": config["remmina"]["protocol"].lower()}
    except KeyError:
        errors.append("Error while reading %s" % snippet)

print("|iconName=remmina-panel\n---")

for group in sorted(result):
    if group:
        print(group)
        indent = "--"
    else:
        indent = ""
    for item in sorted(result[group]):
        print("%s%s | bash='remmina %s' terminal=false iconName=remmina-%s-symbolic" %
              (indent, item, result[group][item]["path"],
               result[group][item]["protocol"]))

for error in errors:
    print(error)
