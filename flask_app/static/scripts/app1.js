document.addEventListener('DOMContentLoaded', function () {
    // Connect to the Socket.IO server
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Initialize Three.js scene
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth / 2, window.innerHeight / 2); // Adjust size as needed
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // Create a rotating cuboid (box)
    var geometry = new THREE.BoxGeometry(1, 2, 1); // Adjust dimensions as needed
    var material = new THREE.MeshBasicMaterial({ color: 0x800080 });
    var cuboid = new THREE.Mesh(geometry, material);
    scene.add(cuboid);

    // Set up camera position
    camera.position.z = 5;

        
    // ... (your existing code)

socket.on('connect_error', (error) => {
    console.error('Connection error', error);
    // Set up a timer to attempt reconnection after a delay
    setTimeout(handleReconnectAttempt, 1000); // 3 seconds delay, adjust as needed
});

// Add the definition of handleReconnectAttempt function
function handleReconnectAttempt() {
    // Implement your reconnection logic here
    console.log('Attempting to reconnect...');
    socket.connect();
}


document.getElementById('captureButton').addEventListener('click', function () {
    // Capture video feed image
    captureVideoImage();

    // Capture IMU and GPS values
    captureSensorValues();
});

function captureVideoImage() {
    // Create a canvas to capture the video frame
    var video = document.getElementById('video-feed');
    var canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    var context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas content to a data URL
    var imageDataURL = canvas.toDataURL('image/jpeg', 0.8);

    // Send the image data to the server (you need to implement this)
    socket.emit('capture_image', imageDataURL);
}

// var video = document.createElement('video');

    // Add an event listener for the 'loadedmetadata' event
    video.addEventListener('loadedmetadata', function () {
        // Now the video is loaded, and you can safely access its properties
        document.getElementById('capture-button').addEventListener('click', function () {
            captureVideoImage(video);
        });
    });

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            var video = document.createElement('video');
            video.srcObject = stream;
            video.play();
        })
        .catch(function (error) {
            console.error('Error accessing camera:', error);
        });

    // Other code...

    function captureVideoImage(video) {
        var canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        var imageData = canvas.toDataURL('image/jpeg', 0.8);
        socket.emit('capture_image', imageData);
    }

