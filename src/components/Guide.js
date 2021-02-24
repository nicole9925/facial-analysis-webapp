import React from 'react';
import guide from '../text_data/guide'
import ReactTypingEffect from 'react-typing-effect';
 
 const Guide = (props) => {

    const beginTyping = () => {
        return (<>
            <ReactTypingEffect
              key = {props.progress}
              text={guide.guide[props.progress]["text"]}
              cursor={cursor => <h1 style={{color: "#ffffff"}}>{cursor}</h1>}
              speed = {guide.guide[props.progress]["speed"]}
              eraseSpeed = {guide.guide[props.progress]["eraseSpeed"]}
              eraseDelay = {guide.guide[props.progress]["eraseDelay"]}
              typingDelay = {guide.guide[props.progress]["typingDelay"]}
              displayTextRenderer={(text) => {
                return (
                  <h4>
                    {text}
                  </h4>
                );
              }}        
            />
          </>
            )
    }

    // const listen = () => {
    //     switch(progress) {
    //         case 'getUpload':
    //             setContent(guide.guide['getUpload'])
    //         case 'Uploading': 
    //             setContent(guide.guide['Uploading'])
    //     }
    // }

    return (
        <>
            {beginTyping(props)}
        </>
    )
 }


export default Guide;