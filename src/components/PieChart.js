import React from 'react';
import * as d3 from "d3";
import './PieChart.css'

// const margin = {"right": 20, "left": 30, "top": 30, "bottom": 30};
const margin = 20

class PieChart extends React.Component {
    
    constructor(props) {
        super(props)
    }


    height = 200;
    width = 300;


    radius = Math.min(this.width, this.height) / 2 - margin

    componentDidMount() {
        const data = this.props.data
        const width = this.width
        const height = this.height
        const radius = this.radius
        const color = this.props.color
        const title = this.props.plotTitle

        var svg = d3.select(`#${this.props.className}`)
        .attr("width", width)
        .attr("height", height)
        .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        // Gradients 
        const defs = svg.append('defs');

        const bgGradient = defs
            .append('linearGradient')
            .attr('id', `${this.props.className}-bg-gradient`)
            .attr('gradientTransform', 'rotate(90)');
        
        bgGradient
            .append('stop')
            .attr('stop-color', color[0])
            .attr('offset', '0%');
        bgGradient
            .append('stop')
            .attr('stop-color', color[1])
            .attr('offset', '100%');

        // Chart Components
        var pie = d3.pie()
        .sort(null) // Do not sort group by size
        .value(function(d) {return d.val; })
        var data_ready = pie(data)

        var arc = d3.arc()
        .innerRadius(radius * 0.5) 
        .outerRadius(radius * 0.8)

        var outerArc = d3.arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9)

        svg
        .selectAll('allSlices')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', arc)
        // .attr('fill', function(d){return(color(d.data.cat)) })
        .attr('fill', `url(#${this.props.className}-bg-gradient)`)
        .attr("stroke", "#1A1939")
        .style("stroke-width", "5px")
        .style("opacity", 0.7)

        svg
        .selectAll('allPolylines')
        .data(data_ready)
        .enter()
        .append('polyline')
            .attr("stroke", "white")
            .style("fill", "none")
            .attr("stroke-width", 1)
            .attr('points', function(d) {
                var posA = arc.centroid(d) // line insertion in the slice
                var posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
                var posC = outerArc.centroid(d); // Label position = almost the same as posB
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
                posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
                return [posA, posB, posC]
             })
    
        svg
        .selectAll('allLabels')
        .data(data_ready)
        .enter()
        .append('text')
        .attr("class", "pieLabels")
        .text( function(d) {return d.data.cat } )
        .attr('transform', function(d) {
            var pos = outerArc.centroid(d);
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
            return 'translate(' + pos + ')';
        })
        .style('text-anchor', function(d) {
            var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
            return (midangle < Math.PI ? 'start' : 'end')
        })
        .attr("fill", "white")
        .attr("font-size", "10px")

        svg.append("g")
        .append("text")
        .attr("x", 2)
        .attr("y", -80)
        .attr("fill", "white")
        .text(title)
        .style("text-anchor", "middle");


    }
    
    render() {
        return(
            <>
            <svg id = {this.props.className} width={this.width} height={this.height}>
            </svg>
            </>
        )
    }
}

export default PieChart;
