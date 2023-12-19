
// document.addEventListener('DOMContentLoaded', function () {
    const socket = io.connect('http://localhost:5000');

    socket.on('connect', function() {
        console.log('Connected to WebSocket server');
        // document.getElementById('zeCO').textContent = `AHAHAHA`;

        
    });

    socket.on('disconnect', function() {
        console.log('Disconnected from WebSocket server');
    });

    socket.on('sensor_data', function(data) {
        updateSensorData(data);
        console.log("HI");
    });

    // socket.on('sensor_data', function(data) {
    //         console.log('Received data:', data);
    //         // You can add more console.log statements to check data for each sensor
    //     });


    function updateSensorData(data) {
        // Update the HTML to display sensor data
        document.getElementById('zeCO').innerText = `CO: ${data.zeo3.co}`;
        document.getElementById('zeO2').innerText = `O2: ${data.ze03.o2}`;
        document.getElementById('zeNH3').innerText = `NH3: ${data.ze03.nh3}`;
        document.getElementById('zeH2').innerText = `H2S: ${data.ze03.h2s}`;
        document.getElementById('zeNO2').innerText = `NO2: ${data.ze03.no2}`;
        document.getElementById('zeSO2').innerText = `SO2: ${data.ze03.so2}`;
        document.getElementById('ze03').innerText = `O3: ${data.ze03.o3}`;
        document.getElementById('zeCl2').innerText = `Cl2: ${data.ze03.cl2}`;

        document.getElementById('temp').innerText = `Temperature: ${data.bme688.temperature}`;
        document.getElementById('press').innerText = `Pressure: ${data.bme688.pressure}`;
        document.getElementById('hum').innerText = `Humidity: ${data.bme688.humidity}`;
        document.getElementById('alt').innerText = `Altitude: ${data.bme688.altitude}`;

        document.getElementById('mq4ch4').innerText = `CH4: ${data.mq4.methane}`;

        document.getElementById('tvoc').innerText = `tVOC: ${data.sgp30.tvoc}`;
        document.getElementById('sgpCO').innerText = `CO: ${data.sgp30.co2}`;

        document.getElementById('soil_temp').textContent = `Temperature: ${data.soil_probe.temperature}`;
        document.getElementById('mois').textContent = `Moisture: ${data.soil_probe.moisture}`;
        document.getElementById('pH').textContent = `pH: ${data.soil_probe.ph_value}`;
}
// });
// });












// function gaussianRandom(min=0, max=1) {
//     return ((Math.random())*(max-min)+min).toFixed(2);
// }

// function ze03_func()
// {
//     var zeCO = gaussianRandom(min=20,max=40);
//     var zeO2 = gaussianRandom(min=19,max=21);
//     var zeNO2 = gaussianRandom(min=20,max=30);
//     var zeNH3 = gaussianRandom(min=30,max=60);
//     var zeH2S = gaussianRandom(min=10,max=20);
//     var zeSO2 = gaussianRandom(min=30,max=40);
//     var ze03 = gaussianRandom(min=10,max=20);
//     var zeCl2 = gaussianRandom(min=0,max=10);
//     document.getElementById("zeCO").textContent = "CO: "+zeCO+" ppm";
//     document.getElementById("zeO2").textContent = "O2: "+zeO2+" %";
//     document.getElementById("zeNH3").textContent = "NH3: "+zeNH3+" ppm";
//     document.getElementById("zeH2").textContent = "H2S: "+zeH2S+" ppm";
//     document.getElementById("zeNO2").textContent = "NO2: "+zeNO2+" ppm";
//     document.getElementById("zeSO2").textContent = "SO2: "+zeSO2+" ppm";
//     document.getElementById("ze03").textContent = "O3: "+ze03+" ppm";
//     document.getElementById("zeCl2").textContent = "Cl2: "+zeCl2+" ppm";
// }

// function mq4_func(){
//     var mp4CH4 = gaussianRandom(min=255,max=354);
//     document.getElementById("mq4ch4").textContent = "CH4: "+mp4CH4+" ppm";
// }

// function sgp_func(){
//     var tvoc = gaussianRandom(min=0,max=20);
//     var sgp_CO = gaussianRandom(min=400,max=430);
//     document.getElementById("tvoc").textContent = "tVOC: "+tvoc+" ppm";
//     document.getElementById("sgpCO").textContent = "CO: "+sgp_CO+" ppm";
// }

// function bme_func(){
//     var temp = gaussianRandom(min=31.4,max=35);
//     var press = gaussianRandom(min=999.46,max=1054);
//     var hum = gaussianRandom(min=79.32,max=86);
//     var alt = gaussianRandom(min=0,max=115.37);
//     document.getElementById("temp").textContent = "Temperature: "+temp+" °C";
//     document.getElementById("press").textContent = "Pressure: "+press+" Hpa"; 
//     document.getElementById("hum").textContent = "Humidity: "+hum+" %";   
//     document.getElementById("alt").textContent = "Altitude: "+alt+" m"; 
// }

// function soil_func(){
//     var soil_tenp = gaussianRandom(min=24,max=26);
//     var mois = gaussianRandom(min=13,max=17);
//     var pH = gaussianRandom(min=6,max=8);
//     document.getElementById("soil_temp").textContent = "Temperature: "+soil_tenp+" °C";
//     document.getElementById("mois").textContent = "Moisture: "+mois+" %"; 
//     document.getElementById("pH").textContent = "pH: "+pH;   
// }

// function randomize_values()
// {
//     ze03_func()
// }

// setInterval(ze03_func,900);
// setInterval(mq4_func,700);
// setInterval(sgp_func,700);
// setInterval(bme_func,800);
// setInterval(soil_func,1000);


