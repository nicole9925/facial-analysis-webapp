import React, {useState} from 'react'
import './App.css';
import Header from './components/Header'
import ImageComponent from './components/ImageComponent'
import Info from './components/Info'
import GuideBox from './components/GuideBox'
import AccuracyGraph from './components/AccuracyGraph'
import background from './text_data/background'
import accuracy from './text_data/accuracy'
import GraphWidget from './components/GraphWidget'
import GraphWidget2 from './components/GraphWidget2'

function Home() {

  const [progress, setProgress] = useState('getUpload');
  const [data, setData] = useState(background)
  const [plotData1, setPlotData1] = useState(accuracy.unbiased)
  const [plotData2, setPlotData2] = useState(accuracy.biased)
  const [width, setWidth] = useState(window.innerWidth)

  const notDesktop = width <= 1050;

  if (notDesktop) {
    return (
      <>
        <p className="desktop-warning"> This app only works on desktops. Please increase your window size and refresh to view page. </p>
      </>
    )
  }
  return (
    <>
    <header>
      <Header className="header" progress={progress}></Header>
    </header>
    {/* <h2 className="page-title">{title}</h2> */}
    <div className="main-container">
      <div className="text-container">
        <div className="info-widget box">
          <Info key = {progress} data={data} progress={progress}></Info>
          </div>
          <div className="stats-container">
            <div className="stats-widget1 box">
              <div className="graph-box">
                {/* <AccuracyGraph className="bar" 
                                key = {plotData1["title"]}
                                data ={plotData1["data"]} 
                                plotTitle = {plotData1["title"]} 
                                colors={plotData1["colors"]} /> */}
                  <GraphWidget 
                              className="pie1"
                              key = {progress}
                              plotData1 = {plotData1}
                              progress = {progress}
                  />
              </div>
            </div>
            <div className="stats-widget2 box">
              <div className="graph-box">
                {/* <AccuracyGraph className="bar2" 
                                    key = {plotData2["title"]}
                                    data ={plotData2["data"]} 
                                    plotTitle = {plotData2["title"]} 
                                    colors={plotData2["colors"]} /> */}
                      <GraphWidget2 
                              className="pie2"
                              key = {progress}
                              plotData2 = {plotData2}
                              progress = {progress}
                      />
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
            <ImageComponent   
                            className="image-upload" 
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
