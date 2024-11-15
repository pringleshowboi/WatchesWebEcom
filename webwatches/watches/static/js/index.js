// Initialize scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('watch-display').appendChild(renderer.domElement);

// Position the camera
camera.position.z = 2;

// Load the GLB model
const loader = new THREE.GLTFLoader();
loader.load('static/models/watches.glb', function (gltf) {
    const watch = gltf.scene;
    scene.add(watch);

    // Animate rotation based on scroll
    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        const rotationFactor = scrollPosition * 0.001;  // Adjust for desired rotation speed

        // Rotate watch based on scroll position
        watch.rotation.y = rotationFactor;
        watch.rotation.x = rotationFactor * 0.5; // Optional: tilt on X-axis
    });

    // Render loop
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
}, undefined, function (error) {
    console.error('An error occurred while loading the model:', error);
});

// Adjust canvas size on window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

