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
import ScreenshotButton from './components/ScreenshotButton'
import Webcam from 'react-webcam'

// Define the component
function SensorDashboard() {
  const videoRef = useRef(null)

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

  const [cameraFrame, setCameraFrame] = useState(null)
  useEffect(() => {
    const socket = io.connect('http://192.168.51.172:5000/')

    socket.on('connect', () => {
      console.log('Connected to WebSocket server')
    })

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server')
    })

    // socket.on('chart_data', (data) => {
    //   setChartData(data.values)
    // })
    // const video = videoRef.current
    // video.src = 'http://localhost:5000/video_feed'
    // video.type = 'multipart/x-mixed-replace; boundary=frame'

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

    socket.on('update_devices', (updatedDevices) => {
      setDevices(updatedDevices)
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

  const [devices, setDevices] = useState([])

  const saveSensorDataToFile = () => {
    const socket = io.connect('http://localhost:5000')

    // Emit a custom event to the server when the button is clicked
    socket.emit('save_sensor_data', sensorData)
    console.log('Requested')

    // Disconnect the socket after sending the event
    socket.disconnect()
  }

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

        {/* <Button id='three'  name='Save Sensor Data' /> */}

        {/* <RecordData /> */}
        <ScreenshotButton />
        <div className='container ' style={{ backgroundColor: '#f0f0f0' }}>
          <h1 className='text-6xl font-bold mb-4'>Device Status</h1>
          <div className='text-2xl flex-col gap-10 pb-10'>
            {devices.map((device) => (
              <div
                key={device.name}
                className={
                  device.connected === 1
                    ? 'text-green-600 border-4 p-10 '
                    : 'text-red-600 border-4 p-10'
                }>
                {device.name} - {device.ip} -{' '}
                {device.connected === 1 ? 'Connected' : 'Not Connected'}
              </div>
            ))}
          </div>
        </div>
      </span>
      <span className='right'>
        <Mq4 data={sensorData} />
        <Sgp data={sensorData} />
        {/* className='microscope' className='subheader' */}
        <div title={sensorData.soil_probe.ph_value} class='microscope'>
          <div class='subheader'>Microscope</div>
          {/* <video
            ref={videoRef}
            style={{ width: '100%', height: '100%' }}
            controls={false}
            autoPlay
          /> */}

          <img
            src='http://192.168.51.172:5000/video_feed'
            alt='Video'
            style={{ width: '100%', height: '88%' }}
          />

          {/* <Webcam ref={webcamRef} style={{ width: '100%', height: '90%' }} /> */}
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
