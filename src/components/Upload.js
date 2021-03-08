import React, {useState} from 'react'
import ImageUploader from 'react-images-upload'
import UploadService from './UploadService'
import CircleLoader from 'react-spinners/CircleLoader'
import { css } from "@emotion/core";
import './Upload.css';
import indian_biased from '../static/indian_biased.png'
import indian_unbiased from '../static/indian_unbiased.png'
import white_unbiased from '../static/white_unbiased.png'
import white_biased from '../static/white_biased.png'
import EA_unbiased from '../static/EA_unbiased.png'
import EA_biased from '../static/EA_biased.png'
import accuracy from '../text_data/accuracy'
import nicole from '../static/nicole.png'
import sudiksha from '../static/sudiksha.png'
import michael from '../static/michael.png'

const UploadComponent = props => (
    <form>
        <ImageUploader
            key='image-uploader'
            withIcon={false}
            singleImage={true}
            label="Please upload an image with a single face."
            buttonText="Choose file"
            onChange={props.onImage}
            imgExtension={['.jpg', '.png', '.jpeg']}
            withPreview={true}
            labelStyles = {{color: '#ffffff'}}
            fileContainerStyle={{backgroundColor: 'var(--primary)', padding: '20px'}}
            buttonStyles = {{backgroundColor: 'var(--highlight)'}}
        />
    </form>
);
const Upload = (props) => {

    const [url, setImageUrl] = useState(undefined);
    const [errorMessage, setErrorMessage] = useState('');
    const [img, setImage] = useState(null);
    const [disableButton, setDisabled] = useState(true);
    const [raceIG, setRaceIG] = useState(null);
    const [genderIG, setGenderIG] = useState(null);
    const [ageIG, setAgeIG] = useState(null);
    const [raceG, setRaceG] = useState(null);
    const [genderG, setGenderG] = useState(null);
    const [ageG, setAgeG] = useState(null);
    const [raceBP, setRaceBP] = useState(null);
    const [genderBP, setGenderBP] = useState(null);
    const [ageBP, setAgeBP] = useState(null);
    const [results, setResults] = useState(null);

    const [vizType, setVizType] = useState("grad");

    const showViz = () => {
        switch(vizType) {
            case "grad":
                return (<>
                    <div className="ig-container">
                        <img className = "image-container-ig" src={raceG} alt="Race Grad"></img>
                        <img className = "image-container-ig" src={genderG} alt="Gender Grad"></img>
                        <img className = "image-container-ig" src={ageG} alt="Age Grad"></img>
                    </div>
                </>)
            case "ig":
                return(<>
                        <div className="ig-container">
                            <img className = "image-container-ig" src={raceIG} alt="Race Integrated Grad"></img>
                            <img className = "image-container-ig" src={genderIG} alt="Gender Integrated Grad"></img>
                            <img className = "image-container-ig" src={ageIG} alt="Age Integrated Grad"></img>
                        </div>
                </>)
            case "bp":
                return(<>
                        <div className="ig-container">
                            <img className = "image-container-ig" src={raceBP} alt="Race Back Prop"></img>
                            <img className = "image-container-ig" src={genderBP} alt="Gender Back Prop"></img>
                            <img className = "image-container-ig" src={ageBP} alt="Age Back Prop"></img>
                        </div>
                </>)

        }
    }
    // function usePrevious(value) {
    //     const ref = useRef();
    //     useEffect(() => {
    //       ref.current = value;
    //     });
    //     return ref.current;
    //   }
    // const prevProgress = usePrevious(props.progress)
    // useEffect(() => {
        

    // })
    const onImage = async (failedImages, successImages) => {
        try {
            setDisabled(false)
            setImage(successImages)

        } catch(error) {
            setErrorMessage(error.message);

        } 
    }

    const loading = () => {
        const override = css`
        display: block;
        margin-left: 0px;
        `;
        
        return(
            <CircleLoader 
            className={'loader'}
            color={'#80D8FF'}
            loading={true}
            size={150}
            css={override}
            />
        )
    }

    const submit = async () => {
        props.setProgress("Uploading");
        const parts = img[0].split(';');
        const name = parts[1].split('=')[1];

        const resp = await UploadService.UploadToServer(img, name)
        setResults(resp)
        setImageUrl('data:image/jpeg;base64,' + resp.pp_img)

        setRaceIG( 'data:image/jpeg;base64,' + resp.race_ig)
        setGenderIG( 'data:image/jpeg;base64,' + resp.gender_ig)
        setAgeIG( 'data:image/jpeg;base64,' + resp.age_ig)

        setRaceG( 'data:image/jpeg;base64,' + resp.race_grad)
        setGenderG( 'data:image/jpeg;base64,' + resp.gender_grad)
        setAgeG( 'data:image/jpeg;base64,' + resp.age_grad)

        setRaceBP( 'data:image/jpeg;base64,' + resp.race_back)
        setGenderBP( 'data:image/jpeg;base64,' + resp.gender_back)
        setAgeBP( 'data:image/jpeg;base64,' + resp.age_back)

        props.setProgress('Uploaded')
        props.setData({"race": resp.race, "gender": resp.gender, "age": resp.age})
        props.setPlotData1({"title": "Race Prediction", "data": resp.race_results, "colors": ["#9900ff", "#00ccff"]})
        props.setPlotData2({"title": "Age Prediction", "data": resp.age_results, "colors": ["#ff4aa7", "#e04646"]})    }
 
    const content = (props) => {
        const progress = props.progress
        switch(progress) {
            case 'getUpload':
                fetch('/api/clear/')
                return <>
                <div className="upload-container">
                    <UploadComponent onImage={onImage} url={url} />
                    <button className="submit" onClick={submit} disabled={disableButton}>Submit</button>
                </div>
                </>
                
            case 'Uploading':
                return loading()
            case 'Uploaded':
                return (
                <>
                    <div className="image-container">
                        <img className = "pp-img" src={url} alt="Your Face"></img>
                    </div>
                </>
                )
            case 'uploadError':
                return (
                    <>
                        <div className="error-message">{errorMessage}</div>
                        <div className="upload-container">
                            <UploadComponent onImage={onImage} url={url} />
                            <button className="submit" onClick={submit} disabled={disableButton}>Submit</button>
                        </div>
                    </>
                )
            case 'Analysis':
                return (
                <>  
                <div className="grid">
                    <div className="viz-headers">
                        <h2>Race</h2>
                        <h2>Gender</h2>
                        <h2>Age</h2>
                    </div>

                    {showViz()}

                    <div className="viz-button-container">
                        <button className="viz-button" name="grad" onClick={() => setVizType('grad')}>Grad-CAM</button>
                        <button className="viz-button" name="ig" onClick={() => setVizType('bp')}>Guided BP</button>
                        <button className="viz-button" name="bp" onClick={() => setVizType('ig')}>Integrated Grad</button>
                    </div>                    
                </div>


                </>
                )
            case 'bias':
                props.setPlotData1(accuracy.unbiased)
                props.setPlotData2(accuracy.biased)
                return (<>
                    <div className="grid-biased">
                        <div className="viz-headers">
                            <p><u>Unbiased</u></p>
                            <p><u>Biased</u></p>
                        </div>
                        <div className="g-container">
                            <div className="wrapper">
                                <div className="viz-with_cap">
                                    <img className = "image-container-ig" src={indian_unbiased} alt="Indian Unbiased"></img>
                                    <div className="caption-wrapper">
                                        <p>Prediction: Indian</p>
                                        <p>
                                            This prediction was correct. We can see that salient feature identified by Grad-CAM was the eyes.
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div className="wrapper">
                                <div className="viz-with_cap">
                                    <img className = "image-container-ig" src={indian_biased} alt="Indian Biased"></img>
                                    <div className="caption-wrapper">
                                        <p>Prediction: Latino/Hispanic</p>
                                        <p>
                                            This is an image of a young Indian girl. The fair model predicted the race correctly as Indian but the biased model predicted Latino Hispanic. 
                                            In this example, the Grad-CAM results for the fair model shows a strong focus on the eye region and the biased model covers a similar region but 
                                            the activation is not as strong. The Indian race was very underrepresented in the biased dataset which can be depicted by the performance of the biased 
                                            and unbiased models after applying Grad-cam. 
                                        </p>

                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="g-container">
                                <div className="wrapper">
                                    <div className="viz-with_cap">
                                        <img className = "image-container-ig" src={white_unbiased} alt="White Unbiased"></img>
                                        <div className="caption-wrapper">
                                            <p>Prediction: White</p>
                                            <p>
                                            This image is of a person who’s ground-truth label is White. The fair model predicted White and shows that the model made its prediction by focusing on the region around the eye.
                                            These results depict that the fair model was a stronger model in this case since it had stronger activation weights for the highlighted features than the biased model which seems to be the weaker model. 
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div className="wrapper">
                                    <div className="viz-with_cap">
                                        <img className = "image-container-ig" src={white_biased} alt="White Biased"></img>
                                        <div className="caption-wrapper">
                                            <p>Prediction: White</p>
                                            <p>
                                            Unlike the unbiased model, the biased model, which also predicted White, shows a slight amount of activation in the same eye region. The biased model seems to have weaker activation since in the biased dataset White is the overrepresented race and therefore could be assumed as a default prediction which led to the model not picking out specific salient features to make its classification. This example shows how even when two models make the same prediction, users can use Grad-CAM to distinguish the stronger and weaker model. 
                                            </p>
                                        </div>
                                    </div>
                                </div>
                        </div>
                        <div className="g-container">
                        <div className="wrapper">
                                <div className="viz-with_cap">
                                        <img className = "image-container-ig" src={EA_unbiased} alt="EA Unbiased"></img>
                                        <div className="caption-wrapper">
                                            <p>Prediction: East Asian</p>
                                            <p>
                                            The Grad-CAM shows that the fair model for our East Asian example seems to have focused on the inner region of the eye.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div className="viz-with_cap">
                                        <img className = "image-container-ig" src={EA_biased} alt="EA Biased"></img>
                                        <div className="caption-wrapper">
                                            <p>Prediction: East Asian</p>
                                            <p>
                                                There is not much activation in the biased model example. While this specific prediction was correct, the model's inability
                                                to detect salient features could explain why the biased model’s accuracy for this East Asians. 
                                            </p>

                                        </div>
                                    </div>
                                </div>
                    </div>
                </>)
            case "conclusion":
                return (<>
                <div className="image-container">
                <div className="g-container">
                        <div className="wrapper">
                                <div className="viz-with_cap_us">
                                        <img className = "image-container-us" src={michael} alt="Michael"></img>
                                        <div className="caption-wrapper">
                                            <p>Models, Integrated Gradient Visualization</p>
                                            <p>
                                            Contact: <a href="https://www.linkedin.com/in/michael-m459/">here</a>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div className="viz-with_cap_us">
                                        <img className = "image-container-us" src={sudiksha} alt="Sudiksha"></img>
                                        <div className="caption-wrapper">
                                            <p>Grad-CAM Visualization</p>
                                            <p>
                                                Contact: <a href="https://www.linkedin.com/in/sudiksha-sarvepalli/">here</a>
                                            </p>

                                        </div>
                                    </div>
                                    <div className="viz-with_cap_us">
                                        <img className = "image-container-us" src={nicole} alt="Nicole"></img>
                                        <div className="caption-wrapper">
                                            <p>Web Application</p>
                                            <p>
                                            Contact: <a href="https://www.linkedin.com/in/nicole-mandy-lee">here</a>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                         </div>
            </>)
            default:
                return <>
                    <div className="image-container">
                        <img className = "pp-img" src={url} alt="Your Face"></img>
                    </div>
                </>
        }
        
    }

    return (
        <div>
            {content(props)}
        </div>
    )
}

export default Upload;