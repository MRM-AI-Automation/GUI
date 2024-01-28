import React from 'react'
import Sensor from './Sensor'

const Soil = ({ data }) => {
  return (
    <div className='soil'>
      <div className='subheader'>Soil Probe</div>
      <Sensor
        id='soil_temp'
        name='Temperature'
        value={data.soil_probe.temperature}
        unit='°C'
      />
      <Sensor
        id='mois'
        name='Moisture'
        value={data.soil_probe.moisture}
        unit='%'
      />
      <Sensor id='pH' name='pH' value={data.soil_probe.ph_value} unit='pH' />
    </div>
  )
}

export default Soil
