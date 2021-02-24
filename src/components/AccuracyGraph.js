import React, { useRef, Component, useEffect } from 'react';
import * as d3 from "d3";
import './AccuracyGraph.css'

const margin = {"right": 20, "left": 30, "top": 30, "bottom": 30};

class AccuracyGraph extends React.Component {
    
    constructor(props) {
        super(props)
    }


    height = 200;
    width = 300;


    xScale  = d3.scaleBand()
        .range([ margin.left, this.width-margin.right ])

    yScale = d3.scaleLinear()   
        .domain([100, 0])
        .range([margin.top, this.height-margin.top-margin.bottom]);

    componentDidMount() {

        const data = this.props.data

        const values = data.map(function(d) {return d.val})
        const cats = data.map(function(d) {return d.cat})

        const x = this.xScale.domain(cats);;
        const y = this.yScale;
        const height = this.height;
        const width = this.width;
        const title = this.props.plotTitle;
        const colors = this.props.colors;
        console.log(colors)

        const svg = d3.select(`#${this.props.className}`)

        // Gradients
        const defs = svg.append('defs');

        const bgGradient = defs
          .append('linearGradient')
          .attr('id', `${this.props.className}-bg-gradient`)
          .attr('gradientTransform', 'rotate(90)');
      
        bgGradient
          .append('stop')
          .attr('stop-color', colors[0])
          .attr('offset', '0%');
        bgGradient
          .append('stop')
          .attr('stop-color', colors[1])
          .attr('offset', '100%');
      
        // Axes
        const xAxis = d3.axisBottom(this.xScale);
        const yAxis = d3.axisLeft(this.yScale);
    
        svg.append("g")
        .attr("class", "accuracy-axis")
        .attr("transform", `translate(0, ${this.height-margin.top-margin.bottom})`)
        .call(xAxis)
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

        svg.append("g")
        .attr("class", "accuracy-axis")
        .attr("transform", `translate(${margin.left}, 0)`)
        .call(yAxis)

        // Bars
        svg.selectAll("bars")
        .data(data)
        .enter()
        .append("rect")
            .attr("x", function(d) {return x(d.cat) + x.bandwidth()/4})
            .attr("y", function(d) {return y(d.val)})
            .attr("width", x.bandwidth()/2)
            .attr("height", function(d) { return height-margin.top-margin.bottom - y(d.val)})
            .attr("fill", `url(#${this.props.className}-bg-gradient)`)
        
        svg.append("g")
        .append("text")
        .attr("x", width/2)
        .attr("y", margin.top)
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

export default AccuracyGraph;
