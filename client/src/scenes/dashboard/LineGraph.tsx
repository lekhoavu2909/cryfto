import React, { Component } from "react";
import * as d3 from "d3";

class LineGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: []
        };
        this.url = "https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=480";
    }

    componentDidMount() {
        this.fetchData();
    }

fetchData() {
        fetch(this.url)
            .then(response => response.json())
            .then(data => {
                const processedData = data.Data.map(d => {
                    return {
                        time: new Date(d.time * 1000),
                        close: d.close
                    };
                });
                this.setState({ data: processedData });
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    render() {
        const { data } = this.state;

        const margin = { top: 20, right: 20, bottom: 30, left: 50 };
        const width = 960 - margin.left - margin.right;
        const height = 500 - margin.top - margin.bottom;

        const x = d3.scaleTime()
            .range([0, width]);

        const y = d3.scaleLinear()
            .range([height, 0]);

        const line = d3.line()
            .x(d => x(d.time))
            .y(d => y(d.close));

        x.domain(d3.extent(data, d => d.time));
        y.domain([d3.min(data, d => d.close)-1000, d3.max(data, d => d.close)]);

        return (
            <svg width={width + margin.left + margin.right} height={height + margin.top + margin.bottom}>
                <g transform={`translate(${margin.left},${margin.top})`}>
                    <g transform={`translate(0,${height})`} ref={node => d3.select(node).call(d3.axisBottom(x)).selectAll("path, line").style("stroke", "white")}></g>
                    <g ref={node => d3.select(node).call(d3.axisLeft(y))
                        .selectAll("path, line")
                        .style("stroke", "white")}></g>
                    <path fill="none" stroke="#73fff8" strokeWidth="2" d={line(data)} />
                </g>
            </svg>
        );
    }
}

export default LineGraph;