#
# cyREST Example Workflow
#
#   Graph-Structure-Aware Visualization
#
# * Perform statistical analysis
# * Detect communities
# * Use them for Visualization
#

library(igraph)
library(RJSONIO)
library(httr)

args = commandArgs(trailingOnly=T)
# Utilities to use Cytoscape and R
source("/data/platform_scripts/R/cytoscape_util.R")

# Step 1: Network Data Preparation

# Load yeast network SIF file as Data Frame
yeast.table <- read.table("/data/platform_scripts/R/cell_similarity.txt", header=T)

# Convert it to simple edge list
yeast.table.edgelist <- yeast.table[c(1,3)]

# Convert DF to undirected igraph object
# This is a PPI network, so import as undirected.
g.original <- graph.data.frame(yeast.table.edgelist, directed=F)

# Remove duplicate edges
g <- simplify(g.original, remove.multiple=T, remove.loops=T)
g$name <- "Cell line similarity"


# Step 4: Send data to Cytoscape

# Convert igraph object into Cytoscape.js JSON
cyjs <- toCytoscape(g)

style.name = "selectedNode"
style.url = paste(base.url,"styles",sep="/")
style.delete.url = paste(style.url, style.name,sep="/")
DELETE(url=style.delete.url)

style.url = paste(base.url, "styles", sep="/")
style.delete.url = paste(style.url, style.name, sep="/")
DELETE(url=style.delete.url)

# Define default values
def.node.color <- list(
  visualProperty = "NODE_FILL_COLOR",
  value = "#aaaaaa"
)

def.node.size <- list(
  visualProperty = "NODE_SIZE",
  value = 50
)


def.node.border.width <- list(
  visualProperty = "NODE_BORDER_WIDTH",
  value = 0
)

def.edge.width <- list(
  visualProperty = "EDGE_WIDTH",
  value = 2
)

def.edge.color <- list(
  visualProperty = "EDGE_STROKE_UNSELECTED_PAINT",
  value = "#aaaaaa"
)

def.edge.target.arrow.color = list(
  visualProperty="EDGE_TARGET_ARROW_UNSELECTED_PAINT",
  value = "#aaaaaa"
)

def.edge.transparency = list(
  visualProperty="EDGE_TRANSPARENCY",
  value = 100
)

def.node.transparency = list(
  visualProperty="NODE_TRANSPARENCY",
  value = 100
)

def.node.label.transparency = list(
  visualProperty="NODE_LABEL_TRANSPARENCY",
  value = 100
)

def.node.labelposition <- list(
  visualProperty = "NODE_LABEL_POSITION",
  value = "S,NW,c,7.00,0.00"  
)

defaults <- list(def.node.color,
                 def.edge.color, def.node.border.width, 
                 def.edge.width, def.edge.target.arrow.color,
				def.node.size
                 )


sel <- "sel"
cells <- strsplit(args[1], split=",")
cells <- cells[[1]]
V(g)[cells]$sel <- sel

mappings = list()

pair1 = list(
  key = sel,
  value = "red"
)
pair2 = list(
	key = sel,
	value = "blue"
)

discrete.mappings = list(pair1)
discrete.mappings2 = list(pair2)


node.color = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="NODE_FILL_COLOR",
  map = discrete.mappings
)

node.label.color = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="NODE_LABEL_COLOR",
  map = discrete.mappings2
)

edge.color = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="EDGE_STROKE_UNSELECTED_PAINT",
  map = discrete.mappings
)

edge.target.arrow.color = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="EDGE_TARGET_ARROW_UNSELECTED_PAINT",
  map = discrete.mappings
)

node.label = list(
  mappingType = "passthrough",
  mappingColumn = "name",
  mappingColumnType = "String",
  visualProperty = "NODE_LABEL"
)

node.label.size = list(
	visualProperty = "NODE_LABEL_FONT_SIZE",
	value = 20
)

pair.transparency = list(
  key = sel,
  value = "255"
)
discrete.transparency = list(pair.transparency)

node.transparency = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="NODE_TRANSPARENCY",
  map = discrete.transparency
)

edge.transparency = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="EDGE_TRANSPARENCY",
  map = discrete.transparency
)

node.label.transparency = list(
  mappingType="discrete",
  mappingColumn="sel",
  mappingColumnType="String",
  visualProperty="NODE_LABEL_TRANSPARENCY",
  map = discrete.transparency
)


mappings = list(node.color, node.label, node.label.color)
style <- list(title=style.name, defaults = defaults, mappings = mappings)
style.JSON <- toJSON(style)

POST(url=style.url, body=style.JSON, encode = "json")
cygraph.updated <- toCytoscape(g)
network.suid = send2cy(cygraph.updated, style.name,'kamada-kawai')

Sys.sleep(3)

network.image.url = paste(
  base.url,
  "networks",
  toString(network.suid),
  "views/first.png",
  sep="/"
)
a <- GET(network.image.url)
bin <- content(a,'raw')
writeBin(bin,paste('/data/ui_input/',args[2],'celllines.png',sep=""))

