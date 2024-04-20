import logo from './logo.svg'
import './App.css'
import {
  BrowserRouter as Router,
  Link,
  Route,
  Switch,
  useHistory,
} from 'react-router-dom'
import socketIOClient from 'socket.io-client'
// Import necessary libraries
import React, { useEffect, useState, useRef } from 'react'
import io from 'socket.io-client'
import Chart from 'chart.js/auto'
// import Webcam from 'react-webcam'
// import Sensor from './components/Sensor'
import Ze03 from './components/Ze03'
// import Button from './components/Button'
import Image from './components/Image'
// import Mq4 from './components/Mq4'
import Sgp from './components/Sgp'
import Bme from './components/Bme'
import Soil from './components/Soil'
// import As726x from './components/As726x'
// import CameraFeed from './components/CameraFeed'
// import ScreenshotButton from './components/ScreenshotButton'
// import { data } from 'autoprefixer'
import Sensor from './components/Sensor'

// Define the component
function SensorDashboard() {
  //const [imageSrc, setImageSrc] = useState('http://localhost:5000/video_feed')

  // async function getImage() {
  //   while (1 === 1) {
  //     setImageSrc('http://localhost:5000/video_feed')
  //   }
  // }
  const [maxGraphVal, setMaxGraphVal] = useState(100)
  // const [devices, setDevices] = useState([])
  const [sensorData, setSensorData] = useState({
    ze03: {
      co: 0,
    },
    gps: {
      lat: 0,
      lon: 0,
      dir: 0,
    },
    flurometer: {
      cur: 0,
      res: 0,
    },
    bme688: {
      temperature: 0,
      pressure: 0,
      humidity: 0,
      altitude: 0,
    },
    mq4: {
      methane: 0,
    },
    sgp30: {
      tvoc: 0,
      co2: 0,
    },
    soil_probe: {
      temperature: 0,
      moisture: 0,
      ph_value: 0,
    },
    as726x: {
      s1: 0,
      s2: 0,
      s3: 0,
      s4: 0,
      s5: 0,
      s6: 0,
    },
  })

  const [cameraFrame, setCameraFrame] = useState(null)
  useEffect(() => {
    const socket = io.connect('http://localhost:5000')

    //getImage()

    socket.on('connect', () => {
      console.log('Connected to WebSocket server')
    })

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server')
    })

    socket.on('sensor_data', (data) => {
      setSensorData(data)
      console.log(data)
      setMaxGraphVal(Math.max(Object.values(data.as726x)))
    })

    return () => {
      socket.disconnect()
    }
  }, [])

  useEffect(() => {
    const ctx = document.getElementById('sensorChart').getContext('2d')
    let sensorChart

    if (!sensorChart) {
      // Create chart only if it doesn't exist
      sensorChart = new Chart(ctx, {
        type: 'bar',
        options: {
          legend: {
            display: false,
          },
        },
        data: {
          labels: [``],
          datasets: [
            {
              label: '',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
              data: sensorData.as726x,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              max: 9000,
            },
          },
        },
      })
    }
    sensorChart.data.datasets[0].data = sensorData.as726x
    sensorChart.update()

    return () => {
      // Cleanup chart on component unmount
      if (sensorChart) {
        sensorChart.destroy()
      }
    }
  }, [sensorData.as726x])

  return (
    <div>
      <span className='left'>
        <Image
          title='37th URC lesgooo'
          src='/static/MRM_logo.png'
          style={{ width: '30%', position: 'relative', top: '3%', left: '5%' }}
        />
        <div title='7th ERC lesgooo' className='header'>
          Science GUI
        </div>
        <Ze03
          title='Where is NH3? Where is H2S? Where is NO2? Where is SO2? Where is O3? Where is Cl2?'
          sensorData={sensorData}
        />
        <div className='gps'>
          <div className='subheader'>GPS</div>
          <Sensor
            id='lat'
            name='Latitude'
            value={sensorData.gps.lat}
            unit='°'
          />
          <Sensor
            id='lon'
            name='Longitude'
            value={sensorData.gps.lon}
            unit='°'
          />
          <Sensor
            id='dir'
            name='Direction'
            value={sensorData.gps.dir}
            unit=''
          />
        </div>
        {/* <Button id='one' name='RDO' />
        <Button id='two' name='IDMO' /> */}
        <Image
          title='Anky@9798'
          src='/static/sm.jpeg'
          style={{
            width: '80%',
            position: 'relative',
            top: '-15%',
            left: '10%',
            borderRadius: 50,
          }}
        />
      </span>
      <span className='right'>
        <div className='mq4'>
          <div className='subheader'>MQ4</div>
          {/* <Sensor id='mq4ch4' name='CH4' value={data.mq4.methane} unit='ppm' /> */}
          <div id='mq4ch4' className='item'>
            CH4 : {sensorData.mq4.methane}
          </div>
        </div>
        <Sgp data={sensorData} />
        {/* className='microscope' className='subheader' */}
        <div title={sensorData.soil_probe.ph_value} class='microscope'>
          <div class='subheader'>Microscope</div>
          {/* <img
            src='http://localhost:5000/video_feed'
            alt='Video'
            style={{ width: '100%', height: '88%' }}
          /> */}
        </div>
        <Bme data={sensorData} />
        <Soil data={sensorData} />
        {/*<As726x data={sensorData} />*/}
        <div className='spectral'>
          <div className='subheader'>AS726x</div>
          {/* <h1>AS726x Sensor Data</h1> */}
          <canvas id='sensorChart' width='400' height='170'></canvas>
        </div>

        <div className='flu'>
          <div className='subheader'>Flurometer</div>
          <Sensor
            id='current'
            name='Current'
            value={sensorData.flurometer.cur}
            unit='A'
          />
          <Sensor
            id='resistance'
            name='Resistance'
            value={sensorData.flurometer.res}
            unit='Ω'
          />
        </div>
      </span>
    </div>
  )
}

export default SensorDashboard
