/**
 * Created by luizfernando2 on 11/19/15.
 */

function classes(root) {
  var classes = [];

  function recurse(name, node) {
    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
    else classes.push({packageName: name, className: node.name, value: node.size, blabla: node.text});
  }

  recurse(null, root);
  return {children: classes};
}

function make_bubbles(root, imagesFolder) {

    var diameter = 480,
            format = d3.format(",d"),
            color = d3.scale.category20c();

    var bubble = d3.layout.pack()
            .sort(null)
            .size([diameter, diameter])
            .padding(1.5);

    var svg = d3.select("#bubbleDiv").append("svg")
            .attr("width", diameter)
            .attr("height", diameter)
            .style("display", "block")
            .style("margin", "auto")
            .attr("class", "bubble");


    var node = svg.selectAll(".node")
            .data(bubble.nodes(classes(root))
                    .filter(function (d) {
                        return !d.children;
                    }))
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

    node.append("circle")
            .attr("r", function (d) {
                return d.r;
            })
            .style("fill", function (d) {
                return color(d.packageName);
            });
    node.append('image')
            .attr('xlink:href', function (d, i) {
                return imagesFolder + d.className + '.png';
            })
            .attr('x', function (d, i) {
                return (-d.r*1.7) / 2;
            })
            .attr('y', function (d, i) {
                return (-d.r*1.7) / 2;
            })
            .attr('width', function (d, i) {
                return (d.r*1.7) + 'px';
            })
            .attr('height', function (d, i) {
                return (d.r*1.7) + 'px';
            });


    d3.select("#bubbleDiv").style("height", diameter + "px");
}
