#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module name: CLIlogger.py
Description: Code for logging progress of a python project. Updates table in the command line. 
Author: David Estrin
Version: 1.0
Date: 08-29-2024
"""
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.box import SIMPLE
import time
import ipdb

console = Console()

class Logger:
    """ Logs in command line progress of project """
    def __init__(self, 
                 table_name, 
                 data=[], 
                 columns_names=["Cage","Subject","Group","Day","Code Step","Progress"],
                 column_styles=["bold cyan","bold green","italic magenta ","italic yellow","bold red","bright_magenta"]):
        
        # Build class with attributes below
        self.table_name = table_name
        self.column_names = columns_names
        self.column_styles = column_styles
        self.data = data # List of lists, containing data for the table to be updated
        self.live = None  # Placeholder for the Live object
        self.step_column = [i for i,j in enumerate(columns_names) if j=="Code Step"][0]
        self.progress_column = [i for i,j in enumerate(columns_names) if j=="Progress"][0]

    def set_up_table(self):
        """Set up the table"""
        # Build table use rich package objects
        table = Table(title=self.table_name,box=SIMPLE)

        # Loop over column names and styles to build table
        for column_oh,style_oh in zip(self.column_names,self.column_styles):
            table.add_column(column_oh, justify="left", style=style_oh, no_wrap=True)

        # If data was orginally given, build the table
        if self.data:
            try:
                for cage, subject, group, day, step, progress in self.data:
                    table.add_row(cage, subject, group, day, step, f"{progress}%")
            except:
                raise('Issue with self.data format, likely in wrong format. Is it a list of lists?')
        return table
    
    def append_data(self,input_data):
        self.data.append(input_data)

    def start_live(self):
        """Start the live display"""
        self.live = Live(self.set_up_table(), console=console, refresh_per_second=4)
        self.live.start()

    def stop_live(self):
        """Stop the live display"""
        if self.live:
            self.live.stop()

    def update_table(self, cage, subject, group, day, step, progress):
        """Update Table with new data"""
        # If table is empty, add first data
        if not self.data:
            input_data_oh = [cage,subject,group,day,step,progress]
            self.append_data(input_data=input_data_oh)

        # Else, table not empty
        else: 
            matching_indices = [index for index, row in enumerate(self.data) if row[0] == cage and row[1] == subject and row[2] == group and row[3] == day]
            matching_index = matching_indices[0] if matching_indices else None

            # If no matching data, append new row
            if matching_index is None:
                input_data_oh = [cage,subject,group,day,step,progress]
                self.append_data(input_data=input_data_oh)

            # If matching data, update that row
            else:
                self.data[matching_index][self.step_column] = step
                self.data[matching_index][self.progress_column] = progress

        # Refresh the table with the updated data
        if self.live:
            self.live.update(self.set_up_table())


if __name__ == '__main__':
    # Build an example table
    cli_log = Logger('Example Table:')
    try:
        cli_log.start_live()
        for i in range(1000):
            time.sleep(0.1)
            cli_log.update_table("124", "235", "Group24", "2024-10-13", "Processing", str(i))
    finally:
        cli_log.stop_live()
