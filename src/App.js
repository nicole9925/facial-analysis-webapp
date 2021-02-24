import React, {useState} from 'react'
import './App.css';
import Header from './components/Header'
import ImageComponent from './components/ImageComponent'
import Info from './components/Info'
import GuideBox from './components/GuideBox'
import AccuracyGraph from './components/AccuracyGraph'
import background from './text_data/background'
import accuracy from './text_data/accuracy'

function Home() {

  const [progress, setProgress] = useState('getUpload');
  const [data, setData] = useState(background)
  const [plotData1, setPlotData1] = useState(accuracy.unbiased)
  const [plotData2, setPlotData2] = useState(accuracy.biased)
  return (
    <>
    <header>
      <Header className="header" progress={progress}></Header>
    </header>
    {/* <h2 className="page-title">{title}</h2> */}
    <div className="main-container">
      <div className="text-container">
        <div className="info-widget box">
          <Info data={data} progress={progress}></Info>
          </div>
          <div className="stats-container">
            <div className="stats-widget1 box">
              <div className="graph-box">
                <AccuracyGraph className="bar" 
                                key = {plotData1["title"]}
                                data ={plotData1["data"]} 
                                plotTitle = {plotData1["title"]} 
                                colors={plotData1["colors"]} />
              </div>
            </div>
            <div className="stats-widget2 box">
              <div className="graph-box">
                <AccuracyGraph className="bar2" 
                                    key = {plotData2["title"]}
                                    data ={plotData2["data"]} 
                                    plotTitle = {plotData2["title"]} 
                                    colors={plotData2["colors"]} />
              </div>
            </div>
          </div>
      </div>
      <div className="interactive-container">
        <div className="guide-container">
          <GuideBox progress={progress} 
                    setProgress={setProgress}>
                  
          </GuideBox>
        </div>
        <div className="image-upload-widget box">
            <ImageComponent className="image-upload" 
                            setData={setData} 
                            setProgress={setProgress} 
                            progress={progress} data={data} 
                            setPlotData1={setPlotData1}
                            setPlotData2={setPlotData2}></ImageComponent>
        </div>
      </div>
    </div>
    </>
  );
}

export default Home;
