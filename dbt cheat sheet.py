Updated: 2020-06-22

========== ADMIN ==========

pip install dbt
pip install --upgrade dbt

========== GETTING STARTED RUNNING THE ELT (USING CONSOLE)  ==========

			------ Commands ------
cd {dev folder / src} # set the project working directory
dbt deps # load custom dependencies
dbt seed # uploads stand-alone csv files to db
dbt compile -m table # compiles the script
dbt run -m table # runs the ELT
dbt run -m +table+ # runs table1 with both upstream and downstream dependencies
dbt run -m table1 table2 table3 # runs a list of tables (do not separate with a , it won't work)
dbt run -m tag:tag_name1 --exclude tag:tag_name2 # runs one model and excludes the other
dbt run -m @table1 # run all the upstream/downstream dependencies of all the models that depend on this table
dbt test -m table # run custom tests on the tables after ELT run



			------ Notes ------
# + before table name: upstream, after table name: downstream

========== CREATING QUERIES ==========

			------ Working with source tables ------

# Adding - add to the schema.yml file
  - name: project_name
	database: database_project
	schema: schema_name
	tables:
	  - name: table_name
		identifier: table_name

	
# Referencing - include this statement top of the script
	{{ dev_sampling([ ('source', 'project1', 'table1'), ('source', 'project1', 'table2') ]) }}
	
	SELECT * FROM project1_table1

# Referencing dbt-created tables
	SELECT * FROM {{ ref('project1_table1') }} AS table1
	
			------ Testing ------
			
# Create a .yml file inside the desired directory with the same name as the directory
	
version: 2

- name: table_name
columns:
  - name: column1
	tests:
	  - not_null
	  - unique
		  
			------ Macros ------

# For reusing repetitive code / case statements

# Define a macro
	{% macro macro1(dyn_column) %}

	CASE
		WHEN LOWER({{ dyn_column }}) LIKE '%/condition1/%' THEN 'value1'
		WHEN LOWER({{ dyn_column }}) LIKE '%/condition2/%' THEN 'value2'
		ELSE 'value3'
	END

	{% endmacro %}
	
# Define a function
	{% macro function1(input) %}
	
		CREATE OR REPLACE FUNCTION {{target.schema}}.function(input STRING)
		RETURNS 
				...

	{% endmacro %}

	# Add to dbt_project.yml
	on-run-start:
    - '{{function1()}}'
	
	# Call in a script
	{{ target.schema }}.function1(column1) AS col1

# Select
	SELECT {{ macro1(dyn_column = 'source_column') }} AS output


# Materialising results of a query
	{{
	  config(
		materialized = "table",
	  )
	}}
	
========== INCREMENTAL MODELS ==========
# Rerunning an incremental model fully
dbt run --full-refresh -m +table # fully reprocesses the table
	
========== SNAPSHOT & LOG TABLES ==========

{% snapshot table_name %}

    {{
        config(
          target_database='db_name',
          target_schema='schema_name',
          strategy='check', # comparison strategy
          unique_key='pk', # primary key for comparison
          check_cols=['column1', 'column2', 'column3'], # columns to compare
          tags=['tag_name'] # what model to associate with
        )
    }}
    
    SELECT * FROM {{ ref('original_table') }} 
    
{% endsnapshot %}

========== OTHER ==========
						
			------ Settings ------

# Dev sampling
	Can be found in dbt_project.yml -> dev_sampling: False
		Set to a small number to significantly increase ELT test time

			------ Navigation ------
			
# Compiled code
	'Target' folder: where the compiled code can be found



Author: Konstantin

References:
https://docs.getdbt.com/docs/snapshots
