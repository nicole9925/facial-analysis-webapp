import React from 'react'
import Upload from './Upload'
import './ImageComponent.css'

const ImageComponent = (props) => {
    
    var progress = props.progress

    const content = () => {
        switch(progress) {  
            case 'getUpload':
                return (
                    <>
                    <div className="upload-container">
                        <Upload setProgress={props.setProgress} 
                                setData={props.setData} 
                                setPlotData1={props.setPlotData1}
                                setPlotData2={props.setPlotData2} 
                                progress={progress}></Upload>
                    </div>
                    </>
                )
            default:
                return (
                    <>
                    <div className="upload-container">
                        <Upload setProgress={props.setProgress} 
                                setData={props.setData}
                                setPlotData1={props.setPlotData1} 
                                setPlotData2={props.setPlotData2} 
                                progress={progress}></Upload>
                    </div>
                    </>
                )
        }
    }
    return (
        <>
            <div>
                {content()}
            </div>
        </>
    )
}

export default ImageComponent;