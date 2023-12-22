import logo from './logo.svg';
import './App.css';

// Import necessary libraries
import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import Webcam from 'react-webcam';

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
  });

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = io.connect('http://localhost:5000');

    // Event listener for successful connection
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    // Event listener for disconnection
    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });

    // Event listener for receiving sensor data
    socket.on('sensor_data', (data) => {
      setSensorData(data);
      console.log('Received data:', data);
    });

    // Clean up the WebSocket connection on component unmount
    return () => {
      socket.disconnect();
    };
  }, []); // Empty dependency array ensures the effect runs once on mount

  // Function to render the component
  return (
    <div>
      <span className="left">
        <img title="37th URC lesgooo" src="/static/MRM_logo.png" style={{ width: '30%', position: 'relative', top: '3%', left: '5%' }} />
        <div title="7th ERC lesgooo" className="header">Science GUI</div>
        <div title="This year's science sensor which definitely works" className="allinone">
          <div className="subheader">ZE03: All in one sensor</div>
          <div id="zeCO" className="item">CO: {sensorData.ze03.co} ppm</div>
          <div id="zeO2" className="item">O2: {sensorData.ze03.o2} %</div>
          <div id="zeNH3" className="item">NH3: {sensorData.ze03.nh3} ppm</div>
          <div id="zeH2" className="item">H2S: {sensorData.ze03.h2s} ppm</div>
          <div id="zeNO2" className="item">NO2: {sensorData.ze03.no2} ppm</div>
          <div id="zeSO2" className="item">SO2: {sensorData.ze03.so2} ppm</div>
          <div id="ze03" className="item">O3: {sensorData.ze03.o3} ppm</div>
          <div id="zeCl2" className="item">Cl2: {sensorData.ze03.cl2} ppm</div>
        </div>
        <button title="They wanted this to be PINK LMAO y'all need to thank me" id="one" className="button">RDO</button>
        <button title="They wanted this to be PINK LMAO y'all need to thank me" id="two" className="button">IDMO</button>
        <button title="They wanted this to be PINK LMAO y'all need to thank me" id="three" className="button">AutEx</button>
        <button title="They wanted this to be PINK LMAO y'all need to thank me" id="four" className="button">Video</button>
      </span>
      <span className='right'>
        <div className="mq4">
          <div className="subheader">MQ4</div>
          <div id="mq4ch4" className="item">CH4: {sensorData.mq4.methane} ppm</div>
        </div>
        <div className="sgp">
          <div className="subheader">SGP</div>
          <div id="tvoc" className="item">tVOC: {sensorData.sgp30.tvoc} ppm</div>
          <div id="sgpCO" className="item">CO: {sensorData.sgp30.co2} ppm</div>
        </div>
        <div title="This shit still works?" className="microscope">
          <div className="subheader">Microscope</div>
          {<Webcam />}
        </div>
        <div title="Last years science sensor which definitely works(doesnt)" className="bme">
          <div className="subheader">BME688</div>
          <div id="temp" className="item">Temperature: {sensorData.bme688.temperature} °C</div>
          <div id="press" className="item">Pressure: {sensorData.bme688.pressure} Hpa</div>
          <div id="hum" className="item">Humidity: {sensorData.bme688.humidity} %</div>
          <div id="alt" className="item">Altitude: {sensorData.bme688.altitude} m</div>
        </div>
        <div className="soil">
          <div className="subheader">Soil Probe</div>
          <div id="soil_temp" className="item">Temperature: {sensorData.soil_probe.temperature} °C</div>
          <div id="mois" className="item">Moisture: {sensorData.soil_probe.moisture} %</div>
          <div id="pH" className="item">pH: {sensorData.soil_probe.ph_value} pH</div>
        </div>
        <div title="Could have been a spectrometer but no lmaoooo" className="spectral">
          <div className="subheader">AS726x</div>
        </div>
        < div title="This is of the class 'stupid' in the source code because of how stupid it is" className="stupid">HANS AND LEIA MODULE</div>
      </span>
    </div>
  );
  
}

// Export the component
export default SensorDashboard;

