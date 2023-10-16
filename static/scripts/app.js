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

    // Animate the scene
    function animate() {
        requestAnimationFrame(animate);

        // Rotate the cuboid for visual interest
        // if (cuboid) {
        //     cuboid.rotation.x += 0.01;
        //     cuboid.rotation.y += 0.01;
        // }

        renderer.render(scene, camera);
    }

    // Start the animation loop
    animate();

    // Handle IMU data from the server
    socket.on('imu_data', function (data) {
        // Update the HTML content with the received IMU data
        document.getElementById('linear-acceleration-x').innerText = data.linear_acceleration.x;
        document.getElementById('linear-acceleration-y').innerText = data.linear_acceleration.y;
        document.getElementById('linear-acceleration-z').innerText = data.linear_acceleration.z;

        document.getElementById('angular-velocity-x').innerText = data.angular_velocity.x;
        document.getElementById('angular-velocity-y').innerText = data.angular_velocity.y;
        document.getElementById('angular-velocity-z').innerText = data.angular_velocity.z;

        document.getElementById('orientation-x').innerText = data.orientation.x;
        document.getElementById('orientation-y').innerText = data.orientation.y;
        document.getElementById('orientation-z').innerText = data.orientation.z;

        // Update cuboid rotation based on orientation with a delay
        setTimeout(function () {
            if (cuboid) {
                // Adjust rotation based on orientation values
                cuboid.rotation.x = -THREE.Math.degToRad(data.orientation.y+90);
                cuboid.rotation.y = -THREE.Math.degToRad(data.orientation.z);// + THREE.MathUtils.degToRad(180);
                cuboid.rotation.z = -THREE.Math.degToRad(data.orientation.x);
            }
        }, 0);
    });
});
