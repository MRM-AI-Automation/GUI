import React from 'react'

const Sensor = ({ id, name, value, unit }) => {
  return (
    <div id={id} className='item'>
      {name}: {value} {unit}
    </div>
  )
}

export default Sensor
