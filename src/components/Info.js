import React from 'react'
import './Info.css'
import modelInfo from '../text_data/modelInfo'
import bias from '../text_data/bias'

const Info = (props) => {
    var progress = props.progress;
    var background = props.data;
    // console.log(background)
    const content = () => {
        switch(progress) {
            case 'getUpload':
                return (
                    <>
                    <div className="background-container">
                        <h3>{background.background[1]["header"]}</h3>
                        <p>{background.background[1]["body"]}</p>

                        <h3>{background.background[2]["header"]}</h3>
                        <p>{background.background[2]["body"]}</p>
                    </div>
                    </>
                )
            case 'Uploading':
                return (
                    <>
                    <div className="background-container">
                        <h3>{background.background[1]["header"]}</h3>
                        <p>{background.background[1]["body"]}</p>

                        <h3>{background.background[2]["header"]}</h3>
                        <p>{background.background[2]["body"]}</p>
                    </div>
                    </>
                )
            case 'Uploaded':
                return ( <>
                <div className="results-container">
                    <h3><strong>OUR GUESSES:</strong></h3>
                    <div className="results">
                        <h5><b>Race:</b></h5>
                        <h5>{background["race"]}</h5>
                    </div>
                    <div className="results">
                        <h5><b>Gender:</b></h5>
                        <h5>{background["gender"]}</h5>
                    </div>
                    <div className="results">
                        <h5><b>Age:</b></h5>
                        <h5>{background["age"]}</h5>
                    </div>
                </div>
                </>
                )
            case 'Input':
                return ( <>
                <div className="correction-container">
                </div>
                </>
                )
            case 'Analysis':
                return ( <>
                    <div className="background-container">
                        <h3>{modelInfo.modelInfo[1]["header"]}</h3>
                        <p>{modelInfo.modelInfo[1]["body"]}</p>

                        <h3>{modelInfo.modelInfo[2]["header"]}</h3>
                        <p>{modelInfo.modelInfo[2]["body"]}</p>
                    </div>
                </>
                )
            case 'bias':
                return ( <>
                    <div className="background-container">
                        <h3>{bias.bias[1]["header"]}</h3>
                        <p>{bias.bias[1]["body"]}</p>

                        <h3>{bias.bias[2]["header"]}</h3>
                        <p>{bias.bias[2]["body"]}</p>
                    </div>
                </>
                )
            case 'conclusion':
                return(<>
                    <div className="background-container">
                        <p><b>References</b></p>
                        <ul>
                            <li>Prediction Models: <a href="https://github.com/rodrigobressan/keras-multi-output-model-utk-face">github</a></li>
                            <li>Grad-CAM: <a href="https://github.com/rodrigobressan/keras-multi-output-model-utk-face">github</a></li>
                            <li>Integrated Gradients: <a href="https://www.tensorflow.org/tutorials/interpretability/integrated_gradients">link</a></li>
                        </ul>
                        <p><b>Works Cited + Further Reading</b></p>
                        <ul>
                            <li><a href="https://www.researchgate.net/figure/Sample-images-from-FairFace-dataset-10_fig4_344373604">Understanding Fairness of Gender Classification Algorithms Across Gender-Race Groups</a></li>
                            <li><a href="https://www.nature.com/articles/d41586-020-03186-4">Is facial recognition too biased to be let loose?</a></li>
                            <li><a href="https://www.nytimes.com/2020/01/12/technology/facial-recognition-police.html">How the Police Use Facial Recognition, and Where It Falls Short</a></li>
                        </ul>
                    </div>
                    
                </>)
            default:
                return (
                    <>
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

export default Info;