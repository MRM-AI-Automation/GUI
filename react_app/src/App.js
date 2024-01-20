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
import Button from './components/Button'
import Image from './components/Image'
import Mq4 from './components/Mq4'
import Sgp from './components/Sgp'
import Bme from './components/Bme'
import Soil from './components/Soil'
import As726x from './components/As726x'
import CameraFeed from './components/CameraFeed'

// Define the component
function SensorDashboard() {
  const [sensorData, setSensorData] = useState({
    ze03: {
      co: 0,
      o2: 0,
      nh3: 0,
      h2s: 0,
      no2: 0,
      so2: 0,
      o3: 0,
      cl2: 0,
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
  console.log(sensorData)

  const [driveMode, setDriveMode] = useState(0)
  const [A, setA] = useState(0)

  const handleKeyDown = (event) => {
    switch (event.keyCode) {
      case 16: // Shift
        setDriveMode((prevMode) => (prevMode === 0 ? 1 : 0))
        break
      case 17: // Control
        setDriveMode((prevMode) => (prevMode === 0 || prevMode === 1 ? 2 : 0))
        break
      case 49: // Keyboard 1
        setA(8)
        break
      case 50: // Keyboard 2
        setA(9)
        break
      case 51: // Keyboard 3
        setA(0)
        break
      // Add more cases for other keys as needed
      default:
        break
    }
  }

  const handleKeyUp = (event) => {
    switch (event.keyCode) {
      case 16: // Left Shift
      case 17: // Right Shift
      case 49: // Keyboard 1
      case 50: // Keyboard 2
      case 51: // Keyboard 3
        setA(0)
        break
      // Add more cases for other keys as needed
      default:
        break
    }
  }

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    document.addEventListener('keyup', handleKeyUp)
  }, [driveMode, A])

  // const [chartData, setChartData] = useState([0, 0, 0, 0, 0, 0])

  // const history = useHistory()

  const openNewTab = () => {
    // Replace 'https://example.com/new-page' with the URL you want to open in the new tab
    const urlToOpen = 'https://example.com/new-page'

    // Open the URL in a new tab
    window.open(urlToOpen, '_blank')
  }
  const [cameraFrame, setCameraFrame] = useState(null)
  useEffect(() => {
    const socket = io.connect('http://localhost:5000')

    socket.on('connect', () => {
      console.log('Connected to WebSocket server')
    })

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server')
    })

    // socket.on('chart_data', (data) => {
    //   setChartData(data.values)
    // })

    socket.on('sensor_data', (data) => {
      setSensorData(data)
      // console.log('Received data:', data)
    })

    socket.on('update_data', (data) => {
      setSensorData(data)
      // console.log('Received data:', data)
    })

    socket.on('camera_frame', (frameData) => {
      setCameraFrame(`data:image/jpeg;base64, ${frameData}`)
    })

    socket.on('camera_feed', function (data) {
      console.log('Real?')
      if (data.image) {
        // Display the camera feed on an HTML img element
        var imgElement = document.getElementById('cameraFeed')
        imgElement.src =
          'data:image/jpeg;base64,' +
          btoa(String.fromCharCode.apply(null, new Uint8Array(data.buffer)))
      }
    })

    return () => {
      socket.disconnect()
    }
  }, [])

  // const saveChartImage = (chart) => {
  //   const base64Image = chart.toBase64Image()
  //   const cleanedBase64Image = base64Image.replace(
  //     /^data:image\/png;base64,/,
  //     ''
  //   )
  //   // Send the base64 image data to the Flask server
  //   const socket = socketIOClient('http://localhost:5000')
  //   socket.emit('save_image', { cleanedBase64Imagebase64Image })
  // }

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
          labels: [
            // 'Sensor 1',
            // 'Sensor 2',
            // 'Sensor 3',
            // 'Sensor 4',
            // 'Sensor 5',
            // 'Sensor 6',
          ],
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
          // onClick: () => {
          //   console.log('Chart save')
          //   // saveChartImage(sensorChart)
          // },
          scales: {
            y: {
              beginAtZero: true,
              max: 4000,
            },
          },
        },
      })
    }
    sensorChart.data.datasets[0].data = sensorData.as726x
    // const base64Image = myChart.toBase64Image()
    // const socket = socketIOClient('http://localhost:5000')
    // socket.emit('save_image', { base64Image })
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
        <Button id='one' name='RDO' />
        <Button id='two' name='IDMO' />
        <Button id='three' name='AutEx' />
        <Button onClick={openNewTab} id='four' name='Video' />
      </span>
      <span className='right'>
        <Mq4 data={sensorData} />
        <Sgp data={sensorData} />
        {/* className='microscope' className='subheader' */}
        <div title={sensorData.soil_probe.ph_value} class='microscope'>
          <div class='subheader'>Microscope</div>
          {/*<img id='cameraFeed' src='' alt='Camera Feed'></img>*/}
          <CameraFeed />
        </div>
        <Bme data={sensorData} />
        <Soil data={sensorData} />
        {/*<As726x data={sensorData} />*/}
        <div className='spectral'>
          <div className='subheader'>AS726x</div>
          {/* <h1>AS726x Sensor Data</h1> */}
          <canvas id='sensorChart' width='400' height='200'></canvas>
        </div>

        {/* <div className='spectral'>
          <canvas id='sensorChart' width='400' height='300'></canvas>
        </div> */}

        <div
          title="This is of the class 'stupid' in the source code because of how stupid it is"
          className='stupid'>
          HANS AND LEIA MODULE
        </div>
      </span>
    </div>
  )
}

export default SensorDashboard
