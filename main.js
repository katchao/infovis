//globals
// Resolves collisions between d and all other circles.
var padding = 20, // separation between circles
	radius=400;

//Toggle stores whether the highlighting is on
var toggle = 0;

//Create an array logging what is connected to what
var linkedByIndex = {};	
	
var svg, g;
var simulation;
var color;
var min_zoom, max_zoom;

var colorOption = "Year";
var topAll = true;

var ret_graph;

function makeGraph() {
  svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

  svg.style("fill", "none")
     .style("pointer-events", "all")
     .call(d3.zoom()
         .scaleExtent([1 / 2, 4])
         .on("zoom", zoomed)
         ).on("dblclick", null);

  g = svg.append("g");

  color = d3.scaleOrdinal(d3.schemeCategory20);

  simulation = d3.forceSimulation()
      .force("link", d3.forceLink().distance(600).id(function(d) { return d.id; }))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

  min_zoom = 0.1;
  max_zoom = 7;

  var force = d3.json("graph.json", function(error, graph) {
    if (error) throw error;

    ret_graph = graph;

    setGraph(graph);
    initGraph(graph);
  });
}

function setGraph(graph) {
	
    // tooltip
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .direction('e')
        .offset(function(d) {
          if(d.group != 1) {
            return [this.getBBox().height / 2, this.getBBox().width / 2];
          }
          else {
            return [-10, 0];
          }})
        .html(function (d) {
            if(d.group != 1) {
                return makeTooltip(d);
            }
            else {
                return d.id;
            }
        })
    svg.call(tip);

    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke-width", function(d) { return Math.sqrt(d.value) / 2; });

    var node = g.append("g")
      .attr("class", "nodes")
      .selectAll("circle")
      .data(graph.nodes)
      .enter();
/*
    for(var i = 0; i < graph.nodes.length; i++) {
       if(graph.nodes[i].radius < 20)
          graph.nodes.splice(i, 1);
    }
*/
    var clicked = false;

    //var nodeCircle = node.append(function(d){ if (d.radius > 20) return d; })
    var nodeCircle = node.append("circle")
      .attr("r", function(d) {return Math.max(d.radius/5, 15);})
      .attr("fill", function(d){
         if(d.group == 1) {
             return d3.rgb("black"); 
         }
         else {
             var hashCode;
             if(colorOption == "Genre")
                return color(hash(d.genre)); 
             else if(colorOption == "Year")
                return color(d.group/200); 
             else if(colorOption == "Country")
                return color(hash(d.country)); 
             else if(colorOption == "Language")
                return color(hash(d.language)); 
         }
      })
      .on('mouseover', tip.show)
      .on('mouseout', function() {
        if(clicked) {
          clicked = false;
          tip.show();
        } else {
          clicked = false;
          tip.hide();
        }})
      .on('click', function() {
        if(clicked) {
          console.log("click");
          clicked = false;
          tip.hide();
        } else {
          clicked = true;
          tip.show();
        }
      })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended))
          .on('dblclick', connectedNodes); //Added code ;

    /*
    var nodeText = node.append("text")
      .attr("dx", 10)
      .attr("dy", ".35em")
      .text(function(d) { return d.id });
    */

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    function ticked() {
      link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      nodeCircle
          .attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });

      nodeCircle.each(collide(20));
    }
    //This function looks up whether a pair are neighbours
    function neighboring(a, b) {
        return linkedByIndex[a.index + "," + b.index];
    }
    function connectedNodes() {
      if (toggle == 0) {
          d = d3.select(this).node().__data__;
          nodeCircle.style("opacity", function (o) {
              return neighboring(d, o) | neighboring(o, d) ? 1 : 0.1;
          });
          link.style("opacity", function (o) {
              return d.index==o.source.index | d.index==o.target.index ? 1 : 0.1;
          });
          toggle = 1;
      } else {
          nodeCircle.style("opacity", 1);
          link.style("opacity", 1);
          toggle = 0;
    }
    }
    function collide(alpha) {
      var quadtree = d3.quadtree(graph.nodes);
      return function(d) {
        var rb = 2*d.radius + padding,
            nx1 = d.x - rb,
            nx2 = d.x + rb,
            ny1 = d.y - rb,
            ny2 = d.y + rb;
        
        quadtree.visit(function(quad, x1, y1, x2, y2) {
          if (quad.point && (quad.point !== d)) {
            var x = d.x - quad.point.x,
                y = d.y - quad.point.y,
                l = Math.sqrt(x * x + y * y);
              if (l < rb) {
              l = (l - rb) / l * alpha;
              d.x -= x *= l;
              d.y -= y *= l;
              quad.point.x += x;
              quad.point.y += y;
            }
          }
          return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
        });
      };
    }

}

