import React from 'react'
import './Header.css'

const Header = (props) => {
    const menu = {
                "getUpload": "Background", 
                "Uploading": "→", 
                "Uploaded":"Prediction", 
                "Input": "→", 
                "Analysis": "Analysis"
            };
    let title = props.progress;
    const activeStyle = {color: '#ffffff'}
    const idleStyle = {color: '#40406B'}

    return (
        <div className="header-container">
            <div className="title-container">
                <h3 className="title-text">Facial Analysis + Bias Visualization</h3>
            </div>
            <div className="nav-container">
                {
                    Object.keys(menu).map(menuItem => 
                        <h3 className="title-labels" style={title === menuItem ? activeStyle : idleStyle}>{menu[menuItem]}</h3>
                    )
                }
            </div>
        </div>
    )
}

export default Header;