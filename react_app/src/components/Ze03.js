import React from 'react'
import Sensor from './Sensor'

const Ze03 = ({ title, sensorData }) => {
  return (
    <div title={title} className='allinone'>
      <div className='subheader'>ZE03: All in one sensor</div>
      <Sensor id='zeCO' name='CO' value={sensorData.ze03.co} unit='ppm' />
      <Sensor id='zeO2' name='GPS' value={sensorData.ze03.o2} /*unit='%'*/ />
      <Sensor
        id='zeNH3'
        name='direction'
        value={sensorData.ze03.nh3} /*unit='ppm'*/
      />
      <Sensor id='zeH2' name='H2S' value={sensorData.ze03.h2s} /*unit='ppm'*/ />
      <Sensor
        id='zeNO2'
        name='NO2'
        value={sensorData.ze03.no2} /*/*unit='ppm'*/
      />
      <Sensor
        id='zeSO2'
        name='SO2'
        value={sensorData.ze03.so2} /*/*unit='ppm'*/
      />
      <Sensor id='zeO3' name='O3' value={sensorData.ze03.o3} /*unit='ppm'*/ />
      <Sensor
        id='zeCl2'
        name='Cl2'
        value={sensorData.ze03.cl2} /*unit='ppm'*/
      />
    </div>
  )
}

export default Ze03