function initGraph(graph) {
    var optArray = [];
    for (var i = 0; i < graph.nodes.length - 1; i++) {
        optArray.push(graph.nodes[i].id);
    }
    optArray = optArray.sort();

    $(function () {
        $("#search").autocomplete({
            source: optArray
        });
    });

    for (i = 0; i < graph.nodes.length; i++) {
        linkedByIndex[i + "," + i] = 1;
    };
    graph.links.forEach(function (d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });	
}

$(document).ready(function () {
	
    makeGraph();

    document.getElementById("box").addEventListener("click", searchNode);
    function searchNode() {
        //find the node
        var selectedVal = document.getElementById('search').value;
        var node = svg.selectAll("circle");
        if (selectedVal == "none") {
            node.style("stroke", "white").style("stroke-width", "1");
        } else {
            var selected = node.filter(function (d, i) {
                return d.id != selectedVal;
            });
            selected.style("opacity", "0");
            var link = svg.selectAll("line")
            link.style("opacity", "0");
            d3.selectAll("circle, line").transition()
                .duration(5000)
                .style("opacity", 1);
        }
    }

    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
       if(event.target.parentNode.id === "myDropdown") {
          var colorNodesBy = event.target.innerHTML; //(year|genre|language|country|cancel)
          svg.selectAll("*").remove();
          colorOption = colorNodesBy;
          makeGraph();
          event.target.parentNode.classList.remove('show');
      }
    }


    document.getElementById("color-filter").addEventListener("click", function(event) {
       document.getElementById("myDropdown").classList.toggle("show");
    });

    
    document.getElementById("toggle-top").addEventListener("click", function(event) {
       var b = event.target; //.innerHTML;
       if(b.innerHTML == "Toggle Top 100")
          b.innerHTML = "Toggle All Movies";
       else
          b.innerHTML = "Toggle Top 100";
       topAll = !topAll;

       var myNode = document.getElementsByTagName("svg")[0];
       myNode.innerHTML = '';
       g = svg.append("g");
	   
       var tempGraph = {};
       if(topAll) { 
          tempGraph.nodes = ret_graph.nodes;
	  tempGraph.links = ret_graph.links;
       }
       else {
          tempGraph.nodes = ret_graph.nodes.filter(d => {return d.radius > 20 || d.group == 1});
	  tempGraph.links = ret_graph.links.filter(function(d){
              for(var i = 0; i < tempGraph.nodes.length; i++) {
                 t = tempGraph.nodes[i];
                 if(d.source.id == t.id || d.target.id == t.id)
                    return true;
              }
          });
       }
       setGraph(tempGraph);
    });


  }); //end ready

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  function zoomed() {
    console.log("zoomed");
    g.attr("transform", d3.event.transform);
  }

  function hash(s){
     return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);              
  }

  function makeTooltip(d) {
    var str = "<div class=\"movie\">";
    str += "<img src=\"" + d.poster + "\" /><br />";
    str += "<div class=\"title\">" + d.id + "</div>";
    str += "<br />Score: " + d.radius;
    str += " | Year: " + d.group;
    str += " |" + d.runtime;
    str += "<br /><strong>Country:</strong> " + d.country;
    str += "<br /><strong>Language:</strong> " + d.language;
    str += "<br /><strong>Director:</strong> " + d.director;
    str += "<br /><strong>Starring:</strong> " + d.actors;
    str += "<br /><div class=\"description\">" + d.plot;
    str += "</div></div>";
    return str;
  }

