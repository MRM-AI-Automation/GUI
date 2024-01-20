import React from 'react'
import Sensor from './Sensor'

const Bme = ({ data }) => {
  return (
    <div
      title='Last years science sensor which definitely works(doesnt)'
      className='bme'>
      <div className='subheader'>BME688</div>
      <Sensor
        id='temp'
        name='Temperature'
        value={data.bme688.temperature}
        unit='°C'
      />
      <Sensor
        id='press'
        name='Pressure'
        value={data.bme688.pressure}
        unit='Hpa'
      />
      <Sensor id='hum' name='Humidity' value={data.bme688.humidity} unit='%' />
      <Sensor id='alt' name='Altitude' value={data.bme688.altitude} unit='m' />
    </div>
  )
}

export default Bme
