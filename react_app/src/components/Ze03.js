import React from 'react'
import Sensor from './Sensor'

const Ze03 = ({ title, sensorData }) => {
  return (
    <div title={title} className='ze03'>
      <div className='subheader'>ZE03</div>
      <Sensor id='zeCO' name='CO' value={sensorData.ze03.co} unit='ppm' />
      {/* <Sensor id='lat' name='Latitude' value={sensorData.ze03.lat} unit='°' />
      <Sensor id='lon' name='Longitude' value={sensorData.ze03.lon} unit='°' /> */}
    </div>
  )
}

export default Ze03
