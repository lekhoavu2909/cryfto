import React, { Component } from "react";
import * as d3 from "d3";

class LineGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            pred: []
        };
        this.url = "https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=480";
        this.predurl = 'http://localhost:5000/predict'
    }

    async componentDidMount() {
        await this.fetchData();
    }

    async fetchData() {
            await fetch(this.url)
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
            const tmp = this.state.data.map(d => d.close);
            await fetch(this.predurl, {
                    method: 'POST',
                    headers: {
                      'Accept': 'application/json, text/plain, */*',
                      'Content-Type': 'application/json;charset=utf-8'
                    },
                    body: JSON.stringify({"data": tmp })
                  }).then(response => response.json())
                  .then(data => {
                    const t = this.state.data[this.state.data.length - 1].time;
                    let cnt = 1;
                    const processedPred = data.prediction.map(d => {
                        return {
                            time: new Date(t.getTime() + cnt++ * 60000),
                            close: d[0]
                        };
                    });
                    this.setState({ pred: processedPred });
                  })
                  .catch(error => console.error('Error fetching pred:', error));
                 
        }

    render() {
        const { data,pred } = this.state;
        console.log(data)
        console.log(pred)

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
        const temp = data.concat(pred)
        x.domain(d3.extent(temp, d => d.time));
        y.domain([d3.min(temp, d => d.close)-100, d3.max(temp, d => d.close)]);
        
        // Define gridlines
        const xAxisGrid = d3.axisBottom(x)
        .tickSize(height)
        .tickFormat("");

        const yAxisGrid = d3.axisLeft(y)
        .tickSize(-width)
        .tickFormat("");
        if(pred.length != 0){
            data.push(pred[0])
        }
        
        return (
            <svg width={width + margin.left + margin.right} height={height + margin.top + margin.bottom}>
                <g transform={`translate(${margin.left},${margin.top})`}>
                    <g className="x-grid" ref={node => d3.select(node).call(xAxisGrid)} />
                    {/* Append y-axis gridlines */}
                    <g className="y-grid" ref={node => d3.select(node).call(yAxisGrid)} />
                    <g transform={`translate(0,${height})`} ref={node => d3.select(node).call(d3.axisBottom(x)).selectAll("path, line").style("stroke", "white")}></g>
                    <g ref={node => d3.select(node).call(d3.axisLeft(y))
                        .selectAll("path, line")
                        .style("stroke", "white")}></g>
                    <path fill="none" stroke="#73fff8" strokeWidth="2" d={line(data)} />
                    <path fill="none" stroke="white" strokeWidth="2" d={line(pred)} />
                </g>
            </svg>
        );
    }
}

export default LineGraph;