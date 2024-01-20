import React from 'react'
import Sensor from './Sensor'

const Sgp = ({ data }) => {
  return (
    <div className='sgp'>
      <div className='subheader'>SGP</div>
      <Sensor id='tvoc' name='tVOC' value={data.sgp30.tvoc} unit='ppm' />
      <Sensor id='sgpCO' name='CO' value={data.sgp30.co2} unit='ppm' />
    </div>
  )
}

export default Sgp
