Last updated: 2019-11-29

            ========== ADMIN ==========
			
pip install --upgrade dbt

						========== GETTING STARTED RUNNING THE ELT (USING CONSOLE)  ==========

			------ Commands ------
cd {dev folder / src} # set the project working directory
dbt deps # load custom dependencies
dbt seed # uploads stand-alone csv files to db
dbt compile -m +table # compiles the script 
dbt run -m +table # runs the ELT
dbt test -m +table # run custom tests on the tables after ELT run

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
	
version: 1

- name: table_name
columns:
  - name: column1
	tests:
	  - not_null
	  - unique
		  
			------ Macros ------

# For reusing repetitive code / case statements

# Define
	{% macro macro1(dyn_column) %}

	CASE
		WHEN LOWER({{ dyn_column }}) LIKE '%/condition1/%' THEN 'value1'
		WHEN LOWER({{ dyn_column }}) LIKE '%/condition2/%' THEN 'value2'
		ELSE 'value3'
	END

	{% endmacro %}

# Select
	SELECT {{ macro1(dyn_column = 'source_column') }} AS output


# Materialising results of a query
	{{
	  config(
		materialized = "table",
	  )
	}}

			------ Settings ------

# Dev sampling
	Can be found in dbt_project.yml -> dev_sampling: False
		Set to a small number to significantly increase ELT test time

			------ Navigation ------
			
# Compiled code
	'Target' folder: where the compiled code can be found




Author: Konstantin