function captureSensorValues() {
    // Capture IMU and GPS values from the HTML elements
    var imuData = {
        linearAccelerationX: document.getElementById('linear-acceleration-x').innerText,
        linearAccelerationY: document.getElementById('linear-acceleration-y').innerText,
        linearAccelerationZ: document.getElementById('linear-acceleration-z').innerText,
        angularVelocityX: document.getElementById('angular-velocity-x').innerText,
        angularVelocityY: document.getElementById('angular-velocity-y').innerText,
        angularVelocityZ: document.getElementById('angular-velocity-z').innerText,
        orientationX: document.getElementById('orientation-x').innerText,
        orientationY: document.getElementById('orientation-y').innerText,
        orientationZ: document.getElementById('orientation-z').innerText,
        // Add other IMU values as needed
    };

    var gpsData = {
        latitude: document.getElementById('latitude').innerText,
        longitude: document.getElementById('longitude').innerText,
        altitude: document.getElementById('altitude').innerText,
    };

    // Combine the captured data and send it to the server (you need to implement this)
    socket.emit('capture_sensor_values', { imu: imuData, gps: gpsData });
}
// ... (your existing code)


    socket.on('connect', () => {
        console.log('Connected');
        hideWarning();
    });

    // socket.on('connect_error', (error) => {
    //     console.error('Connection error', error);
    //     // Set up a timer to attempt reconnection after a delay
    //     setTimeout(handleReconnectAttempt, 1000); // 3 seconds delay, adjust as needed
    // });

    socket.on('disconnect', () => {
        console.warn('Disconnected');
        showWarning('Connection lost. Reconnecting...');
        setTimeout(handleReconnectAttempt, 3000);
    });

    socket.on('reconnect', (attemptNumber) => {
        console.log(`Reconnected after ${attemptNumber} attempts`);
        hideWarning();
    });
    
    let dataReceived = true;
    let lastDataReceivedTime = Date.now();
    const MAX_DATA_AGE = 5000;

    // Animate the scene
    function animate() {
        requestAnimationFrame(animate);

        renderer.render(scene, camera);
        const currentTime = Date.now();
        const timeDifference = currentTime - lastDataReceivedTime;

        if ((timeDifference > MAX_DATA_AGE) && !dataReceived){
            showWarning('No data received from phone. Please check the connection.');
        } else {
            hideWarning();
        }
        dataReceived = false;
    }

    // Start the animation loop
    animate();

    socket.on('gps_data', function(data) {
        // Update the HTML content with the received GPS data
        document.getElementById('latitude').innerText = data.latitude;
        document.getElementById('longitude').innerText = data.longitude;
        document.getElementById('altitude').innerText = data.altitude;
    });

    function showWarning(message) {
        const warningElement = document.getElementById('warning');
        warningElement.innerText = message;
        warningElement.style.display = 'block';
    }
    
    // Function to hide the warning message
    function hideWarning() {
        const warningElement = document.getElementById('warning');
        warningElement.style.display = 'none';
    }

    // Handle IMU data from the server
    socket.on('imu_data', function (data) {
        document.getElementById('linear-acceleration-x').innerText = data.linear_acceleration.x;
        document.getElementById('linear-acceleration-y').innerText = data.linear_acceleration.y;
        document.getElementById('linear-acceleration-z').innerText = data.linear_acceleration.z;

        document.getElementById('angular-velocity-x').innerText = data.angular_velocity.x;
        document.getElementById('angular-velocity-y').innerText = data.angular_velocity.y;
        document.getElementById('angular-velocity-z').innerText = data.angular_velocity.z;

        document.getElementById('orientation-x').innerText = data.orientation.x;
        document.getElementById('orientation-y').innerText = data.orientation.y;
        document.getElementById('orientation-z').innerText = data.orientation.z;

        setTimeout(function () {
            if (cuboid) {
                cuboid.rotation.x = -THREE.Math.degToRad(data.orientation.y+90);
                cuboid.rotation.y = -THREE.Math.degToRad(data.orientation.z);// + THREE.MathUtils.degToRad(180);
                cuboid.rotation.z = -THREE.Math.degToRad(data.orientation.x);
            }
        }, 0);

        dataReceived = true;
    });

    socket.emit('request_video_feed');
    socket.on('video_feed', function (data) {
        document.getElementById('video-feed').src = 'data:image/jpeg;base64,' + data;
    });

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            var video = document.createElement('video');
            video.srcObject = stream;
            video.play();

            setInterval(function () {
                var canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                var context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                var frame = canvas.toDataURL('image/jpeg', 0.8);
                socket.emit('camera_frame', frame);
            }, 1000);  // Adjust the interval as needed
        })
        .catch(function (error) {
            console.error('Error accessing camera:', error);
        });


    if (navigator.getGamepads) {
        // Poll for gamepad input
        function pollGamepad() {
            var gamepads = navigator.getGamepads();

            // Assuming only one controller is connected
            var controller = gamepads[0];

            // Check for button presses, analog stick values, etc.
            if (controller) {
                // Process controller inputs and send to the server
                var controllerInputs = {
                    'buttonA': controller.buttons[0].pressed,
                    'buttonB': controller.buttons[1].pressed,
                    'joystickX': controller.axes[0],
                    'joystickY': controller.axes[1]
                    // Add more inputs as needed
                };

                // Send the controller inputs to the server
                socket.emit('controller_inputs', controllerInputs);
            }

            // Poll again in the next animation frame
            requestAnimationFrame(pollGamepad);
        }

        // Start polling for gamepad input
        pollGamepad();
    }
    
});
