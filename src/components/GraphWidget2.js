import React from 'react';
import AccuracyGraph from './AccuracyGraph'
import dataset from '../text_data/dataset'
import PieChart from './PieChart'

const GraphWidget2 = (props) => {
    const progress = props.progress
    switch(progress) {
        case 'getUpload':
            return (
            <>
                <PieChart 
                    className="biasedPie"
                    data = {dataset["biased"]["data"]}
                    plotTitle = {dataset["biased"]["title"]}
                    color = {dataset["biased"]["color"]}
                />
            </>)
        case 'Uploading':
            return (
                <>
                    <PieChart 
                        className="biasedPie"
                        data = {dataset["biased"]["data"]}
                        plotTitle = {dataset["biased"]["title"]}
                        color = {dataset["biased"]["color"]}
                    />
                </>)
        case "Uploaded": 
            if (props.plotData2 != null) {
                return(
                    <>
                        <AccuracyGraph className="bar2" 
                        key = {props.plotData2["title"]}
                        data ={props.plotData2["data"]} 
                        plotTitle = {props.plotData2["title"]} 
                        colors={props.plotData2["colors"]} />
                    </>
                )
            } return null
        case "Input":
            return(
                <>
                    <AccuracyGraph className="bar2" 
                    key = {props.plotData2["title"]}
                    data ={props.plotData2["data"]} 
                    plotTitle = {props.plotData2["title"]} 
                    colors={props.plotData2["colors"]} />
                </>
            )
        case "Analysis":
            return(
                <>
                    <AccuracyGraph className="bar2" 
                    key = {props.plotData2["title"]}
                    data ={props.plotData2["data"]} 
                    plotTitle = {props.plotData2["title"]} 
                    colors={props.plotData2["colors"]} />
                </>
            )
        case "bias":
            return(
                <>
                    <AccuracyGraph className="bar2" 
                    key = {props.plotData2["title"]}
                    data ={props.plotData2["data"]} 
                    plotTitle = {props.plotData2["title"]} 
                    colors={props.plotData2["colors"]} />
                </>
            )
        default:
            return null

    }
} 

export default GraphWidget2;