import React from 'react';
import AccuracyGraph from './AccuracyGraph'
import dataset from '../text_data/dataset'
import PieChart from './PieChart'

const GraphWidget = (props) => {
    const progress = props.progress
    switch(progress) {
        case 'getUpload':
            return (
            <>
                <PieChart 
                    className="unbiasedPie"
                    data = {dataset["unbiased"]["data"]}
                    plotTitle = {dataset["unbiased"]["title"]}
                    color = {dataset["unbiased"]["color"]}
                />
            </>)
        case 'Uploading':
            return (
                <>
                    <PieChart 
                        className="unbiasedPie"
                        data = {dataset["unbiased"]["data"]}
                        plotTitle = {dataset["unbiased"]["title"]}
                        color = {dataset["unbiased"]["color"]}
                    />
                </>)
        case "Uploaded": 
            if (props.plotData1 != null) {
                return(
                    <>
                        <AccuracyGraph className="bar1" 
                        key = {props.plotData1["title"]}
                        data ={props.plotData1["data"]} 
                        plotTitle = {props.plotData1["title"]} 
                        colors={props.plotData1["colors"]} />
                    </>
                )
            } return null
        case "Input":
            return(
                <>
                    <AccuracyGraph className="bar1" 
                    key = {props.plotData1["title"]}
                    data ={props.plotData1["data"]} 
                    plotTitle = {props.plotData1["title"]} 
                    colors={props.plotData1["colors"]} />
                </>
            )
        case "Analysis":
            return(
                <>
                    <AccuracyGraph className="bar1" 
                    key = {props.plotData1["title"]}
                    data ={props.plotData1["data"]} 
                    plotTitle = {props.plotData1["title"]} 
                    colors={props.plotData1["colors"]} />
                </>
            )
        case "bias":
            return(
                <>
                    <AccuracyGraph className="bar1" 
                    key = {props.plotData1["title"]}
                    data ={props.plotData1["data"]} 
                    plotTitle = {props.plotData1["title"]} 
                    colors={props.plotData1["colors"]} />
                </>
            )
        case "conclusion":
            return(
                <>
                    <div className="conclusion-info">
                        <p><b>Creators:</b> <br/><br/>Nicole Lee, Michael Hung, Sudiksha Sarvepalli</p>
                        <p><b>About:</b> <br/><br/>This web application was created as an undergraduate senior project for the data science department at University of California, San Diego. It is categorized under the Explainable AI domain under Dr. Jürgen P. Schulze.</p>
                    </div>
                </>
            )
        default:
            return null

    }
} 

export default GraphWidget;
