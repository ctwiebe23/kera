"""
kera
"""

from textx import metamodel_from_file

meta_model = metamodel_from_file("./grammer.tx")
model = meta_model.model_from_file("./example.plate")

print(meta_model)
for text in meta_model.nodes:
    print(text)