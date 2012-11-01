Library size
=============

.. highlight:: c

.. csv-table::
    :header: "Comment", "Code snippet", "Program bytes", "Data bytes" 
    :file: generated_code_sizes.csv

The maximum size is calculated as a difference:

Program1 = empty template + code snippet

Program2 = empty template

Maximum library size = Program1 size - Program2 size

Actual size can be lower. MCU=atmega168

Template:

.. literalinclude:: generated_template.c



