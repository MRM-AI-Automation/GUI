import React from 'react'
import Sensor from './Sensor'

const Mq4 = ({ data }) => {
  return (
    <div className='mq4'>
      <div className='subheader'>MQ4</div>
      <Sensor id='mq4ch4' name='CH4' value={data.mq4.methane} unit='ppm' />
    </div>
  )
}

export default Mq4
