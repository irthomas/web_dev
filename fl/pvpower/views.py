# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 12:09:26 2023

@author: iant

VIEWS

"""

def vega_head():
    return """        <head>
          <!-- Import Vega & Vega-Lite (does not have to be from CDN) -->
          <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
          <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
          <!-- Import vega-embed -->
          <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
        </head>"""
        
def vega_embed(json):
    return """        <div id="vis"></div>
        <script type="text/javascript">
          var spec = %s
          vegaEmbed('#vis', spec)
        </script>""" %json



